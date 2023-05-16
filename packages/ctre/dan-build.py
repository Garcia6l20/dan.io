from dan import self
from dan.cxx import Library
from dan.smc import TarSources

version = self.options.add('version', '3.7.2').value
description = 'Compile Time Regular Expression in C++'


class CompileTimeRegularExpressionsSources(TarSources):
    name = 'ctre-source'
    @property
    def url(self):
        return f'https://github.com/hanickadot/compile-time-regular-expressions/archive/refs/tags/v{self.version}.tar.gz'


class CompileTimeRegularExpressions(Library):
    name = 'ctre'
    preload_dependencies = CompileTimeRegularExpressionsSources,
    installed = True

    async def __initialize__(self):
        root = self.get_dependency(CompileTimeRegularExpressionsSources).output / f'compile-time-regular-expressions-{self.version}'
        self.includes.add(root  / 'include', public=True)
        await super().__initialize__()
