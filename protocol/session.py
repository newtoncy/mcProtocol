# -*- coding: utf-8 -*-

# @File    : session.py
# @Date    : 2019-12-27
# @Author  : 王超逸
# @Brief   : 表示和服务器的会话


from socket import socket, timeout
from threading import Thread
from protocol.packet import Packet

BUFF_SIZE = 1024


class Session:

    def __init__(self, socket_: socket, onPacketRecv=None, onClose=None):
        def doNothing(*x, **y):
            pass

        self.socket = socket_
        if onPacketRecv is None:
            onPacketRecv = doNothing
        if onClose is None:
            onClose = doNothing
        self.receiveThread = Session.ReceiveThread(socket_, onPacketRecv, onClose)
        self.receiveThread.start()

    def sendPacket(self, packet: Packet):
        self.socket.sendall(packet.data)

    class ReceiveThread(Thread):
        def __init__(self, socket_: socket, onPacketRecv, onClose):
            super().__init__()
            self.socket = socket_
            self.onClose = onClose
            self.onPacketRecv = onPacketRecv

        def run(self) -> None:
            self.socket.settimeout(1)
            data = bytearray()
            while True:
                packet = Packet()
                # 没读出完整的包之前一直读下去
                while packet.read(data) == -1:
                    readBuff = None
                    try:
                        readBuff = self.socket.recv(BUFF_SIZE)
                    except timeout as e:
                        continue
                    if not readBuff:
                        self.onClose(data)
                        return
                    data += readBuff
                self.onPacketRecv(packet)
                data = data[len(packet.data):]
