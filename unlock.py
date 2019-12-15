import ast
from Crypto.Cipher import AES


hiddenKey   = ''
tag   = ''
ciphertext = ''

with open('keyfile', 'rb') as fin:
    hiddenKey = fin.read()

key = hiddenKey[0:16]
nonce = hiddenKey[16:]


with open('keyfile.sig', 'rb') as fin:
    tag = fin.read()

with open('locked', 'rb') as fin:
    ciphertext = fin.read()

cipher = AES.new(key, AES.MODE_GCM, nonce)

files = cipher.decrypt_and_verify(ciphertext, tag)
files = files.decode()
files = ast.literal_eval(files)

print(files)