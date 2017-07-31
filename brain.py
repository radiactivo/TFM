#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import devices, _emulator_cmd, serials, _adb_dev_list
import argparse
import subprocess
from sys import exit
from dex2oat_fuzzer import main as dex2oat_main


def main(campaign, serial):
	answer = raw_input('Start? [y/n]')

	if answer == 'y':
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

	if args.device in devices:

		adb_process = subprocess.Popen([_adb_dev_list], shell=True, stdout=subprocess.PIPE)
		output = adb_process.stdout.readlines()

		print output
		r = subprocess.Popen([_emulator_cmd + args.device], shell=True)

	serial = serials[0]
	main(args.fuzz, serial)
	r.kill()