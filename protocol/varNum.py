# -*- coding: utf-8 -*-

# @File    : varNum.py
# @Date    : 2019-12-26
# @Author  : 王超逸
# @Brief   : mine craft 协议 VarInt和VarLong实现
# python位运算太操蛋了

from protocol.mcField import MCField

LONG = 64
INT = 32


class VarNum(MCField):

    def __init__(self, _type):
        self._data = None
        self.type = _type

    @property
    def data(self):
        return self._data

    def set(self, num):
        # 这一步相当于先转成无符号数
        if num < 0:
            num = 2 ** self.type + num
        data = bytearray()
        while True:
            temp = num & 0b01111111
            num = num >> 7
            if num != 0:
                temp |= 0b10000000
            data.append(temp)
            if num == 0:
                break
        self._data = data
        return self

    def get(self):
        data = self._data
        if data is None:
            return None
        numRead = 0
        result = 0
        while True:
            read = data[0]
            data = data[1:]
            value = read & 0b01111111
            result |= (value << (7 * numRead))
            numRead += 1
            if read & 0b10000000 == 0:
                # 重新转成带符号数
                # 判断符号位
                if 1 << self.type - 1 & result != 0:
                    return result - 2 ** self.type
                else:
                    return result

    def read(self, data):
        i = 0
        while i != len(data):
            if data[i] < 128:
                break
            i += 1
        if i == len(data):
            return -1
        self._data = data[:i + 1]
        return i + 1


def VarInt(num=None):
    if num is None:
        return VarNum(INT)
    return VarNum(INT).set(num)


def VarLong(num=None):
    if num is None:
        return VarNum(LONG)
    return VarNum(LONG).set(num)
