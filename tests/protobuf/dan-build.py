from dan.cxx import Executable
from dan.testing import Test



from dan.core.pathlib import Path
from dan.pkgconfig.package import find_package
from dan.core.find import find_executable
from dan.core.runners import async_run
from dan.core import asyncio

class _ProtobufWrapper:
    
    from dan.cxx.targets import CXXObject

    class _ProtocObject(CXXObject, internal=True):
            
        def __init__(self, proto_file: Path, parent, *args, **kwargs) -> None:
            self.proto_file = Path(proto_file)
            name = self.proto_file.with_suffix('.pb.cc').name
            source_file = self.proto_file.with_name(name)
            if source_file.is_absolute():
                source_file = source_file.relative_to(parent.source_path)
            super().__init__(parent.build_path / source_file, parent, *args, **kwargs)
            if not self.proto_file.is_absolute():
                self.proto_file = self.source_path / self.proto_file
            self.dependencies.add(self.proto_file)

        async def __build__(self):
            p = self.parent
            self.source.parent.mkdir(parents=True, exist_ok=True)
            await async_run([p.protoc, f'-I{self.proto_file.parent}', f'--cpp_out={self.source.parent}',  self.proto_file], logger=p, log=False, cwd=self.build_path, env=self.toolchain.env)
            await super().__build__()

    async def __initialize__(self):

        pb =  find_package('protobuf', makefile=self.makefile)
        await pb.initialize()
        
        self.protoc = self.makefile.cache.get('protoc_executable')
        if not self.protoc:
            self.protoc = find_executable(
                'protoc', paths=[pb.prefix], default_paths=False)
            self.makefile.cache.protoc_executable = str(self.protoc)

        self.dependencies.add(pb)
        self.includes.add(self.build_path)

        if self.toolchain.system.is_windows:
            self.link_libraries.add('imagehlp', public=True)

        for proto_file in self.protobuf_files:
            pobj = self._ProtocObject(proto_file, self)
            self.objs.append(pobj)
        
        await super().__initialize__()

def wrap(proto_files: list[str] = None):
    if proto_files is None:
        proto_files = []
    def decorator(cls):
        from dan.core.include import context
        @context.current.wraps(cls)
        class ProtobufWapped(_ProtobufWrapper, cls):
            __name__ = f'{cls.__name__}ProtobufWapped'
            protobuf_files = proto_files
        return ProtobufWapped
    return decorator

@wrap(proto_files=['addressbook.proto'])
class ProtobufTest(Executable):
    name = 'protobuf-test'
    dependencies = [
        'protobuf'
    ]
    sources = [
        'main.cpp'
    ]
