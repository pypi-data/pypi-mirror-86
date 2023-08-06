__title__ = 'cvpoc'
__version__ = '1.0.1'
__author__ = 'CV Team'
__author_email__ = '943738808@qq.com'
__license__ = 'GPL 2.0'
__copyright__ = 'Copyright 2020 CV'
__name__ = 'cvpoc'
__package__ = 'cvpoc'

def start():
    print("import successful")


from .lib.core.common import set_paths
from .cli import module_path

set_paths(module_path())
