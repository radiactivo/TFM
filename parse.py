#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

#sys.path.append(os.path.join(dir_name, "/Users/radiactivo/Applications/nightmare"))

pc = None
singal_code = None

signals = ['SIGABORT', 'SIGALARM', 'SIGKILL', '']

def parse_logs(buff):
	for line in buff:
		if 'Fatal' in line:
			ll = line.split()
			signal = ll.index('signal') + 1
			print ll[signal + 1]
	# extract abort message then registers in the next lines

if __name__=='__main__':
	with open('log_example.txt') as fd:
		buff = fd.readlines()
	parse_logs(buff)