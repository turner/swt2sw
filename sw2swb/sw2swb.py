#!/usr/bin/env python
#coding: utf8 

__description__ = \
    """
    Convert Spacewalk files from text (.swt) to HDF5 (.sw)
    """

__author__ = "Douglass Turner"
__date__   = "3 April 2024"

################################################################
# 
# Convert Spacewalk files from text (.swt) to HDF5 (.sw)
#
#
################################################################

import time
import h5py
from .parser import create_command_line_parser
from .header import create_header
from .region_list import create_region_list, append_genomic_position_group_with_region_list, create_region_dictionary
from .spatial_group import create_spatial_group

def main():
    parser = create_command_line_parser()

    try:
        arguments = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    b_time = time.time()

    swbf = h5py.File(arguments.swb_filename + '.sw', 'w')

    spacewalk_file = arguments.spacewalk_file

    header_group, spacewalk_meta_data = create_header(swbf, spacewalk_file)
    root = swbf.create_group(spacewalk_meta_data['name'])

    print('Converting {:} to swb file {:}'.format(arguments.spacewalk_file.name, swbf.filename))

    # discard: chromosome	start	end	x	y	z
    spacewalk_file.readline()

    # First pass.
    # Create genomic position dataset consisting of regions lists
    region_list = create_region_list(spacewalk_file)
    append_genomic_position_group_with_region_list(root, region_list)

    # Build region dictionary
    region_dictionary = create_region_dictionary(region_list)

    # rewind file and reset file pointer to prepare for second pass over file
    spacewalk_file.seek(0)
    # discard: ##format=sw1 name=IMR90 genome=hg38
    spacewalk_file.readline()
    # discard: chromosome	start	end	x	y	z
    spacewalk_file.readline()

    # Second pass.
    # Build spatial_position datasets
    create_spatial_group(root, region_dictionary, spacewalk_file, arguments, header_group)

    swb_filename = swbf.filename

    swbf.close()

    try:
        import hdf5_indexer
        print('indexing {:}...'.format(swb_filename))
        hdf5_indexer.make_index(swb_filename)
        print('done')
    except ImportError:
        print('{:} was not indexed. Could not import module hdf5_indexer'.format(swbf.filename))

    e_time = time.time()
    elapsed = e_time - b_time
    print('File conversion completed in %.3f seconds' % elapsed)

if __name__ == '__main__':
    main()
