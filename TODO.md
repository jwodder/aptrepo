- Write a README
- Add docstrings

Features
--------
- To support:
    - `$(ARCH)` in suite specifications
    - getting a list of available translations from i18n/Index files
    - verifying PGP signatures
    - downloading files to disk and using them as local caches (including
      support for Valid-Until in Release files)
        - `.diff/Index` files
    - parsing the system's sources.list?
        - Use `apt_pkg.config` to get the locations of sources.list and
          sources.list.d
    - RFC 822-style sources.list entries
    - .lz compression
    - acquiring by hash

- Emit a warning if a set of hashes passed to a function contains only non-SHA2
  digests?
- Give Component a method for converting to a sources.list entry or
  representation thereof
- Give Component a method for getting the language codes for all available
  translations
- Give PPA methods for fetching data from Launchpad (pubkey, supported Ubuntu
  releases?, etc.)
- Add methods for actually downloading packages
    - Add a method/command for downloading the latest version of a given
      package in a given repository/set of repositories
- Give `fetch_indexed_file` an argument for specifying what hash algorithms/the
  "minimum" hash algorithm to use
    - Make `copy_and_hash` use whatever hashes it's given instead of filtering
      out the non-SHA2 ones
- Add a way to fetch a file without checking its hashes
- Add logging
- Add a `Contents` class with a `__getitem__` method?
- Allow accessing the elements of an `Index`'s `fields` via attribute access on
  the `Index` object?
    - This lookup should be case-insensitive and treat `_` as equivalent to `-`
- Add commands for fetching:
    - Contents files
    - architectures supported by a suite/component?
    - component release files?
    - list of available translations
- `aptrepo-release`: Support flat repositories
- `aptrepo-suites`: Support searching for flat repositories


Coding & Technologies
---------------------
- Use `aptsources.sourceslist.SourceEntry` from python-apt for parsing
  sources.list entries?  (Downside: The API is terrible.)
- Can the downloading of Release, Packages, etc. files (without modifying the
  system cache) be outsourced to python-apt?
    - cf. `/usr/share/doc/python-apt/examples`?
- Use `apt_pkg.TagFile` from python-apt to parse control files instead of
  python-debian?
- Write my own control file parser, thereby completely eliminating the
  dependency on python-debian?
- It seems that python-debian can be used to parse Release files (including
  handling the PGP signature in InRelease files) and handle compressed files;
  look into this
- Read downloaded files into memory in their entirely instead of using
  temporary files?

Research
--------
- Double-check the format of `sources.list` entries with options

- Important unanswered questions about the repository format:
    - What is the purpose of Release files in `binary-$ARCH/` and `source/`
      directories?  What distributions use them?
    - Can Release files be compressed?
    - Can component names contain slashes?
    - Can a Release file list only the hashes for the uncompressed form of a
      file even when the server only provides compressed forms?
    - Under what conditions do `i18n/` directories not contain an `Index` file?
    - Under what conditions are individual Translations files listed in the
      suite's Release file?
    - Under what conditions are clients expected to use guess-and-check instead
      of indices in order to find out whether a file is available?
    - Do repositories always have nonempty Component fields in their Release
      files if & only if they are not flat?
    - Look into APT's support for translation files in flat repositories
