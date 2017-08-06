- Add docstrings
- Determine the minimum necessary versions of chardet, property-manager, and
  python-apt needed
- Tag the code at each point it was stable?
- Give the commands `--version` options

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
        - Give `Archive.fetch_suite` `verify=BOOL` (default `True`?) and
          `trusted_keys=self.trusted_keys` parameters for specifying whether to
          call `verify` immediately after fetching the Release/InRelease file
          and optionally overriding the Archive's trusted keys
            - Also give `Archive` an `auto_verify` field for use as the default
              value of `fetch_suite(verify=*)`?
    - downloading files to disk and using them as local caches (including
      support for Valid-Until in Release files)
        - `.diff/Index` files
        - Look into how pip does its caching
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

- Give `PPA` methods for fetching data from Launchpad (pubkey, supported Ubuntu
  releases?, etc.)
- Add methods for actually downloading packages
    - Add a method/command for downloading the latest version of a given
      package in a given repository/set of repositories
- Add (more) logging
- Add commands for fetching:
    - Contents files
    - architectures supported by a suite/component?
- Support setting the architecture and Ubuntu release in a config file


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
- Give `IndexFile` a(n optional?) `baseurl` parameter?
- Make the set of known hashes and compression algorithms configurable via
  `config.py`
- Make the values in `config.py` be set & retrieved via functions/classes
  instead of directly as variables?
- Make `Suite` into a `Mapping`?
- Stop using `joinurl` to join relative paths?
- Give `Suite` and `FlatRepository` an `is_synonym`(?) method that compares
  `self` to another `Suite`/`FlatRepository` based solely on `release`
  attributes
- Export `Compression`?
- Rename `IndexFile`? (because that term technically includes Packages and
  Sources files, too, it seems)
- Test as much as possible
- Split the `sources.list` parsing into its own package?
- Use `pydpkg` instead of `python-debian`?
- Use `distro` to implement `ubuntu_release()`?  (It won't make a difference on
  Trusty)


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
    - Under what conditions are clients expected to use guess-and-check instead
      of indices in order to find out whether a file is available?
    - Look into APT's support for translation files in flat repositories
    - Do all non-flat repositories have nonempty Components fields in their
      Release files?
    - In suites whose names contain more than one directory level, regarding
      the fact that the suite's Release file may list component names "prefixed
      by parts of the path following the directory beneath dists":
        - Can component names listed in Release files ever be prefixed by some
          but not all of the aforementioned directories?
        - Can component names in `sources.list` lines also be prefixed in this
          way?
        - Can component names ever contain multiple directory levels in their
          own right, even having directory names that overlap with those in the
          suite's name?
        - How are component names in component-specific Release files listed?
