import asyncio
import websockets
import json
import requests


class Bot:
    url = '127.0.0.1'
    http_port = '5700'
    ws_port = '8888'

    def __init__(self, u, h, w):
        self.url = u
        self.http_port = h
        self.ws_port = w

    def sendGroupMsg(self, group_id, msg):
        #   发送群聊消息（内部使用）
        return requests.get(f'http://{self.url}:{self.http_port}/send_group_msg?group_id={group_id}&message={msg}').text

    def sendPrivateMsg(self, user_id, msg):
        #   发送私聊消息（内部使用）
        return requests.get(f'http://{self.url}:{self.http_port}/send_private_msg?user_id={user_id}&message={msg}').text

    async def run(self, receivegroupmsg, receiveprivatemsg):
        async with websockets.connect(f"ws://{self.url}:{self.ws_port}") as websocket:
            while True:
                a = await websocket.recv()
                #   这里持续等待 websocket 推送，若接收到信息就向后运行
                js = json.loads(a)
                #   js['post_type'] = ‘message’    js['message_type'] = 'group/private'
                if js['post_type'] == 'message':
                    try:
                        post_type = js['post_type']
                        message_type = js['message_type']
                        if message_type == 'group':
                            group_id = js['group_id']
                            user_id = js['sender']['user_id']
                            msg = js['raw_message']
                            print(f'{post_type}|{message_type}[{group_id}]({user_id}){msg}')
                            receivegroupmsg(group_id, user_id, msg)
                        elif message_type == 'private':
                            user_id = js['sender']['user_id']
                            msg = js['raw_message']
                            print(f'{post_type}|{message_type}({user_id}){msg}')
                            receiveprivatemsg(user_id, msg)
                    except Exception as e:
                        print(f"error=> {e}")
                        continue
                        #   如果出现特殊的异常，即在 post_type == message 时 message_type 出现异常将会报错
