class Error(Exception):
    pass


class FileValidationError(Error, ValueError):
    # Subclasses are expected to have `filename` attributes
    pass

class NoSecureChecksumsError(FileValidationError):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(
            '{!r}: no secure checksums to validate against'.format(filename)
        )

class HashMismatchError(FileValidationError):
    def __init__(self, filename, hashname, expected, received):
        self.filename = filename
        self.hashname = hashname
        self.expected = expected
        self.received = received
        super().__init__(
            '{} hash of {!r} was {!r}, expected {!r}'
            .format(hashname, filename, received, expected)
        )

class SizeMismatchError(FileValidationError):
    def __init__(self, filename, expected, received):
        self.filename = filename
        self.expected = expected
        self.received = received
        super().__init__(
            'size of {!r} was {}, expected {}'
            .format(filename, received, expected)
        )


class CannotFetchFileError(Error):
    REASON = 'reason unknown'

    def __init__(self, filename):
        self.filename = filename
        super().__init__('{!r}: {}'.format(filename, self.REASON))

class NoValidCandidatesError(CannotFetchFileError):
    REASON = 'no matching entries with secure checksums listed in index'

class FileInaccessibleError(CannotFetchFileError):
    REASON = 'all requests to server failed'
