from subprocess import call
import sys

args = sys.argv

del args[0]

if len(sys.argv) > 0:
	sys.exit(call(['aria2c','-s16','-x16'] + args))
else:
	print('Error: Too few args!')
	sys.exit(999)