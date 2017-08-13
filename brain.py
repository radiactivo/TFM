#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import devices, _emulator_cmd, serials, _adb_dev_list, _pre_command, dir_logs
import argparse
import subprocess
from sys import exit
from dex2oat_fuzzer import main as dex2oat_main
from contact_fuzzer import main as contact_main
from searchactivity_fuzzer import main as quicksearchbox_main
from searchactivity_fuzzer import main_fuzzed as quicksearchbox_main_fuzz
from utils import run_subproc, run_subprocess,generate_timestamp
import os

def main(campaign, serial, device):
	command = '{} {}'.format('adb -s', serial)
	timestamp = str(generate_timestamp())
	log_dir = '{}{}/{}/{}.dat'.format(dir_logs, device, campaign, timestamp)
	log_adb = '{}{}/{}/{}.log'.format(dir_logs, device, campaign, timestamp)

	answer = raw_input('Start?')

	run_subproc('{} root'.format(command))
	cmd_logcat = '{} logcat >> {}'.format(command, log_adb)
	log_sbp = run_subprocess( cmd_logcat )

	log_fd = open(log_dir, 'a')
	log_fd.write('[*] STARTING CAMPAIGN [*]\n')

	if campaign == 'dex2oat_simple':
		dex2oat_main(serial, log_fd)
	elif campaign == 'dex2oat_smart':
		dex2oat_main(serial, log_fd)
	elif campaign == 'quicksearchbox':
		quicksearchbox_main(serial, log_fd)
	elif campaign == 'quicksearchbox_rand':
		quicksearchbox_main_fuzz(serial, log_fd)
	elif campaign == 'contact':
		contact_main(serial, log_fd, device, cmd_logcat, log_sbp)
	elif campaign == 'contact_gen':
		contact_main(serial, log_fd, device, cmd_logcat, log_sbp)

	log_fd.write('[*] FINISH CAMPAIGN [*]\n\n')
	log_fd.close()

	try:
		log_sbp.kill()
	except:
		pass

def usage():
	print 'usage: \n\t {}'.format('python brain.py --fuz <Campaign type> --device <Serial device>')
	exit(0)

if __name__ == '__main__':
 
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--fuzz', help='Campaign type')
	parser.add_argument('-d' ,'--device', help='Serial number of the android device')
	args = parser.parse_args()

	if (args.fuzz == None or args.device == None): usage()
	if args.device not in devices: usage()

	serial = serials[0]
	adb_process = subprocess.Popen([_adb_dev_list], shell=True, stdout=subprocess.PIPE)
	output = adb_process.stdout.readlines()
	if serial in output[1]:
		serial = serials[1]

	print serial
	r = subprocess.Popen(['{}{}'.format(_emulator_cmd, args.device)], shell=True, stdout=subprocess.PIPE, stderr=None)

	main(args.fuzz, serial, args.device)
	r.kill()