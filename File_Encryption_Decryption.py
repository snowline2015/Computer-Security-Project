import base64
import os
import Crypto.Random
from Crypto.Cipher import AES
import KeyGenerator

# These functions only for file with size less than 10000000 GB
# Default encrypted file format: File Size + IV + Encrypted Ksession Size + Encrypted Ksession + Encrypted Data

CHUNK_SIZE = 1024


def key_session_encryption(Ksession, Kpublic):
    e = base64.b64decode(Kpublic[0]).decode()
    n = base64.b64decode(Kpublic[1]).decode()
    Ksession_encrypted = pow(int.from_bytes(Ksession, 'big'), int(e), int(n))
    return base64.b64encode(str(Ksession_encrypted).encode()).decode()


def key_session_decryption(Ksession_encrypted, Kprivate, password):
    d_encrypted = base64.b64decode(Kprivate[0])
    n = base64.b64decode(Kprivate[1]).decode()
    Ksession_encrypted = base64.b64decode(Ksession_encrypted).decode()

    # Key derived function
    passphase = KeyGenerator.key_derivation(password)

    key = passphase.encode('utf-8')
    IV = d_encrypted[:16]
    cipher = AES.new(key, AES.MODE_CBC, IV)
    d = cipher.decrypt(d_encrypted[16:])

    Ksession = pow(int(Ksession_encrypted), int(d), int(n))
    return Ksession.to_bytes(16, 'big')


def file_encryption(filename, Kpublic):
    outputFile = filename + ".enc"
    filesize = str(os.path.getsize(filename)).zfill(16)

    Ksession = Crypto.Random.get_random_bytes(16)
    IV = Crypto.Random.new().read(16)
    encryptor = AES.new(Ksession, AES.MODE_CBC, IV)

    Ksession_encrypted = key_session_encryption(Ksession, Kpublic)
    Ksession_encrypted_size = str(len(Ksession_encrypted)).zfill(16)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode())
            outfile.write(IV)
            outfile.write(Ksession_encrypted_size.encode())
            outfile.write(Ksession_encrypted.encode())

            while True:
                chunk = infile.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))


def file_decryption(filename, Kprivate, password):
    outputFile = filename[:-4]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        Ksession_encrypted_size = int(infile.read(16))
        Ksession_encrypted = infile.read(Ksession_encrypted_size)
        Ksession = key_session_decryption(Ksession_encrypted, Kprivate, password)

        decryptor = AES.new(Ksession, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)
