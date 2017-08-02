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

def update_magic(filename):
	f = open(filename,'r+')
	f.write(_hMAGIC)
	f.close()

def update_header_size(filename):
	f = open(filename,'r+')
	f.seek(36)
	f.write(_hHEADER_SIZE)
	f.close()

def update_endian_tag(buff):
	f = open(filename,'r+')
	f.seek(40)
	f.write(_hENDIAN_TAG)
	f.close()

files = find('*.dex', dir_mutated)

for file in files:
	with open(file, 'rb') as fd:
		byte_stream = fd.read(112)

	magic = byte_stream[0:8].encode('hex')
	checksum = byte_stream[8:12].encode('hex')
	signature = byte_stream[12:32].encode('hex')
	file_size = byte_stream[32:36].encode('hex')
	header_size = byte_stream[36:40].encode('hex')
	endian_tag = byte_stream[40:44].encode('hex')

	if magic != _MAGIC:
	 	print '[-] NOT SAME MAGIC HEADER IN {} [-]'.format(file.split('/')[-1])
	 	update_magic(file)
	
	if header_size != _HEADER_SIZE:
		print '[-] NOT SAME SIZE HEADER IN {} [-]'.format(file.split('/')[-1])
		update_header_size(file)

	if endian_tag != _ENDIAN_TAG:
		print '[-] NOT SAME ENDIAN TAG IN {} [-]'.format(file.split('/')[-1])
		update_endian_tag(file)
