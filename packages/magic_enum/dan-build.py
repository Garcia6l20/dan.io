from dan import self
from dan.cxx import Library
from dan.smc import TarSources

version = self.options.add('version', '0.8.2').value
description = 'Static reflection for enums (to string, from string, iteration) for modern C++, work with any enum type without any macro or boilerplate code'


class MagicEnumSources(TarSources):
    name = 'magic_enum-source'
    
    @property
    def url(self):
        return f'https://github.com/Neargye/magic_enum/archive/refs/tags/v{self.version}.tar.gz'


class MagicEnum(Library):
    name = 'magic_enum'
    preload_dependencies = MagicEnumSources,
    installed = True

    async def __initialize__(self):
        root = self.get_dependency(MagicEnumSources).output / f'magic_enum-{self.version}'
        self.includes.add(root  / 'include', public=True)
        await super().__initialize__()
