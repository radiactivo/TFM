#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import dir_project, dir_samples, dir_dexs, seeds
import os, fnmatch
from utils import *



#######	DEX2OAT SAMPLE EXTRACTOR
log = dir_project + 'logs/sample_generator_log'

f = open(log, 'w')
sample_num = 0
apks = find('*.apk', dir_samples)

for apk in apks:
	apk_folder = apk[0:len(apk) - 4] + '/'
	os.system('unzip ' + apk + ' -d ' + apk_folder)
	dex_files = find('*.dex', apk_folder)
	if len(dex_files) == 0:
		print '[-] No dex class on: ' + apk_folder
	else:
		for dex_file in dex_files:
			os.system('mv ' + dex_file + ' ' + dir_dexs + 'sample_' + str(sample_num) + '.dex')
			sample_num +=1
			f.write(dex_file + ';' + 'sample_' + str(sample_num))
	os.system('sudo rm -rf ' + apk_folder)

#FUZZED GENERATOR
dexs = find('*.dex', dir_dexs)
fuz_num = 0
for dex in dexs:
	for seed in seeds:
		os.system('radamsa -s ' + str(seed) + ' ' + dir_dexs + 'sample_' + dex[44:] + ' > ' + dir_mutated + 'fuzzed_' + str(fuz_num) + '.dex')
		fuz_num += 1
		print fuz_num
