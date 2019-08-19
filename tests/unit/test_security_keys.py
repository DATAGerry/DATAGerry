# Net|CMDB - OpenSource Enterprise CMDB
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
from cmdb.security.key.holder import KeyHolder

KEY_TEST_DIRECTORY = 'keys'

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx/qofZ/PAo0KGGH2zpCb
EwI3oO5kp2Ipqv6oYfxcfgsdv76egXn1dUcCb95kmxs006zfDcjQQKcZuOijMeAY
aDdaIHvTKdPJ03Rspq+kJpntDlJUR8I6n+IdavDeZQe9KIEzeE0M20+eLCb2GJPp
XJT2ujKICQ3qu890w7XCJa4Q7VdhYobpx8XiwiRDjXTrC4MMSBPTwgDw2EXixalO
THKEBVeW498m6SGg/Le9egEf2PUd/cJyF4kQNWJ70OQDKGgIYeJVNRsatc4Sz0iV
TJfyZsObAizUh7Cj8xilxAvxQsMUia7eM1izYXSsm4k1X0tyXByxboAmhxOTsZQV
zwIDAQAB
-----END PUBLIC KEY-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAx/qofZ/PAo0KGGH2zpCbEwI3oO5kp2Ipqv6oYfxcfgsdv76e
gXn1dUcCb95kmxs006zfDcjQQKcZuOijMeAYaDdaIHvTKdPJ03Rspq+kJpntDlJU
R8I6n+IdavDeZQe9KIEzeE0M20+eLCb2GJPpXJT2ujKICQ3qu890w7XCJa4Q7Vdh
Yobpx8XiwiRDjXTrC4MMSBPTwgDw2EXixalOTHKEBVeW498m6SGg/Le9egEf2PUd
/cJyF4kQNWJ70OQDKGgIYeJVNRsatc4Sz0iVTJfyZsObAizUh7Cj8xilxAvxQsMU
ia7eM1izYXSsm4k1X0tyXByxboAmhxOTsZQVzwIDAQABAoIBAAT2KRwEzQQJL8jv
FUqGt/I+ydaKU6D7hIEjlFXqBvlxmSlat2ALAJYKTvsrj19xy1u9HEOhSdlwy+iU
jQf9wV1Ekk3gBJszD/zZFKEGFpKGmyUR0dl97iptV8GBfGMRUBYjLn27m6gNT6VU
yiJN+So83+o6urlOyRYjzYfViJ2aqrf9I/gcYd2NHpJd++aJXeNDyPWW4+i1zZD/
O85fhCqXxUQd7iaO/Yldy9Qk36GV3Cap52FpwH722490wBBVZRItuScCAmAR0Vp/
ffSvn+mldsXCEqo9/Sy18/5xpXyPXnL5Oaq8lLXth+BGF2vXNxLYOHnQ3wn9qHDH
BWmjBNECgYEAz6GLvvVjDWE1pEX98Vy+Z21SbdnJakfaT9UFvwB3uex9q4iGe1jy
zpWRN5oqEsDL1+RXWxIqOVJXBBu3dT9Ym8l1RK4ukbganW/jUshE0bHwuH6DOamT
WMop8W8JZEKd32DxagfrzXVxpfIkfZu/gAJkr2ecqFcHm4qDCPg9DcMCgYEA9pDG
6veiIgASRX5EMVxIPPwTnUUQjW/OGm5/7z8o/iiMAwO2nYMvtwzSCLmqW0z365zB
VhQJR3UAhyuRR+TCSYYvAzF4+kP6SFKxr0+A/kmC8t26LGVoI3Z/+U1TmLIaJuzk
JLACwkF8VoS6+hwG93qcjl0k5lGdUPrClBEf2wUCgYEAqPhY18CvKXZQxy1GqiPF
uDnZeRhht6Jd4dYEZRomVSJGa1Ah0UPj5YcGtO87CiPoP/vNs4mm3xtJQUilFj/F
BpL+YjQ2JdRjpHgn0Xi1uMlMk3gxpr1/8iQj2h140ST9gYpNLPLhTUUkhd33IFmd
kLlh4vU5Ii4hPM2OMcCDPy0CgYEA0Zcd0AwyQQ6oeXQsyXy1V0m77psPx/q7SxKV
I60fznRvF/znFZu3SrXWMF6K5lNWB21XlzEu9hQKH9y0AVX+pXsvqVo7iRmRvjq1
Gd3OO9oHOyWppSWKUWLgw+2sWwdCXcZO5LTNk40RAYaQXhzG+0W5oPaicDn+LSEL
l8u6tXUCgYBHogAwco6mXXITxMv3VhtKEN2l7os8w1xwa5BO1Azd8dVkB4rXovXo
Tx5sbLJRxPNGcD4Od/awbcTDu/Sl5YPLuMBJcf5fQJScJYqwzp6rq2tuyTjYkh3J
dvLkzddLVovdVO6ItmTL3Nh+awt8/1IFdiZ6wfCcRfciHVfzj2cs8g==
-----END RSA PRIVATE KEY-----"""


@pytest.fixture(scope='session', autouse=True)
def key_dir(tmpdir_factory):
    return tmpdir_factory.mktemp(f'{KEY_TEST_DIRECTORY}')


@pytest.fixture(scope='session')
def key_holder(key_dir):
    with open(f'{key_dir}/token_public.pem', "w+") as fpu:
        fpu.write(PUBLIC_KEY)
        fpu.close()

    with open(f'{key_dir}/token_private.pem', "w+") as fpr:
        fpr.write(PRIVATE_KEY)
        fpr.close()

    return KeyHolder(key_directory=key_dir)


def test_key_holder_instance():
    key_holder = KeyHolder()
    assert isinstance(key_holder, KeyHolder)


def test_pem_loading(key_holder):
    from authlib.jose import JWK
    from authlib.jose import JWK_ALGORITHMS

    # loading public_key
    key_holder.rsa_public = key_holder._load_rsa_public_key()
    assert JWK(algorithms=JWK_ALGORITHMS).dumps(PUBLIC_KEY, kty='RSA') == key_holder.rsa_public

    # loading private key
    key_holder.rsa_private = key_holder._load_rsa_private_key()
    assert JWK(algorithms=JWK_ALGORITHMS).dumps(PRIVATE_KEY, kty='RSA') == key_holder.rsa_private
