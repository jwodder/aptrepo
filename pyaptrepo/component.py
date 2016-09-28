from debian     import deb822
from .index     import Index
from .internals import parse_contents

class Component:
    def __init__(self, suite, name):
        # not for public construction
        self.suite = suite
        self.name = name

    @property
    def archive(self):
        return self.suite.archive

    def fetch_packages(self, arch):
        fp = self.suite.fetch_file(self.name + '/binary-' + arch + '/Packages')
        return deb822.Packages.iter_paragraphs(fp)

    def fetch_sources(self):
        fp = self.suite.fetch_file(self.name + '/source/Sources')
        return deb822.Sources.iter_paragraphs(fp)

    def fetch_translation(self, lang):
        ### TODO: This won't work when the translation files aren't listed in
        ### the suite's Release
        fp = self.suite.fetch_file(self.name + '/i18n/Translation-' + lang,
                                   extensions=('', '.bz2'))
        return deb822.Packages.iter_paragraphs(fp)

    @property
    def has_contents(self):
        # whether the Contents files are in the component or the suite
        return any(
            self.name + '/Contents-' + sarch + '.gz' in self.suite.files
            for sarch in ['source'] + self.suite.architectures
        )

    def fetch_contents(self, sarch):
        # Raises an error if the Contents files are at Suite level
        contents = self.suite.fetch_file(self.name + '/Contents-' + sarch,
                                         extensions=('.gz',))
            ### Include '' in extensions?
        return parse_contents(contents)

    def fetch_i18n_index(self):
        dex = self.suite.fetch_file(self.name + '/i18n/Index')
        return Index.parse(dex)

    ### def fetch_release_file(self):  # Rethink name
