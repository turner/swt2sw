#!/usr/bin/env python
#coding: utf8 

__description__ = \
    """
    Converting *.sw to *.swb format
    """

__author__ = "Douglass Turner"
__date__   = "3 April 2024"

################################################################
# 
# Convert Spacewalk files from text (.sw) to HDF5 (.swb)
#
# usage:
#  ./sw2swb.py -f spacewalk_filename.sw -n swb_filename
#
################################################################

import time
import numpy as np
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

    swbf = h5py.File(arguments.swb_filename + '.swb', 'w')

    spacewalk_file = arguments.spacewalk_file

    header_group, spacewalk_meta_data = create_header(swbf, spacewalk_file)
    root = swbf.create_group(spacewalk_meta_data['name'])
    frame = []
    root.create_dataset('time', data=np.array(frame))

    print('Converting {:} to swb file {:}'.format(arguments.spacewalk_file.name, swbf.filename))

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
    create_spatial_group(root, region_dictionary, spacewalk_file, arguments, header_group)

    swbf.close()

    e_time = time.time()
    elapsed = e_time - b_time
    print('File conversion completed in %.3f seconds' % elapsed)

if __name__ == '__main__':
    main()
