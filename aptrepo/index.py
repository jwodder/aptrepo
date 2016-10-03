from functools   import reduce
from operator    import add
from debian      import deb822
from .internals  import SHA2, detach_signature

### cf. the `Release` class in `debian.deb822`

class Index:  ### Rename "IndexFile"?
    def __init__(self, files, fields):
        ### Also include a(n optional?) `baseurl` parameter?
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
            k.lower(): v for k,v in deb822.Deb822(obj).items()
        }
        files = {}
        for f in ("md5sum", "sha1", "sha224", "sha256", "sha384", "sha512"):
            hashlist = fields.pop(f, '')
            for line in hashlist.splitlines():
                if line.strip() != '':
                    # Filenames will never contain spaces, right?
                    hashsum, size, filename = line.split()
                    size = int(size)
                    if filename in files:
                        ### TODO: Raise a more descriptive error if this fails:
                        assert files[filename]["size"] == size
                    else:
                        files[filename] = {"size": size}
                    if f == "md5sum":
                        f = "md5"
                    files[filename][f] = hashsum.lower()
        return cls(files, fields)

    def __contains__(self, filename):
        return filename in self.files

    def __getitem__(self, filename):
        return self.files[filename]

    def __eq__(self, other):
        return type(self) is type(other) and vars(self) == vars(other)

    def sha2hashes(self, filename):
        # Rename to "secure_hashes"?
        about = self.files.get(filename, {})
        return {alg: about[alg] for alg in SHA2 if alg in about}

    def for_json(self):
        return vars(self)
