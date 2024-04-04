#!/usr/bin/env python
#coding: utf8 

__description__ = \
    """
    Converting *.sw to *.cndb format
    """

__author__ = "Douglass Turner"
__date__   = "3 April 2024"

################################################################
# 
# Convert Spacewalk files (.sw) to Compacted Nucleome Data Bank format (.cndb)
#
# usage:
#  ./spacewalk2cndb.py -f spacewalk_file.sw -n cndb_file_name
#
################################################################

import time
import argparse
import numpy as np
import h5py
from datetime import datetime

parser = argparse.ArgumentParser(description='Converting *.sw to *.cndb format')
parser.add_argument('-f', metavar='input-file-ndb-frames',help='sw file with frames',type=argparse.FileType('rt'))
parser.add_argument('-n', action='store', default='chromatin', dest='arg_name',  help='Name of output file')

try:
    arguments = parser.parse_args()

except IOError as msg:
    parser.error(str(msg))

def to_float(value):
    try:
        return float(value)
    except ValueError:  # This will catch cases where the conversion fails, e.g., if value is 'nan'
        return float(0)

b_time = time.time()

spacewalkFile = arguments.f
spacewalkMetaData = {}
def initializeHeader(spacewalkFile, spacewalkMetaData):
    first_line = spacewalkFile.readline().strip()
    entries = None
    if first_line.startswith('#'):
        entries = first_line[2:].split()  #[2:] because have ##

    for entry in entries:
        key, value = entry.split('=')
        spacewalkMetaData[key] = value

    hash = {
        'version' : '1.0.0',
        'author' : 'Douglass Turner',
        'date' : str(datetime.now())
    }

    hash.update(spacewalkMetaData)

    return hash

dictionary = {}

def build_region_list(file):
    for line in file:
        tokens = line.split()
        if 6 == len(tokens):
            key = tokens[0] + '%' + tokens[1] + '%' + tokens[2]
            if key not in dictionary.keys():
                dictionary[key] = [tokens[0], int(tokens[1]), int(tokens[2])]

name = arguments.arg_name
cndbf = h5py.File(name + '.cndb', 'w')

header = cndbf.create_group('Header')
metaData = initializeHeader(spacewalkFile, spacewalkMetaData)
header.attrs.update(metaData)

print('Converting {:}'.format(arguments.f.name))

# discard: chromosome	start	end	x	y	z
dev_null = spacewalkFile.readline()

root = cndbf.create_group(spacewalkMetaData['name'])

frame = []
root.create_dataset('time', data=np.array(frame))

build_region_list(spacewalkFile)

region_list = list(map(lambda string: string.split('%'), list(dictionary.keys())))

# create genomic position dataset consisting of the list of regions
genomicPosition = root.create_group('genomic_position')
genomicPosition.create_dataset('regions', data=region_list)

cndbf.close()

e_time = time.time()
elapsed = e_time - b_time
print('File conversion completed in %.3f seconds' % elapsed)
