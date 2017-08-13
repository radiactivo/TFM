#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import find, update_buffer
from config import dir_samples, dir_mutated
from hashlib import sha1
from zlib import adler32
from struct import pack
from sys import exit

_MAGIC = '6465780a30333500'
_HEADER_SIZE = '70000000'
_ENDIAN_TAG = '78563412'

_hMAGIC = 'dex\n035\x00'
_hHEADER_SIZE = 'p\x00\x00\x00'
_hENDIAN_TAG = 'xV4\x12'

# from dex_header import fix_header
# fix_header('/Users/radiactivo/Documents/TFM/scripts/fuzzed_1.dex')

def update_checksum(filename, checksum):
	with open(filename, 'r+') as f:  
	    f.seek(8)
	    f.write( checksum )
	return checksum

def update_signature(filename, signature):
	with open(filename, 'r+') as f:
	    f.seek(12)
	    f.write( signature )
	return signature

def update_file_size(filename, file_size):
	with open(filename, 'r+') as f:
		f.seek(32)
		f.write(file_size)	

def update_magic(filename):
	with open(filename, 'r+') as f:
		f.write(_hMAGIC)

def update_header_size(filename):
	with open(filename, 'r+') as f:
		f.seek(36)
		f.write(_hHEADER_SIZE)

def update_endian_tag(filename):
	with open(filename, 'r+') as f:
		f.seek(40)
		f.write(_hENDIAN_TAG)

def check_checksum(buff, current_checksum):
	raw_checksum = adler32( buff[12:] )
	checksum = pack('<I', raw_checksum & 0xffffffff)
	if checksum.encode('hex') == current_checksum:
		return None
	return checksum
		
def check_signature(buff, current_signature):
	m = sha1()
	m.update( buff[32:] )
	signature = m.digest()
	if signature.encode('hex') == current_signature:
		return None
	return signature

def check_file_size(buff, current_file_size):
	size = len(buff)
	file_size = pack('<I', size & 0xffffffff) 
	if file_size.encode('hex') == current_file_size:
		return None
	return file_size

def fix_header(filename):
	
	with open(filename, 'rb') as fd:
			byte_stream = fd.read()

	dex_header = byte_stream[0:112]

	magic = dex_header[0:8].encode('hex')
	checksum = dex_header[8:12].encode('hex')
	signature = dex_header[12:32].encode('hex')
	file_size = dex_header[32:36].encode('hex')
	header_size = dex_header[36:40].encode('hex')
	endian_tag = dex_header[40:44].encode('hex')

	changes = False;

	if endian_tag != _ENDIAN_TAG:
		print '[-] NOT SAME ENDIAN TAG IN {} [-]'.format(filename.split('/')[-1])
		update_endian_tag(filename)
		dex_header = update_buffer(40, dex_header, _hENDIAN_TAG)
		changes = True

	if header_size != _HEADER_SIZE:
		print '[-] NOT SAME SIZE HEADER IN {} [-]'.format(filename.split('/')[-1])
		update_header_size(filename)
		dex_header = update_buffer(36, dex_header, _hHEADER_SIZE)
		changes = True

	if magic != _MAGIC:
	 	print '[-] NOT SAME MAGIC HEADER IN {} [-]'.format(filename.split('/')[-1])
	 	update_magic(filename)
		dex_header = update_buffer(0, dex_header, _hMAGIC)
		changes = True

	result = None	
	result = check_file_size( byte_stream, file_size )
	
	if result != None:
		print '[-] INVALID FILE SIZE IN {} [-]'.format(filename.split('/')[-1])
		update_file_size(filename, result)
		dex_header = update_buffer(32, dex_header, result)
		changes = True

	if changes: 
		byte_stream = update_buffer(0, byte_stream, dex_header)
		changes = False

	result = None
	result = check_signature( byte_stream, signature )
	if result != None:
		print '[-] INVALID SIGNATURE IN {} [-]'.format(filename.split('/')[-1])
		update_signature(filename, result)
		dex_header = update_buffer(12, dex_header, result)
		if not changes: changes = True

	if changes: 
		byte_stream = update_buffer(0, byte_stream, dex_header)
		changes = False

	result = None
	result = check_checksum( byte_stream, checksum )
	if result != None:
		print '[-] INVALID CHECKSUM IN {} [-]'.format(filename.split('/')[-1])
		update_checksum(filename, result)
		dex_header = update_buffer(8, dex_header, result)

def main():
	files = find('*.dex', dir_mutated)

	for file in files:
		fix_header(file)

if __name__=='__main__':
	main()