from Crypto.Cipher import AES
from Crypto import Random
import obfuscate_message
import file_to_hex
import binascii
import random
import string

"""
#####
Sample main routine from start to finish below
#####
"""

"""
step 1:
generate key and init vector (iv)
"""
def encrytion_details(key_size):
    # key_size must be 16, 24, or 32
    key = "".join(random.choices(string.ascii_uppercase + string.digits, k=key_size))
    iv = Random.new().read(AES.block_size)
    return key, iv

"""
step 2:
attacker uses key and iv to obfuscate message
converts that message to hex and generates random list of hex values and their positions
return: tuple holding hex itself and the position mapping list
"""
def attacker_encode_message_routine(filename, key, iv):
    plain_text = file_to_hex.get_file_text(filename)
    cipher_text = obfuscate_message.obfuscate(key, iv, plain_text)
    hex = file_to_hex.to_hex(cipher_text)
    pos_lst = file_to_hex.hex_to_list_pos_data(hex)
    return hex, pos_lst

"""
step 3:
here is where the attacker send all the information over the server
"""

"""
step 4:
then the attacker pieces the information together again as a hex string and move on below
"""

"""
step 5:
Assuming attacker has found all the hex for the message and pieced it back together
They use this function to convert the hex back to the obfuscated message
And then unencrypt that message and write to file
"""
def attacker_decode_message_routine(hex, key, iv, filename):
    unhex = binascii.unhexlify(hex)
    res = obfuscate_message.unobfuscate(key, iv, unhex)
    file = open(filename, "w")
    file.write(res.decode("utf-8"))

"""
Example Usage
"""
key, iv = encrytion_details(24)
hex, pos_lst = attacker_encode_message_routine("lorem_ipsum.txt", key, iv)
# send
# piece together
attacker_decode_message_routine(hex, key, iv, "testing123.txt")
