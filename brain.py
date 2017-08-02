#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import devices, _emulator_cmd, serials, _adb_dev_list, _root_adb_cmd
import argparse
import subprocess
from sys import exit
from dex2oat_fuzzer import main as dex2oat_main
from utils import run_subproc


def main(campaign, serial):
	
	answer = raw_input('Start as root? [y/n]')
	_pre_command = '{} {}'.format(_pre_command, serial)

	if answer == 'y':
		run_subproc('{} root'.format(_pre_command))
	if campaign == 'dex2oat':
		dex2oat_main(serial)
	elif campaign == 'searchactivity':
		#searchactivity_main(serial)
		pass
	elif campaign == 'contact':
		#contact_main()
		pass

def usage():
	print 'Usage: \n\t {}'.format('python brain.py --fuz <Campaign type> --device <Serial device>')
	exit(0)

if __name__ == '__main__':
 
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--fuzz', help='Campaign type')
	parser.add_argument('-d' ,'--device', help='Serial number of the android device')
	args = parser.parse_args()

	if (args.fuzz == None or args.device == None):
		usage()

	if args.device not in devices:
		usage()

	serial = serials[0]
	adb_process = subprocess.Popen([_adb_dev_list], shell=True, stdout=subprocess.PIPE)
	output = adb_process.stdout.readlines()
	if serial in output[1]:
		serial = serials[1]

	print serial
	r = subprocess.Popen([_emulator_cmd + args.device], shell=True, stdout=None, stderr=None)

	main(args.fuzz, serial)
	r.kill()