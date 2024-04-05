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

name = arguments.arg_name
cndbf = h5py.File(name + '.cndb', 'w')

spacewalkFile = arguments.f
spacewalkMetaData = {}
def initialize_header(spacewalkFile, spacewalkMetaData):
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
def create_region_list(file):

    hash = {}
    for line in file:
        tokens = line.split()
        if 6 == len(tokens):
            key = tokens[0] + '%' + tokens[1] + '%' + tokens[2]
            if key not in hash.keys():
                hash[key] = [tokens[0], int(tokens[1]), int(tokens[2])]

    # Build sorted region list
    result = list(map(lambda string: string.split('%'), list(hash.keys())))

    return result

def harvest_xyz(xyz_list, tr_group):
    xyz_stack = np.column_stack((xyz_list[1], xyz_list[2], xyz_list[3]))
    region_id = str(region_dictionary[xyz_list[0]])

    if len(xyz_list[1]) > 1:
        candidate_name = tr_group.name + '/' + region_id
        stmt = 'harvest xyz for dataset(' + candidate_name + ')'
        print(stmt)
        if candidate_name in cndbf:
            dataset = cndbf[candidate_name]
            dataset_size = dataset.shape[0]
            xyz_size = xyz_stack.shape[0]
            new_size = dataset_size + xyz_size
            dataset.resize(new_size, axis=0)
            dataset[-xyz_stack.shape[0]:] = xyz_stack
        else:
            tr_group.create_dataset(region_id, data=xyz_stack, maxshape=(None,3))
    else:
        candidate_name = tr_group.name + '/centroid'
        if candidate_name in cndbf:
            dataset = cndbf[candidate_name]
            dataset_size = dataset.shape[0]
            xyz_size = xyz_stack.shape[0]
            new_size = dataset_size + xyz_size
            dataset.resize(new_size, axis=0)
            dataset[-xyz_stack.shape[0]:] = xyz_stack
        else:
            tr_group.create_dataset('centroid', data=xyz_stack, maxshape=(None, 3))
def create_spatial_positon_datasets(file, sp_group):
    xyz_list = None
    current_key = None
    trace_group = None
    for line in file:
        tokens = line.split()
        if 'trace' == tokens[0]:
            indices.append(int(tokens[1]))
            trace_group_name = str(indices[-1])
            trace_group = sp_group.create_group(trace_group_name)
        elif 6 == len(tokens):
            key = '%'.join([tokens[0], tokens[1], tokens[2]])
            if current_key != key:
                if xyz_list is not None:
                    harvest_xyz(xyz_list, trace_group)
                current_key = key
                xyz_list = [current_key, [], [], []]

            xyz_list[1].append(to_float(tokens[3]))
            xyz_list[2].append(to_float(tokens[4]))
            xyz_list[3].append(to_float(tokens[5]))

    return [xyz_list, trace_group]

region_dictionary = {}
indices = []

header = cndbf.create_group('Header')
metaData = initialize_header(spacewalkFile, spacewalkMetaData)
header.attrs.update(metaData)

print('Converting {:}'.format(arguments.f.name))

# discard: chromosome	start	end	x	y	z
dev_null = spacewalkFile.readline()

root = cndbf.create_group(spacewalkMetaData['name'])

frame = []
root.create_dataset('time', data=np.array(frame))

# First pass.
# Create genomic position dataset consisting of regions lists
region_list = create_region_list(spacewalkFile)
genomicPosition = root.create_group('genomic_position')
genomicPosition.create_dataset('regions', data=region_list)

# Build region dictionary
for region in region_list:
    key = region[0] + '%' + region[1] + '%' + region[2]
    region_dictionary[key] = region_list.index(region)

# Second pass.
# Build spatial_position datasets
spacewalkFile.seek(0)

# discard: ##format=sw1 name=IMR90 genome=hg38
spacewalkFile.readline()
# discard: chromosome	start	end	x	y	z
spacewalkFile.readline()

spatial_position_group = root.create_group('spatial_position')
result = create_spatial_positon_datasets(spacewalkFile, spatial_position_group)

# Harvest last genomic-extent of last trace
harvest_xyz(result[0], result[1])

cndbf.close()

e_time = time.time()
elapsed = e_time - b_time
print('File conversion completed in %.3f seconds' % elapsed)
