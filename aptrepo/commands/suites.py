""" Usage: aptrepo-suites [-F|--flat] {<uri> | <ppa>} [<subdir>]"""

import argparse
from   ..      import Archive, PPA
from   .common import verbosity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', '--flat', action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('uri')
    parser.add_argument('subdir', nargs='?')
    args = parser.parse_args()
    verbosity(args.verbose)
    if args.uri.startswith("ppa:"):
        args.uri = PPA.from_specifier(args.uri).uri
    for suite in Archive(args.uri)\
                    .scrape_suite_names(subdir=args.subdir, flat=args.flat):
        print(suite)

if __name__ == '__main__':
    main()
