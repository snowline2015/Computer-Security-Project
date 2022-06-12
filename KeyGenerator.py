import random
import base64
import hashlib
import Crypto.Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util import number
from Crypto.Cipher import AES


def bezout(a, b, x2=1, x1=0, y2=0, y1=1):
    if a < b:
        a, b = b, a
    if b == 0:
        d, x, y = a, 1, 0
        return d, x, y
    while b:
        q = a//b
        r = a % b
        x, y = x2-q*x1, y2-q*y1
        x2, x1 = x1, x
        y2, y1 = y1, y
        a, b = b, r
    return a, x2, y2


def get_prime(bits):
    while True:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        if p != q:
            return p, q


def key_derivation(password):
    key = hashlib.sha256(password.encode()).hexdigest()[:16]
    return key


def RSA_key_generation(password, length=2048):
    p, q = get_prime(length // 2)
    n = p*q
    euler = (p-1)*(q-1)
    e = random.randint(2, euler)
    while bezout(e, euler)[0] != 1:
        e = random.randint(2, euler)
    d = bezout(e, euler)[2] % euler

    # Key derived function
    passphase = key_derivation(password)

    key = passphase.encode('utf-8')
    IV = Crypto.Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    if len(str(d)) % 16 != 0:
        d = str(d).zfill(len(str(d)) + (16 - (len(str(d)) % 16)))
    ciphertext_d = cipher.encrypt(str(d).encode())

    b64_e = base64.b64encode(str(e).encode()).decode()
    b64_n = base64.b64encode(str(n).encode()).decode()
    b64_d = base64.b64encode(IV + ciphertext_d).decode()

    return (b64_e, b64_n), (b64_d, b64_n)


# (e, n), (d, n) = RSA_key_generation("residentevil4567")
# print(e,"\n",n,"\n",d)