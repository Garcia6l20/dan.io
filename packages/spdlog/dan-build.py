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
    cmake_config_definitions = {
        'SPDLOG_FMT_EXTERNAL': 'ON',
        'SPDLOG_BUILD_PIC': 'ON',
        'SPDLOG_BUILD_EXAMPLE': 'OFF',
        'SPDLOG_BUILD_EXAMPLE_HO': 'OFF',
        'SPDLOG_BUILD_BENCH': 'OFF',
        'SPDLOG_BUILD_TESTS': 'OFF',
        'SPDLOG_BUILD_TESTS_HO': 'OFF',
    }
    cmake_options = {
        'build_pic': ('SPDLOG_BUILD_PIC', True, 'Build position independent code (-fPIC)'),
        'build_shared': ('SPDLOG_BUILD_SHARED', False, 'Build shared library'),
        'disable_default_logger': ('SPDLOG_DISABLE_DEFAULT_LOGGER', False, 'Disable default logger creation'),
        'enable_pch': ('SPDLOG_ENABLE_PCH', False, 'Build static or shared library using precompiled header to speed up compilation time'),
        'no_atomic_levels': ('SPDLOG_NO_ATOMIC_LEVELS', False, 'prevent spdlog from using of std::atomic log levels (use only if your code never modifies log levels concurrently'),
        'no_exceptions': ('SPDLOG_NO_EXCEPTIONS', False, 'Compile with -fno-exceptions. Call abort() on any spdlog exceptions'),
        'no_thread_id': ('SPDLOG_NO_THREAD_ID', False, 'prevent spdlog from querying the thread id on each log call if thread id is not needed'),
        'no_tls': ('SPDLOG_NO_TLS', False, 'prevent spdlog from using thread local storage'),
        'prevent_child_fd': ('SPDLOG_PREVENT_CHILD_FD', False, 'Prevent from child processes to inherit log file descriptors'),
        'wchar_filenames': ('SPDLOG_WCHAR_FILENAMES', False, 'Support wchar filenames'),
        'wchar_support': ('SPDLOG_WCHAR_SUPPORT', False, 'Support wchar api'),
    }

    async def __initialize__(self):
        if self.toolchain.system.is_linux:
            self.cmake_options['clock_coarse'] = ('SPDLOG_CLOCK_COARSE', False, 'Use CLOCK_REALTIME_COARSE instead of the regular clock')
        return await super().__initialize__()

    @property
    def source_path(self):
        return self.get_dependency(SpdlogSources).output
