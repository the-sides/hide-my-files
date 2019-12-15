from utils import readArguments, extractKey
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA, ECC

# Parse arguments
args = readArguments()

privateKey = ''
publicKey = ''
if args['t'] == 'rsa':
    privateKey = RSA.generate(2048)
    publicKey = privateKey.publickey()
elif args['t'] == 'ec':
    privateKey = ECC.generate(curve='P-256')
    publicKey = privateKey.public_key()

pubKeyBytes, privKeyBytes = extractKey(publicKey, privateKey)

print('\nPublic Key:\n', pubKeyBytes)
print('\nPrivate Key:\n', privKeyBytes)

with open(args['pub'], 'wb') as fout: 
    fout.write(pubKeyBytes)

with open(args['priv'], 'wb') as fout: 
    fout.write(privKeyBytes)

