import glob
import os

from cx_Freeze import setup, Executable

# Add any additional modules or packages your application requires.
additional_modules = []

if os.name == 'nt':
    executable = Executable('main.py', target_name="database-table-copy.exe")
else:
    executable = Executable('main.py', target_name="database-table-copy")


# Define a function to get a list of files matching a wildcard pattern.
def get_files_by_pattern(pattern):
    files = glob.glob(pattern)
    return [(file, file) for file in files]


# Use the function to get a list of files matching the wildcard pattern.
include_files = [("../config.example.json", "config.example.json"),
                 ("../README.md", "README.md"),
                 ("../LICENSE.txt", "LICENSE.txt")]

setup(
    name='DatabaseTableCopy',
    version='1.0.3',
    description='A bcp wrapper for copy table data between two databases',
    executables=[executable],
    options={'build_exe':
        {
            'packages': additional_modules,
            'include_files': include_files
        }
    }
)
