#!/usr/bin/python
# -*- coding: utf-8 -*-

#1.- Search apps in Google Play
#2.- Download them

import os
import subprocess

apps = []
api_dir = '/Users/radiactivo/Applications/googleplay-api/'

proc = subprocess.Popen(['python', api_dir + 'search.py', 'word'], stdout=subprocess.PIPE)

for line in iter(proc.stdout.readline,''):
   list1 = line.rstrip().split(';')
   apps.append(list1[1])

print apps

for app in apps:
	os.system('python ' + api_dir + 'download.py ' + app)

os.system('mv *.apk ~/Documents/TFM/apks/')