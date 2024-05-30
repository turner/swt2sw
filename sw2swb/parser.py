import argparse
def create_command_line_parser():
    parser = argparse.ArgumentParser(description='Convert text-based *.swt file to binary HDF5 format *.sw file')
    parser.add_argument('-f', dest='spacewalk_file', type=argparse.FileType('rt'), help='Input spacewalk text-based .swt file')
    parser.add_argument('-n', dest='swb_filename', action='store', help='Output spacewalk binary .sw file')
    parser.add_argument('-live-contact-map', action='store_true', help='Create live-contact-map vertices (use only with -single-point)')

    group = parser.add_mutually_exclusive_group(required=True)

    # Add the options to the group
    group.add_argument('-single-point', action='store_true',help='Indicates ball & stick input file')
    group.add_argument('-multi-point', action='store_true', help='Indicates pointcloud input file')

    return parser
