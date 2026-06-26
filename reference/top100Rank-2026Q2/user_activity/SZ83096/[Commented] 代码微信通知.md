# 代码微信通知

- **链接**: [Commented] 代码微信通知.md
- **作者**: LL62621
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

加入 wq 已经有一段时间了，感觉也是一个很有趣的平台去学习，也学到了不少金融知识，我基本上是根据培训时的三阶模板跑，也能做到天天提交，由于期末原因，最近没有深入去学习如何写自己的模板，这也是下一步想要提升的目标，听完二次的顾问课后，也开始追求提交更高质量的 alpha。
这里分享一个我的代码运行结束提醒的方法，我使用的 WxPusher，官方文档在这里( [https://wxpusher.zjiecode.com/docs/](https://wxpusher.zjiecode.com/docs/)  )，在这个后台创建自己的应用，应该是扫码加入公众号，后续的提醒消息，也会是从这个公众号发送
 ![图片](images/img_ecc9fa5411.png) 
注意保存自己的 appToken ，然后将自己添加到应用，扫码加入就好了
 ![图片](images/img_84254306b7.png)

然就可以给自己发消息，这里给出一个测试代码：

```
import requestsimport json  url = 'https://wxpusher.zjiecode.com/api/send/message'  body = {  "appToken":"XXXXX给出自己的appToken 就打开应用保存的内容，如果忘记保存，可以选择重置", #必传  "content":"<h1>H1标题</h1><br/><p style=\"color:red;\">欢迎你使用WxPusher，推荐使用HTML发送</p>",#必传  #消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度20(微信只能显示20)，可以不传，不传默认截取content前面的内容。  "summary":"消息摘要",  #内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签，推荐使用这种) 3表示markdown  "contentType":2,  #发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。  "uids":[      "给出自己的uid，可以在给出的公众号服务中找到"  ],  #原文链接，可选参数  "url":"https://wxpusher.zjiecode.com",  #是否验证订阅时间，true表示只推送给付费订阅用户，false表示推送的时候，不验证付费，不验证用户订阅到期时间，用户订阅过期了，也能收到。  #verifyPay字段即将被废弃，请使用verifyPayType字段，传verifyPayType会忽略verifyPay  "verifyPay": False,  #是否验证订阅时间，0：不验证，1:只发送给付费的用户，2:只发送给未订阅或者订阅过期的用户  "verifyPayType":0}  headers = {    "Content-Type": "application/json"  # 指定请求头，表明发送的数据是JSON格式}  try:    # 将Python字典转换为JSON字符串后发送，使用json.dumps方法    response = requests.post(url, data=json.dumps(body), headers=headers)    print("状态码:", response.status_code)    print("响应内容:", response.text)except requests.RequestException as e:    print("请求出现错误:", e)
```

运行后得到
 ![图片](images/img_d3750979eb.png)

可以根据自己的需求定制
 ![图片](images/img_a17cb8609d.png)

如此就可以使用这个应用了，如果有什么问题可以和我交流。

---

## 讨论与评论 (3)

### 评论 #1 (作者: XM75236, 时间: 1年前)

感谢分享,我是老毛.

这里借楼分享一下阿里云短信代码通知,我自己实践完全跑的通的代码

用的时候直接用类调用类方法send_sms即可

```
class SmsSend:    def __init__(self):        pass    @staticmethod    def create_client() -> Dysmsapi20170525Client:        """        使用AK&SK初始化账号Client        @return: Client        @throws Exception        """        config = open_api_models.Config(            access_key_id='',            access_key_secret='',        )        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi        config.endpoint = f'dysmsapi.aliyuncs.com'        return Dysmsapi20170525Client(config)    @staticmethod    def send_sms(        task_type,        task_name    ) -> None:        client = SmsSend.create_client()        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(            phone_numbers='',            sign_name='WorldQuant任务',            template_code='',            template_param='{"task_type":"%s","task_name":"%s"}' % (task_type, task_name)        )        runtime = util_models.RuntimeOptions()        try:            # 复制代码运行请自行打印 API 的返回值            response = client.send_sms_with_options(send_sms_request, runtime)            print(response)        except Exception as error:            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。            # 错误 message            print(error.message)            # 诊断地址            print(error.data.get("Recommend"))            UtilClient.assert_as_string(error.message)
```

---

### 评论 #2 (作者: CT98586, 时间: 1年前)

感谢分享，这个好用的，补一个简单的代码案例方便用：

import requests

url = " [https://wxpusher.zjiecode.com/api/send/message](https://wxpusher.zjiecode.com/api/send/message) "

data_json = {

"appToken":"<你自己的app_token>",

"content":"<content>",

"contentType":1,

"uids":[

"<你自己的uid>"

],

}

requests.post(

url=url,

json=data_json

)

---

### 评论 #3 (作者: SZ83096, 时间: 1年前)

[CT98586](/hc/en-us/profiles/28847461245719-CT98586) 
给你点赞，非常简洁容易实现

---

