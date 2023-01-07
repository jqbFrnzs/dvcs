"""
gites - Distributed Version Control System

Client

J. Francuz & D. Gaszewski
January 2023
"""
import sys
import os
import re

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

# run client
if __name__=='__main__':
	check_args()
	