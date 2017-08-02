#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pdb

#sys.path.append(os.path.join(dir_name, "/Users/radiactivo/Applications/nightmare"))

pc = None
singal_code = None

signals = ['SIGABORT', 'SIGALARM', 'SIGKILL', '']

def parse_logs(buff):

	dic = {
		'signal': None,
		'signal_code':None,
		'abort_message':None,
		'program_name':None,
		'pc': None,
		'registers':
			{
				'eax':None,
				'ebx':None,
				'ecx':None,
				'edx':None,
				'esi':None,
				'edi':None,
				'xcs':None,
				'xds':None,
				'xes':None,
				'xfs':None,
				'xss':None,
				'eip':None,
				'ebp':None,
				'esp':None,
				'flags':None,
			},
		'backtrace':[],
		'tombstone':None,
	}
	
	for line in buff:

		#Extract signal_code and signal
		if 'Fatal' in line:	
			ll = line.split()
			signal_code_index 	= ll.index('signal') + 1
			signal_index 		= signal_code_index + 1
			dic['signal_code'] = ll[signal_code_index]

			for sig in signals:
				if sig in ll[signal_index]:
					dic['signal'] = sig
					break

		index = buff.index(line)

		for element in buff[index:]:
			if '>>>' in element and '<<<' in element:
				ll = element.split()
				dic['program_name'] = ll[ll.index('>>>') + 1]
				break

		index = buff.index(line)
		
		pdb.set_trace()
	# extract abort message then registers in the next lines

if __name__=='__main__':
	with open('log_example.txt') as fd:
		buff = fd.readlines()
	parse_logs(buff)