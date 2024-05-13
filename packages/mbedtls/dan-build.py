from dan import self
from dan.cmake import Project as CMakeProject
from dan.core.target import Installer
from dan.pkgconfig.package import create_pkg_config
from dan.cxx import Library
from dan.src.github import GitHubReleaseSources

description = 'An open source, portable, easy to use, readable and flexible TLS library, and reference implementation of the PSA Cryptography API.'
version = self.options.add('version', '3.4.0')

class MbedTLSSources(GitHubReleaseSources):
    name = 'mbedtls-source'
    user = 'Mbed-TLS'
    project = 'mbedtls'


class MBedTls(CMakeProject):
    name = 'mbedtls'
    preload_dependencies = MbedTLSSources,
    installed = True
    provides = ['mbedtls', 'mbedx509', 'mbedcrypto']
    cmake_config_definitions = {
        'ENABLE_PROGRAMS': 'OFF',
        'ENABLE_TESTING': 'OFF',
    }
    
    @property
    def source_path(self):
        return self.get_dependency(MbedTLSSources).output
    
    async def __build__(self):
        if self.version >= "3.6.0":
            (self.source_path / "framework/CMakeLists.txt").touch()
        return await super().__build__()

    async def __install__(self, installer: Installer):
        await super().__install__(installer)

        if self.version < "3.6":
            # create pkgconfig
            crypto = Library('mbedcrypto', makefile=self.makefile)
            x509 = Library('mbedx509', makefile=self.makefile)
            x509.dependencies.add(crypto)
            tls = Library('mbedtls', makefile=self.makefile)
            tls.dependencies.add(x509)
            installer.installed_files.extend((
                await create_pkg_config(crypto, installer.settings),
                await create_pkg_config(x509, installer.settings),
                await create_pkg_config(tls, installer.settings),
            ))
