from dan import include
from dan.cxx import target_toolchain

include(
    "absl",
    "protobuf",
    "farmhash",
    "eigen3",
    "yggdrasil-decision-forests",
    "catch2",
    "ctre",
    "fmt",
    "magic_enum",
    "spdlog",
    "mbedtls",
    "boost",
    "webview",
    "gsl-lite",
    "wg21-linear-algebra",
    "mp-units",
    "OpenAL",
    "yasm",
    "ffmpeg",
    "Qt6",
)

if target_toolchain.system.is_linux:
    include(
        "uring",
        "udev++",
    )
