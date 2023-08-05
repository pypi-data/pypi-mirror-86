import os
import typing
import inspect
import logging
import importlib.util
from functools import lru_cache

from conans import ConanFile

from .version import Version
from .upstream_project import get_upstream_project
from .cci import cci_interface
from .yaml import yaml


logger = logging.getLogger(__name__)


def get_recipes_list(cci_path):
    return os.listdir(os.path.join(cci_path, "recipes"))


class RecipeError(RuntimeError):
    pass


class Status(typing.NamedTuple):
    name: str
    homepage: str
    recipe_version: Version
    upstream_version: Version
    deprecated: bool

    def update_possible(self):
        return (
            not self.upstream_version.unknown
            and not self.recipe_version.unknown
            and self.upstream_version.is_date == self.recipe_version.is_date
            and self.upstream_version > self.recipe_version
        )

    def up_to_date(self):
        return (
            not self.upstream_version.unknown
            and not self.recipe_version.unknown
            and self.upstream_version.is_date == self.recipe_version.is_date
            and self.upstream_version <= self.recipe_version
        )

    def inconsistent_versioning(self):
        return (
            not self.upstream_version.unknown
            and not self.recipe_version.unknown
            and self.upstream_version.is_date != self.recipe_version.is_date
        )

    def prs_opened(self):
        return cci_interface.pull_request_for(self)


class Recipe:
    def __init__(self, cci_path, name):
        self.name = name
        self.path = os.path.join(cci_path, "recipes", name)
        self.config_path = os.path.join(self.path, "config.yml")

    def config(self):
        if not os.path.exists(self.config_path):
            raise RecipeError("No config.yml file")

        with open(self.config_path) as fil:
            return yaml.load(fil)

    @property
    @lru_cache(None)
    def upstream(self):
        return get_upstream_project(self)

    @property
    def versions(self):
        return [Version(v) for v in self.config()["versions"].keys()]

    @property
    def most_recent_version(self):
        return sorted(self.versions)[-1]

    def folder(self, version):
        assert isinstance(version, Version)

        for k, v in self.config()["versions"].items():
            if Version(k) == version:
                return v["folder"]
        raise KeyError(version)

    def source(self, version):
        conandata = self.conandata(version)
        for k, v in conandata["sources"].items():
            if Version(k) == version:
                return v
        raise KeyError(version)

    def status(self, recipe_version=None, upstream_version=None):
        try:
            recipe_version = recipe_version or self.most_recent_version
            recipe_upstream_version = (
                upstream_version or self.upstream.most_recent_version
            )
            homepage = self.upstream.homepage
            deprecated = getattr(
                self.conanfile_class(recipe_version), "deprecated", False
            )
        except RecipeError as exc:
            logger.debug("%s: could not find version: %s", self.name, exc)
            recipe_version = Version()
            recipe_upstream_version = Version()
            homepage = None
            deprecated = None

        return Status(
            self.name,
            homepage,
            recipe_version,
            recipe_upstream_version,
            deprecated,
        )

    def conandata(self, version_or_folder):
        path = self.conandata_path(version_or_folder)
        if not os.path.exists(path):
            raise RecipeError("no conandata.yml")
        with open(path) as fil:
            return yaml.load(fil)

    def conandata_path(self, version_or_folder):
        if isinstance(version_or_folder, Version):
            folder = self.folder(version_or_folder)
        else:
            folder = version_or_folder
        return os.path.join(self.path, folder, "conandata.yml")

    @lru_cache(None)
    def conanfile_class(self, version):
        assert isinstance(version, Version)

        version_folder_path = os.path.join(self.path, self.folder(version))

        spec = importlib.util.spec_from_file_location(
            "conanfile", os.path.join(version_folder_path, "conanfile.py")
        )
        conanfile = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conanfile)

        conanfile_main_class = None
        for symbol_name in dir(conanfile):
            symbol = getattr(conanfile, symbol_name)
            if (
                inspect.isclass(symbol)
                and issubclass(symbol, ConanFile)
                and symbol is not ConanFile
            ):
                conanfile_main_class = symbol
                break

        if conanfile_main_class is None:
            raise RecipeError("Could not find ConanFile class")

        return conanfile_main_class

    def version_exists(self, version):
        return version.fixed in self.config()["versions"]
