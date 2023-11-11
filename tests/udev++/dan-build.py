from dan.cxx import Executable
from dan.testing import Test

class UDevPPTest(Test, Executable):
    cpp_std = 20
    name = 'udev++-test'
    dependencies = [
        'udev++',
    ]
    sources = 'test.cpp',
