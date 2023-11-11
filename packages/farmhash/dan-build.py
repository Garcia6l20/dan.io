from dan import self
from dan.src.tar import TarSources
from dan.cxx import Library
from dan.core import cache

version = self.options.add('version', '0.0.0') # no version
description = 'Google\'s farmhash library'

class FarmHashSources(TarSources):
    url = 'https://github.com/google/farmhash/archive/master.zip'
    archive_name = 'farmhash-sources.zip'

class  FarmHash(Library):
    name = 'farmhash'
    installed = True
    source_path = FarmHashSources
    public_includes = ['src']
    
    @cache.once_method
    def _init_sources(self):
        self.sources = [
            'src/farmhash.cc'
        ]
        super()._init_sources()
