"""
repo-spec :=
    <uri> <suite> <component>
    <uri> <suite/>
    [--distro DISTRO] <ppa>
"""

import logging
import sys
from   .. import Archive, PPA

def get_suite(args):
    if len(args.repo) == 1 and args.repo[0].startswith("ppa:"):
        return PPA.from_specifier(args.repo[0]).repository(args.distro).suite
    elif getattr(args, 'distro', None) is not None:
        sys.exit('--distro can only be used with PPAs')
    elif len(args.repo) != 2:
        ### TODO: Improve:
        sys.exit('wrong number of arguments')
    return Archive(args.repo[0]).fetch_suite(args.repo[1])

def get_component(args):
    if len(args.repo) == 1 and args.repo[0].startswith("ppa:"):
        return PPA.from_specifier(args.repo[0]).repository(args.distro)
    elif getattr(args, 'distro', None) is not None:
        sys.exit('--distro can only be used with PPAs')
    elif len(args.repo) == 2 and args.repo[1].endswith('/'):
        return Archive(args.repo[0]).fetch_suite(args.repo[1])
    elif len(args.repo) == 3:
        return Archive(args.repo[0]).fetch_suite(args.repo[1])[args.repo[2]]
    else:
        ### TODO: Improve:
        sys.exit('wrong number of arguments')

def verbosity(lvl):
    if lvl < 1:
        return
    elif lvl == 1:
        log = logging.getLogger('aptrepo')
        log.setLevel(logging.INFO)
    elif lvl == 2:
        log = logging.getLogger()
        log.setLevel(logging.INFO)
    else:
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())
    logging.captureWarnings(True)
