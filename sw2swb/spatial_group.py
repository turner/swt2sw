import numpy as np

def to_float(value):
    try:
        return float(value)
    except ValueError:  # This will catch cases where the conversion fails, e.g., if value is 'nan'
        return float(0)

def single_point_group_harvest_xyz(group, xyz, index):
    xyz_stack = np.column_stack((xyz[1], xyz[2], xyz[3]))
    dataset_name = 't_' + str(index)
    print('Create dataset {:}'.format(dataset_name))
    group.create_dataset(dataset_name, data=xyz_stack)

def multi_point_dataset_harvest(trace_dataset, regions, hash):
    print('multi_point_dataset_harvest')

    for key in hash.keys():

        xyz = hash[key]

        xyz_stack = np.column_stack((xyz[0], xyz[1], xyz[2]))

        # how many rows
        row_count = xyz_stack.shape[0]

        # create single column
        region_index_column = np.full((row_count, 1), regions[key])

        # prepend region index to xyz-stack
        region_xyz_stack = np.hstack((region_index_column, xyz_stack))

        # Resize the dataset to accommodate the new data
        new_rows = region_xyz_stack.shape[0]
        trace_dataset.resize(trace_dataset.shape[0] + new_rows, axis=0)
        trace_dataset[-new_rows:] = region_xyz_stack

def multi_point_xyz_stack_harvest(stacks, regions, hash):
    print('multi_point_xyz_stack_harvest')

    for key in hash.keys():

        xyz = hash[key]
        xyz_stack = np.column_stack((xyz[0], xyz[1], xyz[2]))

        # how many rows
        row_count = xyz_stack.shape[0]

        # create single column
        region_index_column = np.full((row_count, 1), regions[key])

        # prepend region index to xyz-stack
        region_xyz_stack = np.hstack((region_index_column, xyz_stack))
        stacks.append(region_xyz_stack)

def create_single_point_group(spatial_position_group, spacewalk_file):
    print('Create Ball & Stick Spatial Group')
    indices = []
    xyz_list = None
    for line in spacewalk_file:
        tokens = line.split()
        if 'trace' == tokens[0]:
            indices.append(int(tokens[1]))
            if xyz_list is not None:
                single_point_group_harvest_xyz(spatial_position_group, xyz_list, indices[-2])
                xyz_list = None
        elif 6 == len(tokens):
            if xyz_list is None:
                key = '%'.join([tokens[0], tokens[1], tokens[2]])
                xyz_list = [key, [], [], []]
            xyz_list[1].append(to_float(tokens[3]))
            xyz_list[2].append(to_float(tokens[4]))
            xyz_list[3].append(to_float(tokens[5]))
    return [xyz_list, indices]

def create_multi_point_group(spatial_position_group, regions, spacewalk_file):
    print('Create Pointcloud Spatial Group')
    indices = []
    hash = None
    dataset = None
    for line in spacewalk_file:
        tokens = line.split()
        if 'trace' == tokens[0]:
            indices.append(int(tokens[1]))

            if hash is not None:
                xyz_stacks = []
                multi_point_xyz_stack_harvest(xyz_stacks, regions, hash)
                combined_xyz_stack = np.vstack(xyz_stacks)
                spatial_position_group.create_dataset('t_' + str(indices[-2]), data=combined_xyz_stack)
            hash = {}

        elif 6 == len(tokens):
            key = '%'.join([tokens[0], tokens[1], tokens[2]])
            if key not in hash.keys():
                hash[key] = [[], [], []]
            hash[key][0].append(to_float(tokens[3]))
            hash[key][1].append(to_float(tokens[4]))
            hash[key][2].append(to_float(tokens[5]))
    return [hash, indices]

def create_spatial_group(root, regions, spacewalk_file, args, header_group):
    spatial_position_group = root.create_group('spatial_position')
    if args.single_point:
        header_group.attrs['point_type'] = 'single_point'
        xyz, indices = create_single_point_group(spatial_position_group, spacewalk_file)
        # harvest final xyz list
        single_point_group_harvest_xyz(spatial_position_group, xyz, indices[-1])
    elif args.multi_point:
        header_group.attrs['point_type'] = 'multi_point'
        dictionary, indices = create_multi_point_group(spatial_position_group, regions, spacewalk_file)

        # harvest final hash entries
        xyz_stacks = []
        multi_point_xyz_stack_harvest(xyz_stacks, regions, dictionary)
        combined_xyz_stack = np.vstack(xyz_stacks)
        spatial_position_group.create_dataset('t_' + str(indices[-1]), data=combined_xyz_stack)

    return None