# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes
#加密方法
def encrypt_oracle(key,text0):
    # 秘钥
    # key = '123456'
    # 待加密文本
    # text = 'abc123def456'
    # 初始化加密器
    a = base64.b64encode(bytes(text0,encoding='utf-8'))#字符串转字节，转base64转码
    text=str(a, encoding='utf-8')#字节转字符串、处理中文字符用
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text
#解密方法
def decrypt_oralce(key,text):
    # 秘钥
    # key = '123456'
    # 密文
    # text = 'qR/TQk4INsWeXdMSbCDDdA=='
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8') # 执行解密密并转码返回str
    B_t = str.encode(decrypted_text)#字符串转字节
    b = base64.decodebytes(B_t)#base64解码
    return str(b, encoding='utf-8')#字节转字符串
