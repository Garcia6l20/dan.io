import re
from dan.cxx import Executable
from dan.testing import Test, Case

class SpdlogTest(Test, Executable):
    name = 'spdlog-test'
    dependencies = 'spdlog',
    sources = 'test.cpp',
    cases = [
        Case('default', expected_output=re.compile(r'.+\[info\] Hello world')),
        Case('custom', 'custom', expected_output=re.compile(r'.+\[info\] Hello custom')),
    ]
