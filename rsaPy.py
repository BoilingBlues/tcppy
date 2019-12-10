# -*- coding: UTF-8 -*-

import rsa

class rsaPy():

    def __init__(self):
        pubkey, prikey = rsa.newkeys(1024)
        self.pubkey = pubkey.save_pkcs1()
        self.prikey = prikey

    def encrypt(self,text,publickey):
        """Use public key encryption"""
        publickey = rsa.PublicKey.load_pkcs1(publickey)
        ciphertext = rsa.encrypt(text, publickey)
        return ciphertext

    def decrypt(self,text):
        """Decrypt with private key"""
        decrypt_text = rsa.decrypt(text, self.prikey)
        return decrypt_text


