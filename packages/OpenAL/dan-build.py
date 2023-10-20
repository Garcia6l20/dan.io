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
    installed = True
    cmake_config_definitions = {
        'ALSOFT_UTILS': 'OFF',
        'ALSOFT_EXAMPLES': 'OFF',
        'ALSOFT_TESTS': 'OFF',
        'ALSOFT_INSTALL_UTILS': 'OFF',
        'ALSOFT_INSTALL_EXAMPLES': 'OFF',
    }
    source_path = OpenALSources
