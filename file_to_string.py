import os
import binascii

# opens any given file and returns it as a binary string
def open_to_bin_string(file_name):
    s = ""
    with open(file_name, "rb") as f:
        s = f.read()
    return s

# takes a string ('data') and writes it into a file as a binary string
def string_to_file(data, file_name):
    with open(file_name, "wb") as file:
        file.write(data)
    return
