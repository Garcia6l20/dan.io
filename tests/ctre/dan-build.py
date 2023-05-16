from dan.cxx import Executable
from dan.testing import Test, Case

class CompileTimeRegularExpressionsTest(Test, Executable):
    name = 'ctre-test'
    dependencies = 'ctre',
    sources = 'test.cpp',
    cases = [
        Case('match', 'hello ctre', expected_result=1),
        Case('no-match', 'ola ctre', expected_result=0),
    ]
