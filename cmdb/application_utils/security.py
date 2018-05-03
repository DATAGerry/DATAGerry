from jwcrypto import jwk
import ast
from Cryptodome import Random
from Crypto.Cipher import AES
import base64
from cmdb.data_storage.database_manager import NoDocumentFound


class SecurityManager:
    DEFAULT_BLOCK_SIZE = 32

    def __init__(self, settings_reader, settings_writer):
        self.ssr = settings_reader
        self.ssw = settings_writer
        self.symmetric_key = self.get_sym_key()
        self.key_pair = self.get_key_pair()
        self.salt = "cmdb"

    def generate_hmac(self, data):

        import hashlib
        import hmac
        import base64

        generated_hash = hmac.new(
            bytes(self.symmetric_key, 'utf-8'),
            bytes(data + self.salt, 'utf-8'),
            hashlib.sha256
        )

        generated_hash.hexdigest()

        return base64.b64encode(generated_hash.digest()).decode("utf-8")

    def encrypt_aes(self, raw):
        """
        see https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
        :param raw: unencrypted data
        :return:
        """
        raw = SecurityManager._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.symmetric_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.symmetric_key, AES.MODE_CBC, iv)
        return SecurityManager._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    @staticmethod
    def _pad(s):
        return s + (SecurityManager.DEFAULT_BLOCK_SIZE - len(s) % SecurityManager.DEFAULT_BLOCK_SIZE) * \
                   chr(SecurityManager.DEFAULT_BLOCK_SIZE - len(s) % SecurityManager.DEFAULT_BLOCK_SIZE)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def get_sym_key(self):
        try:
            symmetric_key = self.ssr.get_value('symmetric_key', 'security')
        except (KeyError, NoDocumentFound):
            symmetric_key = jwk.JWK.generate(kty='oct', size=256).export()
            symmetric_key = ast.literal_eval(symmetric_key)
            self.ssw.write('security', {'symmetric_key': symmetric_key})
        return symmetric_key['k']

    def get_key_pair(self):
        try:
            asy_key = self.ssr.get_value('key_pair', 'security')
        except (KeyError, NoDocumentFound):
            asy_key = jwk.JWK.generate(kty='EC', crv='P-256')
            public_key = ast.literal_eval(asy_key.export_public())
            private_key = ast.literal_eval(asy_key.export_private())
            insert_key = {
                'public_key': public_key,
                'private_key': private_key
            }
            self.ssw.write('security', {'key_pair': insert_key})
        return asy_key


class TokenManager:
    def __init__(self):
        pass
