from   enum import Enum
import hashlib

class Hash(Enum):
    ### TODO: Make the set of known hashes configurable via config.py
    ### TODO: Get rid of the non-canonical aliases?
    MD5    = md5 = MD5Sum = MD5sum = (hashlib.md5, 'md5sum')
    SHA1   = sha1 = (hashlib.sha1, 'sha1')
    SHA224 = sha224 = (hashlib.sha224, 'sha224')
    SHA256 = sha256 = (hashlib.sha256, 'sha256')
    SHA384 = sha384 = (hashlib.sha384, 'sha384')
    SHA512 = sha512 = (hashlib.sha512, 'sha512')

    def __init__(self, hashcls, index_field):
        self.hashcls = hashcls
        self.index_field = index_field

    def __str__(self):
        return self.name

    def for_json(self):
        return self.name