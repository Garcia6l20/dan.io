from dan import self
from dan.cxx import Library, Executable
from dan.smc import TarSources
from dan.testing import Test, Case

version_opt = self.options.add('version', '9.1.0')
version = version_opt.value
description = 'A modern formatting library'

class FmtSources(TarSources):
    name = 'fmt-source'
    url = f'https://github.com/fmtlib/fmt/archive/refs/tags/{version}.tar.gz'


class Fmt(Library):
    name = 'fmt'
    preload_dependencies = FmtSources,
    installed = True
    
    async def __initialize__(self):        
        src = self.get_dependency(FmtSources).output / f'fmt-{version}'
        self.includes.add(src / 'include', public=True)
        self.sources = [
            src / 'src/format.cc',
            src / 'src/os.cc',
        ]
        await super().__initialize__()

class FmtTest(Test, Executable):
    name = 'fmt-test'
    dependencies = Fmt,
    sources = 'test.cpp',
    cases = [
        Case('default', expected_output='Hello world'),
        Case('custom', 'custom', expected_output='Hello custom'),
    ]
