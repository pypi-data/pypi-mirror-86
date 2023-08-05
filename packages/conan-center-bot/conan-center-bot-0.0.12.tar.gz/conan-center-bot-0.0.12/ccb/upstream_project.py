import re
import abc
import hashlib
import logging
import subprocess
from functools import lru_cache
import requests

from .version import Version
from .project_specifics import (
    TAGS_BLACKLIST,
    PROJECT_TAGS_BLACKLIST,
    PROJECT_TAGS_WHITELIST,
    PROJECT_TAGS_FIXERS,
)


logger = logging.getLogger(__name__)


class _Unsupported(RuntimeError):
    pass


def get_upstream_project(recipe):
    conanfile_class = recipe.conanfile_class(recipe.most_recent_version)
    for cls in _CLASSES:
        try:
            return cls(recipe, conanfile_class)
        except _Unsupported:
            pass

    logger.debug("%s: unsupported upstream", recipe.name)
    return UnsupportedProject(recipe, conanfile_class)


class UpstreamProject(abc.ABC):
    def __init__(self, recipe, conanfile_class):
        self.recipe = recipe
        self.conanfile_class = conanfile_class

    @property
    def homepage(self) -> str:
        return self.conanfile_class.homepage

    @abc.abstractproperty
    def versions(self) -> dict:
        pass

    @abc.abstractproperty
    def most_recent_version(self) -> Version:
        pass

    @abc.abstractmethod
    def source_url(self, version) -> str:
        pass

    @lru_cache(None)
    def source_sha256_digest(self, version):
        url = self.source_url(version)
        if not url:
            return None
        sha256 = hashlib.sha256()
        tarball = requests.get(url)
        sha256.update(tarball.content)
        return sha256.hexdigest()


class UnsupportedProject(UpstreamProject):
    @property
    def versions(self):  # pylint: disable=invalid-overridden-method
        return {}

    @property
    def most_recent_version(self):
        return Version()

    def source_url(self, version):
        return None


class GitProject(UpstreamProject):
    def __init__(self, recipe, conanfile_class, git_url):
        super().__init__(recipe, conanfile_class)
        self.git_url = git_url
        self.whitelist = PROJECT_TAGS_WHITELIST.get(recipe.name, [])
        self.blacklist = TAGS_BLACKLIST + PROJECT_TAGS_BLACKLIST.get(recipe.name, [])
        self.fixer = PROJECT_TAGS_FIXERS.get(recipe.name, None)

    @property
    @lru_cache(None)
    def versions(self):  # pylint: disable=invalid-overridden-method
        logger.debug("%s: fetching tags...", self.recipe.name)
        git_output = subprocess.check_output(
            ["git", "ls-remote", "-t", self.git_url]
        ).decode()

        tags = [ref.replace("refs/tags/", "") for ref in git_output.split()[1::2]]
        tags = list(set(tag[:-3] if tag.endswith("^{}") else tag for tag in tags))
        logger.debug("%s: found tags: %s", self.recipe.name, tags)

        valid_tags = self._filter_tags(tags)
        logger.debug(
            "%s: ignored %s tags", self.recipe.name, len(tags) - len(valid_tags)
        )

        return tuple(Version(version=tag, fixer=self.fixer) for tag in valid_tags)

    @property
    def most_recent_version(self):
        if not self.versions:
            return Version()
        return sorted(self.versions)[-1]

    def _filter_tags(self, tags):
        valid_tags = list()
        if self.whitelist:
            for tag in tags:
                if any(regex.match(tag) for regex in self.whitelist):
                    valid_tags.append(tag)
                else:
                    logger.debug(
                        "%s: tag %s ignored because it does not match any of %s",
                        self.recipe.name,
                        tag,
                        list(regex.pattern for regex in self.whitelist),
                    )
        else:
            for tag in tags:
                ignored = False
                for regex in self.blacklist:
                    if regex.match(tag):
                        ignored = True
                        logger.debug(
                            "%s: tag %s ignored because it matches regex %s",
                            self.recipe.name,
                            tag,
                            regex.pattern,
                        )
                        break
                if not ignored:
                    valid_tags.append(tag)
        return valid_tags


class GithubProject(GitProject):
    HOMEPAGE_RE = re.compile(r"https?://github.com/([^/]+)/([^/]+)")
    SOURCE_URL_RE = re.compile(r"https?://github.com/([^/]+)/([^/]+)")

    def __init__(self, recipe, conanfile_class):
        owner, repo = self._get_owner_repo(recipe, conanfile_class)
        git_url = f"https://github.com/{owner}/{repo}.git"

        super().__init__(recipe, conanfile_class, git_url)
        self.owner = owner
        self.repo = repo

    def source_url(self, version):
        if version.unknown:
            return None
        return f"https://github.com/{self.owner}/{self.repo}/archive/{version.original}.tar.gz"

    @classmethod
    def _get_owner_repo(cls, recipe, conanfile_class):
        match = cls.HOMEPAGE_RE.match(conanfile_class.homepage)
        if match:
            return match.groups()

        try:
            url = recipe.source(recipe.most_recent_version)["url"]
            match = cls.SOURCE_URL_RE.match(url)
            if match:
                return match.groups()
        except Exception as exc:
            logger.debug(
                "recipe %s not supported as GitHub project because of the following exception: %s",
                recipe.name,
                repr(exc),
            )

        raise _Unsupported()


_CLASSES = [GithubProject]
