from dan import self
from dan.src.github import GitHubReleaseSources
from dan.autoconf import Project as AutoConfProject

version = self.options.add('version', '7.1.1')
description = 'A complete, cross-platform solution to record, convert and stream audio and video.'


class FFMpegSources(GitHubReleaseSources):
    name = 'ffmpeg-source'
    user = 'FFmpeg'
    project = 'FFmpeg'
    use_tags = True
    git_apply = True
    patches = []

class FFMpeg(AutoConfProject):
    name = 'ffmpeg'
    provides = [
        'libavutil',
        'libavcodec',
        'libavdevice',
        'libavfilter',
        'libswresample',
        'libswscale',
    ]
    preload_dependencies = []
    source_path = FFMpegSources
    installed = True
    env = {
        # 'CFLAGS': '-Wno-attributes -Wno-incompatible-pointer-types'
    }
    configure_output = 'config.h'
    configure_options = [
        '--disable-yasm',
        '--disable-doc',
        # '--enable-fft',
        # '--enable-rdft',
    ]
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.toolchain.build_type.is_debug_mode:
            self.configure_options.append('--disable-debug')
