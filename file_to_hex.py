import binascii
import random

def get_file_text(filename):
    bin_str = ""
    with open(filename, "rb") as f:
    	bin_str = f.read()
    return bin_str


def to_hex(bin_str):
    hex_str = binascii.hexlify(bin_str)
    return hex_str


# takes in a byte string of type <class 'bytes'>
def hex_to_list_pos_data(hex_str):
	#if len(h_string) % 4 != 0: # add "xx" to indicate that the last 2 byte chunk is too short
    #	h_string += "xx"
    n = 4
    list_pos_data = [[i//n, hex_str[i:i+n]] for i in range(0, len(hex_str), n)] # break into 2 bytes
    random.shuffle(list_pos_data)
    return list_pos_data
