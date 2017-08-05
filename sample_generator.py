#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import dir_project, dir_samples, dir_dexs, seeds, filename_dictionary_samples, dir_mutated
import os, fnmatch
from utils import *
import pdb

def dex2oat_sample_generator():

	#######	DEX2OAT SAMPLE EXTRACTOR
	log = dir_project + 'logs/sample_generator_log'
	samples_dic =  load_dict(filename_dictionary_samples)

	f = open(log, 'w')

	# #DEX EXTRACTOR
	sample_num = 0
	apks = find('*.apk', dir_samples)

	for apk in apks:
		apk_folder = apk[0:len(apk) - 4] + '/'
		os.system('unzip ' + apk + ' -d ' + apk_folder)
		dex_files = find('*.dex', apk_folder)
		if len(dex_files) == 0:
			print '[-] No dex class on: ' + apk_folder
		else:
			for dex_file in dex_files:
				os.system('mv ' + dex_file + ' ' + dir_dexs + 'sample_' + str(sample_num) + '.dex')
				sample_num +=1
				f.write( dex_file + ';' + 'sample_' + str(sample_num) )
		os.system('sudo rm -rf ' + apk_folder)

	#FUZZED GENERATOR
	dexs = find('*.dex', dir_dexs)
	fuz_num = 0
	for dex in dexs:
		for seed in seeds:
			fuzzed_filename = '{}fuzzed_{}.dex'.format( dir_mutated, str(fuz_num) )
			os.system( 'radamsa -s {} {} >> {}'.format( str(seed), dex, fuzzed_filename) )
			add_hash_seed( samples_dic, dex, fuzzed_filename, str(seed) )
			fuz_num += 1
			print fuz_num

	dump_dict(samples_dic, filename_dictionary_samples)
	dump_json(samples_dic, filename_dictionary_samples)
	f.close()

def contact_sample_generator():
	samples_dic =  load_dict(filename_dictionary_samples)

	files = find('*.vcf', dir_samples)
	fuz_num = 0
	for file in files:
		for seed in seeds:
			fuzzed_filename = '{}fuzzed_{}.vcf'.format( dir_mutated, str(fuz_num) )
			os.system( 'radamsa -s {} {} >> {}'.format( str(seed), file, fuzzed_filename ))
			add_hash_seed( sample_dic, file, fuzzed_filename, str(seed) )
			fuz_num += 1

	dump_dict(samples_dic, filename_dictionary_samples)
	dump_json(samples_dic, filename_dictionary_samples)

def vcard_generate():
	pass

def extract_vcf_from_sample(sample):
	#sample = '/Users/radiactivo/Desktop/1 y otras 175.vcf'

	with open(sample, 'r') as fd:
		buff = fd.readlines()

	previous_point = 0
	sample_counter = 0
	for x in range(0, len(buff)):
		if 'END:' in buff[x]:
			gen_sample = '{}sample_{}.vcf'.format(dir_samples, str(sample_counter))
			with open(gen_sample, 'a') as fd:
				fd.writelines(buff[previous_point:x + 1])
			previous_point = x + 1
			sample_counter += 1

def contact_sample_smart_generator():
	files = find('*.vcf', dir_samples)
	random_strings = extract_random_strings()

	for file in files:
		for seed in seeds:
			vCard = import_vcf(file)
			key_list = vCard.contents.keys()
			for key in key_list:
				
			pdb.set_trace()

	#for seed in seeds:


	# random_strings = extract_random_strings()
	# import vobject

	# j = vobject.vCard()
	# o = j.add('fn')
	# j.fn.value = "Meiner Einer"

	# o = j.add('n')
	# j.n.value = vobject.vcard.Name( family='Einer', given='Meiner' )

	# o = j.add('tel')
	# j.add('tel').type_param = "cell"
	# j.add('tel').value = '+321 987 654321'

	# j.add('tel').type_param = "work"
	# j.add('tel').value = '+01 88 77 66 55'
	
	# j.add('tel').type_param = "home"
	# j.add('tel').value = '+49 181 99 00 00 00'

	# o = j.add('bday')
	# j.bday.value = '1963-09-21'

	# o = j.add('org')
	# j.org.value = 'Comapny Inc.;Dick Department'

	# o = j.add('email')
	# j.email.value = 'wololo@mail.com'

	# with open('currencio.vcf', 'a') as fd:
	# 	fd.write(j.serialize())

	#return j

if __name__=='__main__':
	contact_sample_smart_generator()
			