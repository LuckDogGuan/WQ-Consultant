# 分享Check通过后发送邮件通知

- **链接**: [Commented] 分享Check通过后发送邮件通知.md
- **作者**: ZZ88928
- **发布时间/热度**: 1年前, 得票: 2

## 帖子正文

在check阶段通过之后，可以使用QQ邮箱通知alpha可以提交啦

**代码**

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import os

def send_qq_email(sender, password, receiver, subject, content):
    smtp_server = 'smtp.qq.com'

# 尝试两种连接方式（优先使用SSL+465）
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465, timeout=30)
    except:
        # 备用方案：TLS+587
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()

msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

try:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败：{str(e)}")
    finally:
        server.quit()

def send_success_alpha(alpha_id):
    # 配置发件人信息
    sender = " [xxx@qq.com](mailto:xxx@qq.com) "  # 替换为你的QQ邮箱

app_password = os.environ.get("EMAIL_APP_PASSWORD")
    # 邮件内容配置
    receiver = " [xxx@qq.com](mailto:xxx@qq.com) "  # 接收人邮箱
    subject = "Alpha可以提交啦"
    content = f"<h1>alphaid: {alpha_id} </h1><p> [https://platform.worldquantbrain.com/alpha/{alpha_id}</p](https://platform.worldquantbrain.com/alpha/{alpha_id}</p) >"
    send_qq_email(sender, app_password,receiver, subject, content )

if __name__ == "__main__":
    # 配置发件人信息
    sender = " [xxx@qq.com](mailto:xxx@qq.com) "       # 替换为你的QQ邮箱
    app_password = "XXXXXXXXX"  # 替换为QQ邮箱的应用密码

# 邮件内容配置
    receiver = " [xxx@qq.com](mailto:xxx@qq.com) "  # 接收人邮箱
    subject = "测试邮件"
    content = "<h1>这是一封HTML格式的测试邮件</h1><p>内容正文...</p>"

send_success_alpha('22222')

**注意：应用密码不是你邮箱的密码，需要去账号设置那里生成一个应用密码, 生成完记得复制出来，下次就看不到了**

**![图片](images/img_06da145085.png)**

**效果**

可以直接转发到微信，这样子下次提交alpah就有通知啦

**![图片](images/img_bcdf9e8582.png)**

---

## 讨论与评论 (2)

### 评论 #1 (作者: JL16510, 时间: 1年前)

感谢分享，还是比较实用。

---

### 评论 #2 (作者: CF35175, 时间: 1年前)

给新人提醒: 函数send_success_alpha()声明里,

app_password = os.environ.get()是通过环境变量获取邮箱的应用密码,

直接一点的方法是填写明文密码, app_password = "88888888"

安全性会低一些, 不过QQ邮箱可以管理应用密码, 泄露的可以停用掉

---

