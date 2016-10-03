"""
Usage:
    apt-repo components <uri> <suite>
    apt-repo components [--distro DISTRO] <ppa>
"""

import argparse
from   .common import get_suite

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    for c in get_suite(args).components:
        print(c.name)

if __name__ == '__main__':
    main()