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
    cmake_patch_debug_postfix = ['Catch2', 'Catch2Main']
    cmake_config_definitions = {
        'CATCH_CONFIG_BAZEL_SUPPORT': 'OFF'
    }
    cmake_options = {
        'android_logwrite': ('CATCH_CONFIG_ANDROID_LOGWRITE', False, 'Read docs/configuration.md for details'),
        'colour_win32': ('CATCH_CONFIG_COLOUR_WIN32', False, 'Read docs/configuration.md for details'),
        'console_width': ('CATCH_CONFIG_CONSOLE_WIDTH', 80, 'Read docs/configuration.md for details. Must form a valid integerliteral.'),
        'counter': ('CATCH_CONFIG_COUNTER', False, 'Read docs/configuration.md for details'),
        'cpp11_to_string': ('CATCH_CONFIG_CPP11_TO_STRING', False, 'Read docs/configuration.md for details'),
        'cpp17_byte': ('CATCH_CONFIG_CPP17_BYTE', False, 'Read docs/configuration.md for details'),
        'cpp17_optional': ('CATCH_CONFIG_CPP17_OPTIONAL', False, 'Read docs/configuration.md for details'),
        'cpp17_string_view': ('CATCH_CONFIG_CPP17_STRING_VIEW', False, 'Read docs/configuration.md for details'),
        'cpp17_uncaught_exceptions': ('CATCH_CONFIG_CPP17_UNCAUGHT_EXCEPTIONS', False, 'Read docs/configuration.md for details'),
        'cpp17_variant': ('CATCH_CONFIG_CPP17_VARIANT', False, 'Read docs/configuration.md for details'),
        'default_reporter': ('CATCH_CONFIG_DEFAULT_REPORTER', 'console', 'Read docs/configuration.md for details. The name of thereporter should be without quotes.'),
        'disable': ('CATCH_CONFIG_DISABLE', False, 'Read docs/configuration.md for details'),
        'disable_exceptions': ('CATCH_CONFIG_DISABLE_EXCEPTIONS', False, 'Read docs/configuration.md for details'),
        'disable_exceptions_custom_handler': ('CATCH_CONFIG_DISABLE_EXCEPTIONS_CUSTOM_HANDLER', False, 'Read docs/configuration.md for details'),
        'disable_stringification': ('CATCH_CONFIG_DISABLE_STRINGIFICATION', False, 'Read docs/configuration.md for details'),
        'enable_all_stringmakers': ('CATCH_CONFIG_ENABLE_ALL_STRINGMAKERS', False, 'Read docs/configuration.md for details'),
        'enable_optional_stringmaker': ('CATCH_CONFIG_ENABLE_OPTIONAL_STRINGMAKER', False, 'Read docs/configuration.md for details'),
        'enable_pair_stringmaker': ('CATCH_CONFIG_ENABLE_PAIR_STRINGMAKER', False, 'Read docs/configuration.md for details'),
        'enable_tuple_stringmaker': ('CATCH_CONFIG_ENABLE_TUPLE_STRINGMAKER', False, 'Read docs/configuration.md for details'),
        'enable_variant_stringmaker': ('CATCH_CONFIG_ENABLE_VARIANT_STRINGMAKER', False, 'Read docs/configuration.md for details'),
        'experimental_redirect': ('CATCH_CONFIG_EXPERIMENTAL_REDIRECT', False, 'Read docs/configuration.md for details'),
        'fast_compile': ('CATCH_CONFIG_FAST_COMPILE', False, 'Read docs/configuration.md for details'),
        'getenv': ('CATCH_CONFIG_GETENV', False, 'Read docs/configuration.md for details'),
        'global_nextafter': ('CATCH_CONFIG_GLOBAL_NEXTAFTER', False, 'Read docs/configuration.md for details'),
        'nostdout': ('CATCH_CONFIG_NOSTDOUT', False, 'Read docs/configuration.md for details'),
        'posix_signals': ('CATCH_CONFIG_POSIX_SIGNALS', False, 'Read docs/configuration.md for details'),
        'prefix_all': ('CATCH_CONFIG_PREFIX_ALL', False, 'Read docs/configuration.md for details'),
        'use_async': ('CATCH_CONFIG_USE_ASYNC', False, 'Read docs/configuration.md for details'),
        'wchar': ('CATCH_CONFIG_WCHAR', False, 'Read docs/configuration.md for details'),
        'windows_crtdbg': ('CATCH_CONFIG_WINDOWS_CRTDBG', False, 'Read docs/configuration.md for details'),
        'windows_seh': ('CATCH_CONFIG_WINDOWS_SEH', False, 'Read docs/configuration.md for details')}

    @ property
    def source_path(self):
        return self.get_dependency(Catch2Source).output


@ Catch2.utility
def discover_tests(self, ExecutableClass):
    from dan.cxx import Executable
    from dan.core.pm import re_match

    if not issubclass(ExecutableClass, Executable):
        raise RuntimeError(
            f'catch2.discover_tests requires an Executable class, not a {ExecutableClass.__name__}')

    makefile = ExecutableClass.get_static_makefile()

    from dan.testing import Test, Case

    @ makefile.wraps(ExecutableClass)
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

        @ property
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
                self.debug('test cases found: %s', ', '.join(
                    [c.name for c in self.cases]))
                self.cache['cases'] = self.cases
    return Catch2Test
