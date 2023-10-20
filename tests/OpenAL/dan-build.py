from dan.cxx import Executable
from dan.testing import Test

class OpenALTest(Test, Executable):
    cpp_std = 20
    name = 'openal-test'
    dependencies = [
        'OpenAL',
    ]
    sources = 'test.cpp',
