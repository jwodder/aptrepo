class PyAPTError(Exception):
    pass

class HashMismatchError(PyAPTError, ValueError):
    def __init__(self, filename, hashname, expected, received):
        self.filename = filename
        self.hashname = hashname
        self.expected = expected
        self.received = received
        super().__init__(
            '{} hash of {!r} was {!r}, expected {!r}'
            .format(hashname, filename, received, expected)
        )

class CannotFetchFileError(PyAPTError, ValueError):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(
            '{!r}: no secure checksums listed in index, or server returned 404'
            .format(filename)
        )
        ### TODO: Distinguish between the various cases?
        ### ("FileInaccessibleError" for 404 and 403?)
