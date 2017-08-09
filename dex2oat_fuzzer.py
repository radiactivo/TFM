#!/usr/bin/python
# -*- coding: utf-8 -*-

#3.- Create the fuzzing samples
#4.- Throw them to adb with android emulator
import os
from utils import find, run_subproc, md5
from config import dir_mutated, dir_dexs, dir_samples, dir_project, _pre_command

def run_sample(file, filename, _pre_cmd):
	os.system('{} push  {} /data/{}'.format(_pre_cmd, file, filename))
	cmd = '{} shell dex2oat --dex-file=/data/{}  --oat-file=/data/gen.oat'.format(_pre_cmd, filename)
	run_subproc(cmd)
	os.system('{} shell rm /data/{} /data/gen.oat'.format(_pre_cmd, filename))

def main(serial, log_fd):
	_pre_cmd = 'adb -s {}'.format(serial)
	fuzs = find('*.dex', dir_mutated)
	count = 0

	for fuz in fuzs:
		filename = fuz.split('/')[-1]
		run_subproc('{} shell log -p W -t STARTING SAMPLE: {}'.format(_pre_cmd, str(md5(fuz))))
		run_sample(fuz, filename, _pre_cmd)
		count += 1

	log_fd.write('Total samples executed: {}\n'.format(str(count)))

if __name__=='__main__':
	main()