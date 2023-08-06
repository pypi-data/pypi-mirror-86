import yaml
import os

RESPATH = 'RESPATH'

__module_dir__, _ = os.path.split(__file__)
#__module_dir__, _ = os.path.split(__module_dir__) # so far client and server are in the same package
__package_dir__, __pkg__ = os.path.split(__module_dir__)
pkg_resource_path = []
pkg_resource_path.append(os.path.join(__package_dir__, "share", "pydevmgr_maps"))


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

def find_map(dev_type):
    """ locate the map file from the pydevmgr installation and return the absolute path 
    
    map file will be located there : '%s'
    
    Args:
        dev_type (str):  Device type as 'Motor' the map file shall be found as mapMotor.yml inside 
        the package resource directories
    """%( "' ,''".join(pkg_resource_path))
    for d in pkg_resource_path[::-1]:
        path = os.path.join(d, 'map'+dev_type.capitalize()+".yml")
        if os.path.exists(path):
            return path
    raise ValueError('coud not find map file of device %r from pydevmgr package'%(dev_type))
    
def find_template(dev_type):
    """ locate a template file from the pydevmgr installation and return the absolute path 
    
    template file will be located there : '%s'.
    templates rendered by jinja2 
    
    Args:
        dev_type (str):  Device type as 'Motor' the template file shall be found as templateMotor.yml inside 
        the package resource directories
    """%( "' ,''".join(pkg_resource_path))
    for d in pkg_resource_path[::-1]:
        path = os.path.join(d, 'template'+dev_type.capitalize()+".yml")
        if os.path.exists(path):
            return path
    raise ValueError('coud not find map file of device %r from pydevmgr package'%(dev_type))

    