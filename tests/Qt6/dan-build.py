from dan.cxx import Executable
from dan.testing import Test

class Qt6Simple(Executable):
    name = 'qt6-simple'
    sources = 'simple.cpp',
    dependencies = 'Qt6Widgets',
