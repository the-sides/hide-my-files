import argparse
from Crypto.Cipher import AES

# Parse arguments
def readArguments(program):
    parser = argparse.ArgumentParser()

    if program == 'keygen':
        parser.add_argument('-t', nargs=1, default=None, help='Key Pair Type')
        parser.add_argument('-s', nargs=1, default=None, help='Key Pair Subject')
        parser.add_argument('-pub', nargs=1, default=None, help='Public key output path')
        parser.add_argument('-priv', nargs=1, default=None, help='Private key output path')
    elif program == 'lock':
        parser.add_argument('-d', nargs=1, default=None, help='The directory to lock or unlock.')
        parser.add_argument('-p', nargs=1, default=None, help='Path to public key')
        parser.add_argument('-r', nargs=1, default=None, help='Path to private key')
        parser.add_argument('-s', nargs=1, default=None, help='The subject you want to encrypt the directory for or who you expect it from.')


    args = parser.parse_args()
    cleanargs = {}

    # Error-check parsed arguments
    for arg in args._get_kwargs():
        if arg[1] == None:
            parser.print_help()
            print("Argument '-{}' is not specified".format(arg[0]))
            exit()
        else:
            cleanargs[arg[0]] = arg[1][0]
    return cleanargs



def extractKey(publicKey, privateKey, subject):
    pubString = publicKey.export_key(format='PEM')
    privString = privateKey.export_key(format='PEM')

    #  Convert to bytes
    if type(pubString) == str:
        pubString = str.encode(pubString)

    if type(privString) == str:
        privString = str.encode(privString)
        
    # Attach subject line
    subject = str.encode(subject+'\n')
    pubString = subject + pubString

    return pubString, privString

def encryptFile(content, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, iv)
    cipherText, tag = cipher.encrypt_and_digest(content)
    return cipherText, tag

def decryptFile(content, tag, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, iv)
    message = cipher.decrypt_and_verify(content, tag)
    return message