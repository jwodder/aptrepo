    $ARCHIVE_ROOT/
        dists/
            $DISTRIBUTION/
                Release - lists index files (relative to Release's location)
                          and their hashes
                        - Sometimes (for newer Debian versions?) this includes
                          individual Translation files, sometimes (for older
                          Ubuntu versions?) it doesn't
                Release.gpg

                InRelease - newer alternative to `Release` that contains its
                            own PGP signature

                $COMPONENT/
                    Contents-$SARCH.gz - lists which files are found in which
                                         packages
                                       - $SARCH may be either $ARCH or "source"
                                       - Older repositories place this directly
                                         under $DISTRIBUTION/ instead
                    Contents-udeb-$SARCH.gz
                    binary-$ARCH/
                        Packages - binary package index
                                 - lists files relative to $ARCHIVE_ROOT
                                 - contains sequences of binary package control
                                   stanzas with added "Filename" and "Size" (et
                                   alii) fields
                                 - may also include packages for architecture
                                   `all` "depending on the value of the
                                   Architectures field in the Release file"
                    source/
                        Sources - source index
                                - lists files relative to $ARCHIVE_ROOT
                                - contains sequences of source package control
                                  stanzas with "Source" renamed to "Package"
                                  and with added "Directory" (et alii) field
                    debian-installer/
                        binary-$ARCH/
                            Packages - for udebs(?)
                    i18n/
                        Index - lists SHA1s of files in this directory
                              - Newer repositories also list their
                                `Translation-*` files in the suite's `Release`
                                file, making `Index` files redundant (and some
                                repositories thus no longer have them)
                        Translation-$LANG.bz2 - descriptions in $LANG
                                              - The Debian wiki says these are
                                                only ever compressed with
                                                Bzip2, but some major sources
                                                (including PPAs and the
                                                official Xenial repo) compress
                                                them with Gzip and XZ instead.

File types:
- `*.deb` — Debian packages
- `*.udeb` — Debian packages for the installer
- `*.dsc` — Debian source package descriptions
