import os
from base64 import b64encode

from Crypto.Cipher import AES
import time

from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import aesmodes

counter = os.urandom(16)
salt = b64encode(get_random_bytes(512))
keyL = lambda k: PBKDF2(k, salt, AES.block_size, hmac_hash_module=SHA256)


# Encryption
def encrypt_message(key, plaintext, mode):
    if mode == 'CBC':
        selectMode = aesmodes.CBC()
    elif mode == 'CTR':
        selectMode = aesmodes.CTR()

    return selectMode.enc(plaintext, key).decode(encoding='utf-8')


# Decryption
def decrypt_message(key, ciphertext, mode):
    if mode == 'CBC':
        selectMode = aesmodes.CBC()
    elif mode == 'CTR':
        selectMode = aesmodes.CTR()

    return selectMode.dec(ciphertext, key).decode(encoding='utf-8')


# Main running
def run(msg, mode, key=''):
    if key == '':
        k = 'test'  # os.urandom(16)  # 256 bits key
        key = keyL(k)
    encryptStart = time.time()
    ciphertext = encrypt_message(key, msg, mode)
    encryptEnd = time.time() - encryptStart

    decryptStart = time.time()
    plaintext = decrypt_message(key, ciphertext, mode)
    decryptEnd = time.time() - decryptStart

    result = {
        'plaintext': plaintext,
        'encryptEnd': encryptEnd,
        'decryptEnd': decryptEnd,
        'ciphertext': ciphertext,
        'key': key
    }
    return result


# Helper function
def sort_list(values):
    kbs = []
    mbs = []
    gbs = []
    sorted = []
    for val in values:
        if 'kb' in val:
            kbs.append(int(val.split('kb')[0]))
        elif 'mb' in val:
            mbs.append(int(val.split('mb')[0]))
        elif 'gb' in val:
            gbs.append(int(val.split('gb')[0]))
        else:
            raise Exception('not allowed nam [sorted values can only use kb or mb or gb')

    kbs.sort()
    mbs.sort()
    gbs.sort()

    insert_list(sorted, kbs, 'kb')
    insert_list(sorted, mbs, 'mb')
    insert_list(sorted, gbs, 'gb')

    return sorted


# Helper function
def insert_list(sorted, little_values, label):
    for val in little_values:
        val = str(val) + label
        sorted.append(val)


# for plt
def aes(type='e', mode='CBC'):
    dummy_dir = os.getcwd() + '/dummy'
    dummy_files = sort_list(os.listdir(dummy_dir))
    xlabels = []
    ylabels = []
    if 'e' == type:
        type = 'encryptEnd'
        title_name = 'Encryption'
    elif 'd' == type:
        type = 'decryptEnd'
        title_name = 'Decryption'

    for dummy_file in dummy_files:
        xlabels.append(dummy_file)
        f = open(dummy_dir + '/' + dummy_file, 'r')
        plainT = f.read()

        AES128 = run(plainT, mode)
        cryptoT = AES128.get('plaintext')
        typeEnd = AES128.get(type)  # encryptEnd or decryptEnd

        if plainT != cryptoT:  # integrity check
            raise Exception('integrity violation in filename : ' + dummy_file)

        ylabels.append(typeEnd)

    return xlabels, ylabels, title_name
