from   collections import namedtuple
import re

def detach_signature(txt):
    # See RFC 4880, section 7
    # cf. debian.deb822.Deb822.split_gpg_and_payload (which doesn't handle dash
    # escaping and doesn't verify that the input is well-formed)
    m = re.match(r'^\s*-----BEGIN PGP SIGNED MESSAGE-----\n'
                 r'(?:[^\n]+\n)*'
                 r'\n'
                 r'(.*)\n'
                 r'-----BEGIN PGP SIGNATURE-----\n'
                 r'(.*)\n'
                 r'-----END PGP SIGNATURE-----\s*$',
                 re.sub(r'\r\n?', '\n', txt), flags=re.S)
    if m:
        ### TODO: Also return the armor headers?
        return (re.sub('^- ', '', m.group(1), flags=re.M).replace('\n', '\r\n'),
                m.group(2))
    else:
        return (txt, None)

### TODO: Export this:
ContentsPackage = namedtuple('ContentsPackage', 'area section name')

def parse_contents(fp):
    header = ''
    for line in fp:
        if re.match(r'^\s*FILE\s+LOCATION\s*$', line):
            break
        else:
            header += line
    files = {}
    for line in fp:
        m = re.search(r'\s+(\S+)$', line)
        if not m:
            continue
        filename = line[:m.start()]
        files[filename].setdefault([])
        for pkg in m.group(0).split(','):
            about = pkg.rsplit('/', 2)
            name = about.pop()
            section = about.pop() if about else None
            area = about.pop() if about else None
            files[filename].append(ContentsPackage(area, section, name))
    return (header, files)

def joinurl(url, *paths):
    if not url.endswith('/'):
        url += '/'
    return url + '/'.join(p.strip('/') for p in paths)

def simple_repr(obj):
    return '{}.{}({})'.format(
        __package__,
        obj.__class__.__name__,
        ', '.join('{}={!r}'.format(k,v) for k,v in vars(obj).items()),
    )
