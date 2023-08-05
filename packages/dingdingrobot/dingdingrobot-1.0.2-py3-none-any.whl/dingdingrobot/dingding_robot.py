import json
import requests
import hashlib
import base64
from pathlib import Path


class DingdingRobot:
    def __init__(self, robot_key):
        self.key = robot_key
        self.webhook_address = 'https://oapi.dingtalk.com/robot/send?access_token=' + self.key

    def _do_request(self, data):
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        resp = requests.post(self.webhook_address, headers=headers, data=json.dumps(data))
        return resp.json()

    @staticmethod
    def _at_mobiles(at_mobiles):
        at_mobiles_list = []
        at_all = False
        if at_mobiles:
            if isinstance(at_mobiles, str):
                at_mobiles = at_mobiles.split(',')

            at_mobiles = list(at_mobiles)
        else:
            at_mobiles = []

        for member in at_mobiles:
            if member.lower() == 'all':
                at_all = True
            else:
                at_mobiles_list.append(member.strip())
        return at_mobiles_list, at_all

    def send_text(self, content, at_mobiles=None):
        at_mobiles_list, at_all = self._at_mobiles(at_mobiles)
        data = {
            'msgtype': 'text',
            'text': {
                'content': content
            },
            'at': {
                'atMobiles': at_mobiles_list,
                'isAtAll': at_all
            }
        }

        return self._do_request(data)

    def send_markdown(self, title, contents, at_mobiles=None):
        send_contents = ''
        at_mobiles_list, at_all = self._at_mobiles(at_mobiles)
        for content in contents:
            if content.startswith('>'):
                send_contents += '\n' + content
            else:
                send_contents += '\n\n' + content

        # 被 @ 的人单独一行
        send_contents += '\n\n'

        # 在 text 中增加被 @ 人的手机号，否则不会 @ 指定人
        for member in at_mobiles_list:
            if member == 'all':
                continue
            else:
                send_contents += ' @' + member

        data = {
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': send_contents
            },
            'at': {
                'atMobiles': at_mobiles_list,
                'isAtAll': at_all
            }
        }
        return self._do_request(data)

    def send_link(self, title, text, jump_url, picurl=None):
        data = {
            'msgtype': 'link',
            'link': {
                'title': title,
                'text': text,
                'messageUrl': jump_url,
                'picUrl': picurl
            }
        }

        return self._do_request(data)

    def send_actioncard(self, title, text, btn_info, btns=False, btn_orientation=0):
        """
        :param title: action card title
        :param text:  action card text，support markdown
        :param btn_info:  button info，format: [{'btn_title': 'title', 'btn_url': 'button url}]
        :param btns: single button or multi buttons
        :param btn_orientation: button orientation， 0 vertical, 1 horizontal
        :return:
        """
        single_button = {}
        multi_button = {'btns': []}
        if not btns:
            single_button['singleTitle'] = btn_info[0]['btn_title']
            single_button['singleURL'] = btn_info[0]['btn_url']
        else:
            for button in btn_info:
                if 'btn_title' in button and 'btn_url' in button:
                    multi_button['btns'].append(
                        {
                            'title': button['btn_title'],
                            'actionURL': button['btn_url']
                        }
                    )
                else:
                    raise KeyError(
                        'btn_info format: {}'.format([{'btn_title': 'button title', 'btn_url': 'buton url'}]))

        data = {
            'msgtype': 'actionCard',
            'actionCard': {
                'title': title,
                'text': text,
                'btnOrientation': str(btn_orientation),
                **single_button,
                **multi_button
            }
        }

        return self._do_request(data)

    def send_feedcard(self, links):
        links_format = [{'link_title': 'link title', 'message_url': 'message url', 'pic_url': 'pictur url'}]
        link_keys = ('link_title', 'message_url', 'pic_url')
        new_links = []
        for link in links:
            for link_key in link_keys:
                if link_key not in link:
                    raise KeyError('links format: {}'.format(links_format))
            else:
                new_links.append({
                    'title': link['link_title'],
                    'messageURL': link['message_url'],
                    'picURL': link['pic_url']
                })

        data = {
            'msgtype': 'feedCard',
            'feedCard': {
                'links': new_links
            }
        }
        print(data)

        return self._do_request(data)
