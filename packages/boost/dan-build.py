import asyncio
from pathlib import Path
from dan import self
from dan.cxx import Library
from dan.src.github import GitHubReleaseSources

name = 'boost'
version = self.options.add('version', '1.82.0')
description = 'Boost provides free peer-reviewed portable C++ source libraries.'

class BoostSources(GitHubReleaseSources):
    name = 'boost-source'
    user = 'boostorg'
    project = 'boost'

class Headers(Library):
    name = 'boost-headers'
    preload_dependencies = BoostSources,
    installed = True

    async def __initialize__(self):
        src: Path = self.get_dependency(BoostSources).output
        [self.includes.add(d / 'include', public=True) for d in (src / 'libs').iterdir() if d.is_dir()]
        return await super().__initialize__()
