"""
gites - Distributed Version Control System

Server 1

J. Francuz & D. Gaszewski
January 2023
"""

import sys
import re

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