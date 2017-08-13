#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import dir_project, dir_samples, dir_mutated, seeds, _pre_command
from utils import find, run_subproc, run_subprocess, md5
from time import sleep
import os
import subprocess

def main(serial, log_fd, device, cmd_logcat, log_sb):

	_pre_command = '{} {}'.format('adb -s', serial)
	fuzs = find('*.vcf', dir_mutated)
	count = 0

	for fuz in fuzs:
		filename = fuz.split('/')[-1]
		run_subproc('{} shell log -p W -t STARTING SAMPLE: {}'.format(_pre_command, str(md5(fuz))))
		run_subproc('{} push {} /data/{}'.format(_pre_command, fuz, filename))
		run_subproc('{} shell am start -t "text/vcard" -d "file:///data/{}" -a android.intent.action.VIEW com.android.contacts'.format(_pre_command, filename))
		if 'nougat' in device:
			os.run_subproc('{} shell input keyevent 61'.format(_pre_command))
			os.run_subproc('{} shell input keyevent 23'.format(_pre_command))
		if log_sb.poll() is not None: log_sb = run_subprocess( cmd_logcat )
		sleep(3)
		if log_sb.poll() is not None: log_sb = run_subprocess( cmd_logcat )
		run_subproc('{} shell rm /data/{}'.format(_pre_command, filename))
		count += 1

	log_fd.write('Total samples executed: {}\n'.format(str(count)))

#am start -t "text/vcard" -d "file:///sdcard/sample_0.vcf" -a android.intent.action.VIEW com.android.contacts
if __name__=='__main__':
	main()




"""
		text = r.communicate()[0].split('\n')
		for line in text:
			if 'No space left on device' in line:
				os.system('{} shell pm clear com.android.providers.contacts'.format(_pre_command))
				print '[+] CLEANING CONTACT LIST [+]'
				sleep(5)
				os.system('{} push {} /data/{}'.format(_pre_command, fuz, filename))
		os.system('{} shell am start -t "text/vcard" -d "file:///data/{}" -a android.intent.action.VIEW com.android.contacts'.format(_pre_command, filename))
		r.wait()
"""