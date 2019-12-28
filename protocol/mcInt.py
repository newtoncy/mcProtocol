# -*- coding: utf-8 -*-

# @File    : mcInt.py
# @Date    : 2019-12-27
# @Author  : 王超逸
# @Brief   : 不可边长度的整数

from protocol.mcField import MCField


class MCInt(MCField):
    def __init__(self, value, length, signed):
        self.value = value
        self.length = length
        self.signed = signed

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def read(self, data) -> int:
        if len(data) < self.length:
            return -1
        data: bytearray = data[:self.length]
        self.value = int.from_bytes(data, 'big', signed=self.signed)
        return self.length

    @property
    def data(self) -> bytearray:
        return bytearray(self.value.to_bytes(self.length, 'big', signed=self.signed))


def Byte(value=0):
    return MCInt(value, 1, True)


def Short(value=0):
    return MCInt(value, 2, True)


def Integer(value=0):
    return MCInt(value, 4, True)


def Long(value=0):
    return MCInt(value, 8, True)


def UnsignedByte(value=0):
    return MCInt(value, 1, False)


def UnsignedShort(value=0):
    return MCInt(value, 2, False)


def UnsignedInteger(value=0):
    return MCInt(value, 4, False)


def UnsignedLong(value=0):
    return MCInt(value, 8, False)
