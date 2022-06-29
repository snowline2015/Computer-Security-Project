import hashlib
import base64
from Crypto.Cipher import AES
import KeyGenerator


def sign_file(filename, Kprivate, password):
    d_encrypted = base64.b64decode(Kprivate[0])
    n = base64.b64decode(Kprivate[1]).decode()

    # Key derived function
    passphase = KeyGenerator.key_derivation(password)

    key = passphase.encode('utf-8')
    IV = d_encrypted[:16]
    cipher = AES.new(key, AES.MODE_CBC, IV)
    d = cipher.decrypt(d_encrypted[16:])

    with open(filename, 'rb') as f:
        data = f.read()
    hash_ = hashlib.sha256(data).digest()
    signature = pow(int.from_bytes(hash_, 'big'), int(d), int(n))
    with open(filename + '.sig', 'wb') as f:
        f.write(signature.to_bytes(256, 'big'))


def verify_file(filename, Kpublic):
    e = base64.b64decode(Kpublic[0]).decode()
    n = base64.b64decode(Kpublic[1]).decode()

    with open(filename, 'rb') as f:
        signature = int.from_bytes(f.read(), 'big')
    hash_ = pow(signature, int(e), int(n))
    return hash_ == int.from_bytes(hashlib.sha256(open(filename[:-4], 'rb').read()).digest(), 'big')