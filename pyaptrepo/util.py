import collections
from   datetime    import datetime
import re
import subprocess

def dpkg_architecture():
    # cf. <https://deb-pkg-tools.readthedocs.io/en/latest/#deb_pkg_tools.utils.find_debian_architecture>
    return subprocess.check_output(['dpkg', '--print-architecture'],
                                   universal_newlines=True).strip()

def dpkg_foreign_architectures():
    return subprocess.check_output(['dpkg', '--print-foreign-architectures'],
                                   universal_newlines=True).splitlines()

def for_json(obj):
    if hasattr(obj, 'for_json'):
        return obj.for_json()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, collections.Mapping):
        # This includes all types in debian.deb822.
        return dict(obj)
    elif isinstance(obj, (collections.Iterator, tuple, set, frozenset)):
        ### Sort sets and frozensets?
        return list(obj)
    else:
        try:
            data = vars(obj).copy()
        except TypeError:
            return repr(obj)
        else:
            data["__class__"] = type(obj).__name__
            return data

def package2dict(pkg):
    # `pkg` must be a deb822.Packages object
    data = {k.lower(): v for k,v in pkg.items()}
    data.update(pkg.relations)
    if 'essential' in data and data['essential'].lower() in ('no', 'yes'):
        data['essential'] = (data['essential'].lower() == 'yes')
    if 'size' in data:
        data['size'] = int(data['size'])
    if 'installed-size' in data:
        data['installed-size'] = int(data['installed-size'])
    if 'tag' in data:
        data['tag'] = re.split(r'\s*,\s*', data['tag'])
    if 'task' in data:
        data['task'] = re.split(r'\s*,\s*', data['task'])
    if 'uploaders' in data:
        data['uploaders'] = re.split(r'\s*,\s*', data['uploaders'])
    return data
