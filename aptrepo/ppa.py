import platform
import re
from   urllib.parse import quote
from   .archive     import Archive
from   .internals   import simple_repr

class PPA:
    def __init__(self, ppa_spec=None, owner=None, name=None):
        if ppa_spec is not None:
            if owner is not None or name is not None:
                raise TypeError('Constructor takes ppa_spec XOR owner & name')
            # based on `softwareproperties.ppa.expand_ppa_line()`
            m = re.match(r'^ppa:([^/]+)(?:/([^/]+))?$', ppa_spec)
            if m:
                self.owner = m.group(1)
                self.name = m.group(2) or 'ppa'
            else:
                raise ValueError('invalid PPA specifier: {!r}'.format(ppa_spec))
        elif owner is not None and name is not None:
            self.owner = owner
            self.name = name
        else:
            raise TypeError('Constructor takes ppa_spec XOR owner & name')

    def __str__(self):
        return 'ppa:{0.owner}/{0.name}'.format(self)

    def __repr__(self):
        return simple_repr(self)

    def __eq__(self, other):
        return type(self) is type(other) and \
            self.owner == other.owner and \
            self.name == other.name

    @property
    def uri(self):
        return 'http://ppa.launchpad.net/{}/{}/ubuntu'.format(
            quote(self.owner),
            quote(self.name),
        )

    def repository(self, distro=None):
        if distro is None:
            ### TODO: Use `lsb_release` (the command or the Python module)
            ### instead?
            distro = platform.linux_distribution()[2]
        return Archive(self.uri).fetch_suite(distro)['main']
