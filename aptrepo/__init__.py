__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'aptrepo@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/aptrepo'

from .archive   import Archive
from .component import Component
from .errors    import PyAPTError, HashMismatchError, CannotFetchFileError
from .flat      import FlatRepository
from .index     import Index
from .ppa       import PPA
from .release   import ReleaseFile
from .sources   import AptSource, parse_sources
from .suite     import Suite
from .util      import dpkg_architecture, dpkg_foreign_architectures, for_json

__all__ = [
    'AptSource',
    'Archive',
    'Component',
    'CannotFetchFileError',
    'FlatRepository',
    'HashMismatchError',
    'Index',
    'PPA',
    'PyAPTError',
    'ReleaseFile',
    'Suite',
    'dpkg_architecture',
    'dpkg_foreign_architectures',
    'for_json',
    'parse_sources',
]
