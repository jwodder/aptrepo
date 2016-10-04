""" Usage: aptrepo-suites {<uri> | <ppa>} """

import sys
from   .. import Archive, PPA

def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: %s {<uri> | <ppa>}' % (sys.argv[0],))
    uri = sys.argv[1]
    if uri.startswith("ppa:"):
        uri = PPA(uri).uri
    for suite in Archive(uri).scrape_suite_names():
         print(suite)

if __name__ == '__main__':
    main()
