import os
import os.path


# TODO: consider using less simplistic criteria for predicate
def is_python_source_file(file_name):
    ''' Somewhat simplistic predicate tests if a file is python source
    by checking for a .py extension in the filename. '''
    return file_name.endswith(".py")


def find_python_files(root):
    ''' Recursively search a directory indicated by `root` for a list
    of python source files. '''
    all_files = [
        os.path.join(r, file) for r, _, f in os.walk(root) for file in f
    ]
    python_files = filter(is_python_source_file, all_files)
    return list(python_files)


# TODO: ignores parent directories and concept of submoduling
def get_module_name(f):
    base = os.path.basename(f)
    filename, _ = os.path.splitext(base)
    return filename
