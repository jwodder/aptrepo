import platform
import re
from   .archive import Archive

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

    @property
    def specifier(self):  ### Look for proper term
        ### Use this as __str__?
        return 'ppa:{0.owner}/{0.name}'.format(self)

    @property
    def uri(self):
        ### Perform URL escaping?
        return 'http://ppa.launchpad.net/{0.owner}/{0.name}/ubuntu'.format(self)

    def repository(self, distro=None):
        if distro is None:
            ### Use `lsb_release` (the command or the Python module) instead?
            distro = platform.linux_distribution()[2]
        return Archive(self.uri).fetch_suite(distro)['main']

    ### TODO: Add __repr__ and __eq__ methods
