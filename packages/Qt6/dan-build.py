from pathlib import Path
from dan import self
from dan.core.target import Installer
from dan.core.version import Version
from dan.cmake import Project as CMakeProject
from dan.src import TarSources
from tarfile import TarInfo


class BaseQtSource(TarSources, internal=True):
    default = False
    submodule = None

    def extract_filter(self, member: TarInfo, dst: str):
        # some file members exist in archive without the directory entry defined
        Path(dst).parent.mkdir(exist_ok=True, parents=True)
        return member

    async def available_versions(self):
        return [
            '6.5.1',
        ]

    @property
    def url(self):
        version = Version(self.makefile.version.value)
        maj_min = f'{version.major}.{version.minor}'
        return f'https://download.qt.io/official_releases/qt/{maj_min}/{version}/submodules/{self.submodule}-everywhere-src-{version}.tar.xz'


class BaseQtProject(CMakeProject, internal=True):
    installed = True
    cmake_generator = 'Ninja'

    @property
    def subdirectory(self):
        return self.name

    async def __install__(self, installer: Installer):
        await super().__install__(installer)

        if self.toolchain.build_type.is_debug_mode:
            # patch Qt6Platform pkgconfig
            from dan.core.find import find_file
            from dan.core import aiofiles

            pc = find_file(r'Qt6Platform\.pc', installer.settings.libraries_destination / 'pkgconfig')
            async with aiofiles.open(pc) as f:
                content = await f.readlines()
            new_content = []
            for line in content:

                if line.startswith('Cflags'):
                    # remplace invalid _UNICODE compile definition
                    line = line.replace('_UNICODE>', '_UNICODE')
                
                new_content.append(line)

            async with aiofiles.open(pc, 'w') as f:
                await f.writelines(new_content)

description = 'Qt libraries'

version = self.options.add('version', '6.5.1')

#
# Qt6Base
#

class Qt6BaseSources(BaseQtSource):
    submodule = 'qtbase'

class Qt6Base(BaseQtProject):
    source_path = Qt6BaseSources
    cmake_config_definitions = {
        'QT_BUILD_EXAMPLES': 'FALSE',
        'QT_BUILD_BENCHMARKS': 'FALSE',
        'QT_BUILD_QMAKE': 'FALSE',
        'QT_BUILD_TESTS': 'FALSE',
        'QT_BUILD_ONLINE_DOCS': 'FALSE',
        'QT_INSTALL_DOCS': 'FALSE',
    }
    provides = [
        'Qt6Concurrent',
        'Qt6Core',
        'Qt6DBus',
        'Qt6Gui',
        'Qt6Network',
        'Qt6OpenGL',
        'Qt6OpenGLWidgets',
        'Qt6Platform',
        'Qt6PrintSupport',
        'Qt6Sql',
        'Qt6Test',
        'Qt6Widgets',
        'Qt6Xml',
    ]

#
# Qt6Svg
#

class Qt6SvgSources(BaseQtSource):
    submodule = 'qtsvg'

class Qt6Svg(BaseQtProject):
    source_path = Qt6SvgSources
    cmake_config_definitions = {
        'QT_BUILD_EXAMPLES': 'FALSE',
        'QT_BUILD_TESTS': 'FALSE',
        'QT_INSTALL_DOCS': 'FALSE',
    }
    dependencies = [
        Qt6Base,
    ]
    provides = [
        'Qt6Svg', 'Qt6SvgWidgets'
    ]

