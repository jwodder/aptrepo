import attr
from   .config import SECURE_HASHES
from   .errors import HashMismatchError, SizeMismatchError, \
                        NoSecureChecksumsError
from   .hashes import Hash

@attr.s
class IndexEntry:
    filename = attr.ib()  # string
    size     = attr.ib(default=None, init=False)
    hashes   = attr.ib(default=attr.Factory(dict), init=False)

    def add_checksum(self, algorithm: Hash, digest: str, size: int) -> None:
        if self.size is None:
            self.size = size
        elif self.size != size:
            raise ValueError('{}: conflicting filesizes in index'
                             .format(self.filename))
        digest = digest.lower()
        if algorithm in self.hashes and self.hashes[algorithm] != digest:
            raise ValueError('{}: conflicting {} digests in index'
                             .format(self.filename, algorithm.name))
        self.hashes[algorithm] = digest

    #def iter_check(self, blob_iter: Iterable[bytes]) -> Iterator[bytes]:
    def iter_check(self, blob_iter, allowed_hashes=None):
        if allowed_hashes is None:
            allowed_hashes = SECURE_HASHES
        size = 0
        digestion = {alg: alg() for alg in self.hashes if alg in allowed_hashes}
        if not digestion:
            raise NoSecureChecksumsError(self.filename)
        for chunk in blob_iter:
            for h in digestion.values():
                h.update(chunk)
            size += len(chunk)
            yield chunk
        if self.size is not None and self.size != size:
            raise SizeMismatchError(self.filename, self.size, size)
        for alg, h in digestion.items():
            check = h.hexdigest()
            if self.hashes[alg] != check:
                raise HashMismatchError(
                    self.filename,
                    alg.name,
                    self.hashes[alg],
                    check,
                )

    def filter_hashes(self, allowed_hashes=None):
        if allowed_hashes is None:
            allowed_hashes = SECURE_HASHES
        return {k:v for k,v in self.hashes.items() if k in allowed_hashes}

    def for_json(self):
        return {
            "filename": self.filename,
            "size": self.size,
            "hashes": {k.name: v for k,v in self.hashes.items()}
        }
