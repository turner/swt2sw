def create_region_list(file):

    hash = {}
    for line in file:
        tokens = line.split()
        if 6 == len(tokens):
            key = tokens[0] + '%' + tokens[1] + '%' + tokens[2]
            if key not in hash.keys():
                hash[key] = [tokens[0], int(tokens[1]), int(tokens[2])]

    # Create sorted region list
    key_list = list(hash.keys())
    key_list.sort(key=lambda string: int(string.split('%')[1]))
    result = list(map(lambda string: string.split('%'), key_list))
    return result

def append_genomic_position_group_with_region_list(root, region_list):
    genomic_position_group = root.create_group('genomic_position')
    genomic_position_group.create_dataset('regions', data=region_list)

def create_region_dictionary(region_list):
    dictionary = {}
    for region in region_list:
        key = region[0] + '%' + region[1] + '%' + region[2]
        dictionary[key] = region_list.index(region)
    return dictionary