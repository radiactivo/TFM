import pdb
import subprocess
from utils import find, run_subproc, extract_fuzzdb_strings, fuzz_stream_seed
from time import sleep
import subprocess
from config import seeds
from time import sleep
from random import randint

_NORMAL_MSG = 'Starting: Intent { act=android.intent.action.WEB_SEARCH cat=[android.intent.category.DEFAULT] cmp=com.google.android.googlequicksearchbox/.SearchActivity (has extras) }'
_TOO_LONG_MSG = 'error: write failure during connection: Message too long'
_GENERIC_ERROR = 'error: bad service name length'

# Set the command
_command = 'am start -n "com.google.android.googlequicksearchbox/.SearchActivity" -a "android.intent.action.WEB_SEARCH" -c "android.intent.category.DEFAULT" -e "query"'

# def execute(command):
# 	# Setup the module object
# 	proc = subprocess.Popen(command,
# 	                    shell=True,   
# 	                    stdin=subprocess.PIPE,
# 	                    stdout=subprocess.PIPE,
# 	                    stderr=subprocess.PIPE)

# 	# Communicate the command
# 	stdout_value,stderr_value = proc.communicate()

# 	run_subproc('adb shell log -p W -t @@SEARCHBOX_FUZZ@@ Finishing')

# 	sleep(5)
# 	return [stdout_value, stderr_value, command]

# def check_command_conditions(stdout_value, stderr_value, command):
# 	if _NORMAL_MSG in stdout_value:
# 		if len(command) <= 3908:
# 			return 1
# 		#message accepted as valid with extra length....	
# 		print '[*] WIERD 1 [*]'
# 		print 'File: ' + file
# 		print 'Command: ' +  command
# 	elif _TOO_LONG_MSG in stdout_value:
# 		if len(command) == 3909:
# 			return 1
# 		#message given with diff length than in previous tests
# 		print '[*] WIERD 2 [*]'
# 		print 'File: ' + file
# 		print 'Command: ' +  command

# 	elif _GENERIC_ERROR in stdout_value:
# 		if len(command) >= 3910:
# 			return 1

# 		#message given with lower length than expected
# 		print '[*] WIERD 3 [*]'
# 		print 'File: ' + file
# 		print 'Command: ' +  command

# 	else:
# 		#no match found
# 		print '[*] WIERD 4 [*]'
# 		print 'File: ' + file
# 		print 'Command: ' +  command
# 		print 'STDOUT: ' +  stdout_value
# 		print 'STDERR: ' + stderr_value

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def main_fuzzed(serial, log_fd):
	_pre_cmd = 'adb -s {}'.format(serial)
	half_command = '{} {}'.format(_pre_cmd, _command)
	lines = extract_fuzzdb_strings()

	for line in lines:
		if 'ping' in line:
			print '[*] AVOIDING PING[*]'
			continue

		#command = shellquote('{} "{}"'.format(half_command, line))
		run_subproc('{} shell log -p W -t @@SEARCHBOX_FUZZ@@ Starting subfuzz with command: {}'.format( _pre_cmd, _command))
		#run_subproc(command)
		r = subprocess.Popen(['{} shell'.format(_pre_cmd)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		res = r.communicate(fuzz_stream_seed('{} "{}"'.format(_command, line), str(seeds[randint(0,len(seeds) -1 )])))
		print 'Stdout: {}'.format(res[0])
		print 'Stderr: {}'.format(res[1])
		try:
			r.kill()
		except:
			pass

def main(serial, log_fd):
	
	######
	#NO USAGE OF SERIAL OR log_fd
	#######
	_pre_cmd = 'adb -s {}'.format(serial)
	half_command = '{} {}'.format(_pre_cmd, _command)
	lines = extract_fuzzdb_strings()

	for line in lines:
		if 'ping' in line:
			print '[*] AVOIDING PING[*]'
			continue

		#command = shellquote('{} "{}"'.format(half_command, line))
		run_subproc('{} shell log -p W -t @@SEARCHBOX_FUZZ@@ Starting subfuzz with command: {}'.format( _pre_cmd, _command))
		#run_subproc(command)
		r = subprocess.Popen(['{} shell'.format(_pre_cmd)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		res = r.communicate('{} "{}"'.format(_command, line))
		print 'Stdout: {}'.format(res[0])
		print 'Stderr: {}'.format(res[1])
		try:
			r.kill()
		except:
			pass
		sleep(2)
		# conditions = execute(command)
		# check_command_conditions(conditions[0], conditions[1], conditions[2])

	#adb shell am start -D -n "com.google.android.googlequicksearchbox/.SearchActivity" -a "android.intent.action.WEB_SEARCH" -c "android.intent.category.DEFAULT" -e "query" $(python -c 'print "a"*3000')