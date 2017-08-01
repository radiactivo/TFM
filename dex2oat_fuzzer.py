#!/usr/bin/python
# -*- coding: utf-8 -*-

#3.- Create the fuzzing samples
#4.- Throw them to adb with android emulator
import os
from utils import find, run_subproc
from config import dir_mutated, dir_dexs, dir_samples, dir_project

def main(serial):

	_pre_cmd = 'adb -s {}'.format(serial)

	#LOG
	log = dir_project + 'logs/fuzzed_generator_log'	
	
	f = open(log, 'w')

	#UPLOAD AND FUZZ
	count = 0
	fuzs = find('*.dex', dir_mutated)
	for fuz in fuzs:
		filename = fuz.split('/')[-1]

		os.system('{} push  {} /sdcard/{}'.format(_pre_cmd, fuz, filename))
		#LOG TAG MESSAGE WITH INFO SAMPLE
		cmd = '{} shell dex2oat --dex-file=/sdcard/{}  --oat-file=/sdcard/gen.oat'.format(_pre_cmd, filename)
		run_subproc(cmd)
		os.system('{} shell rm /sdcard/{} /sdcard/gen.oat'.format(_pre_cmd, filename))

		count += 1

	f.close()

if __name__=='__main__':
	main()