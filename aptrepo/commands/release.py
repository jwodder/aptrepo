"""
Usage:
    apt-repo release <uri> <suite>
    apt-repo release [--distro DISTRO] <ppa>
"""

import argparse
import json
from   ..      import for_json
from   .common import get_suite

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    print(json.dumps(get_suite(args).release, default=for_json))

if __name__ == '__main__':
    main()
