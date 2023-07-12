from dan import self
from dan.cmake import Project as CMakeProject
from dan.core.target import Installer
from dan.pkgconfig.package import create_pkg_config
from dan.cxx import Library, LibraryType
from dan.src.github import GitHubReleaseSources
from pathlib import Path

description = 'An open source, portable, easy to use, readable and flexible TLS library, and reference implementation of the PSA Cryptography API.'
version = self.options.add('version', '1.21.0')

class OpenALSources(GitHubReleaseSources):
    name = 'OpenAL-source'
    user = 'kcat'
    project = 'openal-soft'
    use_tags = True


class OpenAL(CMakeProject):
    name = 'OpenAL'
    preload_dependencies = OpenALSources,
    installed = True
    cmake_config_definitions = {
        'ALSOFT_UTILS': 'OFF',
        'ALSOFT_EXAMPLES': 'OFF',
        'ALSOFT_TESTS': 'OFF',
        'ALSOFT_INSTALL_UTILS': 'OFF',
        'ALSOFT_INSTALL_EXAMPLES': 'OFF',
    }
    
    @property
    def source_path(self):
        return self.get_dependency(OpenALSources).output

    async def __install__(self, installer: Installer):
        await super().__install__(installer)

        # create pkgconfig
        lib = Library(self.name, makefile=self.makefile)
        if self.toolchain.system.is_windows:
            # hacky way to add 32-suffix
            lib.library_type = LibraryType.INTERFACE
            lib.link_libraries.add(self.name + '32', public=True)
            lib.library_paths.add(Path('${libdir}/unused'), public=True)
        installer.installed_files.extend((
            await create_pkg_config(lib, installer.settings),
        ))
