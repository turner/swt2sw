import argparse
def create_command_line_parser():
    parser = argparse.ArgumentParser(description='Convert text-based *.swt file to binary HDF5 format *.sw file')
    parser.add_argument('-f', dest='spacewalk_file', type=argparse.FileType('rt'), help='Input spacewalk file')
    parser.add_argument('-n', dest='swb_filename', action='store', help='Output swb file')

    group = parser.add_mutually_exclusive_group(required=True)

    # Add the options to the group
    group.add_argument('-single-point', action='store_true',help='Indicates a ball & stick input spacewalk file')
    group.add_argument('-multi-point', action='store_true', help='Indicates a pointcloud input spacewalk file')

    return parser
