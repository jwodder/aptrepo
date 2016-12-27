import collections.abc
from   functools     import reduce
from   operator      import add
from   debian.deb822 import Deb822
from   .hashes       import Hash
from   .index_entry  import IndexEntry
from   .internals    import detach_signature, simple_repr

class IndexFile(collections.abc.MutableMapping):
    def __init__(self, files, fields):
        self.files = files
        self.fields = fields

    @classmethod
    def parse_signed(cls, obj):
        if not isinstance(obj, (str, bytes)):
            # Assume `obj` is a file-like object or other iterable of lines
            obj = reduce(add, obj)
        if isinstance(obj, bytes):
            obj = obj.decode('utf-8')
        payload, sig = detach_signature(obj)
        ### TODO: Do something with sig!
        return cls.parse(payload)

    @classmethod
    def parse(cls, obj):
        # `obj` can be anything accepted by Deb822: `str`, `bytes`, or a
        # sequence of lines (including file-like objects)
        fields = {
            k.lower(): v for k,v in Deb822(obj).items()
        }
        files = {}
        for h in Hash:
            hashlist = fields.pop(h.index_field, '')
            for line in hashlist.splitlines():
                if line.strip() != '':
                    hashsum, size, filename = line.strip().split(None, 2)
                    size = int(size)
                    if filename not in files:
                        files[filename] = IndexEntry(filename)
                    files[filename].add_checksum(h, hashsum, size)
        return cls(files, fields)

    def __repr__(self):
        return simple_repr(self)

    def __eq__(self, other):
        return type(self) is type(other) and vars(self) == vars(other)

    def __contains__(self, filename):
        return filename in self.files

    def __getitem__(self, filename):
        return self.files[filename]

    def __setitem__(self, key, value):
        self.files[key] = value

    def __delitem__(self, key):
        del self.files[key]

    def __iter__(self):
        return iter(self.files)

    def __len__(self):
        return len(self.files)

    def for_json(self):
        return vars(self)
