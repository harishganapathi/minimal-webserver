import socket
import os
import os.path
import time

sock = socket.socket() #socket pointer 
host = "127.0.0.1"
port = 8080
sock.bind((host, port))
sock.listen(5)

def serve(path):
	filepath =path.split()
	if filepath[2][:4] == "HTTP":
		
		if os.path.isfile(filepath[1][1:]):
			fp = open(filepath[1][1:])
			a=fp.read()
			response=""
			response+="HTTP/1.1 200 OK\r\n" #status 

			#content-type conditional check
			if filepath[1][-3:] == "txt": 
				response += "Content-Type : text/html\r\n":
			else if  filepath[1][-4:] == "html":
				response+="Content-Type : text/html\r\n"
			else:
				response+="Content-Type : image/jpeg\r\n"

			#content length is appended to header
			response+="Content-Length : "+ str(len(a))+ "\r\n"#content-length for both image and text file 
			
			if !filepath:  # connection-type is appended to header
				response+="Connection : Close\r\n\r\n"
			else:
				response+="Connection : Keep-Alive\r\n\r\n"
			return response  # response  header end
		

		else:
			return "HTTP/1.1 404 Not Found\r\n\r\n"
	else:
		return "HTTP/1.1 403 Forbidden\r\n\r\n"

def content(path): #response message send function
	filepath=path.split()
	if os.path.isfile(filepath[1][1:]): 
		fp = open(filepath[1][1:])
		filecontent = fp.read()
		return filecontent  #response message 
	else:
		return "404 Not Found\r\n\r\n"

while 1:
	addr='127.0.0.1'
	client,addr = sock.accept()
	print("Serving HTTP from port "+str(port))
	req=client.recv(4096)
	responseheader=serve(req) #response header 
	responsemessage=content(req)#response content 
	print(str(addr[0:9]) + str(time.ctime()) +  " - " +str(responseheader[0:15]))
	client.send(responseheader)  # response header 
	client.send(responsemessage)  # response content
	client.close()

