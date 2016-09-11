# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import sys
import os
import os.path
sys.argv.append ('py2exe')
# cmd> python py_exe.py py2exe
# python -m py_compile file.py ,py to pyc

#options={"py2exe":{"includes":["sip"]}}
#options = { "py2exe":{"dll_excludes":["MSVCP90.dll"]}}

#python 
includes = ["Tkinter",'decimal'] 
#excludes
excludes = ["tcl", ]
#python packages
packages = []
#dll_excludes #copy those files into dist folder manually
dll_excludes = ["tcl85.dll", "tk85.dll"] 
#distribute folder
dist_dir = 'dist'
#data_files
data_files = ['ris.cfg','ris.ico','logo.gif']
# the syntax for data files is a list of tuples with (dest_dir, [sourcefiles])
# if only [sourcefiles] then they are copied to dist_dir 
data_files = data_files + [   os.path.join (sys.prefix, "DLLs", f) 
               for f in os.listdir (os.path.join (sys.prefix, "DLLs")) 
               if  (   f.lower ().startswith (("tcl", "tk")) 
                   and f.lower ().endswith ((".dll", ))
                   )
                ] 
#python scripts
windows = [{'script': "main.py", "icon_resources": [(1, "ris.ico")]}]

setup (
    options    = 
        {'py2exe': 
            { "bundle_files" : 1    # 3 = don't bundle (default) 
                                     # 2 = bundle everything but the Python interpreter 
                                     # 1 = bundle everything, including the Python interpreter
            , "compressed"   : False  # (boolean) create a compressed zipfile
            , "unbuffered"   : False  # if true, use unbuffered binary stdout and stderr
            , "includes"     : includes
            , "excludes"     : excludes
            , "optimize"     : 0  #-O
            , "packages"     : packages
            , "dist_dir"     : dist_dir
            , "dll_excludes" : dll_excludes
            ,               
            }
        }
    , windows = windows
    , zipfile = None
    # the syntax for data files is a list of tuples with (dest_dir, [sourcefiles])
    # if only [sourcefiles] then they are copied to dist_dir 
    , data_files = data_files
    ,
)

