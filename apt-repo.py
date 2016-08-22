#!/usr/bin/python3
"""
Usage:
    apt-repo suites {<uri> | <ppa>}

    apt-repo release <uri> <suite>
    apt-repo release [--distro DISTRO] <ppa>

    apt-repo components <uri> <suite>
    apt-repo components [--distro DISTRO] <ppa>

    apt-repo packages [--arch ARCH] [--table] <repo-spec>

    apt-repo sources <repo-spec>

    apt-repo translation <lang> <repo-spec>

repo-spec :=
    <uri> <suite> <component>
    [--distro DISTRO] <ppa>
"""

# TO ADD:
# - something for Contents
# - something for getting architectures? (suite- or component-level?)
# - something for component release files???
# - something for listing available translations
# - support for repo-specs of the following forms:
#  - <uri> <suite/>
#  - '[deb[-src]] <uri> <suite/>'
#  - '[deb[-src]] <uri> <suite> <component>'

import argparse
import json
from   prettytable import PrettyTable
from   pyaptrepo   import Archive, PPA, dpkg_architecture, for_json

tblcols = ['Package', 'Version', 'Architecture', 'Description']

def main():
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title='command', dest='cmd')

    cmd_show = cmds.add_parser('suites')
    cmd_show.add_argument('repo', nargs='+')

    cmd_release = cmds.add_parser('release')
    cmd_release.add_argument('-d', '--distro')
    cmd_release.add_argument('repo', nargs='+')

    cmd_comps = cmds.add_parser('components')
    cmd_comps.add_argument('-d', '--distro')
    cmd_comps.add_argument('repo', nargs='+')

    cmd_pkgs = cmds.add_parser('packages')
    cmd_pkgs.add_argument('--arch')
    cmd_pkgs.add_argument('-d', '--distro')
    cmd_pkgs.add_argument('-T', '--table', action='store_true')
    cmd_pkgs.add_argument('repo', nargs='+')

    cmd_srcs = cmds.add_parser('sources')
    cmd_srcs.add_argument('-d', '--distro')
    cmd_srcs.add_argument('repo', nargs='+')

    cmd_trans = cmds.add_parser('translation')
    cmd_trans.add_argument('-d', '--distro')
    cmd_trans.add_argument('lang')
    cmd_trans.add_argument('repo', nargs='+')

    args = parser.parse_args()

    if args.cmd == 'suites':
        base = get_repo(args, level=1)
        for suite in base.scrape_suite_names():
            print(suite)

    elif args.cmd == 'release':
        suite = get_repo(args, level=2)
        print(json.dumps(suite.release, default=for_json))

    elif args.cmd == 'components':
        suite = get_repo(args, level=2)
        for c in suite.components:
            print(c.name)

    elif args.cmd == 'packages':
        repo = get_repo(args)
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

    elif args.cmd == 'sources':
        repo = get_repo(args)
        for src in repo.fetch_sources():
            print(json.dumps(src, default=for_json))

    elif args.cmd == 'translation':
        repo = get_repo(args)
        for desc in repo.fetch_translation(args.lang):
            print(json.dumps(desc, default=for_json))

    else:
        assert False, 'No path defined for command {0!r}'.format(args.cmd)


def get_repo(args, level=3):
    assert 1 <= level <= 3
    if len(args.repo) == 1 and args.repo[0].startswith("ppa:"):
        ppa = PPA(args.repo[0])
        if level == 1:
            return Archive(ppa.uri)
        elif level == 2:
            return ppa.repository(args.distro).suite
        elif level == 3:
            return ppa.repository(args.distro)
    elif getattr(args, 'distro', None) is not None:
        raise SystemExit('--distro can only be used with PPAs')
    elif len(args.repo) != level:
        ### TODO: Improve:
        raise SystemError('wrong number of arguments')
    repo = Archive(args.repo[0])
    if level > 1:
        repo = repo.fetch_suite(args.repo[1])
        if level > 2:
            repo = repo[args.repo[2]]
    return repo

if __name__ == '__main__':
    main()
