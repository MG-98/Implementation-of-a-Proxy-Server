from socket import *
# Create a TCP server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start
port_number = 8888
tcpSerSock.bind(('', port_number))
tcpSerSock.listen(1)
# Fill in end

while True:
    # Accept connection and start receiving data from the client
    tcpCliSock, client_addr = tcpSerSock.accept()
    message = tcpCliSock.recv(2048)
    # Parse the received message and extract the filename, and address
    # of the origin server
    if message.split()[1].decode('ascii') != "/favicon.ico":
        filename = message.split()[1][16:].decode('ascii')
        hostname = message.split()[1][1:10].decode('ascii')
        port = int(message.split()[1][11:15].decode('ascii'))

    # Open the file if it exists in cache, otherwise, contact the origin
    # server
    try:
        # Open the file if it exists in the cache
        f = open(filename)
        outputdata = f.readlines()
        print("I have it cached")
        # ProxyServer finds a cache hit and generates an HTTP response
        #message
        tcpCliSock.send('\nHTTP/1.1 200 OK\r\n'.encode())
        # Send the file to the client
        # Fill in start.
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
            tcpCliSock.send("\r\n".encode())
        # Fill in end.
    except IOError:
        # Create a new tcp socket and contact the origin server
        print("I will get it from server")

        c = socket(AF_INET,SOCK_STREAM)
        c.connect((hostname, port))
        # Create the GET request and send it to the server
        request = 'GET /'+ filename + ' HTTP/1.1\r\n'
        c.send(request.encode())
        # Start receiving data from the origin server
        # Fill in start
        my_message = c.recv(2048)
        my_message = ''
        for i in range(1, 100000):
            rec_message = c.recv(2048)
            my_message += rec_message.decode()
        # Fill in end
        # Send the received data to the client
        # Fill in start
        tcpCliSock.send('\nHTTP/1.1 200 OK\r\n'.encode())
        for i in range(0, len(my_message)):
            tcpCliSock.send(my_message[i].encode())
            tcpCliSock.send("\r\n".encode())
        # Fill in end
        # If the file is found in the origin server, store it in the
        #cache for later use
        # Fill in start
        f = open(filename, "a")
        f.write(my_message)
        f.close()
        # Fill in end
        # Close the TCP sockets that are no longer needed
tcpSerSock.close()