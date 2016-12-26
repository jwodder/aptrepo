from debian.deb822 import Packages, Sources
from .index        import IndexFile
from .internals    import parse_contents, joinurl, simple_repr

class Component:
    def __init__(self, suite, name):
        # not for public construction
        self.suite = suite
        self.name = name

    def __repr__(self):
        return simple_repr(self)

    def __eq__(self, other):
        return type(self) is type(other) and \
            self.suite == other.suite and \
            self.name == other.name

    @property
    def archive(self):
        return self.suite.archive

    def fetch_packages(self, arch):
        fp = self.suite.fetch_indexed_file(
            joinurl(self.name, 'binary-' + arch, 'Packages')
        )
        return Packages.iter_paragraphs(fp)

    def fetch_sources(self):
        fp = self.suite.fetch_indexed_file(
            joinurl(self.name, 'source', 'Sources')
        )
        return Sources.iter_paragraphs(fp)

    def fetch_i18n_index(self):
        dex = self.suite.fetch_indexed_file(joinurl(self.name, 'i18n', 'Index'))
        return IndexFile.parse(dex)

    def fetch_translation(self, lang):
        ### TODO: This won't work when the translation files aren't listed in
        ### the suite's Release
        fp = self.suite.fetch_indexed_file(
            joinurl(self.name, 'i18n', 'Translation-' + lang)
        )
        return Packages.iter_paragraphs(fp)

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

    ### TODO: def fetch_release_file(self):  # Rethink name
