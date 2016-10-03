""" apt-repo packages [--arch ARCH] [--table] <repo-spec> """

import argparse
import json
from   prettytable import PrettyTable
from   ..          import dpkg_architecture, for_json
from   .common     import get_component

tblcols = ['Package', 'Version', 'Architecture', 'Description']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--arch')
    parser.add_argument('-d', '--distro')
    parser.add_argument('-T', '--table', action='store_true')
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()
    repo = get_component(args)
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
