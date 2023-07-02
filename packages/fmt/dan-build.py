from dan import self
from dan.cmake import Project as CMakeProject
from dan.core.pathlib import Path
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '9.1.0')
description = 'A modern formatting library'

class FmtSources(GitHubReleaseSources):
    name = 'fmt-source'
    user = 'fmtlib'
    project = 'fmt'

class Fmt(CMakeProject):
    name = 'fmt'
    preload_dependencies = FmtSources,
    installed = True
    cmake_patch_debug_postfix = ['fmt']
    cmake_config_options = {
        'FMT_DOC': 'OFF',
        'FMT_TEST': 'OFF',
    }

    @property
    def source_path(self) -> Path:
        return self.get_dependency(FmtSources).output
