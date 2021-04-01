#!/usr/bin/env python3 
from pyftpdlib.authorizers import DummyAuthorizer 
from pyftpdlib.servers import FTPServer 
from pyftpdlib.handlers import FTPHandler 
import os 

authorizer = DummyAuthorizer()

authorizer.add_user('root', 'Shehan123', '.', perm='elradfmwMT')
# adding current dir files to remote server 
authorizer.add_anonymous(os.getcwd())

# Instantiate FTP handler class 
handler = FTPHandler 
handler.authorizer = authorizer 

# Define a customized banner(string returned when client connects)
# handler.banner = "pyftpdlib based ftpd ready"

# Specify a masquerade address and the range of ports to use for passive 
# connections. Decomment in case you're behind a NAT(network address translation)
# handler.masquerade_address = '151.25.42.11'
# handler.passive_ports = range(60000, 65535)

# Instantiate FTP server class and listen on 0.0.0.0:21
address = ("0.0.0.0", 22)
server = FTPServer(address, handler)

# set a limit for connections 
server.max_cons = 256 
server.max_cons_per_ip = 5

server.serve_forever()