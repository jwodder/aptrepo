"""
repo-spec :=
    <uri> <suite> <component>
    [--distro DISTRO] <ppa>
"""

from .. import Archive, PPA

def get_archive(args):
    if len(args.repo) == 1 and args.repo[0].startswith("ppa:"):
        return Archive(PPA(args.repo[0]).uri)
    elif getattr(args, 'distro', None) is not None:
        raise SystemExit('--distro can only be used with PPAs')
    elif len(args.repo) != 1:
        ### TODO: Improve:
        raise SystemError('wrong number of arguments')
    return Archive(args.repo[0])

def get_suite(args):
    if len(args.repo) == 1 and args.repo[0].startswith("ppa:"):
        return PPA(args.repo[0]).repository(args.distro).suite
    elif getattr(args, 'distro', None) is not None:
        raise SystemExit('--distro can only be used with PPAs')
    elif len(args.repo) != 2:
        ### TODO: Improve:
        raise SystemError('wrong number of arguments')
    return Archive(args.repo[0]).fetch_suite(args.repo[1])

def get_component(args):
    if len(args.repo) == 1 and args.repo[0].startswith("ppa:"):
        return PPA(args.repo[0]).repository(args.distro)
    elif getattr(args, 'distro', None) is not None:
        raise SystemExit('--distro can only be used with PPAs')
    elif len(args.repo) != 3:
        ### TODO: Improve:
        raise SystemError('wrong number of arguments')
    return Archive(args.repo[0]).fetch_suite(args.repo[1])[args.repo[2]]
