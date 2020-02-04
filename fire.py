# Library Import
import pygame,socket,math,sys
from pygame.locals import *

# Screen
pygame.init()
width, height = 1024, 768

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "192.168.29.139"
port = 12345
s.connect((host,port))
buf = s.recv(1024).decode()
buf = input(buf)
s.send(buf.encode())
me = int(s.recv(1024).decode())

pygame.display.set_caption("player "+str(me)+"user "+buf)

white = (255,255,255,255)
red = (200,0,0)

font = pygame.font.SysFont(None,25)
def txt_obj(msg,colour,x,y):
	txt = font.render(msg,True,colour)
	return txt,txt.get_rect()
def msg_disp(msg,colour,x=width/2,y=height/2):
	txt_surface, txt_rect = txt_obj(msg,colour,x,y)
	txt_rect.center = (x,y)
	screen.blit(txt_surface,txt_rect)

keys = [False, False, False, False, False, False]

# Load Images
tank1 = pygame.image.load("tank3.png")
# Size -> 106 x 50	# Split tank and nozzle
tank2 = pygame.image.load("tank3_flip.png")
grass = pygame.image.load("grass.png")


player1pos = [20, 768-90-tank1.get_height()]
player2pos = [1024-20-tank2.get_width(), 768-90-tank1.get_height()]
player1ang = 0
player2ang = 0
player1pow = 0
player2pow = 0
player1ang_diff = 0
player2ang_diff = 0
player1health = 100
player2health = 100
move_count = 0
turn = True
fire = False

screen = pygame.display.set_mode((width, height))


def fireshoot(player1pos, player2pos, playr1health, playr2health):
	global player1health
	global player2health
	shot = pygame.image.load("shot.png")
	pi = math.pi
	if(turn == True):
		angle = player1ang
		power = player1pow
		x = player1pos[0]
		y = player1pos[1]
		
		while(1):
			screen.blit(shot, [x+tank1.get_width(),player1pos[1]*2-y])
			pygame.display.flip()
			x += 0.75
			y = player1pos[1] + ((x-player1pos[0])*math.tan(angle*pi/180)) - (9.8*(x-player1pos[0])*(x-player1pos[0])/(2*power*power*math.cos(angle*pi/180)*math.cos(angle*pi/180)))
			if(y<player1pos[1]-tank1.get_height()+5):
				diff = player2pos[0]-(x+tank1.get_width())
				if(-250<diff<250):
					player2health -= 50
				break

			
	elif(turn==False):
		angle = player2ang
		power = player2pow
		x = 1024 - player2pos[0]-tank1.get_width()
		y = player2pos[1]
		
		while(1):
			screen.blit(shot, [1024 -tank1.get_width()-shot.get_width()- x,player2pos[1]*2-y])
			pygame.display.flip()
			x += 0.75
			y = player2pos[1] + ((x-1024 + player2pos[0]+tank1.get_width())*math.tan(angle*pi/180)) - (9.8*(x-1024 + player2pos[0]+tank1.get_width())*(x-1024 + player2pos[0]+tank1.get_width())/(2*power*power*math.cos(angle*pi/180)*math.cos(angle*pi/180)))
			if(y<player2pos[1]-tank1.get_height()+5):
				diff = player1pos[0]-(1024 -tank1.get_width()-shot.get_width()- x)
				if(-250<diff<250):
					player1health -= 50
				break
# Big Loop
while 1:
	# Clear screen
	screen.fill(0)
	# Get Land->Tank
	for x in range(int(width/grass.get_width()+1)):
		screen.blit(grass, (x*100, 768-90))
	screen.blit(tank1, player1pos)
	screen.blit(tank2, player2pos)

	if(me == 1):
		msg_disp(str(player1pow), red, 20, 30)
		msg_disp(str(player1ang), red, 20, 50)
	else:
		msg_disp(str(player2pow), red, 960, 30)
		msg_disp(str(player2ang), red, 960, 50)

	# Show nozzle for both

	# Update Screen
	pygame.display.flip()
	if((me==1 and player1health==0)or(me==2 and player2health==0)):
		s.send("lose".encode())
		print("you lose")
		sys.exit()
		#Display losing screen			<--------------------------------------

	for event in pygame.event.get():
		# Check if event is X button
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			if event.key == K_a:
				keys[1] = True
			if event.key == K_s:
				keys[2] = True
			if event.key == K_d:
				keys[3] = True
			if event.key == K_p:
				keys[4] = True
			if event.key == K_o:
				keys[5] = True
			if event.key == K_m:		# m for fire
				fire = True
				s.send(("001").encode())
				fireshoot(player1pos, player2pos, player1health, player2health)
				print("1 : "+str(player1health)+" 2: "+str(player2health))
				turn = not turn				
				move_count = 0
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				keys[0] = False
				player1ang_diff = 0
			if event.key == K_a:
				keys[1] = False
			if event.key == K_s:
				keys[2] = False
				player1ang_diff = 0
			if event.key == K_d:
				keys[3] = False
			if event.key == K_p:
				keys[4] = False
			if event.key == K_o:
				keys[5] = False
	if (turn and me==1):
		if keys[1]:
			if player1pos[0]-1 > 0 and move_count < 200:
				player1pos[0] -= 0.2
				s.send(("400").encode())			#4=left 6 = right 8 = up 2 = down 0 = none
				move_count += 1
		elif keys[3]:
			if player1pos[0] < 1024-tank1.get_width() and player1pos[0]+1 < player2pos[0]-tank2.get_width() and move_count < 200:
				player1pos[0] += 0.2
				s.send(("600").encode())
				move_count += 1
		if keys[0]:
			if player1ang < 90:
				player1ang += 0.5 
				s.send(("080").encode())
		elif keys[2]:
			if player1ang >= 0:
				player1ang -= 0.5
				s.send(("020").encode())
		if keys[4]:
			if player1pow < 100:
				player1pow += 0.5
				s.send("110".encode())				#for power +
		if keys[5]:
			if player1pow > 0:
				player1pow -= 0.5
				s.send("101".encode())
	if(not turn and me==2):
		if keys[1]:
			if(player2pos[0]-1>0 and player2pos[0]-1 > player1pos[0]+tank1.get_width() and move_count < 200):
				player2pos[0] -= 0.2
				s.send(("400").encode())	
				move_count += 1
		elif keys[3]:
			if(player2pos[0]<1024-tank1.get_width() and move_count < 200):
				player2pos[0] += 0.2
				s.send(("600").encode())
				move_count += 1
		if keys[0]:
			if(player2ang<90):
				player2ang += 0.5
				s.send(("080").encode())
		elif keys[2]:
			if(player2ang>=0):
				player2ang -= 0.5
				s.send(("080").encode())
		if keys[4]:
			if player2pow < 100:
				player2pow += 0.5
				s.send("110".encode())				#for power +
		if keys[5]:
			if player2pow > 0:
				player2pow -= 0.5
				s.send("101".encode())
	if((turn and me==2) or (not turn and me==1)):
		buff = s.recv(1024).decode()
		if(buff=="win"):
			print("you win")
			#				<--------------------------display winning screen
			sys.exit()
		if(me==1):
			if(buff=="400"):
				player2pos[0] -= 0.2
			elif(buff=="600"):
				player2pos[0] += 0.2
			elif(buff=="080"):
				player2ang += 1
			elif(buff=="020"):
				player2ang -= 1
			elif(buff=="110"):
				player2pow += 1
			elif(buff=="101"):
				player2pow -= 1
			elif(buff=="001"):
				fireshoot(player1pos, player2pos, player1health, player2health)
				print("1 : "+str(player1health)+" 2: "+str(player2health))
				turn = not turn
		elif(me==2):
			if(buff=="400"):
				player1pos[0] -= 0.2
			elif(buff=="600"):
				player1pos[0] += 0.2
			elif(buff=="080"):
				player1ang += 1
			elif(buff=="020"):
				player1ang -= 1
			elif(buff=="110"):
				player1pow += 1
			elif(buff=="101"):
				player1pow -= 1
			elif(buff=="001"):
				fireshoot(player1pos, player2pos, player1health, player2health)
				print("1 : "+str(player1health)+" 2: "+str(player2health))
				turn = not turn

