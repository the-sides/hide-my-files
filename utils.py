
import argparse

# Parse arguments
def readArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', nargs=1, default=None, help='Key Pair Type')
    parser.add_argument('-s', nargs=1, default=None, help='Key Pair Subject')
    parser.add_argument('-pub', nargs=1, default=None, help='Public key output path')
    parser.add_argument('-priv', nargs=1, default=None, help='Private key output path')

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



def extractKey(publicKey, privateKey):
    pubString = publicKey.export_key(format='PEM')
    privString = privateKey.export_key(format='PEM')

    #  Convert to bytes
    if type(pubString) == str:
        pubString = str.encode(pubString)

    if type(privString) == str:
        privString = str.encode(privString)

    return pubString, privString