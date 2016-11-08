""" Usage: aptrepo-suites [-F|--flat] {<uri> | <ppa>} [<subdir>]"""

import sys
from   .. import Archive, PPA

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-F', '--flat'):
        flat = True
        del sys.argv[1]
    else:
        flat = False
    if len(sys.argv) not in (2,3):
        sys.exit('Usage: {} [-F|--flat] {{<uri> | <ppa>}} [<subdir>]'
                 .format(sys.argv[0]))
    uri = sys.argv[1]
    if uri.startswith("ppa:"):
        uri = PPA(uri).uri
    subdir = sys.argv[2] if len(sys.argv) == 3 else None
    for suite in Archive(uri).scrape_suite_names(subdir=subdir, flat=flat):
        print(suite)

if __name__ == '__main__':
    main()
