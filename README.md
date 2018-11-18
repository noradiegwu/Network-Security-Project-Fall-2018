# Network-Security-Project-Fall-2018

## Set up a server (Ubuntu)

```bash
$ sudo apt update
$ sudo apt install apache2
$ sudo apt install php libapache2-mod-php 
$ sudo systemctl (re)start apache2
```

Server files located in `/var/www/html` folder, available at `http://localhost/index.html`

## Idea for improvments

### Webshell

Use of a webshell agent to create a backdoor on the server (website vulnerable and allows a user to put any file on it).
We can imagine that once connected, the agent sends information via our strange GET requests. 

--> Is it okay for the TA ? 
--> Should we create this vulnerable website so that the first part of the challenge is to find how the agent got on the web server in the first place ? Maybe too much work for a very simple contact form allowing to add files.

### Encrypting the file 

Using an encrypting algorithm --> first sending the key, then algo over the network, and then encrypted file, piece by piece.

--> Is it okay for the TA ? 
