from socket import *

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET , SOCK_STREAM)

# Choose a server port and bind the serverSocket to the server address and  port number
# Fill in start
port_number = 6789

serverSocket.bind(('', port_number))
# Fill in end
# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
    print("The server is ready to receive")
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    try:
        # Receive the request message from the client
        message =  connectionSocket.recv(2048)
        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header
        filename = message.split()[1].decode('ascii')
        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        f = open(filename[1:])
        # Store the entire content of the requested file in a buffer
        outputdata = f.readlines()
        # Send the proper HTTP response header line to client
        connectionSocket.send('\nHTTP/1.1 200 OK\r\n'.encode())
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        # Close the client connection socket
        connectionSocket.close()
    except IOError:
        # Send HTTP response message for file not found
        connectionSocket.send("\nHTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 \
        Not Found</h1></body></html>\r\n".encode())

        # Close the client connection socket
        connectionSocket.close()

serverSocket.close()