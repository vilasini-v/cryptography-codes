import socket

client = socket.socket()
client.connect(("127.0.0.1", 12345))  # Connect to server (change IP if needed)

message = input("Enter message: ")
client.sendall(message.encode())

client.close()
