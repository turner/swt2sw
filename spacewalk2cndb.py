#!/usr/bin/env python
#coding: utf8 

__description__ = \
"""
Converting *.sw to *.cndb format
"""

__author__ = "Douglass Turner"
__date__   = "Mar/2024"

################################################################
# 
# Trajectories file *.sw to Compacted Nucleome Data Bank format .cndb
#
# usage:
#  ./ndb2cndb.py -f file.ndb -n name_CNDB_file
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
    print('################################################')
    print('Chosen file: {:}'.format(arguments.f.name))

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
    'info' : 'Encode',
    'title': 'The Nucleome Data Bank: Web-based Resources Simulate and Analyze the Three-Dimensional Genome',
    'expdta' : '',
    'author' : 'Antonio B Oliveira Junior',
    'cycle' : '',
    'date' : str(datetime.now()),
    'chains' : ''
    }

    hash.update(spacewalkMetaData)

    return hash

loop = 0
types = []
frame = []
inFrame = False
chromosome = None
x, y, z = None, None, None
traceLength = None
dataset = None
traceXYZGroup = None
genomicExtents = {}
counter = 0
currentKey = None
traceDictionary = None
dictionary = {}
regions = []
indices = []

def harvestXYZ(index):
    if dictionary:

        i = str(index - 1)
        # Harvest XYZ
        print('harvest trace ' + i)

        trace_group = spatialPosition.create_group(i)

        def is_xyz(key):
            something = dictionary[key]
            return 0 != len(something[0])

        filtered_keys = list(filter(is_xyz, dictionary.keys()))

        def is_ball_and_stick(key):
            something = dictionary[key]
            return 1 == len(something[0])

        ball_and_stick_keys = list(filter(is_ball_and_stick, dictionary.keys()))

        if len(filtered_keys) == len(ball_and_stick_keys):
            # We have a ball & stick data file, we will only create a centroid dataset
            x = []
            y = []
            z = []
            for key in filtered_keys:
                value = dictionary[key]
                x.append(value[0])
                y.append(value[1])
                z.append(value[2])
            xyz_stack = np.column_stack((x, y, z))
            trace_group.create_dataset('centroid', data=xyz_stack)
        else:
            for key in filtered_keys:
                value = dictionary[key]
                xyz_stack = np.column_stack((value[0], value[1], value[2]))
                trace_group.create_dataset(value[3], data=xyz_stack)

        # Empty array in preparation for harvesting xyz and region-id from next trace.
        # Do NOT discard pre-existing region counters because we want to preserve the
        # region ids across trace accumulations. The is ONE global region id list.
        for key in dictionary.keys():
            dictionary[key][0] = []
            dictionary[key][1] = []
            dictionary[key][2] = []

def traverseTrackList(file):
    chromosome = None

    regionCounter = 0

    for line in file:
        tokens = line.split()
        if 'trace' == tokens[0]:
            token_index = int(tokens[1])
            if 59 == token_index:
                print('token-index ' + str(token_index))

            indices.append(token_index)
            harvestXYZ(indices[-1])

        elif 6 == len(tokens):
            if chromosome is None:
                chromosome = tokens[0]

            key = chromosome + '%' + tokens[1] + '%' + tokens[2]

            # Harvest xyz and region-id into dictionary. The dictionary will be
            # processed into the cndb file - genomic and xyz datasets - after
            # the entire trace is traversed
            if key not in dictionary.keys():
                regions.append('region-' + str(regionCounter))
                regionCounter += 1
                dictionary[key] = [[], [], [], regions[-1]]

            dictionary[key][0].append(to_float(tokens[3]))
            dictionary[key][1].append(to_float(tokens[4]))
            dictionary[key][2].append(to_float(tokens[5]))

name = arguments.arg_name
cndbf = h5py.File(name + '.cndb', 'w')

header = cndbf.create_group('Header')
metaData = initializeHeader(spacewalkFile, spacewalkMetaData)
header.attrs.update(metaData)

print('Converting file...')

# discard: chromosome	start	end	x	y	z
dev_null = spacewalkFile.readline()

root = cndbf.create_group(spacewalkMetaData['name'])

spatialPosition = root.create_group('spatial_position')

# traverse trace list, harvest xyz lists, and build region list
traverseTrackList(spacewalkFile)

# harvest last trace
harvestXYZ(1 + indices[-1])

# create genomic position dataset consisting of the list of regions
genomicPosition = root.create_group('genomic_position')

# simplify dictionary
for key in dictionary.keys():
    value = dictionary[key]
    dictionary[key] = value[3]

# region dictionary is the dictionary inverted
region_dictionary = {value: key for key, value in dictionary.items()}

# add regions list to genomicPosition as a dataset
region_items = []
for key, value in region_dictionary.items():
    region_items.append(value + '%' + key)

genomicPosition.create_dataset('regions', data=region_items, dtype=h5py.string_dtype(encoding='utf-8'))

root.create_dataset('time', data=np.array(frame))

cndbf.close()

print('Finished!')

e_time = time.time()
elapsed = e_time - b_time
print('Ran in %.3f sec' % elapsed)
