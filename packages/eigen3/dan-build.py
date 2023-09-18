from dan import self
from dan.src import TarSources
from dan.cmake import Project as CMakeProject


version = self.options.add('version', '3.4.0')
description = 'C++ template library for linear algebra'

class Eigen3Sources(TarSources):
    name = 'eigen3-sources'

    @property
    def url(self):
        return f'https://gitlab.com/libeigen/eigen/-/archive/{self.version}/eigen-{self.version}.tar.gz'
    
    async def available_versions(self):
        return [
            '3.4.0',
        ]
    
class Eigen3(CMakeProject):
    name = 'eigen3'
    source_path = Eigen3Sources
    installed = True
    cmake_config_definitions = {
        'EIGEN_BUILD_DOC': 'OFF',
        'EIGEN_BUILD_TESTING': 'OFF',
        'EIGEN_BUILD_PKGCONFIG': 'ON',
    }
