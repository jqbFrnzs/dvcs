"""
gites - Distributed Version Control System

Server 4

J. Francuz & D. Gaszewski
January 2023
"""

import sys

# function to check port number assignment
def check_args():

	# error handling argument
	if len(sys.argv) != 2:
		print("ERROR: Must supply port number \nUSAGE: py dfs1.py 10004")
		sys.exit()

	# error handling port number 
	else:
		try:
			if int(sys.argv[1]) != 10004:
				print("ERROR: Port number must be 10004")
				sys.exit()
			else:
				return int(sys.argv[1])
				
		except ValueError:
				print("ERROR: Port number must be a number.")
				sys.exit()