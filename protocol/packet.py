# -*- coding: utf-8 -*-

# @File    : packet.py
# @Date    : 2019-12-27
# @Author  : 王超逸
# @Brief   : 封装成包

from protocol.varNum import VarNum, INT, VarInt
from protocol.mcField import MCField
from typing import List


class Packet:
    def __init__(self, id=None, sendData=None):
        if sendData is None:
            sendData = bytearray()
        self.sendData = sendData
        self.id = id

    def addField(self, field: MCField):
        if self.sendData is None:
            self.sendData = bytearray()
        self.sendData += field.data

    @property
    def data(self):
        return Packet.buildBytes(self.id, self.sendData)

    @data.setter
    def data(self, value):
        varInt = VarInt()
        i = 0
        i += varInt.read(value)
        i += varInt.read(value[i:])
        self.id = varInt.get()
        self.sendData = value[i:]

    @staticmethod
    def buildBytes(id_, sendData):
        if id_ is None or sendData is None:
            raise ValueError("id或data为空")
        bID = VarNum(INT).set(id_).data
        bLength = VarNum(INT).set(len(sendData) + len(bID)).data
        return bytearray(bLength + bID + sendData)

    # 将包中的内容解析成mcField
    def parse(self, fieldClassList: List[callable]):
        data = self.sendData
        out = []
        i = 0
        for t in fieldClassList:
            field: MCField = t()
            i += field.read(data[i:])
            out.append(field)
        return tuple(out)

    def read(self, data: bytearray):
        varInt = VarInt()
        i = varInt.read(data)
        if i == -1:
            return -1
        length = varInt.get()
        if len(data) < i + length:
            return -1
        self.data = data[:length + i]
        return length + i


# for test
# from protocol.mcString import MCString
# from protocol.mcInt import UnsignedShort
#
# packet1 = Packet(1)
# packet1.addField(MCString("艹"))
# packet1.addField(MCString("fuck"))
# packet1.addField(UnsignedShort(65535))
# packet2 = Packet()
# print(len(packet1.data))
# print(packet2.read(packet1.data))
# fieldList = packet2.parse([MCString, MCString, UnsignedShort])
# print("id=%d,字段=%s" % (packet2.id, repr([field.get() for field in fieldList])))
