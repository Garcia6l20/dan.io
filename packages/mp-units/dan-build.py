from dan import self
from dan.cxx import Library
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '0.8.0')
description = 'A Physical Quantities and Units library for C++'


class MpUnitsSources(GitHubReleaseSources):
    name = 'mp-units-sources'
    user = 'mpusz'
    project = 'mp-units'


class MpUnits(Library):
    name = 'mp-units'
    source_path = MpUnitsSources
    installed = True
    dependencies = ['gsl-lite', 'fmt = 9', 'wg21-linear-algebra']
    public_includes = ['src/core/include', 'src/core-fmt/include', 'src/core-io/include']

    async def __initialize__(self):
        for p in (self.source_path / 'src' / 'systems').iterdir():
            p /= 'include'
            if p.exists():
                self.includes.add(p.relative_to(self.source_path), public=True)
        return await super().__initialize__()
