from dan import self
from dan.cxx import Library
from dan.smc import TarSources

version = self.options.add('version', '9.1.0')
description = 'A modern formatting library'

class FmtSources(TarSources):
    name = 'fmt-source'

    @property
    def url(self):
        return f'https://github.com/fmtlib/fmt/archive/refs/tags/{self.version}.tar.gz'


class Fmt(Library):
    name = 'fmt'
    preload_dependencies = FmtSources,
    installed = True
    
    async def __initialize__(self):        
        src = self.get_dependency(FmtSources).output / f'fmt-{self.version}'
        self.includes.add(src / 'include', public=True)
        self.sources = [
            src / 'src/format.cc',
            src / 'src/os.cc',
        ]
        await super().__initialize__()
