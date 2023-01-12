from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
# Assign IP address and port number to socket
serverName = 'localhost'
serverPort = 12000
message = 'ping'
# Send ping 10 times
for i in range(10):
    try:
        # Send message to server
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        clientSocket.sendto(bytes(message + str(i) + '   ' + current_time,'utf-8'), (serverName, serverPort))
        # Receive the server response
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage)
    except timeout:
        # Server does not response
        # Assume the packet is lost
        print('Request timed out')
# Close the client socket
clientSocket.close()
