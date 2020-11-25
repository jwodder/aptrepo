"""
Usage:
    aptrepo-components <uri> <suite>
    aptrepo-components [--distro DISTRO] <ppa>
"""

import argparse
import sys
from   ..      import FlatRepository
from   .common import get_suite, verbosity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    verbosity(args.verbose)
    suite = get_suite(args)
    if isinstance(suite, FlatRepository):
        sys.exit("Flat repositories don't have components")
    for c in suite.components:
        print(c.name)

if __name__ == '__main__':
    main()
