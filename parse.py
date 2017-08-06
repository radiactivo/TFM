#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pdb

#sys.path.append(os.path.join(dir_name, "/Users/radiactivo/Applications/nightmare"))

pc = None
singal_code = None

signals = ['SIGABORT', 'SIGALARM', 'SIGKILL']

def extract_info(md5_sample, filename, samples_dict):
	md5_original_sample = None
	original_seed = None
	for key_hash, value_dict in samples_dict.iteritems():
		if md5_sample in value_dict:
			md5_original_sample = key_hash
			original_seed = value_dict[md5_sample]
			break
	if ((md5_original_sample and original_seed ) not in None):
		print 'Summary info: '
		print 'Original file name: {}'.format(samples_dict[md5_original_sample]['name'])
		print 'Seed used: {}'.format(original_seed)
		print 'Fuzzed sample hash: {}'.format(md5_sample)
	
	else:
		if md5_original_sample == None:
			print 'Original sample not found'
		elif original_seed == None:
			print 'Original seed not found'
	return

def add_crash():
	pass
def parse_logs(filename):

	log_results = {}
	
	count = 0
	with open(filename, 'r') as fd:
		for line in fd:
			# if 'STARTING SAMPLE:' in line:
			# 	last_sample = line
			#Extract signal_code and signal
			if 'Fatal signal' in line:
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
					'previous_sample':None,
				}	
				ll = line.split()
				signal_code_index 	= ll.index('signal') + 1
				signal_index 		= signal_code_index + 1
				dic['signal_code'] = ll[signal_code_index]

				for sig in signals:
					if ll[signal_index].find(sig) == -1:
						dic['signal'] = sig
						break

				for line in fd:
					if '>>>' in line and '<<<' in line and 'DEBUG' in line:
						ll = line.split()
						dic['program_name'] = ll[ll.index('>>>') + 1]

						for line in fd:
							if 'Abort message:' in line  and 'DEBUG' in line:
								dic['abort_message'] = line.split('Abort message: ')[-1]

								for line in fd:
									if 'eax' in line and 'ebx' in line and 'ecx' in line and 'edx' in line and 'DEBUG' in line:
										regis = ['eax', 'ebx', 'ecx', 'edx']
										ll = line.split()
										for reg in regis:
											
											dic['registers'][reg] = ll[ll.index(reg) + 1]
									elif 'esi' in line and 'edi' in line and 'DEBUG' in line:	
										regis = ['esi', 'edi']
										ll = line.split()
										for reg in regis:
											dic['registers'][reg] = ll[ll.index(reg) + 1]
									elif 'xcs' in line and 'xes' in line and 'xfs' in line and 'xss' in line:
										regis = ['xcs', 'xes', 'xfs', 'xss']
										ll = line.split()
										for reg in regis:
											dic['registers'][reg] = ll[ll.index(reg) + 1]
									elif 'eip' in line and 'ebp' in line and 'esp' in line and 'flags' in line:
										regis = ['eip', 'ebp', 'esp', 'flags']
										ll = line.split()
										for reg in regis:
											dic['registers'][reg] = ll[ll.index(reg) + 1]
									elif 'backtrace' in line:
										for line in fd:
											if 'DEBUG' in line and ':     #' in line:
												dic['backtrace'].append(line.split(':     ')[-1])
											else:
												log_results[count] = dic
												count += 1
												break
										break
								break
						break


					#index = buff.index(line)

					#for elem in buff[index + 1:]:
	return log_results
	# extract abort message then registers in the next lines

if __name__=='__main__':
	parse_logs('log_example.txt')