from dan import self
from dan.cmake import Project as CMakeProject
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '3.3.2')
description = 'A modern, C++-native, test framework for unit-tests, TDD and BDD'


class Catch2Source(GitHubReleaseSources):
    name = 'catch2-source'
    user = 'catchorg'
    project = 'Catch2'


class Catch2(CMakeProject):
    name = 'catch2'
    installed = True
    provides = ['catch2-with-main']
    preload_dependencies = [Catch2Source]
    cmake_options_prefix = 'CATCH'
    cmake_patch_debug_postfix = ['Catch2', 'Catch2Main']

    @property
    def source_path(self):
        return self.get_dependency(Catch2Source).output


@Catch2.utility
def discover_tests(self, ExecutableClass):
    from dan.cxx import Executable
    from dan.core.pm import re_match

    if not issubclass(ExecutableClass, Executable):
        raise RuntimeError(
            f'catch2.discover_tests requires an Executable class, not a {ExecutableClass.__name__}')

    makefile = ExecutableClass.get_static_makefile()

    from dan.testing import Test, Case
    @makefile.wraps(ExecutableClass)
    class Catch2Test(Test, ExecutableClass):
        name = ExecutableClass.name or ExecutableClass.__name__

        def __init__(self, *args, **kwargs):
            Test.__init__(self, *args, **kwargs)
            ExecutableClass.__init__(self, *args, **kwargs)
            cases = self.cache.get('cases')
            if cases is not None:
                self.cases = cases
                self._up_to_date = True
            else:
                self._up_to_date = False
        
        @property
        def up_to_date(self):
            return self._up_to_date and super().up_to_date

        async def __build__(self):
            await super().__build__()
            if self.output.exists():
                out, err, rc = await self.execute('--list-tests', no_raise=True, log=False, build=False)
                self.cases = list()
                filepath = self.source_path / self.sources[0]
                for line in out.splitlines():
                    match re_match(line):
                        case r'  (\w.+)$' as m:
                            self.cases.append(Case(m[1], m[1], file=filepath))
                # search lineno
                from dan.core import aiofiles
                async with aiofiles.open(filepath, 'r') as f:
                    for lineno, line in enumerate(await f.readlines()):
                        match re_match(line):
                            case r"(TEST_CASE|SCENARIO|TEMPLATE_TEST_CASE)\(\s?\"(.*?)\".+" as m:
                                # macro = m[1]
                                name = m[2]
                                for case in self.cases:
                                    if case.name == name:
                                        case.lineno = lineno
                                        break
                self.debug('test cases found: %s', ', '.join([c.name for c in self.cases]))
                self.cache['cases'] = self.cases
    return Catch2Test
