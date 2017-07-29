#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, fnmatch
from utils import *

dir_project = '/Users/radiactivo/Documents/TFM/'
dir_apks = dir_project + 'apks/'
dir_dexs = dir_project + 'dexs/'
log = dir_project + 'logs/sample_generator_log'

f = open(log, 'w')
sample_num = 0
apks = find('*.apk', dir_apks)
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
