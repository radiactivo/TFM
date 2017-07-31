#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import dir_project, dir_samples, dir_mutated, seeds
from utils import find
from time import sleep
import os

def main():

	files = find('*.vcf', dir_samples)

	fuz_num = 0
	for file in files:
		for seed in seeds:
			os.system('radamsa -s ' + str(seed) + ' ' + dir_samples + file.split('/')[-1] + ' > ' + dir_mutated + 'fuzzed_' + str(fuz_num) + '.vcf')
			fuz_num += 1

	fuzs = find('*vcf', dir_mutated)

	for fuz in fuzs:
		os.system('adb push ' + fuz + ' /sdcard/vcfs/' + fuz.split('/')[-1])

	for fuz in fuzs:
		os.system('adb shell am start -t "text/x-vcard" -d "file:///sdcard/vcfs/' + fuz.split('/')[-1] + '" -a android.intent.action.VIEW com.android.contacts')
		os.system('adb shell input keyevent 61')
		os.system('adb shell input keyevent 23')
		sleep(2)

if __name__=='__main__'
	main()