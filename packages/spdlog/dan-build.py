from dan import self
from dan.cxx import Library
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '1.11.0')
description = 'Fast C++ logging library'


class SpdlogSources(GitHubReleaseSources):
    name = 'spdlog-source'
    user = 'gabime'
    project = 'spdlog'


class Spdlog(Library):
    name = 'spdlog'
    preload_dependencies = SpdlogSources,
    dependencies = 'fmt = 9',
    public_compile_definitions = 'SPDLOG_COMPILED_LIB', 'SPDLOG_FMT_EXTERNAL'
    header_match = r'^(?:(?!bundled).)*\.(h.?)$'
    installed = True
    
    async def __initialize__(self):
        spdlog_root = self.get_dependency(SpdlogSources).output
        self.includes.add(spdlog_root  / 'include', public=True)
        spdlog_src = spdlog_root / 'src'
        self.sources = [
            spdlog_src / 'async.cpp',
            spdlog_src / 'cfg.cpp',
            spdlog_src / 'color_sinks.cpp',
            spdlog_src / 'file_sinks.cpp',
            spdlog_src / 'stdout_sinks.cpp',
            spdlog_src / 'spdlog.cpp',
        ]
        
        if self.toolchain.type != 'msvc':
            self.link_libraries.add('pthread', public=True)

        await super().__initialize__()
