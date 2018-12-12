from Crypto.Cipher import AES
from Crypto import Random

def obfuscate(key, iv, plain_text):
    """
    Encrypts message
    param key: 16 byte key
    param iv: init vector of AES block_size
    param plain_text: text to be encrypted
    """
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(plain_text)
    return msg

def unobfuscate(key, iv, cipher_text):
    """
    Decrypts message
    param key: same 16 byte key used in obfuscate
    param iv: same init vector used in obfuscate
    param cipher_text: text to be decrypted
    """
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(cipher_text[AES.block_size:])
