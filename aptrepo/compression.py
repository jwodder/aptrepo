from   bz2       import BZ2Decompressor
from   enum      import Enum
from   functools import partial
from   lzma      import LZMADecompressor
import zlib

class Compression(Enum):
    bzip2 = ('.bz2', BZ2Decompressor)
    # See <http://stackoverflow.com/q/2423866/744178>:
    gzip  = ('.gz', partial(zlib.decompressobj, zlib.MAX_WBITS | 16))
    lzma  = ('.lzma', LZMADecompressor)
    xz    = ('.xz', LZMADecompressor)
    uncompressed = ('', None)

    def __init__(self, extension, decompressor):
        self.extension = extension
        self.decompressor = decompressor

    def __bool__(self):
        return self.decompressor is not None

    #def iter_decompress(self, blob_iter: Iterable[bytes]) -> Iterator[bytes]:
    def iter_decompress(self, blob_iter):
        if self.decompressor is None:
            yield from blob_iter
        else:
            d = self.decompressor()
            for chunk in blob_iter:
                yield d.decompress(chunk)
            if hasattr(d, 'flush'):
                yield d.flush()  # Is this absolutely necessary?
            if not d.eof:
                raise ValueError('compressed file did not end with EOF')
            ### TODO: Should anything be done with d.unused_data ???
