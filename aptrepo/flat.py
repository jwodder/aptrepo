import attr
from   debian.deb822 import Packages, Sources

@attr.s
class FlatRepository:
    # not for public construction
    archive = attr.ib()
    name    = attr.ib()
    release = attr.ib()

    def fetch_indexed_file(self, basepath):
        return self.archive.fetch_indexed_file(
            '/' + self.name,
            basepath,
            self.release,
        )

    def fetch_packages(self):
        fp = self.fetch_indexed_file('Packages')
        return Packages.iter_paragraphs(fp, use_apt_pkg=True)

    def fetch_sources(self):
        fp = self.fetch_indexed_file('Sources')
        return Sources.iter_paragraphs(fp, use_apt_pkg=True)

    @property
    def architectures(self):
        return self.release.fields.get('architectures', [])

    @property
    def acquire_by_hash(self):
        ### TODO: Do flat repositories even support Acquire By Hash?
        return self.release.fields.get('acquire-by-hash', False)

    def as_apt_source(self, deb='deb'):
        from .sources import AptSource
        return AptSource(
            deb=deb,
            options={},
            uri=self.archive.uri,
            suite=self.suite.name,
            components=[],
        )
