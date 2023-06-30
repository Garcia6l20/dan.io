from dan import include
from dan.cxx import target_toolchain

include(
    'catch2',
    'ctre',
    'fmt',
    'magic_enum',
    'spdlog',
    'mbedtls',
    'boost',
)

if target_toolchain.system == 'linux':
    include('uring')
