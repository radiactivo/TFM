#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import dir_project, dir_samples, dir_dexs, seeds, filename_dictionary_samples_dat, filename_dictionary_samples_json, dir_mutated
import os, fnmatch
from utils import find, fuzz_stream, fuzz_stream_seed, load_dict, json_load, dump_dict, dump_json, add_hash_seed, extract_fuzzdb_strings
import vobject
import pdb
from base64 import b64encode, b64decode
import subprocess
from random import randint

def extract_dex():
	######	DEX2OAT SAMPLE EXTRACTOR
	sample_num = 0
	apks = find('*.apk', dir_samples)

	for apk in apks:
		apk_folder = apk[0:len(apk) - 4] + '/'
		os.system('unzip {} -d {}'.format(apk, apk_folder))
		dex_files = find('*.dex', apk_folder)
		if len(dex_files) == 0:
			print '[-] No dex class on: {}'.format(apk_folder)
		else:
			for dex_file in dex_files:
				os.system('mv {} {}sample_{}.dex'.format(dex_file, dir_samples, str(sample_num)))
				sample_num +=1
		os.system('sudo rm -rf ' + apk_folder)

def dex2oat_sample_generator():
	samples_dic =  load_dict(filename_dictionary_samples_dat)

	#FUZZED GENERATOR
	dexs = find('*.dex', dir_samples)
	fuz_num = 0
	for dex in dexs:
		for seed in seeds[180:200]:
			fuzzed_filename = '{}fuzzed_{}.dex'.format( dir_mutated, str(fuz_num) )
			os.system( 'radamsa -s {} {} >> {}'.format( str(seed), dex, fuzzed_filename) )
			add_hash_seed( samples_dic, dex, fuzzed_filename, str(seed) )
			fuz_num += 1
			print fuz_num

	dump_dict(samples_dic, filename_dictionary_samples_dat)
	dump_json(samples_dic, filename_dictionary_samples_json)


def contact_sample_generator():
	samples_dic =  load_dict(filename_dictionary_samples_dat)

	files = find('*.vcf', dir_samples)
	fuz_num = 0
	for file in files:
		for seed in seeds:
			fuzzed_filename = '{}fuzzed_{}.vcf'.format( dir_mutated, str(fuz_num) )
			os.system( 'radamsa -s {} {} >> {}'.format( str(seed), file, fuzzed_filename ))
			add_hash_seed( sample_dic, file, fuzzed_filename, str(seed) )
			fuz_num += 1

	dump_dict(samples_dic, filename_dictionary_samples_dat)
	dump_json(samples_dic, filename_dictionary_samples_json)

def vcard_generate():
	j = vobject.vCard()
	o = j.add('fn')
	j.fn.value = "Meiner Einer"

	o = j.add('n')
	j.n.value = vobject.vcard.Name( family='Einer', given='Meiner' )

	o = j.add('tel')
	j.add('tel').type_param = "cell"
	j.add('tel').value = '+321 987 654321'

	j.add('tel').type_param = "work"
	j.add('tel').value = '+01 88 77 66 55'
	
	j.add('tel').type_param = "home"
	j.add('tel').value = '+49 181 99 00 00 00'

	o = j.add('bday')
	j.bday.value = '1963-09-21'

	o = j.add('org')
	j.org.value = 'Comapny Inc.;Dick Department'

	o = j.add('email')
	j.email.value = 'wololo@mail.com'

	with open('currencio.vcf', 'a') as fd:
		fd.write(j.serialize())

	return j

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

def contact_smart_generator():
	samples_dic =  load_dict(filename_dictionary_samples_dat)

	files = find('*.vcf', dir_samples)
	fuzzdb_strings = extract_fuzzdb_strings()

	fuzzed_counter = 0
	count = 0
	for file in files:
		with open(file, 'r') as fd:
			buff = fd.read()
		vCard = buff.split()
		
		for e in vCard:
		    if 'BEGIN' not in e and 'VERSION' not in e and 'END' not in e:
		            vCard[vCard.index(e)] = '{}:{}'.format(e.split(':')[0], fuzzdb_strings[count])
		    count += 1

		fuzzed_filename = '{}fuzzed_{}.vcf'.format(dir_mutated, fuzzed_counter)
		with open(fuzzed_filename, 'a') as fd:
			for line in vCard:
				fd.write( '{}\n'.format(line) )

		add_hash_seed( samples_dic, file, fuzzed_filename, fuzzdb_strings[count] )
		fuzzed_counter += 1

	dump_dict(samples_dic, filename_dictionary_samples_dat)
	dump_json(samples_dic, filename_dictionary_samples_json)

	return samples_dic

def contact_binary_generator():
	samples_dic =  load_dict( filename_dictionary_samples_dat )

	files = find( '*.vcf', dir_samples )
	fuzzdb_strings = extract_fuzzdb_strings()

	fuzzed_counter = 0
	count = 0
	for file in files:
		with open( file, 'r' ) as fd:
			buff = fd.read()
		vCard = buff.split()
		
		for e in vCard:
		    if 'BEGIN' not in e and 'VERSION' not in e and 'END' not in e and 'PHOTO' not in e:
		        vCard[vCard.index(e)] = '{}:{}'.format( e.split(':')[0], fuzzdb_strings[count] )
		    	count += 1
		    elif 'PHOTO' in e:
		    	raw_photo = b64decode( e.split(':')[-1] )
		    	r = subprocess.Popen( ['radamsa'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE )
		    	raw_fuzzed_photo = r.communicate( raw_photo )[0]
		    	vCard[vCard.index(e)] = '{}:{}'.format( e.split(':')[0], b64encode( raw_fuzzed_photo ))

		fuzzed_filename = '{}fuzzed_{}.vcf'.format(dir_mutated, fuzzed_counter)
		with open( fuzzed_filename, 'wb' ) as fd:
			for line in vCard:
				fd.write( '{}\n'.format( line ))

		add_hash_seed( samples_dic, file, fuzzed_filename, fuzzdb_strings[count] )
		fuzzed_counter += 1

	dump_dict( samples_dic, filename_dictionary_samples_dat )
	dump_json( samples_dic, filename_dictionary_samples_json )

	return samples_dic

def contact_fuzzdb_generator():
	with open( 'vcard.vcf', 'r' ) as fd:
		buff = fd.read()
	vCard = buff.split()
	fuzzdb_strings = extract_fuzzdb_strings()

	with open( 'images.txt', 'r') as fd:
		imgs = fd.read().split('\n')

	card_counter = 0
	i=0
	while i < len(fuzzdb_strings):
		j=2
		while j < len(vCard) - 1:
			if 'PHOTO' not in vCard[j]:
				vCard[j] = '{}:{}'.format( vCard[j].split(':')[0],  fuzz_stream( fuzzdb_strings[i] ))
				i+=1
			else:
				vCard[j] = '{}:{}'.format( vCard[j],  b64encode( fuzz_stream( b64decode( imgs[randint(0,len(imgs) -1 )] ))))
			j+=1
			if i == len(fuzzdb_strings) - 1: break

		with open('{}fuzzed{}.vcf'.format(dir_mutated, card_counter), 'a') as f:
			for line in vCard:
				f.write('{}\n'.format(line))
		card_counter += 1
			

if __name__=='__main__':
	contact_fuzzdb_generator()
	#vcard_generate()
	#contact_smart_generator()
	#dex2oat_sample_generator()		