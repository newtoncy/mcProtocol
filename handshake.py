# -*- coding: utf-8 -*-

# @File    : handshake.py
# @Date    : 2019-12-27
# @Author  : 王超逸
# @Brief   : 模拟握手

# 小写的类名有点难受
from socket import socket as Socket
from protocol import Session, Packet, MCString, VarInt, UnsignedShort


def onPacketRecv(packet: Packet):
    if packet.id != 0:
        return
    mcString, = packet.parse([MCString])
    print(mcString.get())


host = "127.0.0.1"
port = 25565
socket = Socket()
socket.connect((host, port))
session = Session(socket, onPacketRecv)
packet = Packet(id=0)
# 协议号，-1表示获取协议号
packet.addField(VarInt(-1))
# host
packet.addField(MCString(host))
# port
packet.addField(UnsignedShort(port))
# Next state
packet.addField(VarInt(1))
session.sendPacket(packet)
# 请求包，id=0，字段为空
packet2 = Packet(0)
session.sendPacket(packet2)
