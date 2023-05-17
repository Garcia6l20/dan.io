import asyncio
from pathlib import Path
from dan import self
from dan.cxx import Library
from dan.smc import TarSources

name = 'boost'
version = self.options.add('version', '1.82.0')
description = 'Boost provides free peer-reviewed portable C++ source libraries.'

class BoostSources(TarSources):
    name = 'boost-source'

    @property
    def url(self):
        return f'https://github.com/boostorg/boost/releases/download/boost-{self.version}/boost-{self.version}.tar.gz'

internal_build = self.options.add('internal-build', False)

if internal_build.value:

    # internal build of boost may fall in the case that command line is too long...
    #
    # to by-pass this, we create an intermediate target that copies all headers into a unique location,
    # in order to avoid long include paths options

    from dan.core.target import Target
    from dan.core.utils import chunks
    from dan.core import aiofiles

    class HeadersBuild(Target):
        preload_dependencies = BoostSources,
        installed = False
        output = 'headers'
        
        async def __build__(self):        
            src: Path = self.get_dependency(BoostSources).output / f'boost-{self.version}'        
            self.output.mkdir(exist_ok=True, parents=True)
            tasks = list()

            # copy all headers into <build_dir>/headers/include
            for d in [d for d in (src / 'libs').iterdir() if d.is_dir()]:
                for header in (d / 'include').rglob('*.hpp'):
                    dest = self.output / header.parent.relative_to(d)
                    dest.mkdir(exist_ok=True, parents=True)
                    tasks.append(aiofiles.copy(header, dest))
            
            # chunk copies since it may result in too many open files
            for sub_tasks in chunks(tasks, 100):
                await asyncio.gather(*sub_tasks)


    class Headers(Library):
        name = 'headers'
        dependencies = HeadersBuild,
        installed = True
        public_includes = HeadersBuild.output / 'include',

else:
    # for non-internal use, everything is ok since all headers will be installed
    
    class Headers(Library):
        name = 'headers'
        preload_dependencies = BoostSources,
        installed = True
    
        async def __initialize__(self):
            src: Path = self.get_dependency(BoostSources).output / f'boost-{self.version}'   
            [self.includes.add(d / 'include', public=True) for d in (src / 'libs').iterdir() if d.is_dir()]
            return await super().__initialize__()
