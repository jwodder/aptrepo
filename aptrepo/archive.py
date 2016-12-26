import bz2
import gzip
import lzma
import re
from   tempfile   import TemporaryFile
from   bs4        import BeautifulSoup
import requests
from   .errors    import NoSecureChecksumsError, FileInaccessibleError
from   .flat      import FlatRepository
from   .internals import copy_and_hash, joinurl
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
        return '{}.{}(uri={!r})'.format(
            __package__,
            self.__class__.__name__,
            self.uri,
        )

    def __eq__(self, other):
        return type(self) is type(other) and self.uri == other.uri

    def _scrape_suite_candidates(self, subdir=None, flat=False):
        path = self.uri
        if not flat:
            path = joinurl(path, 'dists')
        if subdir is not None:
            path = joinurl(path, subdir)
        path = joinurl(path, '')  # Force the URL to end with a slash
        r = self.session.get(path)
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
                suite = m.group(1)
                if subdir is not None:
                    suite = joinurl(subdir, suite)
                if flat:
                    suite += '/'
                yield suite

    def scrape_suites(self, subdir=None, flat=False):
        for suite in self._scrape_suite_candidates(subdir=subdir, flat=flat):
            try:
                yield self.fetch_suite(suite)
            except requests.HTTPError as e:
                if not (400 <= e.response.status_code < 500):
                    raise

    def scrape_suite_names(self, subdir=None, flat=False):
        for suite in self._scrape_suite_candidates(subdir=subdir, flat=flat):
            if flat:
                sdir = joinurl(self.uri, suite)
            else:
                sdir = joinurl(self.uri, 'dists', suite)
            for fname in ('InRelease', 'Release'):
                r = self.session.head(joinurl(sdir, fname))
                if not (400 <= r.status_code < 500):
                    r.raise_for_status()
                    yield suite
                    break

    def fetch_suite(self, suite):
        flat = suite.endswith('/')
        if flat:
            baseurl = joinurl(self.uri, suite)
        else:
            baseurl = joinurl(self.uri, 'dists', suite)
        r = self.session.get(joinurl(baseurl, 'InRelease'))
        if not (400 <= r.status_code < 500):
            r.raise_for_status()
            release = ReleaseFile.parse_signed(r.content)
        else:
            r = self.session.get(joinurl(baseurl, 'Release'))
            r.raise_for_status()
            release = ReleaseFile.parse(r.content)
        ### TODO: Handle/fetch/verify PGP stuff
        if flat:
            return FlatRepository(self, suite, release)
        else:
            return Suite(self, suite, release)

    def fetch_file(self, basepath, fp, hashes):
        # If `not hashes`, this method just assumes you know what you're doing
        # and doesn't complain.
        if basepath.startswith('/'):
            path = joinurl(self.uri, basepath)
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

    def fetch_indexed_file(self, dirpath, basepath, index):
        ### TODO: Add an option for disabling hash checks
        extensions = [''] + list(DECOMPRESSORS.keys())
        # Any file should be checked at least once, either in compressed or
        # uncompressed form, depending on which data is available.
        # -- <https://wiki.debian.org/RepositoryFormat#MD5Sum.2C_SHA1.2C_SHA256>
        baseurl = joinurl(dirpath, basepath)
        clearsums = index.secure_hashes(basepath)
        hashes_available = False
        for ext in extensions:
            if basepath + ext in index.files:
                hashes = index.secure_hashes(basepath + ext)
                if not clearsums and not hashes:
                    continue
                hashes_available = True
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
                    continue
                fp.seek(0)
                return fp
        else:
            if hashes_available:
                raise FileInaccessibleError(basepath)
            else:
                raise NoSecureChecksumsError(basepath)
