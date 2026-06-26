# AI打工人配置指南 - Windows\Mac\Linux

- **链接**: [Commented] AI打工人配置指南 - WindowsMacLinux.md
- **作者**: JL11546
- **发布时间/热度**: 18天前, 得票: 147

## 帖子正文

### AI打工人已推出全新版本，请移步 [https://support.worldquantbrain.com/hc/zh-cn/community/posts/41020681850519--AI%E5%B7%A5%E5%85%B7-%E6%96%B0%E7%89%88AI%E6%89%93%E5%B7%A5%E4%BA%BA%E9%85%8D%E7%BD%AE%E6%8C%87%E5%8D%97-PC-Mac-Linux](https://support.worldquantbrain.com/hc/zh-cn/community/posts/41020681850519--AI%E5%B7%A5%E5%85%B7-%E6%96%B0%E7%89%88AI%E6%89%93%E5%B7%A5%E4%BA%BA%E9%85%8D%E7%BD%AE%E6%8C%87%E5%8D%97-PC-Mac-Linux)

### 

### 1. 前置条件

如果你的系统里安装了非Anaconda或uv配置的Python建议卸载掉，设置 - 应用 - 安装的应用 - 找到Python卸载

### 2. 下载安装包

```
通过网盘分享的文件：AI打工人+华子哥插件链接: https://pan.baidu.com/s/19GghIxf1BwNdBf056eifgA?pwd=7rmy 提取码: 7rmy
```

### 3. 安装AI打工人

右键点击"BRAIN *工具一键安装* windows版本.exe" - 以管理员身份运行，选择(强烈建议新建)一个文件夹一键安装

### 4. 安装的同时去申请一个API(以Kimi为例)

a. 去 [Kimi开放平台官网](https://platform.moonshot.cn/)

b. 登录并进入用户中心

c. 进入API Key管理 - 新建API

d. 自定义一个API Key名称和项目 注意保存好API Key

### 5. 安装完成后配置打工人

a. 选择你用的大模型(Kimi/DeepSeek)

b. 输入你的API Key

c. 选择你的模型

d. 终端里输入claude，进入Claude Cli测试一下模型是否配置成功

---------------------------------------------以下为Mac和Linux版本--------------------------------------

### 1. 前置条件

因为Mac & Linux有默认安装且无法卸载的系统版本，Ubuntu 24.04 LTS默认安装的是3.12.x 符合要求，但是Mac默认版本是3.9.x需要另外安装一个3.11以上3.14以下的版本

```
brew install python@3.12
```

最终确认一下你的python有没有问题

```
python3.12 --version
```

### 2. 下载安装包

```
我用夸克网盘给你分享了「BRAIN_工具一键安装_windows版本.exe」，点击链接或复制整段内容，打开「夸克APP」即可获取。/~a7b03Gj2L2~:/链接：https://pan.quark.cn/s/ad11e1a2dfb3?pwd=a7re提取码：a7re
```

### 3. 解压安装包

```
cd ~/Downloadsmkdir -p ~/AIWorker && unzip "Brain_工具一键安装_MacLinux版本.zip" -d ~/AIWorker && cd ~/AIWorker
```

### 4. 安装AI打工人

```
# 也许你需要给pip换个源pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple# 创建虚拟环境python3.13 -m venv .venv# 如果创建虚拟环境报错运行以下命令sudo apt install python3.12-venv# 激活虚拟环境source .venv/bin/activate# 运行脚本zsh/bash install.sh# 如果无法执行脚本运行以下命令给脚本执行权限chmod +x install.sh
```

### 5. 安装的同时去申请一个API(以Kimi为例)

a. 去 [Kimi开放平台官网](https://platform.moonshot.cn/)

b. 登录并进入用户中心

c. 进入API Key管理 - 新建API

d. 自定义一个API Key名称和项目 注意保存好API Key

### 6. 安装完成后配置打工人

a. 选择你用的大模型(Kimi/DeepSeek)

b. 输入你的API Key

c. 选择你的模型

d. 终端里输入claude，进入Claude Cli测试一下模型是否配置成功

---------------------------------------------------------以下为华子哥插件安装方法---------------------------------------------------

**1. 下载插件和数据包，并解压到目录**

**2. 进入插件管理界面 - 打开开发者模式 - 点击加载未打包的扩展程序 - 选择解压后的插件文件夹加载插件**

**3. 复制解压后的数据包中的data文件到解压后的插件文件夹，确保src和data文件夹在同一目录下即可**

**4. 核心功能**

a. 数据分析: 新版数据分析可以让顾问洞察到数据集和数据字段的OS/IS表现，以及不同中性化下的表现；

b. Genius排名分析.

---

## 讨论与评论 (108)

### 评论 #1 (作者: JC25837, 时间: 4个月前)

说的很详细了！可以说AI打工人原则上是Claude Cdoe+WorldQuant Brain mcp的结合体

---

### 评论 #2 (作者: JX39934, 时间: 4个月前)

谢谢大佬写的指南，昨天邮件收到平台送的兑换卷，正准备拿去消费一波，你这帖子就出现了，及时雨啊

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #3 (作者: XG98059, 时间: 4个月前)

用下来之后感觉有点鸡肋。

---

### 评论 #4 (作者: XB37939, 时间: 4个月前)

ai打工人不能用iflow里面的免费key吗？看看能不能优化下

#========= WORLDQUANT BRAIN CONSULTANT ========== #
#每天进步一点点，加油
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%

# sys.setrecursionlimit(α∞)

# PnL = ∑(Robustness * Creativity)

#无限探索、鲁棒性优先，创新性增值

#=================加油每一天=======================#

---

### 评论 #5 (作者: MH33969, 时间: 4个月前)

请教下mac安装到zsh install.sh这一步
报错：zsh: can't open input file: install.sh要怎么解决呀？

---

### 评论 #6 (作者: ZT78950, 时间: 4个月前)

以管理员运行后，然后显示系统找不到文件

---

### 评论 #7 (作者: WT70694, 时间: 4个月前)

感谢整理！正好需要一个完整的配置教程，一键安装对新手太友好了。请问一下，除了Kimi和DeepSeek之外，用其他兼容OpenAI格式的API也能直接接入吗？比如自己部署的本地模型。另外想确认一下，这个工具的核心工作流程是：AI根据模板自动生成表达式 → 调API回测 → 筛选结果这样的循环吗？

---

### 评论 #8 (作者: SL99784, 时间: 4个月前)

你好，换源安装报错许多红色的error403，不换源的话最终显示

❌ 依赖安装脚本执行失败: Command '['/...AIWorker/配置前运行我_安装必要依赖包.py']' returned non-zero exit status 2.

Step 1 failed: Command '['/Library/Frameworks/Python.framework/Versions/3.13/bin/python3', 'Step1_init_project_files.py']' returned non-zero exit status 1.

是Mac的，请问可以怎么解决呢？

---

### 评论 #9 (作者: JL11546, 时间: 4个月前)

[MH33969](/hc/en-us/profiles/30359049038231-MH33969)

确保你的路径里没有空格，我能想到最可能的原因是这个

---

### 评论 #10 (作者: JL11546, 时间: 4个月前)

[SL99784](/hc/en-us/profiles/36565865351063-SL99784)

403错误你可以检查一下你的防火墙和安全设置这些网络设置，或者你的目标文件夹的权限。

---

### 评论 #11 (作者: GY92881, 时间: 4个月前)

学习了，安装试试看！！！

---

### 评论 #12 (作者: YH47265, 时间: 4个月前)

感谢分享，我给打工人配置了GLM4.7，用起来还可以。学习一下如何在mac上配置，马上要用了

=========================================================================

---

### 评论 #13 (作者: YJ11811, 时间: 4个月前)

提取码显示异常，可用重新发一下吗？

---

### 评论 #14 (作者: HA11071, 时间: 4个月前)

学习了！已成功安装，感谢大佬！

---

### 评论 #15 (作者: HN61241, 时间: 4个月前)

为什么非Anaconda或uv配置的Python需要卸载掉？直接用已有的python安装不行吗？

---

### 评论 #16 (作者: MW39826, 时间: 4个月前)

链接地址显示已经失效，能分享一个有效的吗？

---

### 评论 #17 (作者: HY20507, 时间: 4个月前)

很详细了大佬，exe文件的获取也可以从mcp中找，另外如果遇到无法直接使用claude唤起ai打工人的情况，把C:\Users\AppData\Roaming\npm\ 添加到系统PATH环境变量中即可

---

### 评论 #18 (作者: MH33969, 时间: 4个月前)

谢谢大佬！之前的问题解决了，是我没有安装好环境导致的。但是安装好后，在terminal里直接run claude就显示：

Unable to connect to Anthropic services

Failed to connect to api.anthropic.com: ERR_BAD_REQUEST

Please check your internet connection and network settings.

Note: Claude Code might not be available in your country. Check supported

countries at  [https://anthropic.com/supported-countries](https://anthropic.com/supported-countries)

没有让我选择大模型，这该怎么办呀？

---

### 评论 #19 (作者: SZ90852, 时间: 4个月前)

MAC电脑按步骤安装后，终端运行报错，请问如何解决。
报错：

Unable to connect to Anthropic services

Failed to connect to api.anthropic.com: ERR_BAD_REQUEST

Please check your internet connection and network settings.

Note: Claude Code might not be available in your country. Check supported

countries at  [https://anthropic.com/supported-countries](https://anthropic.com/supported-countries)

---

### 评论 #20 (作者: YB55761, 时间: 4个月前)

![图片](images/img_6e90299a27.png)

老师好，请问打工人回测时，终端出现这个是什么原因？谢谢

---

### 评论 #21 (作者: SG27754, 时间: 4个月前)

运行打工人显示连接不上是什么问题，怎么解决呀 ![图片](images/img_3759ff10a6.png)

---

### 评论 #22 (作者: QH29412, 时间: 4个月前)

hi，听了你今天的分享会收获很大，好想用那个工具呀。

可以麻烦你更新一下链接么，下面那个夸克链接过期了。

---

### 评论 #23 (作者: XE68375, 时间: 4个月前)

mac版本的APP界面不是最新的，请问要怎么升级

---

### 评论 #24 (作者: XY60816, 时间: 4个月前)

感谢分享，说得很详细了

---

### 评论 #25 (作者: JL66317, 时间: 4个月前)

谢谢大佬写的指南

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #26 (作者: ZY90274, 时间: 4个月前)

最新安装第2/5步提示找不到cnhkmcp包。

---

### 评论 #27 (作者: YH25030, 时间: 4个月前)

谢谢分享！现在工具版本升级太快了，fomo了

---

### 评论 #28 (作者: ZP77358, 时间: 4个月前)

老师，app里的模板以及直接来点alpha是基于自己的alpha进行参考输出的吗

---

### 评论 #29 (作者: JL11546, 时间: 4个月前)

[YB55761](/hc/en-us/profiles/33469999356055-YB55761)

从截图看是正常的，红色字只是一个提示

---

### 评论 #30 (作者: JL11546, 时间: 4个月前)

cnhkmcp这个包暂时下了，所以如果用一键安装会报错，春节后看如何安排

---

### 评论 #31 (作者: YQ84572, 时间: 4个月前)

很详细的配置指南，感谢大佬的分享，工具更新迭代太快了，得赶紧跟上节奏。

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #32 (作者: MZ45384, 时间: 4个月前)

感谢分享，国区真是好起来了，工具越来越多了。 ====================================================================================== 知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人） # Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100% # sys.setrecursionlimit(α∞) # PnL = ∑(Robustness * Creativity) #无限探索、鲁棒性优先，创新性增值 #Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。 ======================================================================================

---

### 评论 #33 (作者: YP74336, 时间: 4个月前)

楼上有提到一键安装工具安装cnhkmcp报错的，可以单独安装解决，我已经成功安装了。

参考论坛这个帖子【新人向】mcp app安装和使用教程

用这个命令安装pip install --upgrade cnhkmcp

安装好之后用这个命令检查安装路径

pip show cnhkmcp

---

### 评论 #34 (作者: SC47216, 时间: 4个月前)

感谢大佬的分享，有了这么好用的工具，点塔肯定事半功倍

---

### 评论 #35 (作者: FG65608, 时间: 4个月前)

学到了，非常感谢热心博主分享，安装教程完整而且清晰，给博主点赞！！！
=============================================================================

---

### 评论 #36 (作者: YQ51506, 时间: 3个月前)

还没有用，相比于geminicli +mcp和cursor+mcp有什么优点吗

---

### 评论 #37 (作者: JC31003, 时间: 3个月前)

和72变比哪个好用啊

---

### 评论 #38 (作者: YH55729, 时间: 3个月前)

太感谢了，就靠这个帖子才把mac上的打工人装好了

=============================================================================

---

### 评论 #39 (作者: MM27120, 时间: 3个月前)

感谢分享

尝试一下

---

### 评论 #40 (作者: SY73109, 时间: 3个月前)

打工人只能用kimi和deepseek吗，其他的openAi  如何接入。

---

### 评论 #41 (作者: LM81527, 时间: 3个月前)

谢谢, 很及时，正打算呢，正准备拿去消费一波，你这帖子就出现了，及时雨啊

=============================================================================

人生是一场恩典啊，The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #42 (作者: TB73554, 时间: 3个月前)

感谢楼主的分享，本人代码小白，之前按照官方教程一直使用1、2、3阶段代码生产Alpha，一直想体验AI打工人系列，但是配置总是遇到问题，楼主的一键安装Brain AI打工人真的是对于我这种小白来说是宝藏。

我今天上午安装了一下，只需要把之前下载的Python清除干净，然后一键安装就可以，真的是太方便了。

============================================================================================================================================================================

---

### 评论 #43 (作者: XY20037, 时间: 3个月前)

太感谢这位大佬的干货分享了！AI 打工人日常跨 Windows、Mac、Linux 做开发和量化，系统配置这块真的踩过超多坑，从环境搭建、依赖适配到 GPU 加速部署，每一步都容易出问题，这份多系统配置指南真的刚需！不管是刚入门的新人还是老从业者，都能从大佬的分享里少走很多弯路，狠狠收藏慢慢研究，也希望大佬后续能多更些实操避坑和进阶配置的细节，再次感谢大佬的无私分享～

---

### 评论 #44 (作者: TT21691, 时间: 3个月前)

感谢，大佬提供的教程，现在配置起来方便多了。

---

### 评论 #45 (作者: XM92761, 时间: 3个月前)

![图片](images/img_69362bff46.png) 安装到这一步，要我选择模型的时候，我怎么按键盘都没法输入数字进去。换过输入法，点过光标都没用，卡在这里了，有没有哪位大佬遇到过

---

### 评论 #46 (作者: JL11546, 时间: 3个月前)

@SY37109 可以的，修改环境变量中的base_url, api_token和model_name就可以

---

### 评论 #47 (作者: JL11546, 时间: 3个月前)

[YQ51506](/hc/en-us/profiles/27706511330455-YQ51506)  没有区别，如果配置好了自己的cli+mcp环境就没必要再安装了

---

### 评论 #48 (作者: JL11546, 时间: 3个月前)

[JC31003](/hc/en-us/profiles/32842757029783-JC31003)  这个打工人是一个命令行界面，你可以和AI进行对话式的交互，72变是基于你的一个已知因子让AI进行发散，两者不太一样。

---

### 评论 #49 (作者: JL33484, 时间: 3个月前)

系统找不到指定的文件是什么原因？

---

### 评论 #50 (作者: MZ45384, 时间: 3个月前)

请问这个AI打工人跟MCP或SKILLs有什么不同吗？

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #51 (作者: YZ78577, 时间: 3个月前)

![图片](images/img_c0b376eae4.png)

为什么我的下好了打开长这样

---

### 评论 #52 (作者: RR77827, 时间: 3个月前)

window安装失败了，第一步就直接超时了，第一步和第四部  都是装包吗，  第三步 和第二步  没有py文件，能给个具体过程吗，exe文件看样子是python写的

---

### 评论 #53 (作者: LY63868, 时间: 3个月前)

![图片](images/img_c47769c706.png) 到这一步无法输入，有大佬指点一下吗

---

### 评论 #54 (作者: GZ76728, 时间: 3个月前)

太感谢啦

---

### 评论 #55 (作者: XH28239, 时间: 3个月前)

![图片](images/img_65a24a0048.png)

老师好，用管理员运行安装时，提示这个，我无法修改源代码，如何解决

---

### 评论 #56 (作者: BW14163, 时间: 3个月前)

非常详细，非常好用，感谢大佬的教程，配置起来清楚明了，网页已收藏，文件已保存，方便后期循环使用。

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
Prioritize diversity, strong margin, low correlation, stable diversification; strictly control costs and overfitting.
**********************************

---

### 评论 #57 (作者: HH23877, 时间: 3个月前)

![图片](images/img_08b70392a1.png) 
到这一步为什么一直选择不了，输入不了1，重新安装也不行，win10系统

---

### 评论 #58 (作者: CZ75678, 时间: 3个月前)

按照BRAIN *工具一键安装* windows版本.exe安装AI打工人时，运行到第4步选择LLM模型时，出现键盘无法输入的问题，无法选择Kimi还是Deepseek，我的解决方法是：

1. 关闭当前Terminal，重开一个Powershell的Terminal。

2. 找到AI打工人安装目录下的_auto_setup.ps1文件，定位到46行#Step 4这里，把后面的内容全部复制，新建一个新的ps1文件，粘贴进去，并保存，如图所示：

![图片](images/img_381d051139.png)

3. 新打开的Terminal定位到AI打工人安装目录下，运行该ps1文件，这次就可以输入正常完成安装了。

![图片](images/img_fc6dc59b8e.png)

---

### 评论 #59 (作者: HH34943, 时间: 3个月前)

为什么在下载安装包那里，华子哥插件那个最上面那个，在百度网盘提取时显示提取码错误

---

### 评论 #60 (作者: XZ49562, 时间: 3个月前)

AI打工人安装到本地还是服务器上？哪个比较好，也是回测时电脑不能关机吗？

---

### 评论 #61 (作者: LW17674, 时间: 3个月前)

你好，我之前安装了AI 打工人可以正常使用，但是今天开始出现这个错误，请问是什么原因，该如何解决。错误如下：

API Error: 400 {"error": {"type": "invalid_request_error", "message": "failed to convert toolresultcontent:unsupported content type in ContentBlockParamUnion:tool_reference"}, "request_id": "d510b90b-189f-11f1-abe4-4e36facb8db1", "type": "error"

今天发现自己又好了，更正一下。

---

### 评论 #62 (作者: RL11824, 时间: 3个月前)

目前webapp遇到的问题： 
1、增强历史模板失败
设置的是EUR的TOPCS1600的VECTOR，找灵感—回测—筛选alpha—定位json—增强历史模板，报错如图 ![图片](images/img_92367e48e3.png) 
不知道为啥它自己会找TOP3000然后报错

2，下拉选项栏消失

找灵感页面，从json文件生成表达式——为表达式追加参数页面，都存在下拉菜单选项栏消失的问题
 ![图片](images/img_b4f076febb.png)

2.1 找灵感页面无菜单选项时，无法输入
2.2 从json文件生成表达式——为表达式追加参数页面，下拉菜单选项栏消失后可以英文逗号输入，但是中性化选项手动输入REVERSION-AND-MOMENTUM，回测会报错400 "neutralization":"REVERSION-AND-MOMENTUM\" is not a valid choice，切换输入大小写，缩写RAM都会报错

目前问题1无法解决，问题2关闭重启 运行打开我.py 可以解决

---

### 评论 #63 (作者: JL11546, 时间: 3个月前)

[RR77827](/hc/en-us/profiles/30114294639895-RR77827)  Windows下第一步如果超时，大概率是安装git bash时出现的，请打开魔法软件中的TUN模式试一下。

---

### 评论 #64 (作者: JL11546, 时间: 3个月前)

[XH28239](/hc/en-us/profiles/37256979745815-XH28239)  从图片看是因为找不到cnhkmcp这个包，这个包之前从pypi上下过一次又上架了，也许清华源还没有更新，不过周三的webinar上我换了清华源也安装成功了。你重试一下，如果还是找不到这个包就换个其他源比如阿里源，或者切换回官方源。

---

### 评论 #65 (作者: JL11546, 时间: 3个月前)

[XZ49562](/hc/en-us/profiles/34477300871959-XZ49562)  为了安全不支持远程运行访问，回测时不能关机

---

### 评论 #66 (作者: JL11546, 时间: 3个月前)

@LW17674 这可能是因为Claude Code软件层面最新的tool_reference等嵌套格式不被kimi支持，你可以尝试下中断对话之后再恢复，使用kimi的最新模型等方法。

---

### 评论 #67 (作者: JL11546, 时间: 3个月前)

@RL11824 问题1已修复，最新版最近会发布。问题2.1可能和浏览器的设置有关系，问题2.2的中性化设置是REVERSION_AND_MOMENTUM。

---

### 评论 #68 (作者: ZH71971, 时间: 3个月前)

目前采用ubuntu server版本进行安装后，在使用deepseek并配置完成后，使用claude命令进入程序，还是需要选择对应的账号以及claude API等是什么原因呢
 ![图片](images/img_921ffd902e.png)

---

### 评论 #69 (作者: JL11546, 时间: 3个月前)

[ZH71971](/hc/en-us/profiles/32550313745559-ZH71971)  尝试输入以下命令：

```
echo 'export ANTHROPIC_BASE_URL="你的URL"' >> ~/.bashrcecho 'export ANTHROPIC_AUTH_TOKEN="你的API Key"' >> ~/.bashrcecho 'export ANTHROPIC_MODEL="你的MODEL_NAME"' >> ~/.bashrcecho 'export ANTHROPIC_DEFAULT_OPUS_MODEL="你的MODEL_NAME"' >> ~/.bashrcecho 'export ANTHROPIC_DEFAULT_SONNET_MODEL="你的MODEL_NAME"' >> ~/.bashrcecho 'export ANTHROPIC_DEFAULT_HAIKU_MODEL="你的MODEL_NAME"' >> ~/.bashrcecho 'export CLAUDE_CODE_SUBAGENT_MODEL="你的MODEL_NAME"' >> ~/.bashrcsource ~/.bashrc
```

---

### 评论 #70 (作者: CJ39072, 时间: 3个月前)

视频有回放吗

---

### 评论 #71 (作者: WL91677, 时间: 3个月前)

回测器中我点击开始回测，小窗闪退是什么原因呀

---

### 评论 #72 (作者: LM49676, 时间: 3个月前)

非常详细的安装教程，新手顾问学习了！！

---

### 评论 #73 (作者: YG15313, 时间: 3个月前)

论坛里TRAE+MCP和AI打工人在做因子研究的效果上有什么差别吗？

---

### 评论 #74 (作者: LH27867, 时间: 3个月前)

请问安装AI打工人，会和原本电脑安装的claude code打架吗？我看评论区里面说AI打工人是cc+mcp，是不是只要在原cc上配置cnhkmcp就可以了？如果是这样的话，请问有配置mcp的帖子吗？麻烦了！

---

### 评论 #75 (作者: CT59437, 时间: 3个月前)

老师好，我在使用回测器回测时，出现以下错误：

Traceback (most recent call last):
  File "/data/WorldQuant/Brain/untracked/APP/simulator/temp_automated_1773027842.py", line 10, in <module>
    import simulator_wqb
  File "/data/WorldQuant/Brain/untracked/APP/simulator/simulator_wqb.py", line 20, in <module>
    import msvcrt  # For Windows password input with asterisks
    ^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'msvcrt'
我的MAC系统和Linux的错误都是一样的。MAC 我尝试着改程序（ simulator/simulator_wqb.py ）解决了，Linux我没有修改，但是MAC回测时我只使用2并发，3个槽，系统一直提示429，一个alpha都提交不到 WorldQuant上去。

程序只修改了 simulator_wqb.py。

具体两处：

1、把顶层的 import msvcrt 改成了条件导入。原来是直接导入，macOS/Linux 会立刻报ModuleNotFoundError。
现在是：
try:
    import msvcrt
except ImportError:
    msvcrt = None
2、在 get_password_with_asterisks() 里加了非 Windows 回退逻辑。
如果 msvcrt is None，就改用 getpass.getpass(prompt) 隐藏输入密码，而不是继续走 Windows 的按键读取逻辑。

回测进行不下去，程序改错了吗？不改的话，怎么处理呢？

---

### 评论 #76 (作者: TC42785, 时间: 3个月前)

使用cnhkmcp  3.15进入回测器的测试连接直接报错：❌ Connection failed: Connection failed: Object of type Logger is not JSON serializable

---

### 评论 #77 (作者: WA94369, 时间: 3个月前)

好好好

---

### 评论 #78 (作者: LL99265, 时间: 3个月前)

感谢大佬！想办法接处自己的个人知识库，切片加推理成本有点高....

================================================================================

The secret of change is to focus all of your energy not on fighting the old, but on building the new.

================================================================================

---

### 评论 #79 (作者: JL11546, 时间: 3个月前)

[WL91677](/hc/en-us/profiles/31206373668759-WL91677)  这个问题如果出现在mac/linux上已经修复，请更新至最新版，如果还有问题请继续跟帖。

---

### 评论 #80 (作者: JL11546, 时间: 3个月前)

[YG15313](/hc/en-us/profiles/37879862105239-YG15313)  没有区别

---

### 评论 #81 (作者: JL11546, 时间: 3个月前)

[CT59437](/hc/en-us/profiles/32572117514519-CT59437)  感谢提供修改思路，最新版本已经修复了这个问题

---

### 评论 #82 (作者: ZZ41861, 时间: 3个月前)

================================================================================================================================================

感谢分享！跟着步骤一步步走终于成功了，赶紧试试。

================================================================================================================================================

---

### 评论 #83 (作者: YQ51506, 时间: 3个月前)

AI打工人和Geminicli哪个比较好呢

---

### 评论 #84 (作者: MY65447, 时间: 3个月前)

读了这篇文章，很有收获，深受启发，发现要学的还很多。感谢大佬分享！

=========================================================

Keep going every day, and you will surely reap greater rewards

========================================================

---

### 评论 #85 (作者: HC56618, 时间: 3个月前)

读了此文，深受启发，还需要继续学习，多谢大佬分享。

---

### 评论 #86 (作者: YX91186, 时间: 3个月前)

使用打工人需要配置模型。注意我们直接可以从终端里进行模型的更换,我之前第一次的时候想更换一下模型,因为一开始的模型这个花费太多了，我就直接进行重新安装了一次。其实我们点开问号，我们输了问号,就会有一些提示的我们的快捷命令,我们输入这些功能之后就会发现它其实有呃这个更换模型的命令,我们直接在终端内使用就行了。

---

### 评论 #87 (作者: CW62372, 时间: 3个月前)

=============================================================================

感谢大佬超详细的保姆级教程！Mac 端踩了两个小坑终于顺利装完跑通了，给同用 Mac 的朋友避个雷：一是 Python 版本一定要卡在 3.11-3.14 之间，千万别直接用系统自带的 3.9 版本，不然创建虚拟环境和装依赖都会出问题；二是运行安装脚本前一定要先 cd 到解压后的 AIWorker 目录里，不然就会报找不到 install.sh 文件的错。另外亲测兼容国内其他支持 OpenAI 格式的大模型 API，改下配置就能用，对新手太友好了！

=============================================================================

---

### 评论 #88 (作者: XE68375, 时间: 3个月前)

请问我要命令行打开claude，如果要用其他模型，比如心流平台的模型，我修改环境变量中的base_url, api_token和model_name这些变量，用不了，请问怎么回事呢

![图片](images/img_7053e8f222.png)

---

### 评论 #89 (作者: MY65447, 时间: 3个月前)

很详细，有用！

---

### 评论 #90 (作者: WX89624, 时间: 3个月前)

感谢大佬整理得这么细！我之前装环境一直搞不定，看到Python版本要求这块直接恍然大悟。Windows一键安装包真的太友好了，Mac那边的命令也手把手给出来了，完全不用自己踩坑。

---

### 评论 #91 (作者: YW86963, 时间: 3个月前)

感谢分享，部署成功了

－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

**********************************diversity * quality * stable ************************************

－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

---

### 评论 #92 (作者: WY79095, 时间: 3个月前)

感谢大佬提供的工具，但我用的自己其他模型的api无法调用，报错 API Error: 400 thinking type should be enabled or disabled。不知道其他人有遇到类似问题吗？

另外我在安装的时候也遇到了最后一步无论如何也无法输入数字的情况。后来我改了代码把api和key还有模型名称作为配置读入，跳过了交互才解决的，也不清楚什么原因导致的。

---

### 评论 #93 (作者: LL72182, 时间: 2个月前)

感谢大佬的工具，但是大佬，你好像泄露邮箱和密码了。w***************8@ 是你邮箱吗？我再一次使用过程中看见这个邮箱和密码露出来了。

---

### 评论 #94 (作者: JL11546, 时间: 2个月前)

[LL72182](/hc/en-us/profiles/37987737345431-LL72182)  我没有以w开头的邮箱，应该泄露的不是我的邮箱。感谢提醒，我检查一下。

---

### 评论 #95 (作者: YD47986, 时间: 2个月前)

请问 原来的版本 遇到这个 如何处理的？

---

### 评论 #96 (作者: HL10684, 时间: 1个月前)

请教大佬们，为什么在找灵感里面点了直接来点Alpha，运行到后面显示运行失败

```
*Report generated: 2024-12-07 10:15:00 UTC*  
*Analysis depth: Comprehensive field deconstruction + 8-question framework*  
*Next steps: Implement Tier 1 features, validate assumptions, gather additional data as needed*Traceback (most recent call last):
  File "F:\AIworker\untracked\APP\trailSomeAlphas\run_pipeline.py", line 1155, in <module>
    main()
  File "F:\AIworker\untracked\APP\trailSomeAlphas\run_pipeline.py", line 1066, in main
    raise ValueError("No **Concept** blocks with **Implementation Example** found in the ideas file.")
ValueError: No **Concept** blocks with **Implementation Example** found in the ideas file.

❌ 运行失败，请检查日志。
```

换别的数据集又不会运行失败，是能够下载压缩的，搞不懂欸
望大佬们不吝赐教，帮忙看看，祝大佬们VF1.0，base猛猛涨

---

### 评论 #97 (作者: JL11546, 时间: 1个月前)

[HL10684](/hc/en-us/profiles/37142757523095-HL10684)  看上去你的项目里缺少文件，你是不是使用了最近平台新出的Universe

---

### 评论 #98 (作者: ER48854, 时间: 1个月前)

不想卸载anaconda的python, 有什么其他好方法吗

---

### 评论 #99 (作者: Huairui Wang(HW29135), 时间: 1个月前)

为什么安装完之后要登陆Claude的账号啊，是要有Claude账户才能使用吗，不可以直接使用Kimi的API吗

---

### 评论 #100 (作者: ZX39768, 时间: 1个月前)

请问配置完之后可以换模型吗

---

### 评论 #101 (作者: SD71111, 时间: 1个月前)

老师，请问这个和完成VScode+python+jupyter有什么区别，是不是两种工具，用哪一种都行？

---

### 评论 #102 (作者: SD71111, 时间: 1个月前)

安装中

---

### 评论 #103 (作者: SD71111, 时间: 1个月前)

老师，调用deepseek或者kimi过程中，token会有超用吗？

---

### 评论 #104 (作者: SD71111, 时间: 29天前)

老师，我在听顾问群“AI工具助你研究效率翻倍Community Leader Web App、打工人和AIAC 2.0参赛辅导详解”视频课时，老师提到一个untracked这个文件夹，里面有APP的一个文件夹，这个文件能不能发我一下，一直找不到这个文件，AI打工人已经按论坛指导安装好了，但网页APP施工无法操作成功。

---

### 评论 #105 (作者: SD71111, 时间: 28天前)

老师，想问一下，这个Dataset ID是怎么确定的？是红框里的集合吗？ ![图片](images/img_6276c324cb.png)  ![图片](images/img_351081d9e8.png)

---

### 评论 #106 (作者: HJ33503, 时间: 16天前)

====================================================================================对新人很友好，感谢分享朋友正好需要

====================================================================================

---

### 评论 #107 (作者: JL11546, 时间: 15天前)

[ER48854](/hc/en-us/profiles/31953964171799-ER48854)  请下载最新版AI打工人

---

### 评论 #108 (作者: XW25488, 时间: 15天前)

感谢分享，先收藏

---

