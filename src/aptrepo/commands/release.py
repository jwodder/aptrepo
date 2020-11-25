"""
Usage:
    aptrepo-release <uri> <suite>
    aptrepo-release <uri> <suite/>
    aptrepo-release [--distro DISTRO] <ppa>
"""

import argparse
import json
from   ..      import for_json
from   .common import get_suite, verbosity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    verbosity(args.verbose)
    print(json.dumps(get_suite(args).release, default=for_json))

if __name__ == '__main__':
    main()
