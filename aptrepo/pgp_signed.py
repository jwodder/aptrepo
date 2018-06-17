from   collections import defaultdict
import re
import attr

@attr.s(hash=False)
class PGPSigned:
    body      = attr.ib()
    headers   = attr.ib()
    signature = attr.ib()

    def verify(self, trusted_keys=None):
        raise NotImplementedError

        subprocess.check_call([
            'gpg',
            '--verify',
            '--trusted-key', ... ,
            '--trust-model', 'direct',  ### ???

            ??? signature,
            ??? body,
        ])

    @classmethod
    def from_cleartext(cls, txt):
        # See RFC 4880, section 7
        # cf. debian.deb822.Deb822.split_gpg_and_payload (which doesn't handle
        # dash escaping and doesn't verify that the input is well-formed)
        m = re.match(
            r'^\s*-----BEGIN PGP SIGNED MESSAGE-----\n'
            r'(?P<headers>(?:[^\n]+?: [^\n]*\n)*)'
            r'\n'
            r'(?P<body>.*)\n'
            r'(?P<signature>-----BEGIN PGP SIGNATURE-----\n'
            r'.*\n'
            r'-----END PGP SIGNATURE-----)\s*$',
            re.sub(r'\r\n?', '\n', txt),
            flags=re.S,
        )
        if m:
            body = re.sub('^- ', '', m.group('body'), flags=re.M)\
                     .replace('\n', '\r\n')
            headers = defaultdict(list)
            for head in m.group('headers').splitlines():
                k, _, v = head.partition(': ')
                headers[k].append(v)
            return cls(body, headers, m.group('signature'))
        else:
            raise ValueError('invalid/malformed cleartext signature')
