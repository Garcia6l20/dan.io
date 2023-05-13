from dan import self
from dan.cxx import Library, Executable
from dan.smc import TarSources
from dan.testing import Test, Case

version = self.options.add('version', '3.7.2').value
description = 'Compile Time Regular Expression in C++'


class CompileTimeRegularExpressionsSources(TarSources):
    name = 'ctre-source'
    url = f'https://github.com/hanickadot/compile-time-regular-expressions/archive/refs/tags/v{version}.tar.gz'


class CompileTimeRegularExpressions(Library):
    name = 'ctre'
    preload_dependencies = CompileTimeRegularExpressionsSources,
    installed = True

    async def __initialize__(self):
        root = self.get_dependency(CompileTimeRegularExpressionsSources).output / f'compile-time-regular-expressions-{version}'
        self.includes.add(root  / 'include', public=True)
        await super().__initialize__()

class CompileTimeRegularExpressionsTest(Test, Executable):
    name = 'ctre-test'
    dependencies = CompileTimeRegularExpressions,
    sources = 'test.cpp',
    cases = [
        Case('match', 'hello ctre', expected_result=1),
        Case('no-match', 'ola ctre', expected_result=0),
    ]
