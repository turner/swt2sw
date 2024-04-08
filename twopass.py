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
import numpy as np
import h5py
from parser import create_command_line_parser
from utils import to_float
from header import create_header
from region_list import create_region_list, append_genomic_position_group_with_region_list, create_region_dictionary
from spatial_group import create_spatial_group

parser = create_command_line_parser()

try:
    arguments = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

b_time = time.time()

cndbf = h5py.File(arguments.cndb_filename + '.cndb', 'w')

spacewalk_file = arguments.spacewalk_file

region_dictionary = {}
indices = []

def harvest_xyz(xyz_list, sp_group, trace_group):
    xyz_stack = np.column_stack((xyz_list[1], xyz_list[2], xyz_list[3]))
    region_id = str(region_dictionary[xyz_list[0]])
    if 1 == xyz_stack.shape[0]:
        single_xyz_group_name = sp_group.name + '/single_xyz'
        if single_xyz_group_name not in cndbf:
            sp_group.create_group(single_xyz_group_name)
        single_xyz_group = cndbf[single_xyz_group_name]
        single_xyz_group.create_dataset(region_id, data=xyz_stack)

def create_spatial_positon_datasets(file, sp_group):
    xyz_list = None
    current_key = None
    trace_group = None
    single_xyz_group = None
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
                    harvest_xyz(xyz_list, sp_group, trace_group)
                current_key = key
                xyz_list = [current_key, [], [], []]

            xyz_list[1].append(to_float(tokens[3]))
            xyz_list[2].append(to_float(tokens[4]))
            xyz_list[3].append(to_float(tokens[5]))

    return [xyz_list, trace_group]

spacewalk_meta_data = create_header(cndbf, spacewalk_file)
root = cndbf.create_group(spacewalk_meta_data['name'])
frame = []
root.create_dataset('time', data=np.array(frame))

print('Converting {:} to CNDB file {:}'.format(arguments.spacewalk_file.name, cndbf.filename))

# discard: chromosome	start	end	x	y	z
dev_null = spacewalk_file.readline()

# First pass.
# Create genomic position dataset consisting of regions lists
region_list = create_region_list(spacewalk_file)
append_genomic_position_group_with_region_list(root, region_list)

# Build region dictionary
region_dictionary = create_region_dictionary(region_list)

# rewind file and reset file pointer
spacewalk_file.seek(0)
# discard: ##format=sw1 name=IMR90 genome=hg38
spacewalk_file.readline()
# discard: chromosome	start	end	x	y	z
spacewalk_file.readline()

# Second pass.
# Build spatial_position datasets
create_spatial_group(root, region_dictionary, spacewalk_file, arguments)

# spatial_position_group = root.create_group('spatial_position')
# result = create_spatial_positon_datasets(spacewalk_file, spatial_position_group)

# Harvest last genomic-extent of last trace
# harvest_xyz(result[0], result[1])

cndbf.close()

e_time = time.time()
elapsed = e_time - b_time
print('File conversion completed in %.3f seconds' % elapsed)
