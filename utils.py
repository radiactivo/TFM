#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
import os
import sys
import subprocess
import re
import time
import fnmatch
import vobject
import json
import hashlib
import pickle
import pdb
from sys import exit
from time import time
from datetime import datetime
from tzlocal import get_localzone
import StringIO

from config import dir_project, dir_fuzzdb_attack

def run_subproc(cmd):
    r = subprocess.Popen([cmd], shell=True)
    r.wait()
    
def run_subprocess(cmd):
    r = subprocess.Popen([cmd], shell=True)
    return r

def flush_log(device_id):
    cmd = 'adb -s {} logcat -c'.format((str)(device_id))
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

def find(pattern, path):
    result = [] 
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def update_buffer(index, wbuff, rbuff):
    a = StringIO.StringIO(wbuff)
    a.seek(index)
    a.write(rbuff)
    buff = a.getvalue()
    a.close()
    return buff

def fuzz_stream( byte_stream_sample ):
    r = subprocess.Popen( ['radamsa'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE )
    ans = r.communicate( byte_stream_sample )[0]
    try:
        r.kill()
    except:
        pass
    return ans

def fuzz_stream_seed( byte_stream_sample, seed ):
    r = subprocess.Popen( ['radamsa', '-s', seed], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE )
    ans = r.communicate( byte_stream_sample )[0]
    try:
        r.kill()
    except:
        pass
    return ans

def dump_dict(dictionary, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(dictionary, handle)

def load_dict(filename):
    with open(filename, 'rb') as handle:
        dictionary = pickle.loads(handle.read())
    return dictionary

def generate_timestamp():
    return int(time())

def timestamp_to_datetime(timestamp):
    local_tz = get_localzone()
    return local_tz.localize(datetime.fromtimestamp(timestamp))

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def import_vcf(filename):
    if dir_project not in filename:
        return None
    with open(filename, 'r') as f:
        buf = f.read()
    return vobject.readOne( buf )

def extract_fuzzdb_strings():
    str_list = []
    files = find('*.txt', dir_fuzzdb_attack)
    for filename in files:
        with open(filename, 'r+') as fd:
            list_to_append = fd.readlines()
        list_to_append = [x.strip() for x in list_to_append]
        for line in list_to_append:
            str_list.append( line )
    return str_list

def add_hash_seed(sample_dic, original_filename, fuzzed_filename, seed):
    sample_dic[md5(original_filename)][md5(fuzzed_filename)] = seed
    return sample_dic

def json_load(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data

def dump_json(dictionary, filename):
    with open(filename, 'w') as f:
        json.dump(dictionary, f, sort_keys=True, indent=4)

if __name__=='__main__':
    pass
