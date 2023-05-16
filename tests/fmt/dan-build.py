from dan.cxx import Executable
from dan.testing import Test, Case

class FmtTest(Test, Executable):
    name = 'fmt-test'
    dependencies = 'fmt',
    sources = 'test.cpp',
    cases = [
        Case('default', expected_output='Hello world'),
        Case('custom', 'custom', expected_output='Hello custom'),
    ]
