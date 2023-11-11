from dan import self
from dan.cmake import Project as CMakeProject
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '24.3')
description = 'Protocol Buffers - Google\'s data interchange format'


class ProtobufSources(GitHubReleaseSources):
    name = 'protobuf-sources'
    user = 'protocolbuffers'
    project = 'protobuf'


class Protobuf(CMakeProject):
    name = 'protobuf'
    source_path = ProtobufSources
    installed = True
    dependencies = [
        'absl_synchronization',
    ]
    cmake_config_definitions = {
        'protobuf_INSTALL': 'ON',
        'protobuf_BUILD_TESTS': 'OFF',
        'protobuf_BUILD_EXAMPLES': 'OFF',
        'protobuf_BUILD_PROTOBUF_BINARIES': 'ON',
        'protobuf_BUILD_PROTOC_BINARIES': 'ON',
        'protobuf_BUILD_LIBPROTOC': 'ON',
        'protobuf_ABSL_PROVIDER': 'package',
        'protobuf_JSONCPP_PROVIDER': 'package',
    }
    cmake_options = {
    }
    provides = [
        'protobuf',
        'protobuf-lite'
    ]
    cmake_patch_debug_postfix = provides
