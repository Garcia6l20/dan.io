from dan import self
from dan.jinja import generator
from dan.core.version import Version
from dan.cxx import (
    Library,
    target_toolchain as tc)
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '2.4')
description = 'Helpers to setup and teardown io_uring instances'

class UringSources(GitHubReleaseSources):
    use_tags = True     # use tags, first GH release is 2.4
    name = 'liburing-source'
    user = 'axboe'
    project = 'liburing'


def has_kernel_rwf_t():
    return tc.can_compile('''
        #include <linux/fs.h>
        int main(int argc, char **argv)
        {
            __kernel_rwf_t x;
            x = 0;
            return x;
        }
        ''')


def has_kernel_timespec():
    return tc.can_compile('''
        #include <linux/time.h>
        #include <linux/time_types.h>
        int main(int argc, char **argv)
        {
            struct __kernel_timespec ts;
            ts.tv_sec = 0;
            ts.tv_nsec = 1;
            return 0;
        }
        ''')


def has_open_how():
    return tc.can_compile('''
        #include <sys/types.h>
        #include <sys/stat.h>
        #include <fcntl.h>
        #include <string.h>
        int main(int argc, char **argv)
        {
            struct open_how how;
            how.flags = 0;
            how.mode = 0;
            how.resolve = 0;
            return 0;
        }
        ''')


@generator('liburing/host-config.h', 'host-config.h.jinja')
def host_config():
    return {
        'no_libc': False,
        'has_kernel_rwf_t': has_kernel_rwf_t(),
        'has_kernel_timespec': has_kernel_timespec(),
        'has_open_how': has_open_how(),
        'has_statx': tc.can_compile('''
            #include <sys/types.h>
            #include <sys/stat.h>
            #include <unistd.h>
            #include <fcntl.h>
            #include <string.h>
            int main(int argc, char **argv)
            {
                struct statx x;

                return memset(&x, 0, sizeof(x)) != NULL;
            }
            '''),
        'has_glibc_statx': tc.can_compile('''
            #include <sys/types.h>
            #include <unistd.h>
            #include <fcntl.h>
            #include <string.h>
            #include <sys/stat.h>
            int main(int argc, char **argv)
            {
                struct statx x;

                return memset(&x, 0, sizeof(x)) != NULL;
            }
            '''),
        'has_cxx': True,  # maybe not...
        'has_ucontext': tc.can_compile('''#include <ucontext.h>
            int main(int argc, char **argv)
            {
                ucontext_t ctx;
                getcontext(&ctx);
                makecontext(&ctx, 0, 0);
                return 0;
            }
            '''),
        'has_stringop_overflow': tc.has_cxx_compile_options('-Wstringop-overflow'),
        'has_array_bounds': tc.has_cxx_compile_options('-Warray-bounds'),
        'has_nvme_uring': tc.can_compile('''#include <linux/nvme_ioctl.h>
            int main(void)
            {
                struct nvme_uring_cmd *cmd;

                return sizeof(struct nvme_uring_cmd);
            }
            '''),
        'has_fanotify': tc.can_compile('''#include <linux/nvme_ioctl.h>
            #include <sys/fanotify.h>
            int main(void) { return 0; }
            '''),
    }


@generator('liburing/compat.h', 'compat.h.jinja')
def compat():
    return {
        'has_kernel_rwf_t': has_kernel_rwf_t(),
        'has_kernel_timespec': has_kernel_timespec(),
        'has_open_how': has_open_how(),
    }

@generator('liburing/io_uring_version.h', 'version.h.jinja')
def version_header():
    return {
        'version': Version(version.value)
    }

class LibUring(Library):
    name = 'uring'
    description = description
    preload_dependencies = [UringSources]
    dependencies = [version_header, compat, host_config]
    installed = True
    
    def sources(self):
        src = self.get_dependency(UringSources).output / 'src'
        sources = [
            src / 'syscall.c',
            src / 'queue.c',
            src / 'register.c',
            src / 'setup.c',
        ]
        if self.version >= '2.4':
            sources.append(src / 'version.c')
        return sources
    
    async def __initialize__(self):

        src = self.get_dependency(UringSources).output / 'src'
        self.includes.add(src / 'include', self.build_path, public=True)
        self.compile_definitions.add('_GNU_SOURCE')

        await super().__initialize__()
