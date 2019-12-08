import rsa
from binascii import b2a_hex, a2b_hex



class rsaCrypt():
    def __init__(self):
        pubkey, prikey = rsa.newkeys(256)
        self.pubkey = pubkey
        self.prikey = prikey

    def encrypt(self, text):
        self.ciphertext = rsa.encrypt(text.encode(), self.pubkey)
        # 因为rsa加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        decrypt_text = rsa.decrypt(a2b_hex(text), prikey)
        return decrypt_text

