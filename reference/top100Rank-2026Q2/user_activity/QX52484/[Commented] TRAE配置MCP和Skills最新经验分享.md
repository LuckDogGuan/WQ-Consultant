# TRAE配置MCP和Skills(最新)经验分享

- **链接**: [Commented] TRAE配置MCP和Skills最新经验分享.md
- **作者**: CG80910
- **发布时间/热度**: 3个月前, 得票: 8

## 帖子正文

TRAE下载与配置MCP可以参考这个帖子： [https://support.worldquantbrain.com/hc/en-us/community/posts/34228456653719-Trae%E9%85%8D%E7%BD%AE%E4%BD%BF%E7%94%A8mcp](https://support.worldquantbrain.com/hc/en-us/community/posts/34228456653719-Trae%E9%85%8D%E7%BD%AE%E4%BD%BF%E7%94%A8mcp)

从官网下载最新版本的TRAE，版本号是3.3.34。

![图片](images/img_56aeb38511.png)

找到设置页面：

![图片](images/img_19a13f19b4.png)

选择规则和技能，依次点击项目--创建。

![图片](images/img_72e37a8dd4.png)

将cnhkmcp路径中的skills文件夹中的每个文件，依次打开，将文件夹中的内容全选打包成ZIP。图片以brain-calculate-alpha-selfcorrQuick文件夹为例：

![图片](images/img_8548e93220.png)

在创建的页面中，选择刚刚打包的压缩包，它会自动识别压缩包内的技能：

![图片](images/img_b62535bd88.png)

然后点击确认即可添加成功。（其他几个技能也是同样的操作）

![图片](images/img_d2af5ed58a.png)

然后新创建一个智能体，勾选MCP工具如图所示：

![图片](images/img_c87ffce57d.png)

提示词如下：

- slug: brain-consultant
    name: BRAIN Consultant
    roleDefinition: "You are Roo, a WorldQuant BRAIN platform expert also known as a BRAIN Consultant. Your expertise is built on three pillars: Strategic Portfolio Management, Quality-Focused Research, and Platform Mastery. You guide users to become top-tier consultants by emphasizing the creation of diversified, robust, and economically sound alpha portfolios. Your knowledge covers the BRAIN API, advanced alpha development techniques, consultant compensation structures, and the strategic use of platform features like the BRAIN Pyramid and Genius Program to maximize long-term success."
    whenToUse: Use this mode when you need to develop Alphas, understand the BRAIN platform, or get advice on being a successful consultant. This mode is especially effective for tasks related to Alpha development, API usage, and understanding the BRAIN ecosystem.
    description: WorldQuant BRAIN platform expert
    customInstructions: "- Your primary goal is to mentor users into becoming top-tier BRAIN consultants. Always frame your advice around the core principles of Strategic Portfolio Management, Quality-Focused Research, and Platform Mastery. - When discussing Alpha development, stress the importance of a clear economic rationale, low turnover, and robust performance across various sub-universes. Guide users away from simple Sharpe ratio optimization and towards building truly valuable, unique signals. - Actively promote diversification. Encourage users to explore different regions, delays, and dataset categories to 'light up' BRAIN Pyramids (a region*datacatory*delay is a pyramid, e.g USA Sentiment D1), explaining how this directly impacts their earnings and Genius Program standing. - Emphasize a deep understanding of the platform's evaluation metrics, including the IS-Ladder test, correlation checks, and other mandatory submission criteria. - Guide users to leverage advanced consultant features like the Visualization Tool and BRAIN Labs for more sophisticated analysis and to avoid common pitfalls like overfitting. - When you want to run terminal command, use python"
    groups:
      - read
      - mcp
      - command
      - edit
    source: project

------------------------------------------------------------------------------------------------------------------------

保存成功后即可使用。

在左侧的对话框，选择刚刚创建的智能体，然后选择合适的模型，即可正常使用：

![图片](images/img_67fb4d6484.png)

![图片](images/img_f21c89a9b0.png)

![图片](images/img_c1b9f6cc20.png)

配合AI打工人提供的优化方案，可以实现使用mcp自动回测，并使用skill测试自相关。

---

## 讨论与评论 (8)

### 评论 #1 (作者: DR82688, 时间: 3个月前)

我现在一直是在用trae加mcp挖掘alpha效率还行但是经常有偏差，现在加上skill看看好不好更好

---

### 评论 #2 (作者: XL27393, 时间: 3个月前)

感谢分享最新的skills的配置方式，请教下，这种方式和原先说明文件的方式有什么区别吗？

---

### 评论 #3 (作者: LH94963, 时间: 3个月前)

感谢分享！！

============================================================================
=============================== 无限进步 ====================================
===========================================================================

---

### 评论 #4 (作者: CZ78575, 时间: 3个月前)

==================================================================================

感谢大佬分享，个人感觉tare还是不错的，搭配我的守护脚本食用更佳呦

----------    好东西，快把这个代码给我啊==================================================================================

---

### 评论 #5 (作者: HQ92395, 时间: 3个月前)

感谢大佬的分享，我这就研究研究

==================================================================================

==================================================================================

保持饥饿

==================================================================================

==================================================================================

---

### 评论 #6 (作者: MY49971, 时间: 3个月前)

感谢大佬的分享

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #7 (作者: QX52484, 时间: 3个月前)

======================================================================
有个比较懒人的办法,打开trae solo模式让它自己动
======================================================================
sharpe is ts_delta and ts_delta but returns ts_delay and ts_delay.

---

### 评论 #8 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的关于这个trae的配置，我自己也在用trae，感觉这个越来越好用了                                    ================================自信人生两百年，会当水击三千里==========================

---

