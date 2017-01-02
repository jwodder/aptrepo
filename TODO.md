- Add docstrings

Features
--------
- To support:
    - `$(ARCH)` in suite specifications
    - verifying PGP signatures
        - Give `Archive` and `Suite`/`FlatRepository` a `trusted_keys` (a list
          of PGP keys) attribute; the latter "inherit" their attribute values
          from the former
            - When `trusted_keys` is not defined, calls to `verify` use the
              system keyring in `/etc/apt`
        - Give `Suite`/`FlatRepository` (and/or `ReleaseFile`?) a
          `verify(trusted_keys=self.trusted_keys)` method
        - Change `Archive.fetch_suite`:
            - Option 1: Give `Archive.fetch_suite` `verify=BOOL` (default
              `True`?) and `trusted_keys=self.trusted_keys` parameters for
              specifying whether to call `verify` immediately after fetching
              the Release/InRelease file and optionally overriding the
              Archive's trusted keys
                - Also give `Archive` an `auto_verify` field for use as the
                  default value of `fetch_suite(verify=*)`?
            - Option 2: Rename `Archive.fetch_suite` to `__getitem__` and give
              `Archive` an `auto_verify=BOOL` attribute that determines whether
              `verify` is automatically called after fetching Release/InRelease
              files
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
- Add (more) logging
- Add a way to enable logging from the command line
- Allow accessing the elements of an `IndexFile`'s `fields` via attribute
  access on the `IndexFile` object?
    - This lookup should be case-insensitive and treat `_` as equivalent to `-`
- Add commands for fetching:
    - Contents files
    - architectures supported by a suite/component?
    - component release files?
    - list of available translations
- Support repositories like Chef's that name the "Components" field in Release
  files "Component"
- Make the unparsed fields of `ReleaseFile`s available somewhere?


Coding & Technologies
---------------------
- Can the downloading of Release, Packages, etc. files (without modifying the
  system cache) be outsourced to python-apt?
    - cf. `/usr/share/doc/python-apt/examples`?
- Use `apt_pkg.TagFile` from python-apt to parse control files instead of
  python-debian?
- It seems that python-debian can be used to parse Release files (including
  handling the PGP signature in InRelease files) and handle compressed files;
  look into this
- Read downloaded files into memory in their entirety instead of using
  temporary files?
    - No.  Uncompressed Packages files can be as large as 43 MB, and
      uncompressed Contents files can reach 1 GB.
- Set the User Agent used for HTTP requests?
- Give `IndexFile` a(n optional?) `baseurl` parameter?
- Define classes with [`attrs`](https://attrs.readthedocs.io)?
- Make the set of known hashes and compression algorithms configurable via
  `config.py`
- Make `Suite` into a `Mapping`?


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
