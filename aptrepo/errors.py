import attr

class Error(Exception):
    pass


class FileValidationError(Error, ValueError):
    # Subclasses are expected to have `filename` attributes
    pass


@attr.s(repr=False)
class NoSecureChecksumsError(FileValidationError):
    filename = attr.ib()

    def __str__(self):
        return '{!r}: no secure checksums to validate against'\
               .format(self.filename)


@attr.s(repr=False)
class HashMismatchError(FileValidationError):
    filename = attr.ib()
    hashname = attr.ib()
    expected = attr.ib()
    received = attr.ib()

    def __str__(self):
        return '{0.hashname} hash of {0.filename!r} was {0.received!r},' \
               ' expected {0.expected!r}'.format(self)


@attr.s(repr=False)
class SizeMismatchError(FileValidationError):
    filename = attr.ib()
    expected = attr.ib()
    received = attr.ib()

    def __str__(self):
        return 'size of {0.filename!r} was {0.received}, expected {0.expected}'\
               .format(self)


@attr.s(repr=False)
class CannotFetchFileError(Error):
    filename = attr.ib()

    def __str__(self):
        return '{!r}: reason unknown'.format(self.filename)


class NoValidCandidatesError(CannotFetchFileError):
    def __str__(self):
        return '{!r}: no matching entry with secure checksums listed in index'\
               .format(self.filename)


class FileInaccessibleError(CannotFetchFileError):
    def __str__(self):
        return '{!r}: all requests to server failed'.format(self.filename)
