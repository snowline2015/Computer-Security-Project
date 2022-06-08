import random
import hashlib
import base64
import os
from Crypto.Cipher import AES
import Crypto.Random

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
    passphase = password.ljust(16, '0') if len(password) < 16 else password[:16]

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


# #e = 12914680767564353924726457407078660723880099422640363024284456960750460115362788731999203515972124374142840137716610953685864308685850588539734386007781589740929496637904577135591362718968292981270040857322254737178835128958984149870596568410229715997101933892760168368289378041339509362878529462098303667705011794727037154412030962254587642920550471004940486287537751986675666718317121485874686922323416578853830952693856232152474486968612458881121644940815323749213902911275087273253805712924538955257483817551614637694508813792407526795345948866634371693585138158646810760547983466228928309214448863444168335676649
# #n = 18269791921723698184943274329397558908962461961250352221243135183045984499587785016268917856678798712882154691725573629582644566775938509964885782518613485129672237469919748659951740557208647280978781248996925229902707181921566880969757153249299944916239047750193240124482402964204000493782697785728819914795745975766250946104876988874202439777890723612859340024372777854378766316307230616313494122508886292709287854792513264550898150493690437249624212245376124322967174804715483018883997784397240536029653045035513450391845649120928941093395584963097819892216532843247241728234004344428857128720127056192563246588329
# #d = 000000003207242896950967656631835094400216607502905678631630024533300231205411271381302121979186594424268031916465401528252243448363640281580778110513119602433726487285145258246590338415682964853014292986460194893345958959828373230417631927264732690236208206373667662614790353498469047964966422200547924910528943432805673451424213860694968115591871352474360431573865108214091311055878962000099560552271781908082372878713520085462518768582684869406572360563370040554027779311878404507718512119760664940034260643937469849575209744584788921875550530595157937870935471161802227455530134572921552709792406317901617253234225342549
# #cipher_d = b' R\xb2[s6\x1e\xa4:\xf8r\xf9\x88\x86\x8a\xe8J\x8e\xc2\x17v\x96z\xa6\xc6#8:}\x0b\xc3o\x11\xec#\xc7\xed\x9e\xdbl8C\x87\xef@;=\x14\xd8\x0c\xa4\xd6I}\x95\xdf|\xf5tE`\x98j\x02@\x8d8>%\xec\x1a:\xb6}\xee\x86\xcc@\x0b\x07T\x15\x9f\x12\xd7S"\x07\x92\xbf\xef^\x9am\x98\xcdLy\x8a~\xac\xfa\xe8|\xb6I\xcbLs\xd0\x8eD\xfe\x93\xf3\xab}\xa0\x85p\xfa\xa9M\x91L\xb9g;\xf4\xd9l\xb4\x8c\xce\x8e\xbf\xd3O{]\xd6N\xa9\xa5:z\x14\n2E\x12F\xd6T<"\xd7E\x8c\xd1%\xb3\xd72\x9c\x92_(\xed\xe8ox\x1e\xfa\nA\x16\xd0L\xe4\xabs\xa4F\xef\xca\xd3\xf8Bam2+\x05\x08\x9an}\xd2\xe2\x86\xa7\x0e;\x92$|\x840\x96E\xa2\xee6\xbc\xaf\xf6\x84\x87\xe2\xfc\x14\xdd\\q\xb2\xe9\x8ch\xcec\r\xe9&q\xdf\xf8@\x01c\xc4\xeaBH\xf0S\n\xc6\x04\xbc\xf9{\xb4\xbb\xf9\xcb&zS\xb8\xbe\xb1\x84M\x15\x04\xe9\xbdhr\x10\xe0\x15\xc3sD\xa2b\xd7cC)9J\xeb!i/\xbc3\xf6<\x9fo\x05\xd0bf\xf6\x9ar\xdf\x96\x84\xcc\x15gG6C\xe9\xdb\x02k\xf9\x02\xe0p\xcd\x88\x04Y\x9b\x8e\xa5y\xaf\xaa\xf5\xe3\xb8\xe9\xdfu\xa6%\xd5\xbc\x93Y\xeb\xbc\xe4\x03\x98~\xd98\xf1F4\xd9\xe2\xcas\xb7\x05\xd3\xfa1\xcc\xd1\x9a/\x03>\xf7/\x06\x8c4L$E\x003\xb0\x00@3\xa1XNb\x91\x0f%/\x9bm\x08\xe1_!\xfaL\xa0K\x08\xc7\x05XO\x07<\xbf!b\xe1\x9eRd\x0f\x837\x95\x86\x97\x17\xe30\x9db\xb1@\xaek\xa1n\\\xfd\xfa\xfcEtZ\xd5\x81v\x0b\x1a\xc0\xddN\xc7\xb0\x1a&e\xce\xc9\xf4P\xc1\t\xd4v\x86\xdb\xc9NN\x17S\xe3\xa6?5h\xf8`d\xccq\xd2\xd60@\xa9\x06\x91\x15b\xf1\x13\x80\rF\x9c\x0b\x83t\x82\x99\xaa\x03\xaaV\xdb\xb5\xe0^n\x04\x80b\xfc\xf8\xf3\x15o*ol0\xac\x1b\xed\x19\xfe1\xc4u\x06K\xe3\t\x03.}\xea\xdbf\xe7;e\xb3\xcb\xf422\x86}\xcd\xe8\x94Yw%\xf4E#F\xcc\xf0\xe9b\'-\xcb\xb6\x9a\x1f\xfd\xb3\xb7-\x03Rzo\xb2\xf9\xd6\x10\n\xd5P\xd5\x0e\xdaE\x8a\xc4\x04\xd4]\x83\xa3+\x1b|\x7fp({\xa4\x96\x94\x1c\xb0\x14G\xc5\xe2\x81\xc5\xc5\x957\xc7\xd4\x84\x91\xb0\xab\x06\x81\x04,2A\xa3\xe1'
# e = 'MTI5MTQ2ODA3Njc1NjQzNTM5MjQ3MjY0NTc0MDcwNzg2NjA3MjM4ODAwOTk0MjI2NDAzNjMwMjQyODQ0NTY5NjA3NTA0NjAxMTUzNjI3ODg3MzE5OTkyMDM1MTU5NzIxMjQzNzQxNDI4NDAxMzc3MTY2MTA5NTM2ODU4NjQzMDg2ODU4NTA1ODg1Mzk3MzQzODYwMDc3ODE1ODk3NDA5Mjk0OTY2Mzc5MDQ1NzcxMzU1OTEzNjI3MTg5NjgyOTI5ODEyNzAwNDA4NTczMjIyNTQ3MzcxNzg4MzUxMjg5NTg5ODQxNDk4NzA1OTY1Njg0MTAyMjk3MTU5OTcxMDE5MzM4OTI3NjAxNjgzNjgyODkzNzgwNDEzMzk1MDkzNjI4Nzg1Mjk0NjIwOTgzMDM2Njc3MDUwMTE3OTQ3MjcwMzcxNTQ0MTIwMzA5NjIyNTQ1ODc2NDI5MjA1NTA0NzEwMDQ5NDA0ODYyODc1Mzc3NTE5ODY2NzU2NjY3MTgzMTcxMjE0ODU4NzQ2ODY5MjIzMjM0MTY1Nzg4NTM4MzA5NTI2OTM4NTYyMzIxNTI0NzQ0ODY5Njg2MTI0NTg4ODExMjE2NDQ5NDA4MTUzMjM3NDkyMTM5MDI5MTEyNzUwODcyNzMyNTM4MDU3MTI5MjQ1Mzg5NTUyNTc0ODM4MTc1NTE2MTQ2Mzc2OTQ1MDg4MTM3OTI0MDc1MjY3OTUzNDU5NDg4NjY2MzQzNzE2OTM1ODUxMzgxNTg2NDY4MTA3NjA1NDc5ODM0NjYyMjg5MjgzMDkyMTQ0NDg4NjM0NDQxNjgzMzU2NzY2NDk='
# n = 'MTgyNjk3OTE5MjE3MjM2OTgxODQ5NDMyNzQzMjkzOTc1NTg5MDg5NjI0NjE5NjEyNTAzNTIyMjEyNDMxMzUxODMwNDU5ODQ0OTk1ODc3ODUwMTYyNjg5MTc4NTY2Nzg3OTg3MTI4ODIxNTQ2OTE3MjU1NzM2Mjk1ODI2NDQ1NjY3NzU5Mzg1MDk5NjQ4ODU3ODI1MTg2MTM0ODUxMjk2NzIyMzc0Njk5MTk3NDg2NTk5NTE3NDA1NTcyMDg2NDcyODA5Nzg3ODEyNDg5OTY5MjUyMjk5MDI3MDcxODE5MjE1NjY4ODA5Njk3NTcxNTMyNDkyOTk5NDQ5MTYyMzkwNDc3NTAxOTMyNDAxMjQ0ODI0MDI5NjQyMDQwMDA0OTM3ODI2OTc3ODU3Mjg4MTk5MTQ3OTU3NDU5NzU3NjYyNTA5NDYxMDQ4NzY5ODg4NzQyMDI0Mzk3Nzc4OTA3MjM2MTI4NTkzNDAwMjQzNzI3Nzc4NTQzNzg3NjYzMTYzMDcyMzA2MTYzMTM0OTQxMjI1MDg4ODYyOTI3MDkyODc4NTQ3OTI1MTMyNjQ1NTA4OTgxNTA0OTM2OTA0MzcyNDk2MjQyMTIyNDUzNzYxMjQzMjI5NjcxNzQ4MDQ3MTU0ODMwMTg4ODM5OTc3ODQzOTcyNDA1MzYwMjk2NTMwNDUwMzU1MTM0NTAzOTE4NDU2NDkxMjA5Mjg5NDEwOTMzOTU1ODQ5NjMwOTc4MTk4OTIyMTY1MzI4NDMyNDcyNDE3MjgyMzQwMDQzNDQ0Mjg4NTcxMjg3MjAxMjcwNTYxOTI1NjMyNDY1ODgzMjk='
# d = 'OBXf+bDsaRaLOlyGPW/q4iBSsltzNh6kOvhy+YiGiuhKjsIXdpZ6psYjODp9C8NvEewjx+2e22w4Q4fvQDs9FNgMpNZJfZXffPV0RWCYagJAjTg+JewaOrZ97obMQAsHVBWfEtdTIgeSv+9emm2YzUx5in6s+uh8tknLTHPQjkT+k/OrfaCFcPqpTZFMuWc79NlstIzOjr/TT3td1k6ppTp6FAoyRRJG1lQ8ItdFjNEls9cynJJfKO3ob3ge+gpBFtBM5KtzpEbvytP4QmFtMisFCJpufdLihqcOO5IkfIQwlkWi7ja8r/aEh+L8FN1ccbLpjGjOYw3pJnHf+EABY8TqQkjwUwrGBLz5e7S7+csmelO4vrGETRUE6b1ochDgFcNzRKJi12NDKTlK6yFpL7wz9jyfbwXQYmb2mnLfloTMFWdHNkPp2wJr+QLgcM2IBFmbjqV5r6r147jp33WmJdW8k1nrvOQDmH7ZOPFGNNniynO3BdP6MczRmi8DPvcvBow0TCRFADOwAEAzoVhOYpEPJS+bbQjhXyH6TKBLCMcFWE8HPL8hYuGeUmQPgzeVhpcX4zCdYrFArmuhblz9+vxFdFrVgXYLGsDdTsewGiZlzsn0UMEJ1HaG28lOThdT46Y/NWj4YGTMcdLWMECpBpEVYvETgA1GnAuDdIKZqgOqVtu14F5uBIBi/PjzFW8qb2wwrBvtGf4xxHUGS+MJAy596ttm5ztls8v0MjKGfc3olFl3JfRFI0bM8OliJy3Ltpof/bO3LQNSem+y+dYQCtVQ1Q7aRYrEBNRdg6MrG3x/cCh7pJaUHLAUR8XigcXFlTfH1ISRsKsGgQQsMkGj4Q=='
#
# #file_encryption("D:\\ASUS\\Videos\\Favorites\\Kabaneri of The Iron Fortress OST - KABANERIOFTHEIRONFORTRESS (Feat. Eliana).mp4", (e, n))
# file_decryption("D:\\ASUS\\Videos\\Kabaneri of The Iron Fortress OST - KABANERIOFTHEIRONFORTRESS (Feat. Eliana).mp4.enc", (d, n), "residentevil4567")
