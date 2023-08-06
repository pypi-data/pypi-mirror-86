import yaml
import os

RESPATH = 'RESPATH'

def read_map(file):
    with open(file) as f:
        return yaml.load(f.read(), Loader=yaml.CLoader)

def read_config(file):    
    with open(file) as f:
        return yaml.load(f.read(), Loader=yaml.CLoader)

def load_config(file_name):
    return read_config(find_config(file_name))

def load_extra_of(file_name):
    
    root, ext = os.path.splitext(find_config(file_name))
    
    
    file_name = os.path.join(root+"_extra"+ext)
    if not os.path.exists(file_name):
        return None
    return read_config(file_name)

def load_map(file_name):
    return read_map(find_config(file_name))

def find_config(file_name):
    path_list = os.environ.get(RESPATH, '.').split(':')
    for directory in path_list[::-1]:
        path = os.path.join(directory, file_name)
        if os.path.exists(path):
            return  path
    raise ValueError('coud not find config file %r in any of %s'%(file_name, path_list))


    