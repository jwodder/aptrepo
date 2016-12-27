class Error(Exception):
    pass

class HashMismatchError(Error, ValueError):
    def __init__(self, filename, hashname, expected, received):
        self.filename = filename
        self.hashname = hashname
        self.expected = expected
        self.received = received
        super().__init__(
            '{} hash of {!r} was {!r}, expected {!r}'
            .format(hashname, filename, received, expected)
        )

class SizeMismatchError(Error, ValueError):
    def __init__(self, filename, expected, received):
        self.filename = filename
        self.expected = expected
        self.received = received
        super().__init__(
            'size of {!r} was {}, expected {}'
            .format(filename, received, expected)
        )

class CannotFetchFileError(Error, ValueError):
    REASON = 'reason unknown'

    def __init__(self, filename):
        self.filename = filename
        super().__init__('{!r}: {}'.format(filename, self.REASON))

class NoSecureChecksumsError(CannotFetchFileError):
    REASON = 'no secure checksums listed in index'

class FileInaccessibleError(CannotFetchFileError):
    REASON = 'all requests to server failed'
