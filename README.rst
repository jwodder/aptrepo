.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP - Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://img.shields.io/github/license/jwodder/aptrepo.svg?maxAge=2592000
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/aptrepo>`_
| `Issues <https://github.com/jwodder/aptrepo/issues>`_

``aptrepo`` is a work-in-progress attempt at a pure Python library for fetching
data from arbitrary APT repositories (without having to add them to your
``sources.list`` first).  Currently, its main attractions are the programs in
its command-line interface:

::

    aptrepo-components <uri> <suite>
    aptrepo-components [-d|--distro DISTRO] <ppa>

List the components (a.k.a. "sections" or "areas") available in the given suite

::

    aptrepo-packages [-a|--arch ARCH] [-T|--table] <uri> <suite> <component>
    aptrepo-packages [-T|--table] <uri> <suite/>
    aptrepo-packages [-a|--arch ARCH] [-d|--distro DISTRO] [-T|--table] <ppa>

List the packages provided by the given repository for the given architecture
as a stream of JSON objects.  If the ``--table`` option is supplied, the output
will be in the form of a text table instead.

::

    aptrepo-release <uri> <suite>
    aptrepo-release <uri> <suite/>
    aptrepo-release [-d|--distro DISTRO] <ppa>

Output the contents of the suite's ``Release`` or ``InRelease`` file as a JSON
object

::

    aptrepo-sources <uri> <suite> <component>
    aptrepo-sources <uri> <suite/>
    aptrepo-sources [-d|--distro DISTRO] <ppa>

List the source packages provided by the given repository as a stream of JSON
objects

::

    aptrepo-suites [-F|--flat] {<uri> | <ppa>} [<subdir>]

Try to determine the suites available in the given archive by scraping the
index page of the archive's ``/dists`` directory (or a given subdirectory
beneath it).  If the ``--flat`` option is given, ``aptrepo-suites`` will
instead scrape the archive's main URI (or a given subdirectory beneath it).

::

    aptrepo-translation list <uri> <suite> <component>
    aptrepo-translation list <uri> <suite/>
    aptrepo-translation list [-d|--distro DISTRO] <ppa>

List the language codes of the available package description translations in
the given repository

::

    aptrepo-translation get <lang> <uri> <suite> <component>
    aptrepo-translation get <lang> <uri> <suite/>
    aptrepo-translation [-d|--distro DISTRO] <lang> <ppa>

Fetch the package description translations for the given language code from the
given repository


All commands also take a ``-v`` or ``--verbose`` option that can be given one
or more times to enable INFO or DEBUG logging.


Installation
============
``aptrepo`` requires Python 3.4 or higher.  Just use version 6.0 or higher of
`pip <https://pip.pypa.io/>`_ for Python 3 (You have pip, right?) to install
``aptrepo`` and its dependencies::

    pip3 install git+https://github.com/jwodder/aptrepo.git

Installing inside a `virtual environment
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ is recommended,
especially on pre-16.04 versions of Ubuntu where the ``python-debian`` Python
package installed by the system's ``python3-debian`` Debian package is too old
for ``aptrepo``'s needs.
