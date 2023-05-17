from dan import self
from dan.cxx import Library
from dan.smc import TarSources

description = 'An open source, portable, easy to use, readable and flexible TLS library, and reference implementation of the PSA Cryptography API.'
version = self.options.add('version', '3.4.0')

class MbedTLSSources(TarSources):
    name = 'mbedtls-source'

    @property
    def url(self):
        return f'https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/v{self.version}.tar.gz'
    

class MbedCrypto(Library):
    name = 'mbedcrypto'
    preload_dependencies = MbedTLSSources,
    installed = True

    async def __initialize__(self):        
        self.src = self.get_dependency(TarSources).output / f'mbedtls-{self.version}'
        self.includes.add(self.src / 'include', public=True)
        await super().__initialize__()
    
    def sources(self):
        return [self.src / 'library' / f for f in [
            'aes.c',
            'aesni.c',
            'aesce.c',
            'aria.c',
            'asn1parse.c',
            'asn1write.c',
            'base64.c',
            'bignum.c',
            'bignum_core.c',
            'bignum_mod.c',
            'bignum_mod_raw.c',
            'camellia.c',
            'ccm.c',
            'chacha20.c',
            'chachapoly.c',
            'cipher.c',
            'cipher_wrap.c',
            'constant_time.c',
            'cmac.c',
            'ctr_drbg.c',
            'des.c',
            'dhm.c',
            'ecdh.c',
            'ecdsa.c',
            'ecjpake.c',
            'ecp.c',
            'ecp_curves.c',
            'entropy.c',
            'entropy_poll.c',
            'error.c',
            'gcm.c',
            'hash_info.c',
            'hkdf.c',
            'hmac_drbg.c',
            'lmots.c',
            'lms.c',
            'md.c',
            'md5.c',
            'memory_buffer_alloc.c',
            'nist_kw.c',
            'oid.c',
            'padlock.c',
            'pem.c',
            'pk.c',
            'pk_wrap.c',
            'pkcs12.c',
            'pkcs5.c',
            'pkparse.c',
            'pkwrite.c',
            'platform.c',
            'platform_util.c',
            'poly1305.c',
            'psa_crypto.c',
            'psa_crypto_aead.c',
            'psa_crypto_cipher.c',
            'psa_crypto_client.c',
            'psa_crypto_driver_wrappers.c',
            'psa_crypto_ecp.c',
            'psa_crypto_hash.c',
            'psa_crypto_mac.c',
            'psa_crypto_pake.c',
            'psa_crypto_rsa.c',
            'psa_crypto_se.c',
            'psa_crypto_slot_management.c',
            'psa_crypto_storage.c',
            'psa_its_file.c',
            'psa_util.c',
            'ripemd160.c',
            'rsa.c',
            'rsa_alt_helpers.c',
            'sha1.c',
            'sha256.c',
            'sha512.c',
            'threading.c',
            'timing.c',
            'version.c',
            'version_features.c',
        ]]

class MbedX509(Library):
    name = 'mbedx509'
    preload_dependencies = MbedTLSSources,
    installed = True

    async def __initialize__(self):        
        self.src = self.get_dependency(TarSources).output / f'mbedtls-{self.version}'
        self.includes.add(self.src / 'include', public=True)
        await super().__initialize__()
    
    def sources(self):
        return [self.src / 'library' / f for f in [
            'pkcs7.c',
            'x509.c',
            'x509_create.c',
            'x509_crl.c',
            'x509_crt.c',
            'x509_csr.c',
            'x509write_crt.c',
            'x509write_csr.c',
        ]]

class MbedTLS(Library):
    name = 'mbedtls'
    preload_dependencies = MbedTLSSources,
    installed = True

    async def __initialize__(self):        
        self.src = self.get_dependency(TarSources).output / f'mbedtls-{self.version}'
        self.includes.add(self.src / 'include', public=True)
        await super().__initialize__()
    
    def sources(self):
        return [self.src / 'library' / f for f in [
            'debug.c',
            'mps_reader.c',
            'mps_trace.c',
            'net_sockets.c',
            'ssl_cache.c',
            'ssl_ciphersuites.c',
            'ssl_client.c',
            'ssl_cookie.c',
            'ssl_debug_helpers_generated.c',
            'ssl_msg.c',
            'ssl_ticket.c',
            'ssl_tls.c',
            'ssl_tls12_client.c',
            'ssl_tls12_server.c',
            'ssl_tls13_keys.c',
            'ssl_tls13_server.c',
            'ssl_tls13_client.c',
            'ssl_tls13_generic.c',
        ]]