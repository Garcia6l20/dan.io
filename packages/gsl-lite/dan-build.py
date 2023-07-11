from dan import self
from dan.cmake import Project as CMakeProject
from dan.src.github import GitHubReleaseSources
from dan.core.target import Installer
from dan.cxx import Library, LibraryType
from dan.pkgconfig.package import create_pkg_config

version = self.options.add('version', '0.41.0')
description = 'A single-file header-only version of ISO C++ Guidelines Support Library (GSL) for C++98, C++11, and later'


class GslLiteSources(GitHubReleaseSources):
    name = 'gsl-lite-source'
    user = 'gsl-lite'
    project = 'gsl-lite'


class GslLite(CMakeProject):
    name = 'gsl-lite'
    source_path = GslLiteSources
    installed = True

    async def __install__(self, installer: Installer):
        await super().__install__(installer)

        # create pkgconfig
        lib = Library(self.name, makefile=self.makefile)
        lib.library_type = LibraryType.INTERFACE
        installer.installed_files.append(await create_pkg_config(lib, installer.settings))
