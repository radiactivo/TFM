#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import dir_project, dir_samples, dir_mutated, seeds, _pre_command
from utils import find, run_subproc
from time import sleep
import os

def main(serial):

	_pre_command = '{} {}'.format(_pre_command, serial)
	fuzs = find('*vcf', dir_mutated)

	for fuz in fuzs:
		filename = fuz.split('/')[-1]
		os.system('{} push {} /sdcard/{}'.format(_pre_command, fuz, filename))
		os.system('{} shell am start -t "text/x-vcard" -d "file:///sdcard/vcfs/{}" -a android.intent.action.VIEW com.android.contacts'.format(_pre_command, filename))
		os.system('{} shell input keyevent 61'.format(_pre_command))
		os.system('{} shell input keyevent 23'.format(_pre_command))
		sleep(2)
		run_subproc('{} shell rm /sdcard/{}'.format(_pre_command, filename))

if __name__=='__main__'
	main()