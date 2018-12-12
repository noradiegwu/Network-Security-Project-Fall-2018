from scapy.all import *
#conf.verb = 0 # dans scapy interpreter taper conf output la configuration et on voit verbose = 2 par défault
conf.L3socket = L3RawSocket # to send packet on localhost source: https://stackoverflow.com/questions/6221842/python-raw-sockets-windows-sniffing-ethernet-frames
#conf.L3socket=L3dnetSocket
# just run in terminal with python program_name.py

# source : https://scapy.readthedocs.io/en/latest/usage.html



IP = IP(dst="127.0.0.1") # localhost 127.0.0.1 ou 0.0.0.0 default port 8000 (setup 50000)

gecko = str(20606101) #str(20100101)
getString_Gecko = ("GET /index.html HTTP/1.1\r\nHost: www.test.ch\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/%s Firefox/63.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n" % gecko)

# 3-way handshake
syn = IP / TCP(sport=64242 , dport=50000, flags='S')
syn_ack = sr1(syn)
ack = IP/TCP(dport=syn_ack[TCP].sport, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A')
send(ack)

p = IP/TCP(dport=syn_ack[TCP].sport, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq, flags='PA')/getString_Gecko

send(p)

# close connection : https://stackoverflow.com/questions/42422457/how-can-i-close-a-connection-via-scapy-sending-a-fin-packet

#FIN=IP/TCP(sport=syn_ack[TCP].dport, dport=80, flags="FA", seq=last_pck_to_ack.ack, ack=last_pck_to_ack.seq + 1)
#FINACK=sr1(FIN)
#LASTACK=IP/TCP(sport=syn_ack[TCP].dport, dport=80, flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
#send(LASTACK)
# parce qu'avec truc au dessus close pas la connection :
#RSTACK = IP/TCP(sport=syn_ack[TCP].dport, dport=80, flags="AR", seq=FINACK.ack, ack=FINACK.seq + 1)


sniffed_packets1 = sniff(filter ="tcp port 64242 and src host 127.0.0.1", count=4, lfilter = lambda x: x.haslayer(TCP))
pckt_to_ack1 = sniffed_packets1[3]

#print("pckt we ACKed")
#pckt_to_ack1.show()
ack_to_be_sent1 = IP/TCP(dport=pckt_to_ack1[TCP].sport, sport=pckt_to_ack1[TCP].dport, seq=pckt_to_ack1[TCP].ack, ack=pckt_to_ack1[TCP].seq + 1, flags='A')
send(ack_to_be_sent1)


time.sleep(5)
RSTACK = IP/TCP(sport=syn_ack[TCP].dport, dport=syn_ack[TCP].sport, flags="AR", seq=syn_ack.ack, ack=syn_ack.seq + 1)
send(RSTACK)
# send(IP(dst='127.0.0.1')/TCP(sport=64242, dport=8000, flags="AR", seq=1, ack=1))
