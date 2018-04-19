from jwcrypto import jwk


class TokenManager:

    DEFAULT_ALGORITHM = 'RSA'
    DEFAULT_KEY_SIZE = 2048

    def __init__(self, key_pair, encryption_key, signing_key):
        pass

    @classmethod
    def generate_rsa_key_pair(cls):
        return jwk.JWK.generate(
            kty=cls.DEFAULT_ALGORITHM,
            size=cls.DEFAULT_KEY_SIZE
        )
