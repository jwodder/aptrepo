from   enum import Enum
import hashlib

class Hash(Enum):
    # The main point to this class is providing a mapping between hash
    # algorithms and the names used for them in APT index files.  Hashability
    # (pun not intended) of the values is also nice.

    MD5    = (hashlib.md5,    'md5sum')
    SHA1   = (hashlib.sha1,   'sha1')
    SHA224 = (hashlib.sha224, 'sha224')
    SHA256 = (hashlib.sha256, 'sha256')
    SHA384 = (hashlib.sha384, 'sha384')
    SHA512 = (hashlib.sha512, 'sha512')

    def __init__(self, hashcls, index_field):
        self.hashcls = hashcls
        self.index_field = index_field

    def __call__(self, data=b''):
        return self.hashcls(data)

    def __str__(self):
        return self.name

    def for_json(self):
        return self.name
