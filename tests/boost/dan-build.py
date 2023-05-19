from dan.cxx import Executable
from dan.testing import Test, Case

class BoostTest(Test, Executable):
    name = 'boost-test'
    sources= 'boost_test.cpp',
    dependencies= 'boost:boost-headers',    
    cases = [
        Case('42-12', 42, 12, expected_result=6),
        Case('44-8', 44, 8, expected_result=4),
        Case('142-42', 142, 42, expected_result=2),
    ]
