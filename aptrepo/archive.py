import logging
import re
from   tempfile     import TemporaryFile
from   bs4          import BeautifulSoup
import requests
from   .compression import Compression
from   .config      import ITER_CONTENT_SIZE
from   .errors      import NoValidCandidatesError, FileInaccessibleError
from   .flat        import FlatRepository
from   .internals   import joinurl
from   .release     import ReleaseFile
from   .suite       import Suite

log = logging.getLogger(__name__)

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
        log.info('Fetching InRelease file from %s', baseurl)
        r = self.session.get(joinurl(baseurl, 'InRelease'))
        if not (400 <= r.status_code < 500):
            r.raise_for_status()
            release = ReleaseFile.parse_signed(r.content)
        else:
            log.info('Server returned %d; fetching Release file instead',
                     r.status_code)
            r = self.session.get(joinurl(baseurl, 'Release'))
            r.raise_for_status()
            release = ReleaseFile.parse(r.content)
        ### TODO: Handle/fetch/verify PGP stuff
        if flat:
            return FlatRepository(self, suite, release)
        else:
            return Suite(self, suite, release)

    def fetch_indexed_file(self, dirpath, basepath, index):
        ### TODO: Add an option for disabling hash checks
        # Any file should be checked at least once, either in compressed or
        # uncompressed form, depending on which data is available.
        # -- <https://wiki.debian.org/RepositoryFormat#MD5Sum.2C_SHA1.2C_SHA256>

        # This method will only fetch a file+extension if it is listed in the
        # index and the index includes at least one secure hash for its
        # compressed and/or uncompressed form.

        baseurl = joinurl(self.uri, dirpath, basepath)
        log.info('Fetching %s', baseurl)
        clearentry = index.get(basepath)
        if clearentry is not None and not clearentry.secure_hashes():
            clearentry = None
        hashes_available = False
        for cmprs in Compression:
            log.info('Attempting to fetch as %s ...', cmprs.name)
            extpath = basepath + cmprs.extension
            try:
                hashes = index[extpath]
            except KeyError:
                log.info('%s: no index entry; skipping', extpath)
                continue
            if clearentry is None and not hashes.secure_hashes():
                log.info('%s: no secure hashes in index; skipping', extpath)
                continue
            hashes_available = True
            r = self.session.get(baseurl + cmprs.extension, stream=True)
            if not r.ok:
                log.info('%s: server returned %d; skipping', extpath,
                         r.status_code)
                continue
            log.info('%s fetched; checking hashes...', extpath)
            # `iter_content` needs to be used instead of `.raw.read` in order
            # to handle gzipped/deflated content transfer encodings.
            stream = r.iter_content(ITER_CONTENT_SIZE)
            if hashes.secure_hashes():
                stream = hashes.iter_check(stream)
            if cmprs:
                stream = cmprs.iter_decompress(stream)
                if clearentry is not None:
                    stream = clearentry.iter_check(stream)
            fp = TemporaryFile()
            for chunk in stream:
                fp.write(chunk)
            fp.seek(0)
            log.info('%s downloaded successfully', extpath)
            return fp
        if hashes_available:
            ### TODO: Include the error responses?
            raise FileInaccessibleError(basepath)
        else:
            raise NoValidCandidatesError(basepath)
