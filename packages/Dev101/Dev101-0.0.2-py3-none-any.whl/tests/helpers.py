def read_file(filename):
    filepath = 'tests/raw_diffs/{}'.format(filename)
    file = open(filepath, 'r')
    contents = file.read()
    file.close()
    
    return contents