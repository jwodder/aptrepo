"""
Usage:
    aptrepo-translation list <repo-spec>
    aptrepo-translation get <lang> <repo-spec>
"""

import argparse
import json
import sys
from   ..      import FlatRepository, for_json
from   .common import get_component, verbosity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    cmds = parser.add_subparsers(title='command', dest='cmd')
    cmd_list = cmds.add_parser('list')
    cmd_list.add_argument('-d', '--distro')
    cmd_list.add_argument('repo', nargs='+')
    cmd_get = cmds.add_parser('get')
    cmd_get.add_argument('-d', '--distro')
    cmd_get.add_argument('lang')
    cmd_get.add_argument('repo', nargs='+')
    args = parser.parse_args()
    verbosity(args.verbose)
    repo = get_component(args)
    if isinstance(repo, FlatRepository):
        sys.exit('Translations in flat repositories are not yet supported')
    elif args.cmd == 'list':
        for lang in sorted(repo.available_translations()):
            print(lang)
    elif args.cmd == 'get':
        for desc in repo.fetch_translation(args.lang):
            print(json.dumps(desc, default=for_json))
    else:
        assert False, f'No path defined for command {args.cmd!r}'

if __name__ == '__main__':
    main()
