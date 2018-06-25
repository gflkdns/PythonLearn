# -*- coding: utf-8 -*-
from email import encoders
import os
import traceback
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# 中文处理
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(
        fromName,  # 发件名称
        fromAddress,  # 发件邮箱
        password,  # 这是你邮箱的第三方授权客户端密码，并非你的登录密码
        toaddress,  # 收件人
        subject,
        content,
        files,  # 附件文件
):
    smtp_server = 'smtp.163.com'
    to_addrs = toaddress.split(',')

    msg = MIMEMultipart()
    msg['From'] = fromName + fromAddress  # 显示的发件人
    # msg['To'] = _format_addr('管理员 <%s>' % to_addr)                # 单个显示的收件人
    msg['To'] = ",".join(to_addrs)  # 多个显示的收件人
    msg['Subject'] = Header(subject, 'utf-8').encode()  # 显示的邮件标题
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    for child in files:
        print(child)  # .decode('gbk')是解决中文显示乱码问题
        # 添加附件就是加上一个MIMEBase，从本地读取一个文件
        with open(child, 'rb') as f:
            (filepath, tempfilename) = os.path.split(child);
            # (shotname, extension) = os.path.splitext(tempfilename);
            # 设置附件的MIME和文件名，这里是txt类型:
            mime = MIMEBase('file', 'xls', filename=tempfilename)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=tempfilename)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)

    try:
        server = smtplib.SMTP(smtp_server, 25)
        # server.starttls()
        server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
        server.login(fromAddress, password)
        # print to_addrs
        server.sendmail(fromAddress, to_addrs, msg.as_string())
        server.quit()
    except(Exception):
        print("Error: unable to send email")
        print(traceback.format_exc())


if __name__ == '__main__':
    files = ['C:\\说明.txt']
    send_email("发件人",
               'from@163.com',
               '123456',
               'to@qq.com,to@163.com',
               '邮件title',
               '邮件正文',
               files
               )
