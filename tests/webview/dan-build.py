from dan.cxx import Executable
from dan.testing import Test


class WebviewTest(Test, Executable):
    dependencies = [
        'webview'
    ]
    sources = [
        'webview-test.cpp'
    ]
