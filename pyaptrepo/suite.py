import bz2
import gzip
import lzma
from   tempfile   import TemporaryFile
import requests
from   .component import Component
from   .errors    import CannotFetchFileError
from   .internals import parse_contents

DECOMPRESSORS = {
    '.bz2': bz2.BZ2File,
    '.gz': lambda fp: gzip.GzipFile(fileobj=fp),
    '.lzma': lzma.LZMAFile,
    '.xz': lzma.LZMAFile,
}

class Suite:
    def __init__(self, archive, name, release):
        # not for public construction
        self.archive = archive
        self.name = name
        self.release = release
        self.components = [
            Component(self, c) for c in getattr(self.release, 'components', [])
        ]

    def __eq__(self, other):
        # for use in detecting suite synonyms/symlinks
        return type(self) is type(other) and self.release == other.release

    def __getitem__(self, component):
        return Component(self, component)

    @property
    def architectures(self):
        return getattr(self.release, 'architectures', [])

    @property
    def acquire_by_hash(self):
        return getattr(self.release, 'acquire_by_hash', False)

    @property
    def has_contents(self):
        # whether the Contents files are in the suite or the component
        return any(
            'Contents-' + sarch + '.gz' in self.release.files
            for sarch in ['source'] + self.architectures
        )

    def fetch_contents(self, sarch):
        contents = self.fetch_file('Contents-' + sarch, extensions=('.gz',))
            ### Include '' in extensions?
        return parse_contents(contents)

    def fetch_file(self, basepath, extensions=None):
        ### TODO: Add an option for disabling hash checks
        if extensions is None:
            extensions = [''] + list(DECOMPRESSORS.keys())
        else:
            extensions = [
                ext for ext in extensions if ext in DECOMPRESSORS or ext == ''
            ]
        if not extensions:
            raise ValueError('no supported file extensions specified')
        # Any file should be checked at least once, either in compressed or
        # uncompressed form, depending on which data is available.
        # -- <https://wiki.debian.org/RepositoryFormat#MD5Sum.2C_SHA1.2C_SHA256>
        baseurl = '/dists/' + self.name + '/' + basepath
        clearsums = self.release.sha2hashes(basepath)
        for ext in extensions:
            if basepath + ext in self.release.files:
                hashes = self.release.sha2hashes(basepath + ext)
                if not clearsums and not hashes:
                    continue
                ### TODO: Support acquiring by hash
                fp = TemporaryFile()
                try:
                    if ext in DECOMPRESSORS:
                        self.archive.fetch_compressed_file(
                            baseurl + ext,
                            fp,
                            hashes,
                            clearsums,
                            DECOMPRESSORS[ext],
                        )
                    else:
                        self.archive.fetch_file(baseurl + ext, fp, hashes)
                except requests.HTTPError:
                    continue  ### Let some errors propagate?
                fp.seek(0)
                return fp
        else:
            raise CannotFetchFileError(basepath)
