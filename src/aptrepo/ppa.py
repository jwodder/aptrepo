import re
from   urllib.parse import quote
import attr
from   .archive     import Archive
from   .util        import ubuntu_release

@attr.s(frozen=True)
class PPA:
    owner = attr.ib()
    name  = attr.ib()

    @classmethod
    def from_specifier(cls, ppa_spec):
        # based on `softwareproperties.ppa.expand_ppa_line()`
        m = re.match(r'^ppa:([^/]+)(?:/([^/]+))?$', ppa_spec)
        if m:
            return cls(owner=m.group(1), name=m.group(2) or 'ppa')
        else:
            raise ValueError(f'invalid PPA specifier: {ppa_spec!r}')

    def __str__(self):
        return f'ppa:{self.owner}/{self.name}'

    @property
    def uri(self):
        return 'http://ppa.launchpad.net/{}/{}/ubuntu'.format(
            quote(self.owner),
            quote(self.name),
        )

    def repository(self, distro=None):
        if distro is None:
            distro = ubuntu_release()
        return Archive(self.uri).fetch_suite(distro)['main']

    def as_apt_source(self, distro=None, deb='deb'):
        from .sources import AptSource
        if distro is None:
            distro = ubuntu_release()
        return AptSource(
            deb=deb,
            options={},
            uri=self.uri,
            suite=distro,
            components=['main'],
        )
