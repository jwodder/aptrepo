""" apt-repo translation <lang> <repo-spec> """

import argparse
import json
from   ..      import for_json
from   .common import get_component

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('lang')
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    for desc in get_component(args).fetch_translation(args.lang):
        print(json.dumps(desc, default=for_json))

if __name__ == '__main__':
    main()
