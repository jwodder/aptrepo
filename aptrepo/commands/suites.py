""" Usage: aptrepo-suites {<uri> | <ppa>} [<subdir>]"""

import sys
from   .. import Archive, PPA

def main():
    if len(sys.argv) not in (2,3):
        sys.exit('Usage: {} {{<uri> | <ppa>}} [<subdir>]'.format(sys.argv[0]))
    uri = sys.argv[1]
    if uri.startswith("ppa:"):
        uri = PPA(uri).uri
    subdir = sys.argv[2] if len(sys.argv) == 3 else None
    for suite in Archive(uri).scrape_suite_names(subdir=subdir):
        print(suite)

if __name__ == '__main__':
    main()
