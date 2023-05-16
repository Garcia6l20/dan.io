from dan import self
from dan.cxx import Library
from dan.smc import TarSources

version = self.options.add('version', '1.11.0').value
description = 'Fast C++ logging library'


class SpdlogSources(TarSources):
    name = 'spdlog-source'
    
    @property
    def url(self):
        return f'https://github.com/gabime/spdlog/archive/refs/tags/v{self.version}.tar.gz'


class Spdlog(Library):
    name = 'spdlog'
    preload_dependencies = SpdlogSources,
    dependencies = 'fmt = 9',
    public_compile_definitions = 'SPDLOG_COMPILED_LIB', 'SPDLOG_FMT_EXTERNAL'
    header_match = r'^(?:(?!bundled).)*\.(h.?)$'
    installed = True
    
    async def __initialize__(self):
        spdlog_root = self.get_dependency(SpdlogSources).output / f'spdlog-{self.version}'
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
