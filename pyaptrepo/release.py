from operator    import add
from email.utils import parsedate_to_datetime
from functools   import reduce
from debian      import deb822
from .internals  import SHA2, detach_signature, massage_index

class ReleaseFile:
    def __init__(self, data):
        for k,v in data.items():
            setattr(self, k.replace('-', '_'), v)

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
        data = {
            k.lower(): v for k,v in deb822.Deb822(obj).items()
        }
        if 'components' in data:
            ### TODO: Remove extra directory paths from Components
            data["components"] = data["components"].split()
        if 'architectures' in data:
            data["architectures"] = data["architectures"].split()
        ### TODO: Split Signed-By
        for field in (
            'acquire-by-hash',
            'notautomatic',
            'butautomaticupgrades',
        ):
            if field in data and data[field].lower() in ('no', 'yes'):
                data[field] = (data[field].lower() == 'yes')
        for field in ('date', 'valid-until'):
            if field in data:
                try:
                    data[field] = parsedate_to_datetime(data[field])
                except (TypeError, ValueError):
                    pass
        massage_index(data)
        return cls(data)

    def sha2hashes(self, filename):
        # Rename to "secure_hashes"?
        about = self.files.get(filename, {})
        return {alg: about[alg] for alg in SHA2 if alg in about}

    def for_json(self):
        return vars(self)

    def __eq__(self, other):
        return type(self) is type(other) and vars(self) == vars(other)
