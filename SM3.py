#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   SM3test.py
@Time    :   2020/11/27 10:34:12
@Author  :   Hu RunYang
@Version :   1.0
@Contact :   hurunyang@zxcsec.com
@License :   (C)Copyright 2017-2018, Liu group-NLP-CASA
@Desc    :   None
"""

MAX = 2 ** 32
T = []
for i in range(0, 16):
    T.append(0x79cc4519)
for i in range(16, 64):
    T.append(0x7a879d8a)


def bitnot(num):
    # 32比特非运算
    s = bin(num)[2:]
    res = ""
    for i in range(len(s)):
        res = res + str(int(s[i]) ^ 1)
    while len(res) < 32:
        res = '1' + res
    re = int(res, 2)
    return re


def rotl(num, n):
    # 32比特循环左移
    s = bin(num)[2:]
    while len(s) < 32:
        s = "0" + s
    s = s[n:] + s[0:n]
    return int(s, 2)


def FF(j, x, y, z):
    if 0 <= j <= 15:
        return x ^ y ^ z
    if 16 <= j <= 63:
        return (x & y) | (x & z) | (y & z)


def GG(j, x, y, z):
    if 0 <= j <= 15:
        return x ^ y ^ z
    if 16 <= j <= 63:
        return (x & y) | (bitnot(x) & z)


def P_0(x):
    return x ^ (rotl(x, 9)) ^ (rotl(x, 17))


def P_1(x):
    return x ^ (rotl(x, 15)) ^ (rotl(x, 23))


def CF(V, B):
    # 消息扩展
    W = []
    W_1 = []
    while B:
        W.append(int(B[0:8], 16))
        B = B[8:]
    for j in range(16, 68):
        tem = P_1(W[j - 16] ^ W[j - 9] ^ rotl(W[j - 3], 15)
                  ) ^ rotl(W[j - 13], 7) ^ W[j - 6]
        W.append(tem)

    for j in range(0, 64):
        W_1.append(W[j] ^ W[j + 4])
    # 压缩函数
    a, b, c, d, e, f, g, h = V
    for j in range(64):
        SS_1 = rotl((rotl(a, 12) + e + rotl(T[j], j % 32)) % MAX, 7)
        SS_2 = SS_1 ^ rotl(a, 12)
        TT_1 = (FF(j, a, b, c) + d + SS_2 + W_1[j]) % MAX
        TT_2 = (GG(j, e, f, g) + h + SS_1 + W[j]) % MAX
        d = c
        c = rotl(b, 9)
        b = a
        a = TT_1
        h = g
        g = rotl(f, 19)
        f = e
        e = P_0(TT_2)
    V_1 = [a, b, c, d, e, f, g, h]
    for i in range(8):
        V[i] = V_1[i] ^ V[i]
    return V


def SM3_Hash(message):
    if max(message) > "F":
        return "ERROR"
    # 消息填充
    message = bin(hexstrTohex(message))[2:]
    while len(message) % 4:
        message = '0' + message
    l = bin(len(message))[2:]
    message = message + '1'
    while (len(message) % 512) < 448:
        message = message + "0"
    while len(l) < 64:
        l = '0' + l
    message = binstrTohex(message + l)[2:]
    msg = []
    while message:
        msg.append(message[0:128])
        message = message[128:]
    # 迭代过程
    V = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
         0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]
    for i in msg:
        V = CF(V, i)
    result = ""
    for i in V:
        tem = hex(i)[2:]
        while len(tem) < 8:
            tem = '0' + tem
        result += tem
    return result.upper()


def HMAC_kdf(k_0, pad_0):
    pad = int(pad_0 * 32, 16)
    k_0 = int(k_0, 16)
    re = hex(k_0 ^ pad)[2:]
    return re


def SM3_HMAC(k, message):
    # HMAC(K,M)=H[(K^+⨁opad)||H[(K^+⨁ipad)||M]]
    b = 64
    kl = len(k)
    if kl == b:
        k_0 = k
    elif kl > b:
        k_0 = SM3_Hash(k)
    else:
        k_0 = k
    k_0 = k_0 + (b - len(k_0)) * '0'
    k_1 = HMAC_kdf(k_0, '36')
    k_2 = HMAC_kdf(k_0, '5c')
    return SM3_Hash(k_2 + SM3_Hash(k_1 + message))


def SM3_Check(k, message, r):
    re = SM3_HMAC(k, message)
    if re == r:
        return True
    return False


def hexstrTohex(source):
    whex = {'0': 0x00, '1': 0x01, '2': 0x02, '3': 0x03, '4': 0x04, '5': 0x05, '6': 0x06, '7': 0x07,
            '8': 0x08, '9': 0x09, 'A': 0x0a, 'B': 0x0b, 'C': 0x0c, 'D': 0x0d, 'E': 0x0e, 'F': 0x0f}
    num = 0x00
    temp = 0x01
    for item in source[::-1]:
        num = num + temp * whex[item]
        temp = temp * 0x10
    # num = hex(num)
    return num


def binstrTohex(source):
    w = {'0': 0, '1': 1}
    num = 0
    temp = 1
    for item in source[::-1]:
        num = num + temp * w[item]
        temp = temp * 2
    num = hex(num)
    return num
