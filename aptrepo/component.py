import logging
from   os.path          import splitext
import attr
from   debian.deb822    import Packages, Sources
from   property_manager import cached_property
from   .config          import I18N_INDEX_HASHES
from   .contents        import parse_contents
from   .index           import IndexFile
from   .internals       import joinurl

log = logging.getLogger(__name__)

@attr.s
class Component:
    # not for public construction
    suite = attr.ib()
    name  = attr.ib()

    @property
    def archive(self):
        return self.suite.archive

    def fetch_packages(self, arch):
        fp = self.suite.fetch_indexed_file(
            joinurl(self.name, 'binary-' + arch, 'Packages')
        )
        return Packages.iter_paragraphs(fp, use_apt_pkg=True)

    def fetch_sources(self):
        fp = self.suite.fetch_indexed_file(
            joinurl(self.name, 'source', 'Sources')
        )
        return Sources.iter_paragraphs(fp, use_apt_pkg=True)

    def fetch_i18n_index(self):
        dex = self.suite.fetch_indexed_file(joinurl(self.name, 'i18n', 'Index'))
        return IndexFile.parse(dex)

    @cached_property
    def translation_index(self):
        dex = self.suite.release.subindex(self.name, 'i18n')
        have_i18n_index = 'Index' in dex
        dex.files = {
            k:v for k,v in dex.files.items() if k.startswith('Translation-')
        }
        if dex:
            self.using_i18n_index = False
            return dex
        elif have_i18n_index:
            self.using_i18n_index = True
            return self.fetch_i18n_index()
        else:
            self.using_i18n_index = False
            return IndexFile({}, {})

    def available_translations(self):
        xlates = set()
        prefix_len = len('Translation-')
        for fname in self.translation_index.files:
            assert fname[:prefix_len] == 'Translation-'
            fname, _ = splitext(fname[prefix_len:])
            ### TODO: Do I ever need to remove more than one extension?  Are
            ### there "extensions" that shouldn't be removed (i.e., will a
            ### translation file ever be named "Translation-en_US.UTF-8")?
            xlates.add(fname)
        return xlates

    def fetch_translation(self, lang):
        index = self.translation_index
        fp = self.archive.fetch_indexed_file(
            joinurl('dists', self.suite.name, self.name, 'i18n'),
            'Translation-' + lang,
            index,
            allowed_hashes=I18N_INDEX_HASHES if self.using_i18n_index else None,
        )
        return Packages.iter_paragraphs(fp, use_apt_pkg=True)

    @property
    def has_contents(self):
        # whether the Contents files are in the component or the suite
        return any(
            joinurl(self.name, 'Contents-' + sarch + '.gz') in self.suite.files
            for sarch in ['source'] + self.suite.architectures
        )

    def fetch_contents(self, sarch):
        # Raises an error if the Contents files are at Suite level
        contents = self.suite.fetch_indexed_file(
            joinurl(self.name, 'Contents-' + sarch),
        )
        return parse_contents(contents)

    def as_apt_source(self, deb='deb'):
        from .sources import AptSource
        return AptSource(
            deb=deb,
            options={},
            uri=self.archive.uri,
            suite=self.suite.name,
            components=[self.name],
        )

    ### TODO: def fetch_release_file(self):  # Rethink name
