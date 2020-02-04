import socket, threading

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = ""
port = 12345

client_list = []
act_list = []
thread_list = []
client_dict = {}

print("Server Ready")
s.bind((host,port))
s.listen(10)

def get_info():
	c = act_list[0][0]
	act_list.pop(0)
	c.send(("enter name").encode())
	buff = c.recv(1024).decode()
	client_dict[buff] = 0
	
	
def start():
	a = []
#	print("add"+str(client_list[0][0])+" "+str(client_list[1][0]))
	p1 = act_list[0][0]
	p2 = act_list[1][0]
	t1 = threading.Thread(target=get_info, name="t1", args=())
	t1.start()
	t2 = threading.Thread(target=get_info, name="t1", args=())
	t2.start()
	pla1 = t1.join()
	pla2 = t2.join()
#	print(pla1)
	print(client_dict)
	p1.send(("1").encode())
	p2.send(("2").encode())
	print("pla1 : "+str(pla1)+"------------pla2 : "+str(pla2))
	p2.send(str(pla1).encode())
	p1.send(str(pla2).encode())
	turn = True
	while True:
		p1msg = ""
		p2msg = ""
		if turn:
			p1msg = p1.recv(1024).decode()
			if(p1msg=="001"):
				turn = False
			p2.send(p1msg.encode())
		elif not turn:
			p2msg = p2.recv(1024).decode()
			if(p2msg == "001"):
				turn = True	
			p1.send(p2msg.encode())
		if p1msg == "lose":
			p2.send(("win").encode())
			break
		elif p2msg == "lose":
			p1.send(("win").encode())
			break
		
while True:
	conn, add = s.accept()
	client_list.append((conn,add))
	act_list.append((conn,add))
	print("Got connection "+ str(add))
	while len(client_list)>1:
		t = threading.Thread(target=start, name="1", args=())
		t.start()
#		act_list.append(client_list[0])
#		act_list.append(client_list[1])
		client_list.pop(0)
		client_list.pop(0)

