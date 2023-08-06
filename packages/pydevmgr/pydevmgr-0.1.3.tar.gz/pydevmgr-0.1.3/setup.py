#!/usr/bin/env python

import os
import sys

#from distutils.core import setup # dependency does not works
from setuptools import setup

name = "pydevmgr"
names = ["pydevmgr", "pydevmgr_qt"] # if None build only the package defined by name

version='0.1.3' # https://www.python.org/dev/peps/pep-0440/
author='Sylvain Guieu'
author_email='sylvain.guieu@univ-grenoble-alpes.fr'
install_requires = ['opcua', 'pyyaml', 'jinja2', 'argparse']
# in setuptools the egg fragment must have the version in it
# unlike with the pip install git+https://gricad-gitlab.univ-grenoble-alpes.fr/guieus/instru#egg=instru
#dependency_links=['git+https://gricad-gitlab.univ-grenoble-alpes.fr/guieus/instru#egg=instrutools-0.1.dev0']
dependency_links=[]
# any file inside the data relative directory name/data_dir will be include as data file
data_directories = [(os.path.join('pydevmgr_qt','uis'), '.ui', 'pydevmgr_qt_uis'), 
                    (os.path.join('pydevmgr', 'resources'), '.yml', 'pydevmgr_maps')]

#[(os.path.join(name,'resources'),'', 'pydevmgr_resources')]

#(os.path.join(name,'guis'),'.ui')]

script_directories = ["pydevmgr/scripts", "pydevmgr_qt/scripts"]
license='Creative Commons Attribution-Noncommercial-Share Alike license'




# Python 3.0 or later needed
if sys.version_info < (3, 0, 0, 'final', 0):
    raise SystemExit('Python 3.0 or later is required!')


## ######################################################
##
##  Try to make this part bellow stand alone so I can copy/past
##   to other projects
##
## ######################################################


rootdir = os.path.abspath(os.path.dirname(__file__))



# Build a list of all project modules
packages = []
if names:
    for _nme in names:
        for dirname, dirnames, filenames in os.walk(_nme):
            if '__init__.py' in filenames:
                packages.append(dirname.replace('/', '.'))
else:
    for dirname, dirnames, filenames in os.walk(name):
        if '__init__.py' in filenames:
            packages.append(dirname.replace('/', '.'))

#package_dir = {name: name}

# Data files used e.g. in tests
#package_data = {name: [os.path.join(name, 'tests', 'prt.txt')]}

# The current version number - MSI accepts only version X.X.X
#exec(open(os.path.join(name, 'version.py')).read())

# Scripts
scripts = []
for script_dir in script_directories:
    for dirname, dirnames, filenames in os.walk(script_dir):
        for filename in filenames:
            if not filename.endswith('.bat'):
                scripts.append(os.path.join(dirname, filename))

# Provide bat executables in the tarball (always for Win)
# if 'sdist' in sys.argv or os.name in ['ce', 'nt']:
#     for s in scripts[:]:
#         scripts.append(s + '.bat')

# Data_files (e.g. doc) needs (directory, files-in-this-directory) tuples

data_files = []

for data_dir, file_ext, tdir in data_directories:
    for dirname, dirnames, filenames in os.walk( os.path.join(data_dir)):
        fileslist = []
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if (not file_ext) or (ext == file_ext):
                fullname = os.path.join(dirname, filename)
                fileslist.append(fullname)
                #print(('share/' + dirname, fileslist))
        if tdir:
            data_files.append(( os.path.join('share' , tdir), fileslist ))
        else:
            data_files.append(( os.path.join('share' , dirname), fileslist ))

print("---------------")
print(data_files)
print("---------------")

#####

for path in ["README.md", "readme.md", "readme.txt"]:
    try:
        readme = open('README.md').read()
    except Exception as er:
        print("No readme file : ", er)
    else:
        break
else:
    readme = ""


setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    packages=packages,
    scripts=scripts,
    data_files=data_files,
    license=license,
    long_description=readme,
    install_requires=install_requires,
    dependency_links=dependency_links,
    long_description_content_type='text/markdown'
)
