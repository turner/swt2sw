from datetime import datetime
def create_header(cndbf, spacewalk_file):
    spacewalk_meta_data = {}
    header = cndbf.create_group('Header')
    first_line = spacewalk_file.readline().strip()
    entries = None
    if first_line.startswith('#'):
        entries = first_line[2:].split()  #[2:] because have ##

    for entry in entries:
        key, value = entry.split('=')
        spacewalk_meta_data[key] = value

    hash = {
        'version' : '1.0.0',
        'author' : 'Douglass Turner',
        'date' : str(datetime.now())
    }

    hash.update(spacewalk_meta_data)
    header.attrs.update(hash)

    return spacewalk_meta_data
