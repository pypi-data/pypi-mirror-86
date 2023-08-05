import sys
import os
import argparse

import tenc


def main(args=None):
    parser = argparse.ArgumentParser(description='Encrypt and decrypt files')

    parser.add_argument('-f', dest='path', help='Path to file', required=True)
    parser.add_argument('-p', dest='password', help='The password', required=True)
    parser.add_argument('-d', action='store_true', help='Should decrypt otherwise encrypt')

    args = parser.parse_args()


    if not args.d:
        filename = args.path + '.enc'

        try:
            with open(args.path, 'r') as plainFile:
                with open(filename, 'w') as f:
                    f.write(tenc.encrypt(plainFile.read(), args.password))
                    print('{} encrypted and saved as {}'.format(args.path, filename))
                    f.close()

                plainFile.close()
        except FileNotFoundError:
            print('{} not found'.format(args.path))
    else:
        filename = os.path.join(os.path.dirname(args.path), 'dec_' + os.path.basename(args.path).replace('.enc', ''))

        try:
            with open(args.path, 'r') as encryptedFile:
                with open(filename, 'w') as f:
                    decrypted = tenc.decrypt(encryptedFile.read(), args.password)
                    if decrypted:
                        f.write(decrypted)
                        print('{} decrypted and saved as {}'.format(args.path, filename))
                    f.close()

                encryptedFile.close()
        except FileNotFoundError:
            print('{} not found'.format(args.path))



if __name__ == "__main__":
    sys.exit(main())
