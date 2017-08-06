#!/usr/bin/python
# -*- coding: utf-8 -*-

#3.- Create the fuzzing samples
#4.- Throw them to adb with android emulator
import os
from utils import find, run_subproc, md5
from config import dir_mutated, dir_dexs, dir_samples, dir_project, _pre_command

def run_sample(file, filename, _pre_cmd):
	os.system('{} push  {} /sdcard/{}'.format(_pre_cmd, fuz, filename))
	cmd = '{} shell dex2oat --dex-file=/sdcard/{}  --oat-file=/sdcard/gen.oat'.format(_pre_cmd, filename)
	run_subproc(cmd)
	os.system('{} shell rm /sdcard/{} /sdcard/gen.oat'.format(_pre_cmd, filename))

def main(serial):

	_pre_cmd = 'adb -s {}'.format(serial)

	log = '{}logs/dex2oat_{}_log'.format(dir_project, device)
	f = open(log, 'w')
	f.write('[*] STARTING CAMPAIGN [*]\n')

	count = 0
	fuzs = find('*.dex', dir_mutated)

	for fuz in fuzs:
		filename = fuz.split('/')[-1]
		run_subproc('{} log -p W -t STARTING SAMPLE: {}'.format(_pre_cmd, str(md5(fuz))))
		run_sample(fuz, filename, _pre_cmd)
		count += 1

	f.write('Total samples executed: {}\n'.format(str(count)))
	f.write('[*] FINISH CAMPAIGN [*]\n\n')
	f.close()

if __name__=='__main__':
	main()