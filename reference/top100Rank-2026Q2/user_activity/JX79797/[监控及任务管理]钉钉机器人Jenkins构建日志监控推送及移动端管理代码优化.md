# [监控及任务管理]钉钉机器人+Jenkins构建日志监控推送及移动端管理代码优化

- **链接**: [监控及任务管理]钉钉机器人Jenkins构建日志监控推送及移动端管理代码优化.md
- **作者**: JX79797
- **发布时间/热度**: 1年前, 得票: 47

## 帖子正文

### 关键词：量化因子流水线、日志实时监控、移动端策略管理、消息驱动自动化

整合 ​ **钉钉机器人** 与​ **Jenkins 实现移动端日志监控及任务管理** ，实现一套自动化、可扩展的7x24小时回测系统，最终支持钉钉群消息驱动任务流。

**需求场景：为什么需要钉钉+Jenkins？**

1. 移动端管理：使用jenkins通过移动端直接查看构建日志、回测、产生alpha、优化alpha、稳定性监测、提交alpha等可视化操作，摆脱电脑限制。

2. 日志监控推送：十分钟循环推送运行状态，避免回测中断

**图例**

**![图片](images/img_1eb455318b.jpeg)**

**核心功能实现**

**1. 钉钉机器人配置**

创建机器人:

在钉钉群设置 → 机器人 → 自定义机器人 → 设置安全策略→ 获取 `Webhook URL`。

安全增强：启用  加签（`SEC`)，防止恶意调用。 python 通过webhook url 和sec 发送消息

**2. Ubuntu安装配置jenkins**

> ```
> sudo apt update sudo apt install openjdk-17-jdkwget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'sudo apt update sudo apt install jenkins
> ```

参考:  [https://cloud.tencent.com/developer/article/1666282](https://cloud.tencent.com/developer/article/1666282)

**钉钉代码参考实现**

```
def send_dingtalk_notification(content: str):    """发送钉钉文本通知并记录日志"""    try:        # 计算签名（钉钉安全要求）        timestamp=str(round(time.time() *1000))        secret_enc=DINGTALK_SECRET.encode("utf-8")        string_to_sign=f"{timestamp}\n{secret_enc.decode()}"        string_to_sign_enc=string_to_sign.encode("utf-8")        hmac_code=hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()        sign=base64.b64encode(hmac_code).decode("utf-8")        # 构造请求        url=f"{DINGTALK_WEBHOOK}&timestamp={timestamp}&sign={sign}"        headers= {"Content-Type": "application/json"}        payload= {            "msgtype": "text",            "text": {"content": content}         }         response=requests.post(url, json=payload, headers=headers, timeout=10)         response.raise_for_status()         # 记录成功日志到文件         dingtalk_logger.info("钉钉通知发送成功，内容：%s", content)    except Exception as e:        # 记录失败日志到文件（包含异常信息）        dingtalk_logger.error("钉钉通知发送失败，内容：%s，错误：%s", content, str(e))
```

 **钉钉发送参考**

```
def send_summary_log():    """每半小时发送关键摘要日志"""    current_time=time.strftime("%Y-%m-%d %H:%M:%S")    ds1_progress=f"{status_manager['completed_alphas']}/{status_manager['total_alphas']}"    loop_progress=f"{status_manager['loop_completed_alphas']}/{status_manager['loop_total_alphas']}"    content=f"【回测系统状态通知】\n" \    +f"时间：{current_time}\n" \    +f"DS1状态：{status_manager['ds1_status']}\n" \    +f"Loop状态：{status_manager['loop_status']}\n" \    +f"Loop当前步骤：{status_manager['loop_current_step']}\n" \    +f"DS1运行进度：{ds1_progress}\n" \    +f"Loop运行进度：{loop_progress}\n" \    +f"最近错误：{status_manager['last_error'] or'无'}\n"    if CUSTOM_BUILD_NUM is not None:        content+=f"日志链接:{JENKINS_URL}job/{JOB_NAME}/{CUSTOM_BUILD_NUM}/console"    print(content)    message= (        content    )    send_dingtalk_notification(message)    # 每1800秒（半小时）重复执行    threading.Timer(1800, send_summary_log).start()threading.Timer(120,send_summary_log).start()
```

**后续拓展**

**打通钉钉机器人驱动jenkins，在钉钉群内实现命令行驱动jenkins功能**

---

## 讨论与评论 (3)

### 评论 #1 (作者: XC66172, 时间: 1年前)

谢谢大佬分享~  我也是用钉钉给我推送消息 （例如一二三阶脚本回测跑完给我推送消息）

目前还没有接触过jenkins 看你的描述是可以 移动端管理 （我一直都很想做个可视化界面可以看到哪些数据集的一二三阶跑过，哪些还没有跑过；码力不够 现在还是手动挑数据集去跑回测，想知道jenkins可以做这样的可视化界面吗？）

期待大佬的后续分享~~

---

### 评论 #2 (作者: JX79797, 时间: 0年前)

@ [XC66172](/hc/en-us/profiles/28880767093655-XC66172)      这个不应该你用数据库管理么，没什么可查看的价值吧，太多了

---

### 评论 #3 (作者: JX28185, 时间: 0年前)

谢谢分享

---

