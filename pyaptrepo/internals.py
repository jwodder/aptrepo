from   collections import namedtuple
import hashlib
import re
import shutil
import requests
from   .errors     import HashMismatchError

SHA2 = ("sha224", "sha256", "sha384", "sha512")

def copy_and_hash(fpin, fpout, filename, hashes, chunk_size=2048):
    digestion = {alg: hashlib.new(alg) for alg in SHA2 if alg in hashes}
    if digestion or isinstance(fpin, requests.Response):
        if isinstance(fpin, requests.Response):
            # `iter_content` needs to be used instead of `.raw.read` in order
            # to handle gzipped/deflated content transfer encodings.
            stream = fpin.iter_content(chunk_size)
        else:
            stream = iter(lambda: fpin.read(chunk_size), b'')
        ### TODO: If `isinstance(fpout, BinaryIO)`, just read the whole input
        ### at once instead of in chunks.
        for chunk in stream:
            for h in digestion.values():
                h.update(chunk)
            fpout.write(chunk)
        for alg, h in digestion.items():
            check = h.hexdigest()
            if hashes[alg] != check:
                raise HashMismatchError(filename, alg, hashes[alg], check)
    else:
        shutil.copyfileobj(fpin, fpout)

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
        ### Also return the armor headers?
        return (re.sub('^- ', '', m.group(1), flags=re.M).replace('\n', '\r\n'),
                m.group(2))
    else:
        return (txt, None)

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

def massage_index(index):
    """
    Given a `dict` with "md5sum", "sha1", etc. fields as would be found in a
    Release file, combine the fields into a single "files" sub-`dict` that maps
    filenames to sub-sub-`dict`s of sizes & checksums
    """
    files = {}
    for field in ("md5sum", "sha1", "sha224", "sha256", "sha384", "sha512"):
        hashlist = index.pop(field, '')
        for line in hashlist.splitlines():
            if line.strip() != '':
                # Filenames will never contain spaces, right?
                hashsum, size, filename = line.split()
                size = int(size)
                if filename in files:
                    assert files[filename]["size"] == size
                else:
                    files[filename] = {"size": size}
                if field == "md5sum":
                    field = "md5"
                files[filename][field] = hashsum.lower()
    index["files"] = files
