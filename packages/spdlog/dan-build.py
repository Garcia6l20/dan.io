from dan import self
from dan.cmake import Project as CMakeProject
from dan.core.requirements import RequiredPackage
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '1.11.0')
description = 'Fast C++ logging library'


class SpdlogSources(GitHubReleaseSources):
    name = 'spdlog-source'
    user = 'gabime'
    project = 'spdlog'

class Spdlog(CMakeProject):
    name = 'spdlog'
    preload_dependencies = SpdlogSources,
    installed = True
    dependencies = [
        RequiredPackage('fmt = 9'),
    ]
    cmake_patch_debug_postfix = ['spdlog']
    cmake_config_options = {
        'SPDLOG_FMT_EXTERNAL': 'ON',
        'SPDLOG_BUILD_PIC': 'ON',
        'SPDLOG_BUILD_EXAMPLE': 'OFF',
    }
    
    @property
    def source_path(self):
        return self.get_dependency(SpdlogSources).output
