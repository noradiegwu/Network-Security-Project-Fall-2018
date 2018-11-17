import binascii
import random

# returns a byte string of type <class 'bytes'>
def string_to_hex(s):
    return binascii.hexlify(s.encode("utf-8"))

# takes in a byte string of type <class 'bytes'>
def hex_to_2_byte_chunks(h):
    h_string = h.decode("utf-8")

    if len(h_string) % 4 != 0: # add "xx" to indicate that the last 2 byte chunk is too short
        h_string += "xx"
    n = 4
    result = [(i//n, h_string[i:i+n]) for i in range(0, len(h_string), n)] # break into 2 bytes

    random.shuffle(result)
    return result

### example use ###
# st = "hello from mars"
# hex_st = string_to_hex(st)
# print(hex_st)
# res = hex_to_2_byte_chunks(hex_st)
# print(res) --> [(3, '6672'), (1, '6c6c'), (4, '6f6d'), (2, '6f20'), (5, '206d'), (0, '6865'), (6, '6172'), (7, '73xx')]
