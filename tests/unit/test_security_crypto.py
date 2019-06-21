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
import pytest

from cmdb.security.crypto import RSADecryption


def test_aes_crypto():
    from Crypto.Random import get_random_bytes
    from cmdb.security.crypto import AESEncryption, AESDecryption

    key = get_random_bytes(32)

    aes_crypter = AESEncryption(key=key)
    aes_decrypter = AESDecryption(key=key)

    test_dict = {'test': 'test'}

    encrypted_test_data = aes_crypter.encrypt(test_dict)
    assert encrypted_test_data != test_dict
    decrypted_test_data = aes_decrypter.decrypt(encrypted_test_data)
    assert decrypted_test_data == test_dict


@pytest.mark.usefixtures("key_holder")
def test_rsa_crypto(key_holder):
    from cmdb.security.crypto import RSAEncryption
    public_pem = key_holder.get_public_pem()
    private_pem = key_holder.get_private_pem()
    rsa_encrypter = RSAEncryption(public_key_pem=public_pem)

    plaintext = 'TESTtest123'
    rsa_encrypted = rsa_encrypter.encrypt(plaintext.encode('UTF-8'))
    assert plaintext != rsa_encrypted
    rsa_decrypter = RSADecryption(private_key_pem=private_pem)
    rsa_decrypted = rsa_decrypter.decrypt(rsa_encrypted)
    assert plaintext == rsa_decrypted.decode('UTF-8')
