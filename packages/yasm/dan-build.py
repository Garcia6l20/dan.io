from dan import self
from dan.core.pathlib import Path
from dan.src.github import GitHubReleaseSources
from dan.core.target import Installer
from dan.cmake import Project as CMakeProject
from dan.pkgconfig.package import create_pkg_config

version = self.options.add('version', '1.3.0')
description = 'Yasm Assembler mainline development tree.'


class YasmSources(GitHubReleaseSources):
    name = 'yasm-source'
    user = 'yasm'
    project = 'yasm'
    use_tags = True


class Yasm(CMakeProject):
    name = 'yasm'
    source_path = YasmSources
    installed = True
    cmake_config_definitions = {
        'YASM_BUILD_TESTS': 'OFF',
    }
