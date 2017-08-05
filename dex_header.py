#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import find
from config import dir_dexs, dir_mutated
import hashlib
import argparse
import hashlib
import zlib
import struct
from sys import exit

_MAGIC = '6465780a30333500'
_HEADER_SIZE = '70000000'
_ENDIAN_TAG = '78563412'

_hMAGIC = 'dex\n035\x00'
_hHEADER_SIZE = 'p\x00\x00\x00'
_hENDIAN_TAG = 'xV4\x12'

def update_checksum(filename, checksum):
	with open(filename, 'r+') as f:  
	    f.seek(8)
	    f.write( struct.pack('<I',checksum & 0xffffffff) )
	return checksum

def update_signature(filename, signature):
	with open(filename, 'r+') as f:
	    f.seek(12)
	    f.write( signature )
	return m.hexdigest()

def update_magic(filename):
	with open(filename, 'r+') as f:
		f.write(_hMAGIC)

def update_header_size(filename):
	with open(filename, 'r+') as f:
		f.seek(36)
		f.write(_hHEADER_SIZE)

def update_endian_tag(buff):
	with open(filename, 'r+') as f:
		f.seek(40)
		f.write(_hENDIAN_TAG)

def check_checksum(buff, current_checksum, filename):
	raw_checksum = zlib.adler32( buff[12:] )
	checksum = struct.pack('<I', raw_checksum & 0xffffffff)
	if checksum.encode('hex') == current_checksum:
		return None
	return checksum
		

def check_signature(buff, current_signature, filename):
	m = hashlib.sha1()
	m.update( buff[32:] )
	signature = m.digest()
	if signature.encode('hex') == current_signature:
		return None
	return signature
		

files = find('*.dex', dir_mutated)

for file in files:
	with open(file, 'rb') as fd:
		byte_stream = fd.read()

	dex_header = byte_stream[0:112]

	magic = dex_header[0:8].encode('hex')
	checksum = dex_header[8:12].encode('hex')
	signature = dex_header[12:32].encode('hex')
	file_size = dex_header[32:36].encode('hex')
	header_size = dex_header[36:40].encode('hex')
	endian_tag = dex_header[40:44].encode('hex')

	if magic != _MAGIC:
	 	print '[-] NOT SAME MAGIC HEADER IN {} [-]'.format(file.split('/')[-1])
	 	update_magic(file)
	
	if header_size != _HEADER_SIZE:
		print '[-] NOT SAME SIZE HEADER IN {} [-]'.format(file.split('/')[-1])
		update_header_size(file)

	if endian_tag != _ENDIAN_TAG:
		print '[-] NOT SAME ENDIAN TAG IN {} [-]'.format(file.split('/')[-1])
		update_endian_tag(file)

	with check_signature(byte_stream, signature, file) as result:
		if result != None:
			print '[-] INVALID SIGNATURE IN {} [-]'.format(file.split('/')[-1])
			update_signature(file, result)

	with check_checksum( byte_stream, checksum , file) as result:
		if result != None:
			print '[-] INVALID CHECKSUM IN {} [-]'.format(file.split('/')[-1])
			update_checksum(file, result)