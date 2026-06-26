# win10解决cmd窗口不显示图标和特殊符号的问题经验分享

- **链接**: [Commented] win10解决cmd窗口不显示图标和特殊符号的问题经验分享.md
- **作者**: MS70058
- **发布时间/热度**: 5个月前, 得票: 4

## 帖子正文

1.升级之前，运行cli的窗口是这样的，todo列表因为不显示✅️等特殊符号，不明显，字体也不好看，背景也没有高级感

![图片](images/img_936bfa9ceb.png)

2.升级之后，是这样的，舒服多了

![图片](images/img_22153edcb8.png)

3.解决思路，用window Terminal替代原始的cmd窗口作为默认启动的命令行工具

4.详细步骤

①安装Windows Terminal

下载地址：   [https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-GB&gl=CA](http://%C2%A0%20https//apps.microsoft.com/detail/9n0dx20hk701?hl=en-GB&gl=CA)

安装完毕后，鼠标在空白地方右键可出现“在终端打开(T)”,即可用wt启动iflow cli等工具，但是遇到比如chnkmcp中的一键启动的脚步，默认还是调用的原始CMD窗口，下一步怎么把wt设置默认启动窗口

②升级win10

搜索得知， Windows 10 的默认终端设置选项主要出现在 ‌ **22H2** ‌ 或更高版本中，或通过安装最新更新后出现；如果系统未显示该选项，建议进入“设置”>“更新和安全”>“Windows 更新”，安装所有可用更新后重启系统。‌

先检查自己的win10系统版本是否符合标准，不符合，就先升级。

③设置Window Terminal为默认启动命令行工具

升级之后，先打开cmd窗口，然后在当前窗口头部边框上右键点击“属性”，设置默认终端为

“windows终端”

![图片](images/img_97e07c7867.png)

④验证

然后，用cmd命令启动，可以愉快的使用了。

PS：

对于Alpha的研究，一直都在学习的路上，没有什么独特见解，只能在细枝末节上贡献点经验了。

---

## 讨论与评论 (6)

### 评论 #1 (作者: HZ99685, 时间: 5个月前)

下载链接打不开啊

---

### 评论 #2 (作者: JX14975, 时间: 5个月前)

感谢楼主分享，真是帮了大忙。

补充一点：这个东西对gemini cli其实更加重要。否则Gemini非常容易出现花屏，闪屏等情况，尤其是在等待回测与。使用原cmd窗口时复制粘贴也会卡顿。

---

### 评论 #3 (作者: MZ45384, 时间: 4个月前)

大佬，这个链接打开后显示

# 500 Internal Privoxy Error

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #4 (作者: MS70058, 时间: 4个月前)

MZ45384 HZ99685 百度搜Windows terminal就行  可能我之前开着魔法，给我的是国外地址，或者直接去win10的应用商店搜都可以哒

 [https://apps.microsoft.com/detail/9n0dx20hk701?ocid=webpdpshare](https://apps.microsoft.com/detail/9n0dx20hk701?ocid=webpdpshare)

---

### 评论 #5 (作者: HZ99685, 时间: 4个月前)

MZ45384 HZ99685 百度搜Windows terminal就行 可能我之前开着魔法，给我的是国外地址，或者直接去win10的应用商店搜都可以哒
 [https://apps.microsoft.com/detail/9n0dx20hk701?ocid=webpdpshare](https://apps.microsoft.com/detail/9n0dx20hk701?ocid=webpdpshare)

应用商店无法加载此页面。。。。

---

### 评论 #6 (作者: MS70058, 时间: 4个月前)

[HZ99685](/hc/zh-cn/profiles/32603557750935-HZ99685)  这我也不知道了，我是可以打开的，就在普通网络下，不行你就直接问AI，问搜索引擎，Windows terminal的下载地址，总有一个能打开的

---

