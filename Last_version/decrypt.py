#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto import Random

if __name__ == "__main__":
	
	key = "XssHUDBM3hP78t38"
	IV = 16 * '\x00'

	filename = "super_secret"

	ciphertext = open(filename).read()

	mode = AES.MODE_CBC
	encryptor = AES.new(key, mode, IV=IV)

	plaintext = encryptor.decrypt(ciphertext)

	new_filename = "key.txt"
	new_file = open(new_filename, 'wb')
	new_file.write(plaintext)
	new_file.close
