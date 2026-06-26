# 抄作业版--分离账号密码与代码的小tips代码优化

- **链接**: 抄作业版--分离账号密码与代码的小tips代码优化.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 16

## 帖子正文

周所周周周知,近来因为不少顾问在网上泄露了自己的账号密码,喜提封号处理. 而我们目前所使用的各种代码文件,最开始的时候,账号密码都是明文写在代码文件里面的,这既不安全,也不优雅.即使很多顾问没有把自己的账号密码泄漏到github,但是顾问之间,顾问AI之间,复制粘贴代码进行交流也是常有的事,所以还是要把账号密码和代码隔离开来.以上废话纯凑字数.下面给出一个直接抄的解决方式:首先我们在你的本地代码同级目录下新建一个config.json文件,里面写上账号密码:{"username": "your_username","password": "your_password"}之后我们写一个读取账号密码的函数:import json# 定义一个全局变量来存储配置信息_config = Nonedef load_config():global _configtry:with open('config.json', 'r', encoding='utf-8') as file:_config = json.load(file)except FileNotFoundError:print("未找到 config.json 文件。")except json.JSONDecodeError:print("无法解析 config.json 文件，可能格式有误。")def conf_get(key):global _configif _config is None:load_config()return _config.get(key)之后把这个代码放到你的代码文件里面,你的账号密码读取方式就变成了这样:# 如果用的是machine_lib:username = conf_get('username')password = conf_get('password')# 如果用的是WQB:wqbs = WQBSession((conf_get('username'), conf_get('password')), logger=logger)最后把原先所有明文出现账号密码的地方都这么处理一下,就可以了.

---

## 讨论与评论 (4)

### 评论 #1 (作者: XM75236, 时间: 1年前)

这我有点忍不了了,兄弟(假装生气)用户名密码应该放在物理机的环境变量里面啊,你还放文件------------------------------------------------------------------------------------------------------------------------------------------------------------------------------热爱生活的老毛-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

楼上老哥说的对,放在系统环境变量也是很安全的方式.那再来一个系统环境变量版本代码吧.windows使用cmd或者powershell输入如下设置:set WQ_USERNAME=your_usernameset WQ_PASSWORD=your_password在代码文件中使用时:import osusername=os.environ.get('WQ_USERNAME')password=os.environ.get('WQ_PASSWORD')从代码角度来看.确实是简洁了很多.同时,如果需要更新账号密码的话,跟设置的操作一致:set WQ_USERNAME=new_usernameset WQ_PASSWORD=new_password如果是linux或者mac,相对复杂一点,他们还是要把数据放到文件里面,操作也麻烦一点点,可以自己尝试看看.

---

### 评论 #3 (作者: ZZ88928, 时间: 1年前)

虽然如此，但是我这样子的username = os.environ.get('BRAIN_CREDENTIAL_EMAIL')password = os.environ.get('BRAIN_CREDENTIAL_PASSWORD')

---

### 评论 #4 (作者: YQ51506, 时间: 8个月前)

这个配置分离的方法确实是个实用的工程实践，在量化开发中很常见。大佬提到的通过json文件管理敏感信息，避免了代码中硬编码账号密码的风险，这点在团队协作和代码分享时特别重要。不过在实际应用中，可能还需要考虑配置文件的安全存储和访问权限管理，比如使用环境变量或者专门的密钥管理服务。在WorldQuant Brain平台上做回测时，我们通常也会把这类配置信息与alpha因子逻辑分离，这样既保证了代码的整洁性，也便于不同环境下的部署。虽然这篇文章没有涉及具体的交易策略，但这种工程化思维对量化开发很有参考价值。

---

