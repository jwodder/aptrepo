""" Usage: aptrepo-sources <repo-spec> """

import argparse
import json
from   ..      import for_json
from   .common import get_component, verbosity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    verbosity(args.verbose)
    for src in get_component(args).fetch_sources():
        print(json.dumps(src, default=for_json))

if __name__ == '__main__':
    main()
