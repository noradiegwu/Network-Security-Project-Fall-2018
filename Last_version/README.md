# Network-Security-Project-Fall-2018

Last version

```bash
tshark -Y http.request -n -r dump_test.pcap -T fields -e http.request.full_uri -e http.user_agent | grep 'type=data' | grep -o 'pos.*' | grep -e 'pos=[0-9]*' -e 'Gecko/[0-9a-f]*' -o | paste - - | grep -oP 'pos=\K.*' | sort -n | grep -oP '[0-9 ]*Gecko/\K.*' | tr -d '\n' | xxd -p -r > file
```
