# -*- coding: utf-8 -*-

# @File    : mcField.py
# @Date    : 2019-12-27
# @Author  : 王超逸
# @Brief   : 字段基类


# 这个程序写的很智障的一点在于：read接收的参数是一个bytes或者byteArray而不是一个流
# 不过这个操蛋的点会在session中得到妥善处理
# 主要是python好像处理流这种东西不太得劲

class MCField:
    # 设置这个字段的值
    def set(self, value):
        raise NotImplementedError()

    # 得到这个字段的值
    def get(self):
        raise NotImplementedError()

    # 从一个bytes或者byteArray对象中取出这个字段，并返回长度
    # 如果数据不完整应该返回-1
    def read(self, data) -> int:
        raise NotImplementedError

    # 获得字节流格式的数据
    @property
    def data(self) -> bytearray:
        raise NotImplementedError
