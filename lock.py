import os
from utils import readArguments
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

args = readArguments('lock')
public = ''
files = {}

# Read public key for encrypting keyfile
with open(args['p'], 'rb') as fin: 
    public = fin.read()

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
cipher = AES.new(key, AES.MODE_GCM)
nonce  = cipher.nonce

# Keyfile for single party decrypting
keyfileContent = key + nonce
print(key == keyfileContent[0:16])
with open('keyfile', 'wb') as fout:
    fout.write(keyfileContent)
    # fout.write(nonce)

# Encryption Process
hidden, tag = cipher.encrypt_and_digest(files['secrets/hideThisFile'])

cipherDec = AES.new(key, AES.MODE_GCM, cipher.nonce)
washed = cipherDec.decrypt_and_verify(hidden, tag)

print(hidden, washed)