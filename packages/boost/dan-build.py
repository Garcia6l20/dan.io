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


def get_include_dirs(p: Path):
    return list(p.rglob('**/include/'))

class Headers(Library):
    name = 'boost-headers'
    source_path = BoostSources
    installed = True

    async def __initialize__(self):
        for d in get_include_dirs(self.source_path / 'libs'):
            self.includes.add(d, public=True)
        return await super().__initialize__()
