#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto import Random

if __name__ == "__main__":
	
	key = "XssHUDBM3hP78t38"
	IV = 16 * '\x00'

	filename = "real_sensitive_document.txt"

	plaintext = open(filename).read()

	mode = AES.MODE_CBC
	encryptor = AES.new(key, mode, IV=IV)

	ciphertext = encryptor.encrypt(plaintext)

	#ciphertext = obfuscate_message.obfuscate(key, iv, plaintext)

	new_filename = "super_secret"
	new_file = open(new_filename, 'wb')
	new_file.write(ciphertext)
	new_file.close
