import threading

import requests
import json


class Listener:
    ip = '127.0.0.1'
    hp = '5700'
    wp = '8888'

    def __init__(self, i, h, w):
        self.ip = i
        self.hp = h
        self.wp = w

    def sendGroupMsg(self, group_id, msg):
        url = f'http://{self.ip}:{self.hp}/send_group_msg?group_id={group_id}&message={msg}'
        print(f'send|group|({group_id}){msg}')
        return requests.get(url)

    def sendPrivateMsg(self, user_id, msg):
        url = f'http://{self.ip}:{self.hp}/send_private_msg?user_id={user_id}&message={msg}'
        print(f'send|private({user_id}){msg}')
        return requests.get(url)

    def recG(self, group_id, user_id, msg, sender):
        """
            sender用于发送群聊消息，用法
            sender(group_id, msg)
        """
        try:
            #   处理群聊消息
            #   self.sendGroupMsg(group_id, '你发送了： ' + msg)
            #   这是一个简单的复读机实例,返回一个 requests 对象，text为返回文本内容
            return
        except Exception as e:
            print(f"error=> {e}")
            return

    def recP(self, user_id, msg, sender):
        """
            sender用于发送私聊消息，用法
            sender(user_id, msg)
        """
        try:
            #   处理私聊消息
            #   self.sendPrivateMsg(user_id, f'你发送了=> {msg}')
            threading.Thread(target=self.sendPrivateMsg, args=(user_id, f'你发送了=> {msg}')).start()
            return
        except Exception as e:
            print(f"error=> {e}")
            return
