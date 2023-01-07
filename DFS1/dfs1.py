"""
gites - Distributed Version Control System

Server 1

J. Francuz & D. Gaszewski
January 2023
"""

import sys
import re
import

# function to check port number assignment
def check_args():

	# error handling argument
	if len(sys.argv) != 2:
		print("ERROR: Must supply port number \nUSAGE: py dfs1.py 10001")
		sys.exit()

	# error handling port number 
	else:
		try:
			if int(sys.argv[1]) != 10001:
				print("ERROR: Port number must be 10001")
				sys.exit()
			else:
				return int(sys.argv[1])
				
		except ValueError:
				print("ERROR: Port number must be a number.")
				sys.exit()

# get authentication parameters
def auth_params():

	# use dfs configuration file 
	config_file='dfs.conf'

	# get usernames from config file 
	fh=open(config_file, mode='r', encoding='cp1252')
	users=re.findall(r'Username: .*', fh.read())
	usernames=list()
	for i in range(0, len(users)):
		usernames.append(str(users[i]).split()[1])
	fh.close()

	# get passwords from config file
	fh=open(config_file, mode='r', encoding='cp1252')
	passes=re.findall(r'Password: .*', fh.read())
	passwords=list()
	for i in range(0, len(passes)):
		passwords.append(str(passes[i]).split()[1])
	fh.close()

	# create dict with usernames:passwords 
	global auth_dict 
	auth_dict = {}
	for i in range(0, len(users)):
		entry={usernames[i]:passwords[i]}
		auth_dict.update(entry)

	return auth_dict

# authorize client, given username and password
def client_auth(auth_dict, username, password):
	ct = 0
	auth_status=''
	for key, value in auth_dict.items():
		ct += 1
		if auth_status != '':
			pass
		else:
			# check all users up to last
			if ct < len(auth_dict):
			
				if username == key:
					print('Correct username.')
					
					if password == value:
						print('Correct password.')
						
						auth_status='Authorization Granted.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						pass
					else:
						print('Incorrect password.')
						auth_status = 'Authorization Denied.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						sys.exit()
				else:
					continue
			
			# check last user
			else:
				if username == key:
					print('Correct username.')
							
					if password == value:
						print('Correct password.')
						
						auth_status='Authorization Granted.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						pass
					else:
						print('Incorrect password.')
						auth_status = 'Authorization Denied.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						sys.exit()
				else:
					print('Incorrect username.')
					auth_status = 'Authorization Denied.\n'
					print(auth_status)
					conn.send(auth_status.encode())
					sys.exit()