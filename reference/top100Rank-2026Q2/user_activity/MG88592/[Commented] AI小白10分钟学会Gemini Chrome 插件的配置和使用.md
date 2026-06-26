# AI小白10分钟学会Gemini Chrome 插件的配置和使用～～

- **链接**: [Commented] AI小白10分钟学会Gemini Chrome 插件的配置和使用.md
- **作者**: LL61351
- **发布时间/热度**: 4个月前, 得票: 11

## 帖子正文

众所周知，Gemini 3.0非常聪明（模型强大，Token支持百万级），不过直接开通服务，一方面要完成支付认证，另一方面Gemini 3.0每月124.99美刀，估计劝退了不少小伙伴。国区的很多同学使用Gemini cli，具体可以安装使用可以参考OB53521同学的贴子： [../LZ63377/[Commented] 【Community Leader - 因子构造】AI从0到1全自动探索α工作流技巧思路工作流经验分享.md](../LZ63377/[Commented] 【Community Leader - 因子构造】AI从0到1全自动探索α工作流技巧思路工作流经验分享.md)

除了Gemini cli，现在还有一种更简单且免费使用Gemini方案，即Gemini chrome插件。费话不多说，直接上图：

**1.解释数据集及字段**

![图片](images/img_0674eb17c4.jpeg)

**2.生成因子**

![图片](images/img_d099fd7234.jpeg)

**3.因子优化**

![图片](images/img_25b8ac1ad7.jpeg)

**4.模型选择**

![图片](images/img_02f50da0c3.jpeg)

至于生成因子说明这种，太easy，就不一一演示了，Gemini Chrome还有好多功能有待进一步探索～～

不过，目前Gemini chrome 插件仅在大美丽国上线，国内chrome版本不修改一下配置，暂时还不能使用，下面说明一下配置过程。

**第一步：升级Chrome**

确保是最新版本。打开 chrome://settings/help，让它自动更新到最新。

![图片](images/img_6e6751e162.jpeg)

**第二步：改系统地区**

打开chrome设置，把语言设置成美国。（界面语言也必须是english（美国），否则不会展现）

![图片](images/img_1713b5db18.jpeg)

注意，Mac中可能还需要在系统设置中，将chrome改为英文。

![图片](images/img_e9a203910e.jpeg)

**第三步：关闭Chrome**

完全关闭。Windows去任务管理器里确认没有chrome.exe在后台跑着。

**第四步：改配置文件**

这是关键步骤。先备份！

找到这个文件：

Windows：C:\Users\你的用户名\AppData\Local\Google\Chrome\User Data\Local State

Mac为：~/Library/Application Support/Google/Chrome/Local State

复制一份存好，然后用记事本打开原文件，找到这三个字段并修改：

"is_glic_eligible": true

"variations_country": "us"

// 注意这一项不是把值完全改成us，是把国家简称改成us

"variations_permanent_consistency_country": "us"

保存，关闭。

**第五步：重启Chrome**

重新打开浏览器，右上角应该就能看到Gemini图标了。

如果改完Chrome打不开，说明JSON格式写坏了，把备份的文件恢复回去重来。

最后，使用Gemini Chrome一样要科学上网啊，这个没办法。

---

## 讨论与评论 (6)

### 评论 #1 (作者: HY20507, 时间: 4个月前)

真不错，能直接读取页面信息，个人来说使用感觉比mcp还好

---

### 评论 #2 (作者: MZ45384, 时间: 4个月前)

学到了，这个是不是就相当于edge浏览器中的copilot。可以在这个上面使用mcp, skills吗?

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #3 (作者: XW23690, 时间: 4个月前)

很实用的功能，直接读取网页信息，节约截图复制的时间。

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #4 (作者: BW14163, 时间: 4个月前)

先收藏了，看着帖子像是在ios的系统中讲解gemini使用教程，目前电脑还是win，以后有机会了再去尝试下

---

### 评论 #5 (作者: MG88592, 时间: 3个月前)

感谢分享，论坛真满是宝藏。
=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #6 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢大佬的配置分享 ,太实用了，虽然我用的是window系统                                                              ================================自信人生两百年，会当水击三千里==========================

---

