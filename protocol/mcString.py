# -*- coding: utf-8 -*-

# @File    : mcString.py
# @Date    : 2019-12-27
# @Author  : 王超逸
# @Brief   : mc string字段

from protocol.mcField import MCField
from protocol.varNum import VarInt


class MCString(MCField):

    def __init__(self, string=None):
        self._data = None
        if string is not None:
            self.set(string)

    def set(self, string):
        encodeStr = string.encode("utf-8")
        self._data = VarInt(len(encodeStr)).data + encodeStr

    def get(self):
        varInt = VarInt()
        i = varInt.read(self.data)
        return self.data[i:].decode("utf-8")

    def read(self, data) -> int:
        varInt = VarInt()
        i = varInt.read(data)
        # -1表示数据不完整
        if i == -1:
            return -1
        length = i + varInt.get()
        if len(data) < length:
            return -1
        self._data = data[:length]

        return length

    @property
    def data(self) -> bytearray:
        return self._data


# for test
# mcString = MCString("fuck！艹")
# mcString2 = MCString()
# print(mcString2.read(mcString.data))
# print(mcString2.get())
# print(mcString2.read(mcString.data[0:1]))
