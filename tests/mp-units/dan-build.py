from dan.cxx import Executable
from dan.testing import Test

cpp_std = 20

class MpUnitsTest(Test, Executable):
    dependencies = [
        'mp-units'
    ]
    sources = [
        'mp-units-test.cpp'
    ]
