import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Your script description.')

# Create a mutually exclusive group
group = parser.add_mutually_exclusive_group(required=True)

# Add the options to the group
group.add_argument('-single-point', action='store_true',
                   help='Use the single point mode.')
group.add_argument('-multi-point', action='store_true',
                   help='Use the multi point mode.')

# Parse the arguments
args = parser.parse_args()

# Example usage of parsed arguments
if args.single_point:
    print('Single point mode selected.')
elif args.multi_point:
    print('Multi point mode selected.')
