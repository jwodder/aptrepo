from .hashes import Hash

ITER_CONTENT_SIZE = 65536

SECURE_HASHES = {Hash.SHA224, Hash.SHA256, Hash.SHA384, Hash.SHA512}  # SHA-2

I18N_INDEX_HASHES = SECURE_HASHES | {Hash.SHA1}
