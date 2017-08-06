#!/usr/bin/python
# -*- coding: utf-8 -*-

#1.- Search apps in Google Play
#2.- Download them

import os
import subprocess
from config import dir_api

apps = []
proc = subprocess.Popen(['python', '{}search.py'.format(dir_api), 'word'], stdout=subprocess.PIPE)

for line in iter(proc.stdout.readline,''):
   list1 = line.rstrip().split(';')
   apps.append(list1[1])

print apps

for app in apps:
	os.system('python {}download.py {}'.format(dir_api, app))

os.system('mv *.apk ~/Documents/TFM/apks/')