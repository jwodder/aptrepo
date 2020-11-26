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
        return f'{self.filename!r}: no secure checksums to validate against'


@attr.s(repr=False)
class HashMismatchError(FileValidationError):
    filename = attr.ib()
    hashname = attr.ib()
    expected = attr.ib()
    received = attr.ib()

    def __str__(self):
        return (
            f'{self.hashname} hash of {self.filename!r} was {self.received!r},'
            f' expected {self.expected!r}'
        )


@attr.s(repr=False)
class SizeMismatchError(FileValidationError):
    filename = attr.ib()
    expected = attr.ib()
    received = attr.ib()

    def __str__(self):
        return (
            f'size of {self.filename!r} was {self.received},'
            f' expected {self.expected}'
        )


@attr.s(repr=False)
class CannotFetchFileError(Error):
    filename = attr.ib()

    def __str__(self):
        return f'{self.filename!r}: reason unknown'


class NoValidCandidatesError(CannotFetchFileError):
    def __str__(self):
        return (
            f'{self.filename!r}: no matching entry with secure checksums listed'
            ' in index'
        )


class FileInaccessibleError(CannotFetchFileError):
    def __str__(self):
        return f'{self.filename!r}: all requests to server failed'
