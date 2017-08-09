#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import dir_project, dir_samples, dir_mutated, seeds, _pre_command
from utils import find, run_subproc, md5
from time import sleep
import os

def main(serial, log_fd):

	_pre_command = '{} {}'.format('adb -s', serial)
	fuzs = find('*.vcf', dir_mutated)
	count = 0

	for fuz in fuzs:
		filename = fuz.split('/')[-1]
		os.system('{} push {} /data/{}'.format(_pre_command, fuz, filename))
		os.system('{} shell chmod 777 /sdcard/{}'.format(_pre_command, filename))
		run_subproc('{} shell log -p W -t STARTING SAMPLE: {}'.format(_pre_command, str(md5(fuz))))
		os.system('{} shell am start -t "text/vcard" -d "file:///data/{}" -a android.intent.action.VIEW com.android.contacts'.format(_pre_command, filename))
		os.system('{} shell input keyevent 61'.format(_pre_command))
		os.system('{} shell input keyevent 23'.format(_pre_command))
		sleep(2)
		run_subproc('{} shell rm /data/{}'.format(_pre_command, filename))
		count += 1

	log_fd.write('Total samples executed: {}\n'.format(str(count)))

#am start -t "text/vcard" -d "file:///sdcard/sample_0.vcf" -a android.intent.action.VIEW com.android.contacts
if __name__=='__main__':
	main()