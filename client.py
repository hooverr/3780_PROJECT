import socket
serverAddress = '192.168.0.17'
clientAddress = '192.168.0.20'
port = 2500

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((clientAddress,port))
source = input('Enter identification: ')
seqNo = "1"
while(1):
  option = input('Enter option (1 - send, 2 - get, 0 - exit)')
  option = int(option)
  if(option == 1):
    type = "SEND"
    destination = input('Enter name of receiver:')
    payload = input('Enter message to send : ')
    frame = seqNo + "/" + type + "/" + source + "/" + destination + "/" + payload
    s.sendto(frame.encode('utf-8'), (serverAddress,port))
  elif(option == 2):
    type = "GET"
    frame = seqNo + "/" + type + "/" + source + "/" + " " + "/" + " "
    s.sendto(frame.encode('utf-8'), (serverAddress,port))
    data, address = s.recvfrom(1024)
    data = data.decode('utf-8')
    dataList = data.split("/")
    print (dataList[4])