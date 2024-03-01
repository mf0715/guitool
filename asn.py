#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   asn.py
@Time    :   2023/4/2615:53
@Author  :   Hu RunYang
@Version :   1.0
@Contact :   hurunyang@zxcsec.com
@License :   (C)Copyright 2017-2018, Liu group-NLP-CASA
@Desc    :   None
"""
import base64
import pyasn1

whex = {'0': 0x00, '1': 0x01, '2': 0x02, '3': 0x03, '4': 0x04, '5': 0x05, '6': 0x06, '7': 0x07,
            '8': 0x08, '9': 0x09, 'A': 0x0a, 'B': 0x0b, 'C': 0x0c, 'D': 0x0d, 'E': 0x0e, 'F': 0x0f}
wbin = {'0': "0000", '1': "0001", '2': "0010", '3': "0011", '4': "0100", '5': "0101", '6': "0110", '7': "0111",
            '8': "1000", '9': "1001", 'A': "1010", 'B': "1011", 'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"}


DERdata = "MIICGzCCAcMCAQEwSjAHBgUrDgMCGqQfMB0xCzAJBgNVBAYTAkNOMQ4wDAYDVQQDDAVzc2xjYQQUezl+dA6kOmlbgwCOY5/nAUBjNkMCCGbxkWCqAbocMIIBXKCCAVgwCwYJKoZIhvcNAQEBAgIIADAKBggqgRzPVQGCLTAJBgcqgRzPVQFoMAcGBSsOAwIaMIIBIwIIUNY3zyzO62owWTATBgcqhkjOPQIBBggqgRzPVQGCLQNCAASM9KARaBjmE+WsG5ulOuT0Vnn5y4AXDCyM8ka0624YnZlK3E3F6Z4lhH/lJQLLBypw1qU5eTLtyODRpSoVQRhNGA8yMDE5MDgxMjA4MTc1OFoYDzIwMjAwODExMDgxNzU4WqCBmQSBljCBkzELMAkGA1UEBhMCQ04xCzAJBgNVBAgMAlNEMQswCQYDVQQHDAJKTjEPMA0GA1UECgwGU0FOU0VDMQswCQYDVQQLDAJDQTEWMBQGA1UEAwwNU2Fuc2VjQ0FfVGVzdDEkMCIGCSqGSIb3DQEJARYVc3VwcG9ydEBzYW5zZWMuY29tLmNuMQ4wDAYDVQQQDAVKaW5hbhgPMjAxOTA4MjcwMjUzMTlaAgECMAoGCCqBHM9VAYN1BEYwRAIgQMm/FVPzCSUgvlfeJgJg4HEtDepjn1L9p04GzlKdIIwCIDqKOO+10l+MzuOjgchjdLl+WrjSALlp0O+uPhc9tKs3"
decode_data = base64.b64decode(DERdata).hex().upper()
print(decode_data)

class derData():
    def __init__(self, tag, length, value, end):
        self.tag = tag
        self.len = length
        self.val = value
        self.end = end

def hsTobs(source):
    res = ''
    for item in source:
        res = res + wbin[item]
    return res

def binstrTohex(source):
    w = {'0': 0, '1': 1}
    num = 0
    temp = 1
    for item in source[::-1]:
        num = num + temp * w[item]
        temp = temp * 2
    # num = hex(num)
    return num

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

def tlv_decode(data) :
    tag = data[:2]
    data = data[2:]
    if data[:2] == '80':
        data = data[2:]
        value = data[::-1].split('0000')[1][::-1]
        data = data[::-1].split('0000')[0][::-1]
    else:
        if hsTobs(data[0])[0] == '1':
            ll = binstrTohex(hsTobs(data[:2])[1:]) * 2
            data = data[2:]
            length = hexstrTohex(data[:ll]) * 2
            data = data[ll:]
            value = data[:length]
            data = data[length:]
        else:
            length = hexstrTohex(data[:2]) * 2
            data = data[2:]
            value = data[:length]
            data = data[length:]
    # print(value, '\n', data)
    if len(value) > 6:
        return value
    else:
        return data

def der_decode(data):
    while(data != ''):
        print(data)
        data = tlv_decode(data)

der_decode(decode_data)
