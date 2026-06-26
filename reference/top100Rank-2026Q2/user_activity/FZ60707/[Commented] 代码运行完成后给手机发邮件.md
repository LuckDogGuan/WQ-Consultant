# 代码运行完成后给手机发邮件

- **链接**: [Commented] 代码运行完成后给手机发邮件.md
- **作者**: XL54032
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

之前有同学写了一篇给手机发推送的文章，但是必须是苹果手机，
这里优化了一下，给大家推荐出一种代码运行结束后给发送邮件消息的方法。

只需要在qq邮箱或者其他邮箱拿到授权码然后通过下面的py方法就可以实现给自己发邮件消息了

```
import smtplibfrom email.mime.text import MIMETextfrom email.mime.multipart import MIMEMultipartfrom email.mime.base import MIMEBasefrom email import encoders# 发送邮件def send_email(subject, body, to_emails, attachment_path=None):    '''    发送邮件    :param subject: 邮件主题 str    :param body: 邮件正文 str    :param to_emails: 收件人邮箱 list    :param attachment_path: 附件路径,可选参数，可以把本次发掘的alpha数据附件上     '''    # 邮件服务器配置    smtp_server = 'smtp.qq.com'    smtp_port = 587    smtp_user = '填写你自己的邮箱'  # 发送者邮箱    smtp_password = '填写你自己的授权码'  # 授权码    # 创建MIME多部分消息对象    msg = MIMEMultipart()    msg['From'] = smtp_user    msg['To'] = ', '.join(to_emails)    msg['Subject'] = subject    # 添加邮件正文    msg.attach(MIMEText(body, 'plain'))    # 如果提供了附件路径，则添加附件    if attachment_path:        with open(attachment_path, "rb") as attachment:            part = MIMEBase('application', 'octet-stream')            part.set_payload(attachment.read())            encoders.encode_base64(part)            part.add_header('Content-Disposition', f'attachment; filename="{attachment_path.split("/")[-1]}"')            msg.attach(part)    try:        # 连接至SMTP服务器        server = smtplib.SMTP(smtp_server, smtp_port)        server.starttls()  # 启动TLS加密        server.login(smtp_user, smtp_password)  # 登录SMTP服务器        # 发送邮件        server.sendmail(smtp_user, to_emails, msg.as_string())        print("邮件发送成功！")    except Exception as e:        print(f"邮件发送失败: {e}")    finally:        server.quit()
```

获取QQ邮箱的授权码的方法

1. 打开浏览器并访问  [QQ邮箱官网](https://mail.qq.com/) 。
2. 登录你的QQ邮箱账户。
3. 访问QQ邮箱的设置页面，这通常可以通过点击页面右上角的“设置”图标来完成。
4. 在设置菜单中找到与“账户”、“POP3/IMAP”或者“SMTP服务”相关的选项。
5. 开启POP3/IMAP和SMTP服务，如果你还没有开启的话。这里可能会要求你通过手机验证身份。
6. 一旦服务被开启，你应该能看到一个生成授权码的选项。点击它以生成一个新的授权码。
7. 保存这个授权码，填写到上面的方法里面。

 ![图片](images/img_6422b7fdd2.png)

---

## 讨论与评论 (3)

### 评论 #1 (作者: JS30938, 时间: 1年前)

支持使用126邮箱实现回测结果发送邮件通知

```
import yagmailfrom datetime import datetimedef sendmail(contents,region,attachments):    # 邮件配置      from_mailbox = 'xxxxx@126.com'       password = 'xxxxxx' # 此处同样是登录网页邮箱，开启POP3/IMAP和SMTP服务后，提供的邮箱授权码      smtp_server = 'smtp.126.com'      to_mailbox = 'xxxx@xxxx.com'      maildate = current_datetime.strftime("%Y-%m-%d") # 日期格式如2024-12-25      subject = maildate + f'-{region}-alpha-check-result'  # 邮件主题格式如 2024-12-25-USA-alpha-check-result      contents = contents  # 邮件正文这里使用字符串类型      attachments = attachments  # 提供邮件附件路径，同样支持如xlsx、csv文件      yag = yagmail.SMTP(from_mailbox,password,smtp_server)       yag.send(to_mailbox,subject,contents,attachments)         
```

---

### 评论 #2 (作者: ZZ83981, 时间: 1年前)

感谢分享~另外想说一下我遇到的问题。

我用的是阿里云服务器，发现对于以下设置跑不通

smtp_server = 'smtp.163.com'
smtp_port = 25

用上述smtplib.SMTP接口连接不上没法发邮件，后来在网上搜到了可以用SMTP_SSL接口，然后smtp_port = 465就可以了，代码如下

![图片](images/img_e726a8e60f.png)

---

### 评论 #3 (作者: FZ60707, 时间: 9个月前)

很好的文章，本来是要去网上搜怎么用python发送邮箱的，结果一看论坛里面就有现成的，真是方便。

=================================包上GM的===================================================================================================================================================================================================================================================================

---

