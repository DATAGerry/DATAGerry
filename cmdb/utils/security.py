import base64
import ast
from Cryptodome import Random
from Cryptodome.Cipher import AES
from cmdb.data_storage.database_manager import NoDocumentFound
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter
from jwcrypto import jwk, jwt, jws


class SecurityManager:
    DEFAULT_BLOCK_SIZE = 32
    DEFAULT_ALG = 'HS512'
    DEFAULT_EXPIRES = int(10)

    def __init__(self, database_manager, expire_time=None):
        self.ssr = SystemSettingsReader(database_manager)
        self.ssw = SystemSettingsWriter(database_manager)
        self.salt = "cmdb"
        self.expire_time = expire_time or SecurityManager.DEFAULT_EXPIRES

    def _setup(self):
        pass

    def encrypt_token(self, payload: dict, timeout: int=(DEFAULT_EXPIRES*60)) -> str:
        import json
        payload = json.dumps(payload)
        jws_token = jws.JWS(payload=payload)
        jws_token.add_signature(
            key=self.get_sym_key(),
            alg=SecurityManager.DEFAULT_ALG,
            protected={'alg': SecurityManager.DEFAULT_ALG},
            header={'kid': self.get_sym_key().thumbprint()}
        )
        import time
        req_claim = {
            'exp':  int(time.time()) + timeout
        }

        enc_token = jwt.JWT(header={"alg": "HS512"}, claims=jws_token.serialize(), default_claims=req_claim)
        enc_token.make_signed_token(self.get_sym_key())

        return enc_token.serialize()

    def decrypt_token(self, token):
        t = jwt.JWT(key=self.get_sym_key(), jwt=token)
        jsw_token = jws.JWS()
        jsw_token.deserialize(t.claims)
        jsw_token.verify(self.get_sym_key())

        return jsw_token.payload

    def generate_hmac(self, data):
        import hashlib
        import hmac

        generated_hash = hmac.new(
            bytes(self.get_sym_key().export_symmetric(), 'utf-8'),
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
            symmetric_key = self.generate_sym_key()
        return jwk.JWK(**symmetric_key)

    def generate_sym_key(self):
        symmetric_key = jwk.JWK.generate(kty='oct', size=256).export()
        symmetric_key = ast.literal_eval(symmetric_key)
        self.ssw.write('security', {'symmetric_key': symmetric_key})
        return jwk.JWK(**symmetric_key)

    def get_key_pair(self):
        try:
            asy_key = self.ssr.get_value('key_pair', 'security')
        except (KeyError, NoDocumentFound):
            asy_key = self.get_key_pair()
        return asy_key

    def generate_key_par(self):
        asy_key = jwk.JWK.generate(kty='EC', crv='P-256')
        public_key = ast.literal_eval(asy_key.export_public())
        private_key = ast.literal_eval(asy_key.export_private())
        insert_key = {
            'public_key': public_key,
            'private_key': private_key
        }
        self.ssw.write('security', {'key_pair': insert_key})
        return insert_key

    def get_private_key(self):
        pub_key = self.get_key_pair()['private_key']
        return jwk.JWK(**pub_key)

    def get_public_key(self):
        pub_key = self.get_key_pair()['public_key']
        return jwk.JWK(**pub_key)
