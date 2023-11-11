from dan.cxx import Executable
from dan.testing import Test

class AbseilTest(Test, Executable):
    dependencies = [
        'absl_flags'
    ]
    sources = [
        'main.cpp'
    ]
