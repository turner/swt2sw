indices = []
def create_single_point_group(spatial_position_group, spacewalk_file):
    print('Create Ball & Stick Spatial Group')
    for line in spacewalk_file:
        tokens = line.split()
        if 'trace' == tokens[0]:
            indices.append(int(tokens[1]))
            trace_group_name = str(indices[-1])
            trace_group = spatial_position_group.create_group(trace_group_name)

def create_multi_point_group(spatial_position_group, spacewalk_file):
    print('Create Pointcloud Spatial Group')

def create_spatial_group(root, spacewalk_file, args):
    spatial_position_group = root.create_group('spatial_position')
    if args.single_point:
        create_single_point_group(spatial_position_group, spacewalk_file)
    elif args.multi_point:
        create_multi_point_group(spatial_position_group, spacewalk_file)

    return None