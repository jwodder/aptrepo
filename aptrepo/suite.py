from   .component import Component
from   .internals import parse_contents, simple_repr

class Suite:
    def __init__(self, archive, name, release):
        # not for public construction
        self.archive = archive
        self.name = name
        self.release = release
        self.components = [
            Component(self, c) for c in self.release.fields.get('components',[])
        ]

    def __repr__(self):
        return simple_repr(self)

    def __eq__(self, other):
        # for use in detecting suite synonyms/symlinks
        return type(self) is type(other) and self.release == other.release

    def __getitem__(self, component):
        return Component(self, component)

    @property
    def architectures(self):
        return self.release.fields.get('architectures', [])

    @property
    def acquire_by_hash(self):
        return self.release.fields.get('acquire-by-hash', False)

    @property
    def has_contents(self):
        # whether the Contents files are in the suite or the component
        return any(
            'Contents-' + sarch + '.gz' in self.release.files
            for sarch in ['source'] + self.architectures
        )

    def fetch_contents(self, sarch):
        contents = self.fetch_indexed_file('Contents-' + sarch)
        return parse_contents(contents)

    def fetch_indexed_file(self, basepath):
        return self.archive.fetch_indexed_file(
            '/dists/' + self.name,
            basepath,
            self.release,
        )
