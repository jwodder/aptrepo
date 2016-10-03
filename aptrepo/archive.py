import bz2
import gzip
import lzma
import re
from   tempfile   import TemporaryFile
from   bs4        import BeautifulSoup
import requests
from   .errors    import CannotFetchFileError
from   .flat      import FlatRepository
from   .internals import copy_and_hash
from   .release   import ReleaseFile
from   .suite     import Suite

DECOMPRESSORS = {
    '.bz2': bz2.BZ2File,
    '.gz': lambda fp: gzip.GzipFile(fileobj=fp),
    '.lzma': lzma.LZMAFile,
    '.xz': lzma.LZMAFile,
}

class Archive:
    def __init__(self, uri):
        self.uri = uri
        self.session = requests.Session()

    def __repr__(self):
        return '{}(uri={!r})'.format(self.__class__.__name__, self.uri)

    def _scrape_suite_candidates(self):
        ### TODO: Add a `flat=False` parameter
        r = self.session.get(self.uri + '/dists/')
        r.raise_for_status()
        if 'charset' in r.headers.get('content-type', '').lower():
            enc = r.encoding
        else:
            enc = None
        doc = BeautifulSoup(r.content, 'html.parser', from_encoding=enc)
        for link in doc.find_all('a'):
            ### TODO: Try to find a better pattern
            m = re.match(r'^(?:\./)*([\w.-]+)/?$', link.attrs.get('href'))
            if m:
                yield m.group(1)

    def scrape_suites(self):
        ### TODO: Add a `flat=False` parameter
        for suite in self._scrape_suite_candidates():
            try:
                yield self.fetch_suite(suite)
            except requests.HTTPError as e:
                if not (400 <= e.response.status_code < 500):
                    raise

    def scrape_suite_names(self):
        ### TODO: Add a `flat=False` parameter
        for suite in self._scrape_suite_candidates():
            for fname in ('InRelease', 'Release'):
                r = self.session.head('%s/dists/%s/%s'
                                      % (self.uri, suite, fname))
                if not (400 <= r.status_code < 500):
                    r.raise_for_status()
                    yield suite
                    break

    def fetch_suite(self, suite, flat=False):
        ### TODO: parameters for later:
        ###           [something for PGP keys],
        ###           verify=True [for controlling whether to check signatures]
        if flat:
            baseurl = self.uri + '/' + suite
        else:
            baseurl = self.uri + '/dists/' + suite
        r = self.session.get(baseurl + '/InRelease')
        if not (400 <= r.status_code < 500):
            r.raise_for_status()
            release = ReleaseFile.parse_signed(r.text)
        else:
            r = self.session.get(baseurl + '/Release')
            r.raise_for_status()
            release = ReleaseFile.parse(r.text)
        ### TODO: Handle/fetch/verify PGP stuff
        if flat:
            return FlatRepository(self, suite, release)
        else:
            return Suite(self, suite, release)

    def fetch_file(self, basepath, fp, hashes):
        # If `not hashes`, this method just assumes you know what you're doing
        # and doesn't complain.
        if basepath.startswith('/'):
            path = self.uri + basepath
        else:
            path = basepath
        r = self.session.get(path, stream=True)
        r.raise_for_status()
        copy_and_hash(r, fp, basepath, hashes)

    def fetch_compressed_file(self, basepath, fp, compressed_hashes,
                                    uncompressed_hashes, decompressor):
        # If both hash sets are empty, this method just assumes you know what
        # you're doing and doesn't complain.
        zipped = TemporaryFile()
        self.fetch_file(basepath, zipped, compressed_hashes)
        zipped.seek(0)
        unzipped = decompressor(zipped)
        copy_and_hash(unzipped, fp, basepath, uncompressed_hashes)

    def fetch_indexed_file(self, dirpath, basepath, index, extensions=None):
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
        baseurl = dirpath + '/' + basepath
        clearsums = index.sha2hashes(basepath)
        for ext in extensions:
            if basepath + ext in index.files:
                hashes = index.sha2hashes(basepath + ext)
                if not clearsums and not hashes:
                    continue
                ### TODO: Support acquiring by hash
                fp = TemporaryFile()
                try:
                    if ext in DECOMPRESSORS:
                        self.fetch_compressed_file(
                            baseurl + ext,
                            fp,
                            hashes,
                            clearsums,
                            DECOMPRESSORS[ext],
                        )
                    else:
                        self.fetch_file(baseurl + ext, fp, hashes)
                except requests.HTTPError:
                    continue  ### Let some errors propagate?
                fp.seek(0)
                return fp
        else:
            raise CannotFetchFileError(basepath)
