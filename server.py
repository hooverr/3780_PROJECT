#Robert Hoover
#3780 Project
#SERVER - UPDATE
#2013-11-12

import socket
host = '192.168.0.17'
port = 2500
messageList = []
acknowledgementList = []
def getMessage(destination, list):
  for message in list:
    if(message[3] == destination):
      return message
def removeMessage(sequenceNumber,source,list):     
  for message in reversed(list):
    if(message[0] == sequenceNumber and message[2] == source):
      list.remove(message)
      
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
print ("Server waiting on port:", port)
while 1:
  message, address = s.recvfrom(256)
  message = message.decode('utf-8')
  print("Received "+ message + "\n")
  message = message.split('/')
  if(message[1] == 'SEND'):
    messageList.append((message[0],message[1],message[2],message[3],message[4]))
  if(message[1] == 'GET'):
    response = getMessage(message[2], messageList)
    if(response != None):
      response = '/'.join(response)
      print("Sent " + response + "\n")
      s.sendto(response.encode('utf-8'), (address[0],port))
    else:
      response = '1/SEND/SERVER/' + message[2] + '/'
      print("Sent " + response + "\n")
      s.sendto(response.encode('utf-8'), (address[0],port))
  if(message[1] == 'ACK'):
    acknowledgementList.append((message[0],message[1],message[2],message[3],message[4]))
    removeMessage(message[0],message[3],messageList)
    response = getMessage(message[2], messageList)
    if(response != None):
      response = '/'.join(response)
      print("Sent " + response + "\n")
      s.sendto(response.encode('utf-8'), (address[0],port))
    else:
      response = '1/SEND/SERVER/' + message[2] +'/'
      print("Sent " + response + "\n")
      s.sendto(response.encode('utf-8'), (address[0],port))
  if(message[1] == 'READ'):
    response = getMessage(message[2], acknowledgementList)
    if(response != None):
      removeMessage(response[0],response[2],acknowledgementList)
      response = '/'.join(response)
      print("Sent " + response + "\n")
      s.sendto(response.encode('utf-8'), (address[0],port))
    else:
      response = '1/SEND/SERVER/' + message[2] + '/'
      print("Sent " + response + "\n")
      s.sendto(response.encode('utf-8'), (address[0],port))
  