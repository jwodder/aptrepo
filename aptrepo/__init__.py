__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'aptrepo@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/aptrepo'

from .archive     import Archive
from .component   import Component
### TODO: Export Compression?
from .errors      import Error, HashMismatchError, SizeMismatchError, \
                            CannotFetchFileError, NoSecureChecksumsError, \
                            FileInaccessibleError
from .flat        import FlatRepository
from .hashes      import Hash
from .index       import IndexFile
from .index_entry import IndexEntry
from .ppa         import PPA
from .release     import ReleaseFile
from .sources     import AptSource, parse_sources
from .suite       import Suite
from .util        import dpkg_architecture, dpkg_foreign_architectures, for_json

__all__ = [
    'AptSource',
    'Archive',
    'Component',
    'CannotFetchFileError',
    'Error',
    'FileInaccessibleError',
    'FlatRepository',
    'Hash',
    'HashMismatchError',
    'IndexEntry',
    'IndexFile',
    'NoSecureChecksumsError',
    'PPA',
    'ReleaseFile',
    'SizeMismatchError',
    'Suite',
    'dpkg_architecture',
    'dpkg_foreign_architectures',
    'for_json',
    'parse_sources',
]
