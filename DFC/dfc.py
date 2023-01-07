"""
gites - Distributed Version Control System

Client

J. Francuz & D. Gaszewski
January 2023
"""
import sys
import os
import re
import hashlib
import time
import socket

# check argument to open dfc.conf 
def check_args():

	# error handling no argument 
	if len(sys.argv) != 2:
		print("ERROR: Must supply an argument \nUSAGE: python dfc.py dfc.conf")
		sys.exit()

	# error handling argument passed 
	elif sys.argv[1].lower() != 'dfc.conf':
		print("ERROR: Must supply a valid argument \nUSAGE: python dfc.py dfc.conf")
		sys.exit()
		
	# error if there is no dfc.conf file
	elif os.path.isfile(sys.argv[1]) != True:
		print("ERROR: dfc.conf not found.")
		sys.exit()	
	
	# if no error, return dfc.conf 
	else:
		return sys.argv[1]

# params for user auth from dfc.conf
def user_auth():
	
	# get usernames
	fh = open('dfc.conf', mode='r', encoding='cp1252')
	users=re.findall(r'Username: .*', fh.read())
	usernames=list()
	for i in range(0, len(users)):
		usernames.append(str(users[i]).split()[1])
	fh.close()
		
	# get passwords 
	fh = open('dfc.conf', mode='r', encoding='cp1252')
	passes=re.findall(r'Password: .*', fh.read())
	passwords=list()
	for i in range(0, len(passes)):
		passwords.append(str(passes[i]).split()[1])
	fh.close()

	# dict with usernames:passwords 
	global auth_dict 
	auth_dict = {}
	for i in range(0, len(users)):
		entry={usernames[i]:passwords[i]}
		auth_dict.update(entry)
	
	return auth_dict

# client-side auth
def authenticate():
	
	# config params
	user_auth()
	
	# authenticate username
	
	# initialize an auth status 
	auth_status = ''
	
	# give user 4 attempts
	for i in range(0, 4):
		if auth_status == 'Valid username.':
			# go to password auth 
			pass
		
		else:
			# get username 
			username = input('username: ')
		
			# initialize username auth 
			username_auth = []
			ct = 0
			for key, value in auth_dict.items():
				ct += 1
				if username == key:
					# get specific username index in dictionary 
					username_auth.append(ct)
				else:
					username_auth.append(0)
							
			if i < 2:
				if sum(username_auth) > 0:
					auth_status = 'Valid username.'
					continue
				else:
					print('Username does not exist. You have ' +str(3-i) + ' attempts left.')
					continue 
			elif i == 2:
				if sum(username_auth) > 0:
					auth_status = 'Valid username.'
					continue
				else:
					print('Username does not exist. You have ' +str(3-i) + ' attempt left.')
					continue 				
			else:
				if sum(username_auth) > 0:
					auth_status = 'Valid username.'
					continue
				else:
					print('Username does not exist. You have no more attempts.\nExiting now....')
					sys.exit()

    # authenticate password 
	# get the index of the user in the auth_dict to check password in that index
	user_index = sum(username_auth)

	# re-initialize auth status
	auth_status = ''
	for i in range(0, 4):
		if auth_status == 'Valid password.':
			# pass authentication 
			pass
			
		else:
			# get password
			password = input('password: ')
			# hash 
			hash=hashlib.md5()
			hash.update(password.encode())
			password = hash.hexdigest()
			
			# initialize password auth 			
			password_auth = []
			ct = 0
			for key, value in auth_dict.items():
				ct += 1
				if password == value:
					password_auth.append(ct)
				else:
					password_auth.append(0)
			
			if i < 2:
				if sum(password_auth) > 0:
					# check that index of password matches user index
					if user_index == sum(password_auth):
						auth_status = 'Valid password.'
						continue
					else:
						print('Wrong password. You have ' +str(3-i) + ' attempts left.')
						continue
				else:
					print('Wrong password. You have ' +str(3-i) + ' attempts left.')
					continue
			elif i == 2:
				if sum(password_auth) > 0:
					if user_index == sum(password_auth):
						auth_status = 'Valid password.'
						continue
					else:
						print('Wrong password. You have ' +str(3-i) + ' attempt left.')
						continue 				
				else:
					print('Wrong password. You have ' +str(3-i) + ' attempt left.')
					continue 
			else:
				if user_index == sum(password_auth):
					auth_status = 'Valid password.'
					continue
				else:
					print('Wrong password. You have no more attempts.\nExiting now....')
					sys.exit()

    # Final auth after passing all checks
	print('Authorization Granted.')					
	global final_authorization
	final_authorization = (username, password)
	return final_authorization

# config params for server
def server_conf():	

	# open config file 
	fh = open('dfc.conf', mode='r', encoding='cp1252')
	params = re.findall(r'DFS.*', fh.read())

	# get server names 
	s_names = list()
	for i in range(0, len(params)):
		s_names.append(str(params[i]).split()[1].split(":")[0])
	
	# get server ports 
	s_ports = list()
	for i in range(0, len(params)):
		s_ports.append(str(params[i]).split()[1].split(":")[1])

	# dict with server names
	s_names_dict = {}
	for i in range(0, len(params)):
		entry={'server' +str(i+1):s_names[i]}
		s_names_dict.update(entry)
		
	# dict with server ports
	s_ports_dict = {}
	for i in range(0, len(params)):
		entry={'server' +str(i+1):s_ports[i]}
		s_ports_dict.update(entry)
	
	# lists of (sever name, server port) lists
	global server_list
	server_list = list()
	ct = 0
	for i in range(0, len(params)):
		ct += 1
		server_list.append((s_names_dict['server' +str(ct)],\
							int(s_ports_dict['server' + str(ct)])))
	return server_list

# split a file given a chunk size 
def split_files(filename, chunksize):

	# create chunks 
	with open(filename + '.txt', 'rb') as bytefile:
		content = bytearray(os.path.getsize(filename + '.txt'))
		bytefile.readinto(content)
		
		for count, i in enumerate(range(0, len(content), chunksize)):
			with open(filename + '_' + str(count+1) + '.txt.', 'wb') as fh:
				fh.write(content[i: i + chunksize])

				
# determine server location for chunk pairs
def chunk_pairs(filename):
		
	# group chunks in paired lists							# per table:
	pair1 = [filename +'_1.txt', filename +'_2.txt']    	# 1,2
	pair2 = [filename +'_2.txt', filename +'_3.txt'] 		# 2,3
	pair3 = [filename +'_3.txt', filename +'_4.txt']		# 3,4 
	pair4 = [filename +'_4.txt', filename +'_1.txt']		# 4,1

	# md5 hash value of file 

	hash=hashlib.md5()
	with open(filename +'.txt', 'rb') as fh:
		buffer = fh.read()
		hash.update(buffer)
		
		# modulus determines server pairs
		storeval = int(hash.hexdigest(), 16) % 4

	# server pairs depending on modulus
	if storeval == 0:
		dfs1 = pair1
		dfs2 = pair2
		dfs3 = pair3
		dfs4 = pair4
	elif storeval == 1:
		dfs1 = pair4
		dfs2 = pair1
		dfs3 = pair2
		dfs4 = pair3
	elif storeval == 2:
		dfs1 = pair3
		dfs2 = pair4
		dfs3 = pair1
		dfs4 = pair2
	else:
		dfs1 = pair2
		dfs2 = pair3
		dfs3 = pair4
		dfs4 = pair1
	
	return dfs1, dfs2, dfs3, dfs4 

# get command from user
def get_command():

	global command
	command = ''
	for i in range(0, 4):
		if command != '':
			return command
			break
		else:
			comm = input('Please specify a command [get, list, put]: ')
			if i < 2:
				if comm.lower() == 'get':
					command = 'get'
					continue
				elif comm.lower() == 'list':
					command = 'list'
					continue
				elif comm.lower() == 'put':
					command = 'put'
					continue
				else:
					print('There is no such command. You have ' +str(3-i) + ' attempts left.')
					continue
			elif i == 2:
				if comm.lower() == 'get':
					command = 'get'
					continue
				elif comm.lower() == 'list':
					command = 'list'
					continue
				elif comm.lower() == 'put':
					command = 'put'
					continue
				else:
					print('There is no such command. You have ' +str(3-i) + ' attempt left.')
					continue
			else:
				print('There is no such command. You have no more attempts.\nExiting now....')
				sys.exit()

# define client socket connection
def client():
	
	# authenticate with client ----------------------------
	authenticate()
	username = final_authorization[0]
	password = final_authorization[1]
	
	# connect to servers ----------------------------------
	
	# config params for servers 
	server_conf()

	# DFS1 
	try:
		client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket1.connect(server_list[0])
		status1 = ('Connected to server', 'DFS1')
		print(status1[0], status1[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status1 = ('Could not connect to server', 'DFS1')
		print(status1[0], status1[1])
		
	# DFS2
	try:
		client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket2.connect(server_list[1])
		status2 = ('Connected to server', 'DFS2')
		print(status2[0], status2[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status2 = ('Could not connect to server', 'DFS2')
		print(status2[0], status2[1])
		
	# DFS3
	try:
		client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket3.connect(server_list[2])
		status3 = ('Connected to server', 'DFS3')
		print(status3[0], status3[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status3 = ('Could not connect to server', 'DFS3')
		print(status3[0], status3[1])
		
	# DFS4
	try:
		client_socket4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket4.connect(server_list[3])
		status4 = ('Connected to server', 'DFS4')
		print(status4[0], status4[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status4 = ('Could not connect to server', 'DFS4')
		print(status4[0], status4[1])	


	# if all servers are down, exit client 
	if status1[0] == 'Could not connect to server' and status2[0] == 'Could not connect to server' \
		and status3[0] == 'Could not connect to server' and status4[0] == 'Could not connect to server':
		print('All servers are down.\nExiting now...')
		sys.exit()
	else:
		pass
		
	# looping lists: connections, and server names
	conns = (client_socket1, client_socket2, client_socket3, client_socket4)
	DFSS = ('DFS1', 'DFS2', 'DFS3', 'DFS4')	

	
	# authenticate with servers ---------------------------
	
	# send usernames 
	for i in range(0,4):
		try:
			conns[i].send(username.encode())
			time.sleep(1)
		except OSError:
			pass 
	
	# send passwords
	for i in range(0,4):
		try:
			conns[i].send(password.encode())
		except OSError:
			pass 		
				
	# server authorization response
	for i in range(0,4):
		try:
			response = conns[i].recv(1024)
			print('From ' +DFSS[i] +': ' +response.decode())
		except OSError:
			pass

# run client
if __name__=='__main__':
	check_args()
	