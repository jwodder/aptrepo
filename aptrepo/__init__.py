__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'aptrepo@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/aptrepo'

from .archive     import Archive
from .component   import Component
from .contents    import ContentsPackage, parse_contents
from .errors      import (
                            Error,
                                FileValidationError,
                                    NoSecureChecksumsError,
                                    HashMismatchError,
                                    SizeMismatchError,
                                CannotFetchFileError,
                                    NoValidCandidatesError,
                                    FileInaccessibleError,
                         )
from .flat        import FlatRepository
from .hashes      import Hash
from .index       import IndexFile
from .index_entry import IndexEntry
from .ppa         import PPA
from .release     import ReleaseFile
from .sources     import AptSource, parse_sources
from .suite       import Suite
from .util        import (
                            dpkg_architecture,
                            dpkg_foreign_architectures,
                            for_json,
                            ubuntu_release,
                         )

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    'AptSource',
    'Archive',
    'CannotFetchFileError',
    'Component',
    'ContentsPackage',
    'Error',
    'FileInaccessibleError',
    'FileValidationError',
    'FlatRepository',
    'Hash',
    'HashMismatchError',
    'IndexEntry',
    'IndexFile',
    'NoSecureChecksumsError',
    'NoValidCandidatesError',
    'PPA',
    'ReleaseFile',
    'SizeMismatchError',
    'Suite',
    'dpkg_architecture',
    'dpkg_foreign_architectures',
    'for_json',
    'parse_contents',
    'parse_sources',
    'ubuntu_release',
]
