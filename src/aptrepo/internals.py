from   pathlib import PurePosixPath
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

def joinurl(url, *paths):
    if not url.endswith('/'):
        url += '/'
    return url + '/'.join(p.strip('/') for p in paths)

def unprefix(suite, component):
    """
    If ``component`` begins with one or more path components (excluding the
    last) that also occur at the end of ``suite`` (excluding the first), remove
    the prefix from ``component`` and return the remainder.

    This function is used for removing prefixes that may occur in component
    names listed in suite Release files when the suite name contains multiple
    path components.

    >>> unprefix('stable', 'main')
    'main'

    >>> unprefix('stable/updates', 'updates/main')
    'main'

    >>> unprefix('stable/updates', 'main')
    'main'

    >>> unprefix('trusty', 'trusty/main')
    'trusty/main'

    >>> unprefix('foo', 'foo')
    'foo'

    >>> unprefix('foo', 'foo/bar')
    'foo/bar'

    >>> unprefix('foo/bar', 'bar')
    'bar'
    """
    suite = PurePosixPath(suite)
    component = PurePosixPath(component)
    for i in range(min(len(suite.parts), len(component.parts))):
        if suite.parts[-(i+1):] != component.parts[:i+1]:
            break
    return str(PurePosixPath(*component.parts[i:]))
