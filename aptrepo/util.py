import collections
from   datetime   import datetime
from   subprocess import check_output

def dpkg_architecture():
    # cf. <https://deb-pkg-tools.readthedocs.io/en/latest/#deb_pkg_tools.utils.find_debian_architecture>
    return check_output(
        ['dpkg', '--print-architecture'],
        universal_newlines=True,
    ).strip()

def dpkg_foreign_architectures():
    return check_output(
        ['dpkg', '--print-foreign-architectures'],
        universal_newlines=True,
    ).splitlines()

def for_json(obj):
    if hasattr(obj, 'for_json'):
        return obj.for_json()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, collections.Mapping):
        # This includes all types in debian.deb822.
        return {str(k): obj[k] for k in obj}
    elif isinstance(obj, (collections.Iterator, tuple, set, frozenset)):
        ### TODO: Sort sets and frozensets?
        return list(obj)
    else:
        try:
            data = vars(obj).copy()
        except TypeError:
            return repr(obj)
        else:
            data["__class__"] = type(obj).__name__
            return data

def ubuntu_release():
    ### TODO: Support Ubuntu derivatives somehow
    # See <http://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/lsbrelease.html> for specification
    lsb_release = check_output(['lsb_release', '-ic'], universal_newlines=True)
    relinfo = dict(line.split('\t') for line in lsb_release.splitlines())
    if relinfo['Distributor ID:'] != 'Ubuntu':
        raise RuntimeError('not running on Ubuntu')
    return relinfo['Codename:']
