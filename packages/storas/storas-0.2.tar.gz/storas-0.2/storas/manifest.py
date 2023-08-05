"""Module for dealing with manifest files."""
import logging
import os
from typing import Dict, Iterable, List, Optional, Set
import urllib.parse
import xml.etree.ElementTree

DEFAULT_MANIFEST_FILE = "default.xml"
KNOWN_ELEMENTS = ("default", "include", "project", "remote")
LOGGER = logging.getLogger(__name__)

class ManifestParseError(Exception):
	"""Indicates a bad manifest file was found."""

class Remote():
	"A remote."
	def __init__(self,
		name: str,
		fetch: Optional[str],
		review: Optional[str]):
		self.fetch = urllib.parse.urlparse(fetch)
		self.fetch_host = str(self.fetch.netloc).split(".")[0]
		self.name = name
		self.review = urllib.parse.urlparse(review)

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Remote):
			raise NotImplementedError()
		return all([
			self.fetch == other.fetch,
			self.fetch_host == other.fetch_host,
			self.name == other.name,
			self.review == other.review,
		])

	def __hash__(self) -> int:
		return hash((self.name, self.fetch, self.review))

	def __repr__(self) -> str:
		return str(self)

	def __str__(self) -> str:
		return "Remote {name} review {review} fetch {fetch}".format(
			fetch=self.fetch,
			name=self.name,
			review=self.review,
		)

class Manifest():
	"""Represents a bundle of manifest files."""

	def __init__(self, path: str):
		self.defaults: Dict[str, str] = {}
		self.includes: List[Manifest] = []
		# The manifest that was the source of the '<include>' that pulled
		# in this manifest.
		self.parent: Optional[Manifest] = None
		self.path = path
		self._projects: Dict[str, Project] = {}
		self._remotes: Dict[str, Remote] = {}

	@staticmethod
	def parse(path: str, tree: xml.etree.ElementTree.ElementTree) -> "Manifest":
		"Parse a manifest from an xml tree."
		# pylint: disable=protected-access
		root = tree.getroot()
		if not root.tag == "manifest":
			raise ManifestParseError("Root node is not 'manifest'")
		result = Manifest(path)
		for child in root.getchildren():
			if child.tag == "default":
				result._handle_default(child)
			elif child.tag == "include":
				result._handle_include(child)
			elif child.tag == "project":
				result._handle_project(child)
			elif child.tag == "remote":
				result._handle_remote(child)
			else:
				raise NotImplementedError("No handler for {}".format(child.tag))
		result._add_parents()
		return result

	@property
	def projects(self) -> Iterable["Project"]:
		"Iterate over all projects."
		for manifest in self.includes:
			for project in manifest.projects:
				yield project
		for project in self._projects.values():
			yield project

	def remote(self, name: str) -> Remote:
		"""Get a particular remote by name.

		Turns out that repo is...clever. You can refer to a remote in any manifest file so long as it
		has been loaded via 'include' into the context that is shared by all manifests and repo is
		perfectly happy. This means I can load up manifest A, which includes B, which defines a remote
		X. Then manifest A can include another manifest C which can refer to X even though it doesn't
		define it.

		Yay.

		We therefore traverse to the root manifest and then use it to build the set of all remotes
		and search those.
		"""
		if self.parent:
			return self.parent.remote(name)
		all_remotes = self.remotes()
		matching = []
		for remote in all_remotes:
			if remote.name == name:
				matching.append(remote)
		if len(matching) > 2:
			raise Exception(
				"Not sure which remote to use, there are {} which have the name '{}'".format(
				len(matching), name))
		if not matching:
			raise KeyError("Unable to find a remote named '{}' in {}".format(name, self.path))
		return matching[0]

	def remotes(self) -> Set[Remote]:
		"""Get the set of remotes known to this manifest.

		This includes any remotes defined in this manifest or in any of its includes.
		"""
		all_remotes = set()
		for include in self.includes:
			for remote in include.remotes():
				all_remotes.add(remote)
		for remote in self._remotes.values():
			all_remotes.add(remote)
		return all_remotes

	def _add_parents(self) -> None:
		project_by_path = {p.path: p for p in self.projects}
		for project in self.projects:
			parent_dir = project.path
			while parent_dir:
				parent_dir, _ = os.path.split(parent_dir)
				if parent_dir in project_by_path:
					project.parent = project_by_path[parent_dir]
					break

	def _handle_default(self, node: xml.etree.ElementTree.Element) -> None:
		for attribute in node.attrib.keys():
			assert attribute not in self.defaults
			self.defaults.update(node.attrib)
		LOGGER.debug("Updated defaults with %s", node.attrib)

	def _handle_include(self, node: xml.etree.ElementTree.Element) -> None:
		base = os.path.dirname(self.path)
		newpath = os.path.join(base, node.attrib["name"])
		# Most includes are strictly in the same directory. The special
		# .repo/manifest.xml file may include files from .repo/manifests/
		try:
			submanifest = load(newpath, parent=self)
		except FileNotFoundError:
			newpath = os.path.join(base, "manifests", node.attrib["name"])
			submanifest = load(newpath, parent=self)
		self.includes.append(submanifest)

	def _handle_project(self, node: xml.etree.ElementTree.Element) -> None:
		path = node.attrib.get("path")
		project = Project(
			self,
			name=node.attrib["name"],
			parent=None,
			path=path,
			remote=node.attrib["remote"],
			revision=node.attrib.get("revision"),
			sheriff=node.attrib.get("sheriff"),
		)
		self._projects[project.name] = project
		LOGGER.debug("Added project %s", project.name)

	def _handle_remote(self, node: xml.etree.ElementTree.Element) -> None:
		remote = Remote(
			fetch=node.attrib.get("fetch"),
			name=node.attrib["name"],
			review=node.attrib.get("review"),
		)
		self._remotes[remote.name] = remote
		LOGGER.debug("Added remote %s", remote.name)

class Project():
	"A single project in a manifest."
	def __init__(self, # pylint: disable=too-many-arguments
			manifest: Manifest,
			name: str,
			remote: str,
			path: Optional[str],
			revision: Optional[str],
			parent: Optional["Project"],
			sheriff: Optional[str],
		):
		self.manifest = manifest
		self.name = name
		self.parent = parent
		self.path = path or name
		self._remote = remote
		self._revision = revision or manifest.defaults.get("revision", "master")
		self.sheriff = sheriff

	def __hash__(self) -> int:
		return hash((self.name, self.remote, self.path, self.revision))

	@property
	def remote(self) -> Remote:
		"Get the remote used."
		return self.manifest.remote(self._remote)

	@property
	def revision(self) -> str:
		"Get the revision this tracks"
		if self._revision:
			return self._revision
		return self.manifest.defaults.get("revision", "master")

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Project):
			raise NotImplementedError()
		return all([
			self.name == other.name,
			self.parent == other.parent,
			self.path == other.path,
			self.remote == other.remote,
			self.revision == other.revision,
			self.sheriff == other.sheriff,
		])

	def __repr__(self) -> str:
		return str(self)

	def __str__(self) -> str:
		return "Project {name} at {path} from {remote} on {revision}".format(
			name=self.name,
			path=self.path,
			remote=self._remote,
			revision=self.revision,
		)

def load(manifest_path: str, parent: Optional[Manifest] = None) -> Manifest:
	"Load a manifest and return it."
	with open(manifest_path, "r") as inp:
		tree = xml.etree.ElementTree.parse(inp)
	LOGGER.debug("Loaded manifest XML file '%s'", manifest_path)
	result = Manifest.parse(manifest_path, tree)
	if parent:
		result.parent = parent
	return result
