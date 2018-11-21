from scapy.all import *
#conf.verb = 0 # dans scapy interpreter taper conf output la configuration et on voit verbose = 2 par défault

# juste run dans cmd avec python nom_du_programe.py

# source : https://scapy.readthedocs.io/en/latest/usage.html

IP = IP(dst='www.unil.ch')

# String peut être utilisé comme RAW()
getString = "GET /index.html HTTP/1.1\r\nHost: detectportal.firefox.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0\r\n"

# http://www.ntu.edu.sg/home/ehchua/programming/webprogramming/http_basics.html expliqe pourquoi j'avais 400 Bad Request ie un espace en trop après version HTTP

gecko = str(20606101) #str(20100101)
getString_Gecko =  ("GET /index.html HTTP/1.1\r\nHost: detectportal.firefox.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/%s Firefox/63.0\r\nAccept: */*\r\nAccept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nConnection: keep-alive\r\n\r\n" % gecko)
# p = IP(dst="www.slashdot.org")/TCP()/getString_Gecko
# p = IP(dst="www.epfl.ch")/TCP()/getString_Gecko
getString_Gecko_unil = ("GET /index.html HTTP/1.1\r\nHost: www.unil.ch\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/%s Firefox/63.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n" % gecko)

#source : https://stackoverflow.com/questions/4750793/python-scapy-or-the-like-how-can-i-create-an-http-get-request-at-the-packet-leve
# 3-way handshake
syn = IP / TCP(sport=50000 , dport=80, flags='S')
#print("syn : %s" % raw(syn))
syn_ack = sr1(syn)
#print("syn_ack : %s" % raw(syn_ack))
ack = IP/TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A')
send(ack)
#print("ack : %s" % raw(ack))

p = IP/TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq, flags='PA')/getString_Gecko_unil  # www.unil.ch/index.html (http pas https)
#print("Sent packet :")
#print(p)
#r = sr1(p) #  sr1(p)

# sr method : They return a couple of two lists. The first element is a list of couples (packet sent, answer), and the second element is the list of unanswered packets.
#ans_pck,unans_pck = sr(p) # sr renvoie un tuple voir doc scapy
send(p)
#print("Reply : ")
#print(r.summary(), r, sep='\n') # r.summary() si ecrit r = sr() r n'a pas de summary car c'est un tuple

#time.sleep(5) # pause 5 sec j'imagine
# pourrait faire un while unans_pck not empty ou un truc comme ça

#last_pck_to_ack = ans_pck[-1][1] # [-1] pour acceder dernière élément liste [-n] accederait au n en partant de la fin le [1]c'est pour acceder au deuxième element tuple
#last_pck_to_ack.show() # show2 same sur assembled packet
#ack_to_send = IP/TCP(dport=80, sport=last_pck_to_ack[TCP].dport, seq=last_pck_to_ack[TCP].ack, ack=last_pck_to_ack[TCP].seq + 1, flags='A')
#send(ack_to_send)


# https://stackoverflow.com/questions/33476561/ack-number-to-acknowledge-data-in-scapy pour ack data sent
# rp c'est field read packet ? non
#tcp_seg_len = len(rp.getlayer(Raw).load)
#ans_ack,unans_ack = sr(IP/TCP(sport=pkt[1].dport, \
#                                          dport=pkt[1].sport, \
#                                          seq=rp[1].ack, \
#                                          ack=tcp_seg_len + 1, \
#                                          flags="A"), \
#                           verbose=0, timeout=1)

# close connection : https://stackoverflow.com/questions/42422457/how-can-i-close-a-connection-via-scapy-sending-a-fin-packet

#FIN=IP/TCP(sport=syn_ack[TCP].dport, dport=80, flags="FA", seq=last_pck_to_ack.ack, ack=last_pck_to_ack.seq + 1)
#FINACK=sr1(FIN)
#LASTACK=IP/TCP(sport=syn_ack[TCP].dport, dport=80, flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
#send(LASTACK)
# parce qu'avec truc au dessus close pas la connection :
#RSTACK = IP/TCP(sport=syn_ack[TCP].dport, dport=80, flags="AR", seq=FINACK.ack, ack=FINACK.seq + 1)

#ACK sent by mozilla :
#ack1 = IP/TCP(dport=80, sport=syn_ack[TCP].dport, seq=353, ack=3921, flags='A')
#time.sleep(0.1)
#ack1.show()
#send(ack1)
#ack2 = IP/TCP(dport=80, sport=syn_ack[TCP].dport, seq=353, ack=6841, flags='A')
#time.sleep(0.1)
#send(ack2)
#ack3 = IP/TCP(dport=80, sport=syn_ack[TCP].dport, seq=353, ack=9761, flags='A')
#time.sleep(0.1)
#send(ack3)

#TODO try sniffed_packets = sniff(filter ="tcp port 20 and src host 130.223.27.54", iface=wifi0, count=2, prn=lambda x: x.summary())
# et essayer d'acceder au sniffed packets sniffed_packets[0] pour ceux tcp (à verifier) et sniffed_packets[0][-1] pour acceder au dernier reçu ?
# jouer avec param count pour savoir combien doit en recevoir ?
sniffed_packets1 = sniff(filter ="tcp port 50000 and src host 130.223.27.54", count=4, lfilter = lambda x: x.haslayer(TCP)) # prn=lambda x: x.show()
# le lfilter au dessus normalement inutile vu que filter prends dejà tcp mais au moins voit comment s'utilise
#print("sniffed packets :", sniffed_packets1)
#tcp_sniffed = sniffed_packets1[3]
#print("sniffed tcp packets :", tcp_sniffed.show())
pckt_to_ack1 = sniffed_packets1[3]
#pckt_to_ack1 = tcp_sniffed[3] # dans quel sens sont ajouté nouveau packet au debut ou à la fin ? en fait apparement on a jsute les packets on a pas un tuple (tcp, udp etc) puis des listes
# et ça au dessus prennait les layers du message ie le load (qui était du padding)
print("pckt we ACKed")
pckt_to_ack1.show()
ack_to_be_sent1 = IP/TCP(dport=80, sport=pckt_to_ack1[TCP].dport, seq=pckt_to_ack1[TCP].ack, ack=pckt_to_ack1[TCP].seq + 1, flags='A')
send(ack_to_be_sent1)

sniffed_packets2 = sniff(filter ="tcp port 50000 and src host 130.223.27.54", count=3, lfilter = lambda x: x.haslayer(TCP)) # prn=lambda x: x.show()
pckt_to_ack2 = sniffed_packets2[2]
print("pckt we ACKed")
pckt_to_ack2.show()
ack_to_be_sent2 = IP/TCP(dport=80, sport=pckt_to_ack2[TCP].dport, seq=pckt_to_ack2[TCP].ack, ack=pckt_to_ack2[TCP].seq + 1, flags='A')
send(ack_to_be_sent2)

sniffed_packets3 = sniff(filter ="tcp port 50000 and src host 130.223.27.54", count=4, lfilter = lambda x: x.haslayer(TCP)) # prn=lambda x: x.show()
pckt_to_ack3 = sniffed_packets3[3]
print("pckt we ACKed")
pckt_to_ack3.show()
ack_to_be_sent3 = IP/TCP(dport=80, sport=pckt_to_ack3[TCP].dport, seq=pckt_to_ack3[TCP].ack, ack=pckt_to_ack3[TCP].seq + 1, flags='A')
send(ack_to_be_sent3)


time.sleep(5)
RSTACK = IP/TCP(sport=syn_ack[TCP].dport, dport=80, flags="AR", seq=syn_ack.ack, ack=syn_ack.seq + 1)
send(RSTACK)
# send(IP(dst='www.unil.ch')/TCP(sport=50000, dport=80, flags="AR", seq=1, ack=1))
