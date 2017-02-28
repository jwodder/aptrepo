from   collections import namedtuple
import re
from   .archive    import Archive

class AptSource(namedtuple('AptSource', 'deb options uri suite components')):
    def __str__(self):
        sline = self.deb
        if self.options:
            sline += ' ' + ' '.join('{}={}'.format(k,v) if v is not None else k
                                    for k,v in self.options.items())
        sline += ' {0.uri} {0.suite}'.format(self)
        if self.components:
            sline += ' ' + ' '.join(self.components)
        return sline

    def repositories(self):
        ### TODO: Incorporate `options` (and `deb`?) somehow
        suite = Archive(self.uri).fetch_suite(self.suite)
        if self.suite.endswith('/'):
            return [suite]
        else:
            return [suite[c] for c in self.components]


def parse_sources(fp):
    for line in fp:
        line = line.partition('#')[0].strip()
        if not line:
            continue
        m = re.search(r'^(deb(?:-src)?)(?:\s+\[(.*?)\])?((?:\s+\S+){2,})$',
                      line)
        if m:
            deb, optstr, words = m.groups()
            options = {}
            if optstr is not None:
                for opt in optstr.split():
                    key, eq, value = opt.partition('=')
                    options[key] = value if eq == '=' else None
            words = words.split()
            yield AptSource(deb=deb, options=options, uri=words[0],
                            suite=words[1], components=words[2:])
        else:
            raise ValueError('{!r}: could not parse sources.list entry'
                             .format(line))
