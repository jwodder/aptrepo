- Write a README
- Add docstrings

Features
--------
- To support:
    - `$(ARCH)` in suite specifications
    - getting a list of available translations from i18n/Index files
    - verifying PGP signatures
        - Possible API:
            - Give `Archive` and `Suite`/`FlatRepository` a `trusted_keys`
              attribute; the latter "inherit" their attribute values from the
              former
                - When `trusted_keys` is not defined, calls to `verify` use the
                  system keyring in `/etc/apt`
            - Give `Suite`/`FlatRepository` (and/or `ReleaseFile`?) a
              `verify(trusted_keys=self.trusted_keys)` method
            - Give `Archive` an `auto_verify=BOOL` attribute that determines
              whether `verify` is automatically called after fetching
              Release/InRelease files
            - Rename `fetch_suite` to `__getitem__`
    - downloading files to disk and using them as local caches (including
      support for Valid-Until in Release files)
        - `.diff/Index` files
    - parsing the system's sources.list?
        - Use `apt_pkg.config` to get the locations of sources.list and
          sources.list.d
    - RFC 822-style sources.list entries
    - .lz compression
    - acquiring by hash

- Hash checking:
    - Emit a warning if a set of hashes passed to a function contains only
      non-SHA2 digests?
    - Give `fetch_indexed_file` an argument for specifying what hash
      algorithms/the "minimum" hash algorithm to use
        - Make `copy_and_hash` use whatever hashes it's given instead of
          filtering out the non-SHA2 ones
    - Add a way to fetch a file without checking its hashes?
    - Add an option for downgrading hash mismatch errors to warnings?
        - Downgrade by default?
    - If a hash mismatch occurs, continue trying to fetch the other compressed
      forms of the same file and only raise an error if they all fail

- Give Component a method for converting to a sources.list entry or
  representation thereof
- Give Component a method for getting the language codes for all available
  translations
- Give PPA methods for fetching data from Launchpad (pubkey, supported Ubuntu
  releases?, etc.)
- Add methods for actually downloading packages
    - Add a method/command for downloading the latest version of a given
      package in a given repository/set of repositories
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
- `aptrepo-suites`: Support searching for flat repositories


Coding & Technologies
---------------------
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
    - No.  Uncompressed Packages files can be as large as 43 MB, and
      uncompressed Contents files can reach 1 GB.
- Give all of the classes `__repr__` (and `__eq__`?) methods
- Use `requests-toolbelt` <https://toolbelt.readthedocs.io> to:
    - rewrite `copy_and_hash` (for reading HTTP responses, at least)
        - <https://toolbelt.readthedocs.io/en/latest/downloadutils.html#requests_toolbelt.downloadutils.tee.tee>
        - This will work out best if I can find an incremental Gzip decoder
    - automatically prepend the base URI to requests
        - <https://toolbelt.readthedocs.io/en/latest/sessions.html>
    - set the User Agent

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
    - Look into APT's support for translation files in flat repositories
    - Do all non-flat repositories have nonempty Components fields in their
      Release files?
