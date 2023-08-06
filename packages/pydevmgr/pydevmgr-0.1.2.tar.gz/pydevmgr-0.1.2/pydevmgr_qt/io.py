import os
__module_dir__, _ = os.path.split(__file__)
#__module_dir__, _ = os.path.split(__module_dir__) # so far client and server are in the same package
__package_dir__, __pkg__ = os.path.split(__module_dir__)
uis_path =[]
uis_path.append(os.path.join(__package_dir__, "share", "pydevmgr_qt_uis"))

def find_ui(name):
    for dirname in uis_path:
        path = os.path.join(dirname, name)
        if os.path.exists(path):
            return path
    raise ValueError('could not found ui file  %r in any of %r'%(name, uis_path))
