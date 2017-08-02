from os import listdir
import os
import sys
import subprocess
import re
import time
import fnmatch
import vobject

from config import dir_project, dir_fuzzdb_atack

def run_subproc(cmd):
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

def flush_log(device_id):
    cmd = 'adb -s ' + (str)(device_id) + ' logcat -c'
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

def find(pattern, path):
    result = [] 
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def import_vcf(filename):
    if dir_project not in filename:
        return None
    with open(filename, 'r') as f:
        buf = f.read()
    return vobject.readOne( buf )

def extract_random_strings():
    files = find('*.txt', dir_fuzzdb_atack)
    for files in files:
        with open(file, 'r') as fd:
            str_list.append(fd.readlines())
    return str_list

def read_json(filename):
    pass

if __name__=='__main__':
    read_json()
