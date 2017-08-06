import pdb
import subprocess
from utils import find, run_subproc
from time import sleep

_NORMAL_MSG = 'Starting: Intent { act=android.intent.action.WEB_SEARCH cat=[android.intent.category.DEFAULT] cmp=com.google.android.googlequicksearchbox/.SearchActivity (has extras) }'
_TOO_LONG_MSG = 'error: write failure during connection: Message too long'
_GENERIC_ERROR = 'error: bad service name length'

# Set the command
_command = 'adb shell am start -n "com.google.android.googlequicksearchbox/.SearchActivity" -a "android.intent.action.WEB_SEARCH" -c "android.intent.category.DEFAULT" -e "query" '

def execute(command):
	# Setup the module object
	proc = subprocess.Popen(command,
	                    shell=True,   
	                    stdin=subprocess.PIPE,
	                    stdout=subprocess.PIPE,
	                    stderr=subprocess.PIPE)

	# Communicate the command
	stdout_value,stderr_value = proc.communicate()

	run_subproc('adb shell log -p W -t @@SEARCHBOX_FUZZ@@ Finishing')

	sleep(5)
	return [stdout_value, stderr_value, command]

def check_command_conditions(stdout_value, stderr_value, command):
	if _NORMAL_MSG in stdout_value:
		if len(command) <= 3908:
			return 1
		#message accepted as valid with extra length....	
		print '[*] WIERD 1 [*]'
		print 'File: ' + file
		print 'Command: ' +  command
	elif _TOO_LONG_MSG in stdout_value:
		if len(command) == 3909:
			return 1
		#message given with diff length than in previous tests
		print '[*] WIERD 2 [*]'
		print 'File: ' + file
		print 'Command: ' +  command

	elif _GENERIC_ERROR in stdout_value:
		if len(command) >= 3910:
			return 1

		#message given with lower length than expected
		print '[*] WIERD 3 [*]'
		print 'File: ' + file
		print 'Command: ' +  command

	else:
		#no match found
		print '[*] WIERD 4 [*]'
		print 'File: ' + file
		print 'Command: ' +  command
		print 'STDOUT: ' +  stdout_value
		print 'STDERR: ' + stderr_value

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

files = find('*', dir_fuzzdb_atack)
for file in files:

	with open(file, 'r') as f:
		out = f.read()
	lines = out.split('\n')

	for line in lines:
		if 'ping' in line:
			print '[*] AVOIDING PING[*]'
			continue
		command = shellquote('{} "{}"'.format(command, line))
		run_subproc('adb shell log -p W -t @@SEARCHBOX_FUZZ@@ Starting subfuzz with command: ' + command)
		conditions = execute(command)

		check_command_conditions(conditions[0], conditions[1], conditions[2])

#adb shell am start -D -n "com.google.android.googlequicksearchbox/.SearchActivity" -a "android.intent.action.WEB_SEARCH" -c "android.intent.category.DEFAULT" -e "query" $(python -c 'print "a"*3000')