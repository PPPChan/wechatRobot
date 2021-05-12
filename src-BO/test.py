# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    :
# @Software: PyCharm

from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading


logging.basicConfig(level=logging.INFO)
queue_recved_event = Queue()


# 这是消息回调函数，所有的返回消息都在这里接收，建议异步处理，防止阻塞
def on_message(message):
    print(message)
    message_data = message.get('data')
    # 这里是判断是否是转账消息 如果是转账消息存起来 由其他线程判断是否收款
    if message_data and isinstance(message_data, dict) and message_data.get('data_type') == '49' and message_data.get('is_recv') and '<title><![CDATA[微信转账]]></title>' in message_data.get('msgcontent'):
        queue_recved_event.put((0, message))
    if message_data and isinstance(message_data, dict) and message_data.get('data_type') == '37' and message_data.get('is_recv'):
        queue_recved_event.put((1, message))
    if message_data and isinstance(message_data, dict) and message_data.get('data_type') == '49' and message_data.get('is_recv') and '<title><![CDATA[邀请你加入群聊]]></title>' in message_data.get('msgcontent'):
        queue_recved_event.put((2, message))


def on_error():
    print('error!!!')


def main():
    # 初次使用需要pip安装两个库：
    # pip install requests
    # pip install pycryptodomex
    #
    # 查看支持的接口信息
    help(WechatPCAPI)

    wx_inst = WechatPCAPI(on_message=on_message, on_wx_exit_handle=on_error,log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    print(wx_inst.get_myself())

    time.sleep(15)

    # 开启保存文件图片等功能，不调用默认不保存，调用需要放在登陆成功之后
    wx_inst.start_auto_save_files()
    # 发送消息并@某人
    # wx_inst.send_text_and_at_someone('22941059407@chatroom', 'wxid_6ij99jtd6s4722', '车臣', '你好')
    # time.sleep(2)
    # 发送消息
    # wx_inst.send_text(to_user='filehelper', msg='作者QQ:\r1446684220')
    # 发图片
    # wx_inst.send_img(to_user='filehelper', img_abspath=r'C:\Users\Leon\Pictures\1.jpg')
    # time.sleep(1)
    # 发分享链接
    # wx_inst.send_link_card(
    #     to_user='filehelper',
    #     title='博客',
    #     desc='我的博客，红领巾技术分享网站',
    #     target_url='http://www.honglingjin.online/',
    #     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
    # )
    # time.sleep(1)

    # 这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
    # wx_inst.get_member_of_chatroom('21644142615@chatroom')

    # # 删除好友
    # wx_inst.delete_frinds("wx_123231212121")  # 参数写wxid

    # # 更新好友 一般不用调，后台会维护好友表，但是不放心表不准，可以先调用这个再调get_friends
    # wx_inst.update_frinds()

    # 这个是更新所有好友、群、公众号信息的，结果信息也从上面的on_message返回
    # wx_inst.get_friends()

    # 发送文件或视频
    # wx_inst.send_file('filehelper', r'C:\Users\Leon\Desktop\wechat\1.txt')
    time.sleep(5)
    # 查询群成员中特定人的详细信息
    # wx_inst.get_chatroom_member_detail('21644142615@chatroom', 'wxid_nft9am31y67222')

    # 备注好友
    wx_inst.remark_frinds('wxid_6ij99jtd6s4722', '小2')

    time.sleep(2)
    # 修改群名称
    wx_inst.modify_group_name('22941059407@chatroom', '新群名')

    time.sleep(2)
    # 踢出群成员
    wx_inst.remove_group_member('22941059407@chatroom', 'wxid_6ij99jtd6s4722')

    time.sleep(2)
    # 修改群公告，会自动@所有人
    wx_inst.modify_group_notice('22941059407@chatroom', '新公告内容')

    time.sleep(2)
    # 拉人进群
    wx_inst.invite_into_group('22941059407@chatroom', 'wxid_6ij99jtd6s4722')

    # 接受事件处理
    while True:
        msg_type, message = queue_recved_event.get()
        if msg_type == 0:  # 这里可以添加是否收款的判断， 调用下面接口完成收款
            wx_inst.accept_transfer(message)
        elif msg_type == 1:  # 这里可以添加是否同意好友请求的判断， 调用下面接口完成收款
            wx_inst.accept_friend(message)
        elif msg_type == 2:  # 这里可以添加是否同意好友请求的判断， 调用下面接口完成收款
            wx_inst.accept_chatroom(message)
        time.sleep(1)


if __name__ == '__main__':
    main()
