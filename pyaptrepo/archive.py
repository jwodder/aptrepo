import re
from   tempfile   import TemporaryFile
from   bs4        import BeautifulSoup
import requests
from   .internals import copy_and_hash
from   .release   import ReleaseFile
from   .suite     import Suite

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

    def fetch_suite(self, suite):
        ### TODO: parameters for later:
        ###           flat=False,
        ###           [something for PGP keys],
        ###           verify=True [for controlling whether to check signatures]
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
