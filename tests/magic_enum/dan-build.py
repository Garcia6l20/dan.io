from dan.cxx import Executable
from dan.testing import Test, Case

class MagicEnumTest(Test, Executable):
    name = 'magic_enum-test'
    dependencies = 'magic_enum',
    sources = 'test.cpp',
    cases = [
        Case('default', expected_output='ONE'),
    ]
