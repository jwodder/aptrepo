""" Usage: aptrepo-packages [--arch ARCH] [--table] <repo-spec> """

import argparse
import json
from   prettytable import PrettyTable
from   ..          import FlatRepository, dpkg_architecture, for_json
from   .common     import get_component, verbosity

tblcols = ['Package', 'Version', 'Architecture', 'Description']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--arch')
    parser.add_argument('-d', '--distro')
    parser.add_argument('-T', '--table', action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    verbosity(args.verbose)
    repo = get_component(args)
    if isinstance(repo, FlatRepository):
        packages = repo.fetch_packages()
    else:
        packages = repo.fetch_packages(args.arch or dpkg_architecture())
    if args.table:
        tbl = PrettyTable(tblcols)
        tbl.align = 'l'
        for pkg in packages:
            pkg['Description'] = pkg['Description'].splitlines()[0]
            tbl.add_row([pkg[c] for c in tblcols])
        print(tbl.get_string())
    else:
        for pkg in packages:
            print(json.dumps(pkg, default=for_json))

if __name__ == '__main__':
    main()
