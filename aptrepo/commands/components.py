"""
Usage:
    aptrepo-components <uri> <suite>
    aptrepo-components [--distro DISTRO] <ppa>
"""

import argparse
from   .common import get_suite, verbosity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    verbosity(args.verbose)
    ### TODO: Fail faster if the user specifies a flat repository?
    for c in get_suite(args).components:
        print(c.name)

if __name__ == '__main__':
    main()
