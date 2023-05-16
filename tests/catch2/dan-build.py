from dan import requires
from dan.cxx import Executable

catch2, = requires('catch2')

@catch2.discover_tests
class Catch2Test(Executable):
    name = 'catch2-test'
    sources = 'test.cpp',
    dependencies = catch2,
