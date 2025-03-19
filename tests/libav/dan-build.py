from dan.cxx import Executable
from dan.testing import Test

class LibAvTest(Test, Executable):
    name = 'libav-test'
    dependencies = [
        'libavutil',
        'libavcodec',
        'libavdevice',
        'libavfilter',
        'libswresample',
        'libswscale',
    ]
    sources = 'test.cpp',
