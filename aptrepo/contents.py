from   collections import namedtuple
import re

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
