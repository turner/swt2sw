import argparse
def create_command_line_parser():
    parser = argparse.ArgumentParser(description='Convert text-based *.swt file to binary format *.sw file')
    parser.add_argument('-f', dest='swt_file', type=argparse.FileType('rt'), help='Input legacy text-based spacewalk file (.swt)')
    parser.add_argument('-n', dest='sw_filename', action='store', help='File name prefix for output spacewalk binary file (.sw)')
    parser.add_argument('-live-contact-map', action='store_true', help='Create live-contact-map vertices (use only with -single-point)')

    group = parser.add_mutually_exclusive_group(required=True)

    # Add the options to the group
    group.add_argument('-single-point', action='store_true',help='Data is ORCA (ball & stick) input file')
    group.add_argument('-multi-point', action='store_true', help='Data is OligoSTORM (point cloud) input file')

    return parser
