from   os.path    import dirname, join
import re
from   setuptools import setup, find_packages

with open(join(dirname(__file__), 'aptrepo', '__init__.py')) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError('Unable to find own __version__ string')

with open(join(dirname(__file__), 'README.rst')) as fp:
    long_desc = fp.read()

setup(
    name='aptrepo',
    version=version,
    packages=find_packages(),
    license='MIT',
    author='John Thorvald Wodder II',
    author_email='aptrepo@varonathe.org',
    keywords='apt dpkg deb debian packaging apt-get repository ppa',
    description='Examining & traversing APT repositories',
    long_description=long_desc,
    url='https://github.com/jwodder/aptrepo',
    python_requires='~=3.4',

    install_requires=[
        'attrs~=17.1',
        'beautifulsoup4~=4.4',
        # python-debian needs chardet, but it doesn't list it in its setup.py!
        'chardet',
        'prettytable>=0.7.2,<1',
        'property-manager',
        'python-debian>=0.1.23',
        'requests~=2.2',
    ],

    extras_require={
        "libapt": ['python-apt'],
        # Note: Installing python-apt from source requires libapt-pkg-dev,
        # intltool, and <https://launchpad.net/python-distutils-extra> (which
        # isn't even on PyPI!)
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'License :: OSI Approved :: MIT License',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Software Distribution',
    ],

    entry_points={
        "console_scripts": [
            'aptrepo-components = aptrepo.commands.components:main',
            'aptrepo-packages = aptrepo.commands.packages:main',
            'aptrepo-release = aptrepo.commands.release:main',
            'aptrepo-sources = aptrepo.commands.sources:main',
            'aptrepo-suites = aptrepo.commands.suites:main',
            'aptrepo-translation = aptrepo.commands.translation:main',
        ]
    },
)
