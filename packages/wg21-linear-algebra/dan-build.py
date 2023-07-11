from dan import self
from dan.cmake import Project as CMakeProject
from dan.src.github import GitHubReleaseSources
from dan.core.target import Installer
from dan.cxx import Library, LibraryType, CppStd
from dan.pkgconfig.package import create_pkg_config

version = self.options.add('version', '0.7.3')
description = 'Production-quality reference implementation of P1385: A proposal to add linear algebra support to the C++ standard library'


class WG21LinearAlgebraSources(GitHubReleaseSources):
    name = 'wg21-linear-algebra-sources'
    user = 'BobSteagall'
    project = 'wg21'


class WG21LinearAlgebra(CMakeProject):
    name = 'wg21-linear-algebra'
    source_path = WG21LinearAlgebraSources
    installed = True
    dependencies = []
    cmake_config_definitions = {
        'LA_ENABLE_TESTS': 'OFF',
        'LA_BUILD_PACKAGE': 'OFF',
    }
    cmake_options = {
    }
    
    async def __install__(self, installer: Installer):
        await super().__install__(installer)

        # create pkgconfig
        lib = Library(self.name, makefile=self.makefile)
        lib.library_type = LibraryType.INTERFACE
        installer.installed_files.append(await create_pkg_config(lib, installer.settings))
