from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

import Crypto.Random
import binascii


class Wallet:

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
    
    def save_keys(self):
        if self.public_key and self.private_key:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('Error creating wallet.')
                return False
    
    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as f:
                self.public_key = f.readline()[:-1]
                self.private_key = f.readline()
            return True
        except (IOError, IndexError):
            print('Error loading wallet.')
            return False
    
    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.export_key('DER')).decode('ascii'), binascii.hexlify(public_key.export_key('DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.import_key(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf-8'))
        signature = signer.sign(h)
        return (binascii.hexlify(signature)).decode('ascii')
    
    @staticmethod
    def verify_transaction(transaction):
        pub_key = RSA.import_key(binascii.unhexlify(transaction.sender))
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf-8'))
        verifier = PKCS1_v1_5.new(pub_key)
        return verifier.verify(h, binascii.unhexlify(transaction.signature))