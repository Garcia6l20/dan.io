from dan.cxx import Executable

class Eigen3Test(Executable):
    name = 'eigen-test'
    sources = [
        'main.cpp',
    ]
    dependencies = [
        'eigen3',
    ]
