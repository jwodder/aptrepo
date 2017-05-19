import collections.abc
from   functools     import reduce
from   operator      import add
from   pathlib       import PurePosixPath
import attr
from   debian.deb822 import Deb822
from   .hashes       import Hash
from   .index_entry  import IndexEntry
from   .internals    import detach_signature

@attr.s
class IndexFile(collections.abc.MutableMapping):
    # The keys are all (supposed to be) relative POSIX paths.

    files  = attr.ib()
    fields = attr.ib()

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

    def __bool__(self):
        return bool(self.files)

    def for_json(self):
        return vars(self)

    def subindex(self, *path):
        """
        Returns an `IndexFile` object listing only those files in or below the
        directory given by ``*path``.  The path keys in the resulting object
        will be relative to ``*path``.

        ``*path`` may be any relative path specification accepted by
        `PurePath.relative_to`, such as a string (e.g., ``"main"`` or
        ``"main/binary-amd64"``), a sequence of strings (e.g., ``"main",
        "binary-amd64"``), or a `PurePosixPath` object.
        """
        ### TODO: Add an option for also updating the `filename` attributes of
        ### the IndexEntries?
        ### TODO: Add an option for controlling whether to keep `fields`?
        subfiles = {}
        for p, entry in self.files.items():
            pathobj = PurePosixPath(p)
            ### TODO: Handle absolute paths and paths beginning with .. (or .?)
            try:
                subpath = pathobj.relative_to(*path)
            except ValueError:
                pass
            else:
                subfiles[str(subpath)] = entry
        return self.__class__(files=subfiles, fields=self.fields.copy())
