"""
Files named __init__.py are used s
to mark directories on disk as a Python package directories. If you have the files
mydir/spam/__init__.py
mydir/spam/module.py
and mydir is on your path, you can import the code in module.py as:
import spam.module
or
from spam import module
If you remove the __init__.py file, Python will no longer look for 
submodules inside that directory, so attempts to import the module will fail.
"""
