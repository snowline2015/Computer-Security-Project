import json
import hashlib
import os
import base64

import Crypto
from Crypto.Cipher import AES

import KeyGenerator
import File_Encryption_Decryption
import DigitalSignature
from json.decoder import JSONDecodeError

path = 'database\\users.json'
f = open(path)
try:
    data = json.load(f)
except JSONDecodeError:
    data = {}


def register(email, password, fullname, dob, phone, address):
    if email in data:
        return False
    salt = os.urandom(32)
    data[email] = {
        'password': hashlib.sha256(password.encode() + salt).hexdigest(),
        'fullname': fullname,
        'dob': dob,
        'phone': phone,
        'address': address,
        'salt': salt.hex(),
        'Kpublic': '',
        'Kprivate': '',
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    return True


def login(email, password):
    if email not in data:
        return False, 'Email not found'
    if data[email]['password'] != hashlib.sha256(password.encode() + bytes.fromhex(data[email]['salt'])).hexdigest():
        return False, 'Wrong password'
    return True, None


def edit_profile(email, password, fullname, dob, phone, address):
    if email not in data:
        return False, 'Account not found'
    data[email]['fullname'] = fullname
    data[email]['dob'] = dob
    data[email]['phone'] = phone
    data[email]['address'] = address
    if password is not None:
        d_encrypted = base64.b64decode(data[email]['Kprivate']['d'])

        # Key derived function
        passphase = KeyGenerator.key_derivation(data[email]['password'])

        key = passphase.encode('utf-8')
        IV = d_encrypted[:16]
        cipher = AES.new(key, AES.MODE_CBC, IV)
        d = int(cipher.decrypt(d_encrypted[16:]))

        # Key derived function
        passphase = KeyGenerator.key_derivation(password)

        key = passphase.encode('utf-8')
        IV = Crypto.Random.new().read(16)
        cipher = AES.new(key, AES.MODE_CBC, IV)
        if len(str(d)) % 16 != 0:
            d = str(d).zfill(len(str(d)) + (16 - (len(str(d)) % 16)))
        ciphertext_d = cipher.encrypt(str(d).encode())
        b64_d = base64.b64encode(IV + ciphertext_d).decode()

        data[email]['Kprivate']['d'] = b64_d
        data[email]['password'] = password
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    return True, ''


def generate_key(email):
    (e, n), (d, n) = KeyGenerator.RSA_key_generation(data[email]['password'])
    data[email]['Kpublic'] = {'e': e, 'n': n}
    data[email]['Kprivate'] = {'d': d, 'n': n}
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    return True


def file_encrypt(email, file_path):
    if data[email]['Kpublic'] == '':
        return False
    File_Encryption_Decryption.file_encryption(file_path, (data[email]['Kpublic']['e'], data[email]['Kpublic']['n']))
    return True


def file_decrypt(email, file_path):
    if data[email]['Kprivate'] == '':
        return False
    File_Encryption_Decryption.file_decryption(file_path, (data[email]['Kprivate']['d'], data[email]['Kprivate']['n']), data[email]['password'])
    return True


def digital_signature(email, file_path):
    if data[email]['Kprivate'] == '':
        return False
    DigitalSignature.sign_file(file_path, (data[email]['Kprivate']['d'], data[email]['Kprivate']['n']), data[email]['password'])
    return True


def digital_signature_verification(email, file_path):
    if data[email]['Kpublic'] == '':
        return False
    if os.path.exists(file_path[:-4]):
        return False
    if DigitalSignature.verify_file(file_path, (data[email]['Kpublic']['e'], data[email]['Kpublic']['n'])):
        return True
    return False