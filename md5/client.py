import socket

client = socket.socket()
client.connect(("127.0.0.1", 12345))

message = input("Enter message: ")
client.sendall(message.encode())

client.close()
