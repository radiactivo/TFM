
sys.path.append(os.path.join(dir_name, "/Users/radiactivo/Applications/nightmare"))

pc = None
singal_code = None
def parse_logs(log):
	buff = buff.split()
	for line in buff:
		if 'Fatal' in line:
			ll = line.split(' ')
			signal = ll.index('signal') + 1
	# extract abort message then registers in the next lines



if __name__=='__main__':
	with open('log_example.txt') as fd:
		buff = fd.read()
	parse_logs(buff)