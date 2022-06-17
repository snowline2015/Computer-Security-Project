import json
import hashlib
import os
import KeyGenerator
import File_Encryption_Decryption
import DigitalSignature

path = 'database\\data.json'
f = open(path)
data = json.load(f)


def register(email, password, fullname, dob, phone, address):
    if email in data:
        return False
    salt = os.urandom(32)
    data['users'].append({
        'email': email,
        'password': hashlib.sha256(password.encode() + salt).hexdigest(),
        'fullname': fullname,
        'dob': dob,
        'phone': phone,
        'address': address,
        'salt': salt.hex(),
        'Kpublic': '',
        'Kprivate': '',
        'password_backup': ''
    })
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
        return False
    data[email]['fullname'] = fullname
    data[email]['dob'] = dob
    data[email]['phone'] = phone
    data[email]['address'] = address
    if password is not None:
        salt = os.urandom(32)
        data[email]['password'] = hashlib.sha256(password.encode() + salt).hexdigest()
        data[email]['salt'] = salt.hex()
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    return True


def generate_key(email):
    (e, n), (d, n) = KeyGenerator.RSA_key_generation(data[email]['password'])
    data[email]['Kpublic'] = {'e': e, 'n': n}
    data[email]['Kprivate'] = {'d': d, 'n': n}
    data[email]['password_backup'] = hashlib.sha256(data[email]['password'].encode() + bytes.fromhex(data[email]['salt'])).hexdigest()
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
    File_Encryption_Decryption.file_decryption(file_path, (data[email]['Kprivate']['d'], data[email]['Kprivate']['n']), data[email]['password_backup'])
    return True


def digital_signature(email, file_path):
    if data[email]['Kprivate'] == '':
        return False
    DigitalSignature.sign_file(file_path, (data[email]['Kprivate']['d'], data[email]['Kprivate']['n']), data[email]['password_backup'])
    return True


def digital_signature_verification(email, file_path):
    if data[email]['Kpublic'] == '':
        return False
    if os.path.exists(file_path[:-4]):
        return False
    if DigitalSignature.verify_file(file_path, (data[email]['Kpublic']['e'], data[email]['Kpublic']['n'])):
        return True
    return False