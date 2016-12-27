from .config import SECURE_HASHES
from .errors import HashMismatchError, SizeMismatchError, NoSecureChecksumsError
from .hashes import Hash

class IndexEntry:
    def __init__(self, filename: str):
        self.filename = filename
        self.size = None
        self.hashes = {}

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
    def iter_check(self, blob_iter):
        size = 0
        digestion = {
            alg: alg.hashcls() for alg in self.hashes if alg in SECURE_HASHES
        }
        if not digestion:
            ### TODO: This isn't semantically correct:
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

    def secure_hashes(self):
        return {k:v for k,v in self.hashes.items() if k in SECURE_HASHES}

    ### TODO: for_json
