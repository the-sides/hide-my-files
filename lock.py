import os
import ast
from utils import readArguments, encryptFile
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

args = readArguments('lock')
public = ''
private = ''
files = {}

# Read public key for encrypting keyfile
with open(args['p']) as fin: 
    public = RSA.import_key(fin.read())

# Read private key for signing keyfile into keyfile.sig
with open(args['r']) as fin: 
    private = ECC.import_key(fin.read())


# Crawl for all files within specified directory
for dirName, subdirList, fileList in os.walk(args['d']):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        print('\t%s' % fname)
        files[dirName + '/' + fname] = b''

# Read all the files that were found
for filename in files:
    with open(filename, 'rb') as fin:
        files[filename] = fin.read()

# Encryption Setup
key    = get_random_bytes(16)
iv     = get_random_bytes(16)

# Keyfile for single party decrypting
keyfileContent = key + iv
print(key == keyfileContent[0:16])
with open('keyfile', 'wb') as fout:
    fout.write(keyfileContent)
    # fout.write(nonce)

# Encryption Process
hidden, tag = encryptFile(files['secrets/hideThisFile'], key, iv)
# washed = decryptFile(hidden, tag, key, iv)
# print(washed)

for filename in files:
    hidden, tag = encryptFile(files[filename], key, iv) 
    files[filename] = (hidden, tag)

packedFiles = str(files).encode()
# Send to 'locked' read from unlock.py
with open ('locked', 'wb') as fout:
    fout.write(packedFiles)

##########    Done by unlock.py   ###########
# washedFiles = ast.literal_eval(packedFiles.decode())
# for filename in washedFiles:
#     print(filename)
#     revealed = decryptFile(washedFiles[filename][0], washedFiles[filename][1], key, iv)
############################################

# Create keyfile with key and iv
# Encrypt using RSA pub
rsa_enc = PKCS1_OAEP.new(public)
print('before key', key)
print('before  iv', iv)
secretKey = rsa_enc.encrypt(keyfileContent)
with open('keyfile', 'wb') as fout:
    fout.write(secretKey)

# rsa_dec = PKCS1_OAEP.new(private)
# washed = rsa_dec.decrypt(secretKey)
# print('after ', washed)

# Sign keyfile with ECC priv, write to keyfile.sig

##########    Done by unlock.py   ###########
# Decrypt using RSA priv
# Verify keyfile.sig with ECC pub
############################################


with open('keyfile.sig', 'wb') as fout:
    fout.write(tag)
