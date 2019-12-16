import ast
from utils import readArguments, decryptFile
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA, ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS


args = readArguments('lock')
public = ''
private = ''
packedFiles = ''
hiddenKey   = ''
signature = ''
subject = ''

# Read public key for encrypting keyfile
with open(args['p'], 'rb') as fin: 
    subject = fin.readline()[:-1]
    public = ECC.import_key(fin.read())

# Read private key for signing keyfile into keyfile.sig
with open(args['r'], 'rb') as fin: 
    private = RSA.import_key(fin.read())

with open('keyfile', 'rb') as fin:
    hiddenKey = fin.read()

with open('keyfile.sig', 'rb') as fin:
    signature = fin.read()

with open('locked', 'rb') as fin:
    packedFiles = fin.read()

# Decrypt hiddenKey
rsa_dec = PKCS1_OAEP.new(private)
hiddenKeyDec = rsa_dec.decrypt(hiddenKey)

key = hiddenKeyDec[0:16]
iv = hiddenKeyDec[16:]
print('Hashing:', hiddenKey)

# Verify keyfile
verifier = DSS.new(public, 'fips-186-3')
hashOfKey = SHA256.new(hiddenKey)
try:
    verifier.verify(hashOfKey, signature)
    print("The message is authentic.")
except ValueError:
    print("The message is not authentic.")
    exit()

# Decrypt, verify, and create files
files = ast.literal_eval(packedFiles.decode())
for filename in files:
    print(filename)
    revealed = decryptFile(files[filename][0], files[filename][1], key, iv)
    files[filename] = revealed

print(files)