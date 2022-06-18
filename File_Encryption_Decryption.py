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


# #e = 5588488030241310681904350075143759286631994412831272344258920243217607944844380792604905882924246052999668169978914865956975593682530250836252359022027833015079431004552055293356634447230151803709920406817170946459020003084727923180098208534435122551013302453384578384683639392701808452908860441770481785078443850673903763135331680195817009270702545805395686517515007804587284312435508615464804873254514696302738274447259052832495282379364534645944453090203373092345496441141114075552464280489751348163675242989287318061670972922528209403642281262410250939788024076048574887435879574090218033769078449895158074948431
# #n = 11295083401725202219574229588776195339987524796005104741889178831494176167704008789145449686329416836423694453647771425133056039759533348150955301607042826959026039010596305603831651832746772676243654065221231645989345660750231808911107055008215126392557786895176695239351887270056581987213912928116113737276330331785641966738573500530043151333762667467507594663928478758979001829424884898668721326998482803944515237951537168337878209890989065401206951635014883930712561968272330039406085377096308446003658224582193046740805727697481212643786809239311114747625562057696998158348358242943627163371580146967007096869389
# #d = 000000006295792051506624512950824660288324966273005887033207188005984483844068203742413791611296361859336110765500882823149274499459683019243245464921866095530243090426643751127858306561854932865268349197769555894552213557744044788040361826935831942852631284303242190153684468676311902092714053253789618372159937771834073711221186357344029939205950902432467040742112684069117791741675807979819438382561311702285450417254137751334025125546470615233986688252005936049215481572721468606785888035476290962372278496802967958710471497802382716393479848599508520305180756336531120856763862335629963572724634557314145334147381970351
# #cipher_d = 'b'J\x13\x19C\xd4%sI\xe3\xce?\xc09\xe0R\x87\xfa\x1a)\xa9\xb3\x1d\x95\xac\xf7\x10p\xd9[\x00M\xf7\xc5a\xbfk\xa9{\x8dnO\x0f0\x1eI\x8d;DS\x0f\xae\x1fS\xa8d\xe9(\xfc\x9c\xdb\xbdu\xcak]\x14\xbc)[\x87\xf0\xc9E\x9auJ\xed\xf4v\xb7\x11\x99\xd2\xf2\xa4\xc3S\x9cT.h\x17\xf7!/\x0cVE\xca\xeaU7\xbdr\xf1\xeb\xac\xfa7\x00\x93\xe6\x95\xae}?\xee.i\x1aDw\xce\x85K\xc9N\xc1@\x89\'\xf9\x84Pv\xe99\xc5\xe5\x00Z\x1a\x99\x1f\x1f\x8f\xb0I\xdaT,\xc9\xaf\xb7>=\x98/e\x8cq\x84\x8cS\xd78\xef?\xbc\x9f\xfb\xab\x8f\xa2\xed\xbf\xaa\xe0\x02\x16q%\x17\xe2\x05*\xb5\xc4\x8c\x14\xe7\x1d\xf6G\xbc^{\x83{\x83U\x13\\A\xe03\xc1\x8f\x06Q\xad\x98\xe5\xebs\xe8\x1dK;\xda2$=C\x01\xd0\x0er\x87~\xab5N,A_\xb3\xf4\x0b\xe6D\xc4\xc7\x0crM\x9c\xfdH7>t\xf9Pj\x0f\xbc7\xce\x93w\xf3v\x89I\xd5\xc3\x1a\x82u\xc4\xf0.vf\x98\x80XT\xac\xd6Sg\x8b\t\x0b\xc7\x11^\xdf&\x84j\xd1*\x148\x15\x0e\x1b,\x11\xb0Zy\xf5\x9d\xd1*\xba7}\xf7G\xe77^\x91\xdd|XN\x07\x82\t\xe7\x17\xa0\x0c\xf9}\xed_`\x97\'\xee\x06\xd3\r\xa2\x95F\xdbd"~\xb66<\x05t\x85V\x96\'\x15oY\x8b\x87\xe3\x99\x83\x7f\xe1\xaff\xb3\x8eE\x07j\xf79\xcb\xcc\xf83\xce\xfe\xdb\xee{pf\x89\x83\x1bXC4\xbd`\x95\xc9\x0c\xd3\xf3\xeb\x83\x1c\xda\x8c\xa5\x06\xc4\xf6Gi\xdfg\xc2\x9d\xe9\xa9\x9e\xb4d\x0e37\x89\x86/\xf8B\x10\xde\xb0\x06\x8e\xdc\xe7\xdd\xf7K\x15I\xff=B\xeb\x7f\x9e\x98#zGH\x91\xca\xa2e\xd6T\xf7\xcda9Lp\xa8;is\x99\xe9\x81v\xa4\xf9\xac!&!W2\xe1\xbe\xd5\x1au\x0bvP\t\xe4\xa3U\xb4\x12\xe7i\xc2\xd5\xf5\xa5\x18\xe8\x97\xdb\xc0\xc8f\xa2\x91\\9\xfdi\xbdrB\x0fw\xd9\x91FZy\xfa\x83\x91\x9c\xbd\xfdr\x17\x8f\x0b6!\xa5H\x10\xfe\x8c\x83*\xb3\x8dp9lvI\xcb\x94\xed\xfb`\xc1(\xbf\x84\x06\xd5\xb3\xcf\xc9\x9d`B\x8cx\xda\xcb\xb7\xeb\xaa\xf8\x02\xdb\xc4\x12\xd0\xd2\xc1Y\xa60\xc0\xe7|\xcc/H\xefS\xdb\x0c\x1a\xb0\x9a\xed\xed\xe8\xa7z\x1a\x17\xa0\x889a\x0ci\xa5\xcb=\xdf\x9d\xd0\xbda\x15\x00\xa7\xa6[\x1bT\xba''
# e = 'NTU4ODQ4ODAzMDI0MTMxMDY4MTkwNDM1MDA3NTE0Mzc1OTI4NjYzMTk5NDQxMjgzMTI3MjM0NDI1ODkyMDI0MzIxNzYwNzk0NDg0NDM4MDc5MjYwNDkwNTg4MjkyNDI0NjA1Mjk5OTY2ODE2OTk3ODkxNDg2NTk1Njk3NTU5MzY4MjUzMDI1MDgzNjI1MjM1OTAyMjAyNzgzMzAxNTA3OTQzMTAwNDU1MjA1NTI5MzM1NjYzNDQ0NzIzMDE1MTgwMzcwOTkyMDQwNjgxNzE3MDk0NjQ1OTAyMDAwMzA4NDcyNzkyMzE4MDA5ODIwODUzNDQzNTEyMjU1MTAxMzMwMjQ1MzM4NDU3ODM4NDY4MzYzOTM5MjcwMTgwODQ1MjkwODg2MDQ0MTc3MDQ4MTc4NTA3ODQ0Mzg1MDY3MzkwMzc2MzEzNTMzMTY4MDE5NTgxNzAwOTI3MDcwMjU0NTgwNTM5NTY4NjUxNzUxNTAwNzgwNDU4NzI4NDMxMjQzNTUwODYxNTQ2NDgwNDg3MzI1NDUxNDY5NjMwMjczODI3NDQ0NzI1OTA1MjgzMjQ5NTI4MjM3OTM2NDUzNDY0NTk0NDQ1MzA5MDIwMzM3MzA5MjM0NTQ5NjQ0MTE0MTExNDA3NTU1MjQ2NDI4MDQ4OTc1MTM0ODE2MzY3NTI0Mjk4OTI4NzMxODA2MTY3MDk3MjkyMjUyODIwOTQwMzY0MjI4MTI2MjQxMDI1MDkzOTc4ODAyNDA3NjA0ODU3NDg4NzQzNTg3OTU3NDA5MDIxODAzMzc2OTA3ODQ0OTg5NTE1ODA3NDk0ODQzMQ=='
# n = 'MTEyOTUwODM0MDE3MjUyMDIyMTk1NzQyMjk1ODg3NzYxOTUzMzk5ODc1MjQ3OTYwMDUxMDQ3NDE4ODkxNzg4MzE0OTQxNzYxNjc3MDQwMDg3ODkxNDU0NDk2ODYzMjk0MTY4MzY0MjM2OTQ0NTM2NDc3NzE0MjUxMzMwNTYwMzk3NTk1MzMzNDgxNTA5NTUzMDE2MDcwNDI4MjY5NTkwMjYwMzkwMTA1OTYzMDU2MDM4MzE2NTE4MzI3NDY3NzI2NzYyNDM2NTQwNjUyMjEyMzE2NDU5ODkzNDU2NjA3NTAyMzE4MDg5MTExMDcwNTUwMDgyMTUxMjYzOTI1NTc3ODY4OTUxNzY2OTUyMzkzNTE4ODcyNzAwNTY1ODE5ODcyMTM5MTI5MjgxMTYxMTM3MzcyNzYzMzAzMzE3ODU2NDE5NjY3Mzg1NzM1MDA1MzAwNDMxNTEzMzM3NjI2Njc0Njc1MDc1OTQ2NjM5Mjg0Nzg3NTg5NzkwMDE4Mjk0MjQ4ODQ4OTg2Njg3MjEzMjY5OTg0ODI4MDM5NDQ1MTUyMzc5NTE1MzcxNjgzMzc4NzgyMDk4OTA5ODkwNjU0MDEyMDY5NTE2MzUwMTQ4ODM5MzA3MTI1NjE5NjgyNzIzMzAwMzk0MDYwODUzNzcwOTYzMDg0NDYwMDM2NTgyMjQ1ODIxOTMwNDY3NDA4MDU3Mjc2OTc0ODEyMTI2NDM3ODY4MDkyMzkzMTExMTQ3NDc2MjU1NjIwNTc2OTY5OTgxNTgzNDgzNTgyNDI5NDM2MjcxNjMzNzE1ODAxNDY5NjcwMDcwOTY4NjkzODk='
# d = 'SmMa3+W6qMG8YE3JwRHnlkoTGUPUJXNJ484/wDngUof6Gimpsx2VrPcQcNlbAE33xWG/a6l7jW5PDzAeSY07RFMPrh9TqGTpKPyc2711ymtdFLwpW4fwyUWadUrt9Ha3EZnS8qTDU5xULmgX9yEvDFZFyupVN71y8eus+jcAk+aVrn0/7i5pGkR3zoVLyU7BQIkn+YRQduk5xeUAWhqZHx+PsEnaVCzJr7c+PZgvZYxxhIxT1zjvP7yf+6uPou2/quACFnElF+IFKrXEjBTnHfZHvF57g3uDVRNcQeAzwY8GUa2Y5etz6B1LO9oyJD1DAdAOcod+qzVOLEFfs/QL5kTExwxyTZz9SDc+dPlQag+8N86Td/N2iUnVwxqCdcTwLnZmmIBYVKzWU2eLCQvHEV7fJoRq0SoUOBUOGywRsFp59Z3RKro3ffdH5zdekd18WE4HggnnF6AM+X3tX2CXJ+4G0w2ilUbbZCJ+tjY8BXSFVpYnFW9Zi4fjmYN/4a9ms45FB2r3OcvM+DPO/tvue3BmiYMbWEM0vWCVyQzT8+uDHNqMpQbE9kdp32fCnempnrRkDjM3iYYv+EIQ3rAGjtzn3fdLFUn/PULrf56YI3pHSJHKomXWVPfNYTlMcKg7aXOZ6YF2pPmsISYhVzLhvtUadQt2UAnko1W0EudpwtX1pRjol9vAyGaikVw5/Wm9ckIPd9mRRlp5+oORnL39chePCzYhpUgQ/oyDKrONcDlsdknLlO37YMEov4QG1bPPyZ1gQox42su366r4AtvEEtDSwVmmMMDnfMwvSO9T2wwasJrt7einehoXoIg5YQxppcs9353QvWEVAKemWxtUug=='
#
# # file_encryption("D:\\ASUS\\Videos\\Favorites\\Kabaneri of The Iron Fortress OST - KABANERIOFTHEIRONFORTRESS (Feat. Eliana).mp4", (e, n))
# file_decryption("D:\\ASUS\\Videos\\Kabaneri of The Iron Fortress OST - KABANERIOFTHEIRONFORTRESS (Feat. Eliana).mp4.enc", (d, n), "residentevil4567")
