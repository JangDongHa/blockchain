import struct
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

encoding = 'utf-8'
salt = b64encode(get_random_bytes(512))
# 동일한 value로 key를 생성하면 동일한 key 가 나오게 할지, 같게 나오게 할지 고민 (일단 전자)
key = lambda k: PBKDF2(k, salt, AES.block_size, hmac_hash_module=SHA256)


class CBC(object):
    def enc(self, m, k):
        cipher = AES.new(k, AES.MODE_CBC)
        if type(m) == int:
            encodeM = struct.pack('i', m)
        else:
            encodeM = m.encode(encoding)

        return b64encode(cipher.iv + cipher.encrypt(pad(encodeM,
                                                        AES.block_size)))

    def dec(self, c, k):
        raw = b64decode(c)
        cipher = AES.new(k, AES.MODE_CBC, raw[:AES.block_size])

        # if plaintext not bytes code is that you want : struct.unpack('i', decResult.encode('utf-8'))[0] (for integer)
        return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)


class CTR(object):
    def enc(self, m, k):
        cipher = AES.new(k, AES.MODE_CTR, nonce=salt[:AES.block_size - 1])
        if type(m) == int:
            encodeM = struct.pack('i', m)
        else:
            encodeM = m.encode(encoding)
        return b64encode(cipher.nonce + cipher.encrypt(encodeM))

    def dec(self, c, k):
        raw = b64decode(c)
        cipher = AES.new(k, AES.MODE_CTR, nonce=raw[:AES.block_size - 1])

        # if plaintext not bytes code is that you want : struct.unpack('i', decResult.encode('utf-8'))[0] (for integer)
        return cipher.decrypt(raw[AES.block_size - 1:])