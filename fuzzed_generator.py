#!/usr/bin/python
# -*- coding: utf-8 -*-

#3.- Create the fuzzing samples
#4.- Throw them to adb with android emulator
import os
from utils import *

dir_project = '/Users/radiactivo/Documents/TFM/'
dir_dexs = dir_project + 'dexs/'
log = dir_project + 'logs/fuzzed_generator_log'

seeds = ['764225987', '328117335', '454487956', '748305375', '260137859']

f = open(log, 'w')
dexs = find('*.dex', dir_dexs)
fuz_num = 0

for dex in dexs:
	for i in range(0,5):
		os.system('radamsa -s ' + seeds[i] + ' ' + dir_dexs + 'sample_' + dex[44:] + ' > ' + dir_dexs + 'fuzzed_' + str(fuz_num) + '.dex')
		fuz_num += 1
		print fuz_num

fuzs = find('fuzzed_*', dir_dexs)
for fuz in fuzs:
	os.system('adb push ' + fuz + ' /sdcard/dexs/' + fuz[37:])
	
count = 0
for fuz in fuzs:
	cmd = 'adb shell dex2oat --dex-file=/sdcard/dexs/' + fuz[37:] + ' --oat-file=/sdcard/oats/gen' + str(count) + '.oat'
	run_subproc(cmd)
	count += 1
