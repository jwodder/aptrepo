""" Usage: aptrepo-translation <lang> <repo-spec> """

import argparse
import json
import sys
from   ..      import FlatRepository, for_json
from   .common import get_component

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--distro')
    parser.add_argument('lang')
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    repo = get_component(args)
    if isinstance(repo, FlatRepository):
        sys.exit('Translations in flat repositories are not yet supported')
    else:
        for desc in repo.fetch_translation(args.lang):
            print(json.dumps(desc, default=for_json))

if __name__ == '__main__':
    main()
