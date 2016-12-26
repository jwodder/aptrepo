from debian.deb822 import Packages, Sources
from .internals    import simple_repr

class FlatRepository:
    def __init__(self, archive, name, release):
        self.archive = archive
        self.name = name
        self.release = release

    def __repr__(self):
        return simple_repr(self)

    def __eq__(self, other):
        # for use in detecting suite synonyms/symlinks
        return type(self) is type(other) and self.release == other.release

    def fetch_indexed_file(self, basepath):
        return self.archive.fetch_indexed_file(
            '/' + self.name,
            basepath,
            self.release,
        )

    def fetch_packages(self):
        fp = self.fetch_indexed_file('Packages')
        return Packages.iter_paragraphs(fp)

    def fetch_sources(self):
        fp = self.fetch_indexed_file('Sources')
        return Sources.iter_paragraphs(fp)

    @property
    def architectures(self):
        return self.release.fields.get('architectures', [])

    @property
    def acquire_by_hash(self):
        ### TODO: Do flat repositories even support Acquire By Hash?
        return self.release.fields.get('acquire-by-hash', False)
