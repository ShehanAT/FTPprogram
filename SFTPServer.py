_author_ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'

#!/usr/bin/env python3 
import time, socket, optparse, sys, textwrap
import paramiko
from sftpserver.stub_sftp import StubServer, StubSFTPServer 

HOST, PORT = 'localhost', 3373
BACKLOG = 10 

def start_server(host, port, keyfile, level):
    paramiko_level = getattr(paramiko.common, level)
    paramiko.common.logging.basicConfig(level=paramiko_level)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((host, port))
    server_socket.listen(BACKLOG)
    print(host, port)
    while True:
        conn, addr = server_socket.accept()
        
        host_key = paramiko.RSAKey.from_private_key_file(keyfile)
        transport = paramiko.Transport(conn)
        transport.add_server_key(host_key)
        transport.set_subsystem_handler(
            'sftp', paramiko.SFTPServer, StubSFTPServer
        )

        server = StubServer()
        transport.start_server(server=server)

        channel = transport.accept()
        while transport.is_active():
            time.sleep(1)

def main():
    usage = """\
    usage: sftpserver [options]
    -k/--keyfile should be specified 
    """
    parser = optparse.OptionParser(usage=textwrap.dedent(usage))
    parser.add_option(
        '--host', dest='host', default=HOST,
        help='listen on HOST [default: %default]')
    parser.add_option(
        '-p', '--port', dest='port', type='int', default=PORT,
        help='listen on PORT [default: %default]'
    )
    parser.add_option(
        '-l', '--level', dest='level', default='INFO',
        help='Debug level: WARNING, INFO, DEBUG [default: %default]'
    )
    parser.add_option(
        '-k', '--keyfile', dest='keyfile', metavar='FILE',
        help='Path to private key, for example /tmp/test_rsa.key'
    )

    options, args = parser.parse_args()

    if options.keyfile is None:
        parser.print_help()
        sys.exit(-1)
    
    start_server(options.host, options.port, options.keyfile, options.level)

if __name__ == '__main__':
    main()

'''
authorizer = DummyAuthorizer()

authorizer.add_user('root', 'Shehan123', './', perm='elradfmwMT')
# adding current dir files to remote server 
authorizer.add_anonymous(os.getcwd())

# Instantiate FTP handler class 
handler = TLS_FTPHandler 
handler.certfile = "C:Users\\sheha\\.ssh\\id_rsa.pub.pem"
handler.authorizer = authorizer 

# Define a customized banner(string returned when client connects)
# handler.banner = "pyftpdlib based ftpd ready"
handler.timeout = 700

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
'''