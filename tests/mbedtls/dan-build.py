from pathlib import Path
import aiofiles
from dan.cxx import Executable
from dan.testing import Test

class CriptAndHash(Executable):
    name = 'crypt_and_hash'
    sources = f'{name}.c',
    dependencies = 'mbedtls:mbedcrypto',

class CriptAndHashTest(Test):
    executable = CriptAndHash

    async def run_test(self):        
        aes_file = Path(__file__).with_suffix('.aes')
        args = ['AES-128-CBC', 'SHA1', 'hex:E76B2413958B00E193']
        await self.executable.execute('0', __file__, aes_file.name, *args, cwd=self.workingDir)
        output_file = aes_file.with_suffix('.back').name
        await self.executable.execute('1', aes_file.name, output_file, *args, cwd=self.workingDir)
        async with aiofiles.open(__file__) as orig, \
                   aiofiles.open(self.workingDir / output_file) as back:
            for o, b in zip(await orig.readlines(), await back.readlines()):
                assert o == b
        return True
