# dataGerry - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Cryptographic module for symmetric/asymmetric encryption and data verification.
Default symmetric algorithm is AES `Advanced Encryption Standard <https://en.wikipedia.org/wiki/Advanced_Encryption_Standard>`_.
With a 256-bit key and permutation in CBC-Mode
`Cipher Block Chaining <https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29>`_.
Default asymmetric algorithm is RSA `Rivest–Shamir–Adleman <https://en.wikipedia.org/wiki/RSA_(cryptosystem)>`
"""

import json
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

PADDING_CHARACTER_CODING = 'UTF-8'


class AESEncryption:
    """
    AES cipher - using a 32bit key it first serializes a dictionary and returns an encrypted byte string
    """
    BS = 16

    def __init__(self, key):
        """
        generates an new random initialisation vector
        Args:
            key: encryption key, must have this specification length (16,24,32 bit)
        """
        self.iv = Random.new().read(AESEncryption.BS)
        self.key = key

    @classmethod
    def _pad(cls, p):
        """
        padding function for the data input. So the blocks has the correct size
        based in the given block size - BS (normal 16bit)
        Args:
            p: data

        Returns:
            data with padding
        """
        return p + (cls.BS - len(p) % cls.BS) * chr(
            cls.BS - len(p) % cls.BS)

    def encrypt(self, data: dict) -> bytes:
        """
        encrypt the dictionary - returns an encrypted byte string
        Args:
            data: dictionary for encryption

        Returns:
            encrypted byte string
        """
        serialize_data = json.dumps(data)
        raw = self._pad(serialize_data).encode(PADDING_CHARACTER_CODING)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # return base64.b64encode(self.iv + cipher.encrypt(raw))
        return self.iv + cipher.encrypt(raw)


class AESDecryption:
    """
    AES Cipher - decrypts the given data. Returns a dictionary.
    """

    def __init__(self, key):
        """
        Init the symmetric key
        Args:
            key: symmetric key
        """
        self.key = key

    @classmethod
    def _unpad(cls, p):
        """removes the block size padding"""
        return p[:-ord(p[len(p) - 1:])]

    def decrypt(self, data: bytes) -> dict:
        """
        decrypt the byte string back to a dictionary
        Args:
            data: encrypted byte string

        Returns:
            plaintext dict
        """
        # data = base64.b64decode(data)
        iv = data[:AESEncryption.BS]
        encrypted_msg = data[AESEncryption.BS:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return json.loads(self._unpad(cipher.decrypt(encrypted_msg)).decode(PADDING_CHARACTER_CODING))


class RSAEncryption:
    """
    RSA Cipher - for key loading use a instance of KeyHolder
    """

    def __init__(self, public_key_pem):
        """
        checks if public key is well formatted an not the private key
        Args:
            public_key_pem: content from the pem file of the public key
        """
        self.rsa_public_key = RSA.import_key(public_key_pem)
        if self.rsa_public_key.has_private():
            raise ValueError('Use public key for encryption')

    def encrypt(self, data):
        """encrypts data with rsa"""
        cipher = PKCS1_OAEP.new(self.rsa_public_key)
        enc_data = cipher.encrypt(data)
        return enc_data


class RSADecryption:
    """
    RSA Decrypter - for key loading use a instance of KeyHolder
    """

    def __init__(self, private_key_pem):
        """
        loads the private key
        Args:
            private_key_pem: content from the pem file of the private key
        """
        self.rsa_private_key = RSA.import_key(private_key_pem)

    def decrypt(self, data):
        cipher = PKCS1_OAEP.new(self.rsa_private_key)
        dec_data = cipher.decrypt(data)
        return dec_data


class RSASigning:

    def __init__(self):
        raise NotImplemented()

    def sign(self, data):
        raise NotImplemented()


class RSAVerifying:

    def __init__(self):
        raise NotImplemented()

    def verify(self, data) -> bool:
        raise NotImplemented()
