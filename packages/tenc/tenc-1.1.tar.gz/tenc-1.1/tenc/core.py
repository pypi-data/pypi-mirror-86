import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# encrypt a text with a password
def encrypt(raw, password):
    """Return iv and content in hex

    :meta public:"""

    cipher = AES.new(password.encode(), AES.MODE_CBC)
    cypher_text_bytes = cipher.encrypt(pad(raw.encode(), AES.block_size))

    return cipher.iv.hex() + ':' + cypher_text_bytes.hex()

# decrypt a text with a password
def decrypt(data, password):
    """Return decrypted string in utf-8

    :meta public:"""
    try:
        content = data.split(':')

        iv = bytes(bytearray.fromhex(content[0]))
        cipher_text = bytes(bytearray.fromhex(content[1]))

        cipher = AES.new(password.encode(), AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(cipher_text), AES.block_size).decode('utf-8')
    except ValueError:
        print("There was an error")
        raise ValueError
