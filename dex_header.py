#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import find
from config import dir_dexs, dir_mutated
import hashlib
import argparse
import hashlib
import zlib
import struct

def update_signature(filename):
    f = open(filename,'r+')
    data = f.read()[32:]
    m = hashlib.sha1()
    m.update(data)
    signature = m.digest()
    f.seek(12)
    f.write(signature)
    f.close()
    return m.hexdigest()

def update_checksum(filename):
    
    f = open(filename,'r+')
    data = f.read()[12:]
    checksum = zlib.adler32(data)
    f.seek(8)
    f.write(struct.pack('<I',checksum & 0xffffffff))
    f.close()

    return checksum

_MAGIC = '6465780a30333500'
_HEADER_SIZE = '70000000'
_ENDIAN_TAG = '78563412'

files = find('*.dex', dir_dexs)

def reconstruct_header(buff):
	pass

for file in files:

	with open(file, 'rb') as fd:
		byte_stream = fd.read(112)

	magic = byte_stream[0:8].encode('hex')
	checksum = byte_stream[8:12].encode('hex')
	signature = byte_stream[12:32].encode('hex')
	file_size = byte_stream[32:36].encode('hex')
	header_size = byte_stream[36:40].encode('hex')
	endian_tag = byte_stream[40:44].encode('hex')

	print magic
	print checksum
	print signature
	print file_size
	print header_size
	print endian_tag

	# if magic != _MAGIC:
	# 	print '[-] NOT SAME MAGIC HEADER IN {} [-]'.format(file.split('/')[-1])
	
	# if header_size != _HEADER_SIZE:
	# 	print '[-] NOT SAME SIZE HEADER IN {} [-]'.format(file.split('/')[-1])
	
	# if endian_tag != _ENDIAN_TAG:
	# 	print '[-] NOT SAME ENDIAN TAG IN {} [-]'.format(file.split('/')[-1])
	# else:
	# 	print '[+] SAME ENDIANG TAG [+]'

