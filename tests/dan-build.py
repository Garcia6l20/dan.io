from dan import include
from dan.cxx import target_toolchain

name = 'dan.io-tests'

include(
    'absl',
    'protobuf',
    'eigen3',
    'yggdrasil-decision-forests',
    'catch2',
    'ctre',
    'fmt',
    'magic_enum',
    'spdlog',
    'mbedtls',
    'boost',
    'webview',
    'mp-units',
    'OpenAL',
    'libav',
    'Qt6',
)


if target_toolchain.system.is_linux:
    include(
        'udev++',
    )
