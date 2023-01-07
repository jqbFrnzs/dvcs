"""
gites - Distributed Version Control System

Client

J. Francuz & D. Gaszewski
January 2023
"""
import sys
import os

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

# run client
if __name__=='__main__':
	check_args()
	