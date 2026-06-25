# ❗【顾问必读】如何使用BRAIN API ？

- **链接**: https://support.worldquantbrain.com/hc/en-us/community/posts/21728222349335--%E9%A1%BE%E9%97%AE%E5%BF%85%E8%AF%BB-%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8BRAIN-API
- **作者**: KJ42842
- **发布时间/热度**: 2 years ago, 得票: 17

## 帖子正文

为方便大家学习使用API，我们将API相关资料收录于此，敬请参阅：【准备工作】👉Python的安装、学习和API文档的下载【新手必读】👉BRAIN API可以实现的功能(Course 1 content, most important)【学习必读】👉如何自动化创建Alpha（Machine Alpha）合集内容【常见报错】👉BRAIN API及日常回测时常见的报错【使用技巧】👉Brain API技巧：如何挖掘API【使用技巧】👉使用大语言模型创建一个BRAIN代码助手【下载样例】👉ACE：Alpha Creation Engine如何设置云电脑之京东云？如何免费领取阿里无影云电脑使用如何使用天翼云主机进行云端程序挂载

---

## 讨论与评论 (2)

### 评论 #1 (作者: WL13229, 时间: 1 year ago)

代码框架性路线图，如果您第一次接触BRAIN API，请先在上述文档的支持下，实现Note Book1，再攻克Note Book2Note Book1登录：调用sign_in函数进行登录并建立会话。定义模拟设置：设置模拟参数，包括区域、延迟、宇宙、和工具类型。数据集检索和过滤：调用get_datasets函数检索数据集。根据用户的需求进行过滤，比如基于覆盖率过滤数据集。数据字段检索：遍历数据集，检索符合用户需求的数据字段，比如类型为 'MATRIX' 的数据字段。Alpha 表达式构建和模拟：使用模板构建 alpha 表达式，通过循环遍历有效的数据字段或运算符构建 alpha 表达式。将 alpha 表达式添加到回测设置中，形成有效的 alpha 请求，！！并将所有 alpha 请求存入列表中！！！👈非常关键，便于日后检查遍历 alpha 列表，并将每个 alpha 请求发送至服务器进行回测。

---

### 评论 #2 (作者: WL13229, 时间: 1 year ago)

Note Book2登录：调用sign_in函数进行登录并建立会话。读取Note Book 1中存储的Alpha列表：注意关注每个Alpha的Setting和表达式。获取账号IS Alpha List结果：调用 get_n_is_alphas 函数获取IS Alpha列表，它们都是已完成回测的Alpha。将上一步读取到的Alpha列表里的每个Alpha与IS Alpha列表进行匹配，查看哪些Alpha已完成回测，哪些没有完成。将已完成回测的Alpha进行存储，以便日后分析。系统性检验已完成回测的Alpha质量：效率分：有多少个可以提交的Alpha。质量分：除异常值及无信号的值后，Alpha的OS/IS统计表现如何提交Alpha：选取合适的Alpha进行提交。

---

