from dan import self
from dan.cmake import Project as CMakeProject
from dan.src.github import GitHubReleaseSources
from dan.core.target import Installer
from dan.cxx import Library, LibraryType
from dan.pkgconfig.package import create_pkg_config


version = self.options.add('version', '1.0')
description = 'A Udev Library for C++'


class UDevPPSources(GitHubReleaseSources):
    name = 'udevpp-source'
    user = 'dimitry-ishenko-cpp'
    project = 'libudevpp'
    use_tags = True



class UDevPP(CMakeProject):
    name = 'udev++'
    installed = True
    cmake_config_definitions = {
    }
    source_path = UDevPPSources

    async def __install__(self, installer: Installer):
        await super().__install__(installer)

        # create pkgconfig
        lib = Library('udev++', makefile=self.makefile)
        lib.library_type = LibraryType.SHARED
        lib.link_options.add('-ludev', public=True)
        installer.installed_files.append(await create_pkg_config(lib, installer.settings))

