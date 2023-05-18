from dan import self
from dan.cxx import Library
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '0.8.2')
description = 'Static reflection for enums (to string, from string, iteration) for modern C++, work with any enum type without any macro or boilerplate code'


class MagicEnumSources(GitHubReleaseSources):
    name = 'magic_enum-source'
    user = 'Neargye'
    project = 'magic_enum'


class MagicEnum(Library):
    name = 'magic_enum'
    preload_dependencies = MagicEnumSources,
    installed = True

    async def __initialize__(self):
        root = self.get_dependency(MagicEnumSources).output
        self.includes.add(root  / 'include', public=True)
        await super().__initialize__()
