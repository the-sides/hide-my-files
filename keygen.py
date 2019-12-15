from utils import readArguments
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA, ECC

# Parse arguments
args = readArguments()

privatekey = ''
publicKey = ''
if args['t'] == 'rsa':
    privatekey = RSA.generate(2048)
    publicKey = privatekey.publickey()
elif args['t'] == 'ec':
    privatekey = ECC.generate(curve='P-256')
    publicKey = privatekey.public_key()


print('\nPrivate Key:\n', privatekey.export_key(format='PEM'))
print('\nPublic Key:\n', publicKey.export_key(format='PEM'))
