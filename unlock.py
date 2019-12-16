import ast
from utils import readArguments, decryptFile
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA, ECC


args = readArguments('lock')
public = ''
private = ''
packedFiles = ''
hiddenKey   = ''

# Read public key for encrypting keyfile
with open(args['p']) as fin: 
    public = ECC.import_key(fin.read())

# Read private key for signing keyfile into keyfile.sig
with open(args['r']) as fin: 
    private = RSA.import_key(fin.read())

with open('keyfile', 'rb') as fin:
    hiddenKey = fin.read()

# Decrypt hiddenKey
rsa_dec = PKCS1_OAEP.new(private)
hiddenKey = rsa_dec.decrypt(hiddenKey)

key = hiddenKey[0:16]
iv = hiddenKey[16:]
print('after  key', key)
print('after   iv', iv)


# with open('keyfile.sig', 'rb') as fin:
#     tag = fin.read()

with open('locked', 'rb') as fin:
    packedFiles = fin.read()

files = ast.literal_eval(packedFiles.decode())
for filename in files:
    print(filename)
    revealed = decryptFile(files[filename][0], files[filename][1], key, iv)
    files[filename] = revealed

print(files)