import attr
from   property_manager import cached_property
from   .component       import Component
from   .contents        import parse_contents
from   .internals       import unprefix

@attr.s
class Suite:
    # not for public construction
    archive = attr.ib()
    name    = attr.ib()
    release = attr.ib()

    def __getitem__(self, component):
        return Component(self, component)

    @cached_property
    def components(self):
        return [
            Component(self, unprefix(self.name, c))
            for c in self.release.fields.get('components', [])
        ]

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
