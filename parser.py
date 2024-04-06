import argparse
def create_command_line_parser():
    parser = argparse.ArgumentParser(description='Convert *.sw to *.cndb format')
    parser.add_argument('-f', dest='spacewalk_file', type=argparse.FileType('rt'), help='Input spacewalk file')
    parser.add_argument('-n', dest='cndb_filename', action='store', help='Output CNDB file')
    return parser
