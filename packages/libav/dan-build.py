from dan import self
from dan.src.github import GitHubReleaseSources
from dan.autoconf import Project as AutoConfProject

version = self.options.add('version', '12.3')
description = 'A complete, cross-platform solution to record, convert and stream audio and video.'


class LibAvSources(GitHubReleaseSources):
    name = 'libav-source'
    user = 'libav'
    project = 'libav'
    use_tags = True

class LibAv(AutoConfProject):
    name = 'libav'
    provides = [
        'libavutil',
        'libavcodec',
        'libavdevice',
        'libavfilter',
        'libavresample',
        'libswscale',
    ]
    preload_dependencies = []
    source_path = LibAvSources
    installed = True
    env = {
        'CFLAGS': '-Wno-attributes'
    }
    configure_output = 'config.h'
    configure_options = [
        '--disable-yasm',
        '--disable-doc',
    ]
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.toolchain.build_type.is_debug_mode:
            self.configure_options.append('--disable-debug')
