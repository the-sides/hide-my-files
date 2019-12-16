import os
import ast
from utils import readArguments, encryptFile, decryptFile
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
washedFiles = ast.literal_eval(packedFiles.decode())

for filename in washedFiles:
    print(filename)
    print(decryptFile(washedFiles[filename][0], washedFiles[filename][1], key, iv))
# print(washedFiles)
# with open ('locked', 'wb') as fout:
#     fout.write(hidden)

# with open('keyfile.sig', 'wb') as fout:
#     fout.write(tag)
