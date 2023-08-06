# coding:utf -8
import smtplib
from email.mime.text import MIMEText
from time import sleep

import numpy as np
from notetool import SecretManage
from notetool.crawler.ba import BodyGuardPharm
from notetool.tool.log import log

logger = log("ba-crawler")


def send_mail_163(subject="有货了", content="抢到了，快找牛哥，晚了就没了", receive="1007530194@qq.com"):
    if receive is None:
        receive = ["1007530194@qq.com"]
    elif isinstance(receive, str):
        receive = [receive]

    sender = "15068733021@163.com"  # 发送方
    password = "LXGFFHMVBECEBOXO"  # 邮箱密码
    message = MIMEText(content, "plain", "utf-8")
    # content 发送内容     "plain"文本格式   utf-8 编码格式

    message['Subject'] = subject  # 邮件标题
    message['To'] = receive[0]  # 收件人
    message['From'] = sender  # 发件人

    smtp = smtplib.SMTP_SSL("smtp.163.com", 994)  # 实例化smtp服务器
    smtp.login(sender, password)  # 发件人登录
    # as_string 对 message 的消息进行了封装
    smtp.sendmail(sender, receive, message.as_string())
    smtp.close()
    logger.info("sen to {} success".format(receive))


ba = BodyGuardPharm()


for i in range(10):
    res1 = ba.add_cart(product_id=44434)
    sleep(np.random.randint(2, 10))
    # res2 = ba.add_cart(product_id=44435)
    res2 = ba.add_cart(product_id=169826)
    print(res1)
    print(res2)
    if res1['status'] == 200 or res2['status'] == 200:
        for j in range(3):
            #send_mail_163(receive=["1007530194@qq.com", '594210169@qq.com'])
            send_mail_163(receive=["1007530194@qq.com"])
            sleep(np.random.randint(10, 20))
        break
    print('sleep')
    sleep(np.random.randint(60, 120))
