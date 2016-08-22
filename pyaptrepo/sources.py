from   collections import namedtuple
import re

AptSource = namedtuple('AptSource', 'deb options uri suite components')

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
            raise ValueError('%r: could not parse source.list entry' % (line,))
