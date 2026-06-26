# 关于手机上安装cnhkmcp的方法经验分享

- **链接**: [Commented] 关于手机上安装cnhkmcp的方法经验分享.md
- **作者**: LD27384
- **发布时间/热度**: 6个月前, 得票: 43

## 帖子正文

1.安装termux github仓库地址为

[https://github.com/termux/termux-app](https://github.com/termux/termux-app)

安装后进入termux,页面应该长这样

![图片](images/img_c74daac92e.jpeg)

2.在termux里安装linux子系统,我这里安装的是只有cli的ubuntu,也可以安装其他的系统

复制以下命令进行安装

```
 pkg update -y && pkg install wget curl proot tar -y && wget https://raw.githubusercontent.com/AndronixApp/AndronixOrigin/master/Installer/Ubuntu22/ubuntu22.sh -O ubuntu22.sh && chmod +x ubuntu22.sh && bash ubuntu22.sh
```

3.进入ubuntu子系统

执行命令

```
 ./start-ubuntu22.sh
```

进入之后前面的提示符应该会变化

![图片](images/img_8eb60144dc.jpeg)

4.安装npm和geminicli以及cnhkmcp(或者其他cli工具,如ifow cli, qwen-code都行)

现在安装的这个是一个极简的系统,很多常见工具都没有如pip,vim,curl,可以先安装一下

```
 #安装npm apt update apt install -y nodejs npm #安装 geminicli npm install -g @google/gemini-cli #安装cnhkmcp pip3 install cnhkmcp
```

5.进入gemini cli并连接mcp

终端输入gemini即可进入gemini cli

然后要用谷歌账号登录,登录完之后连接mcp,告诉ai mcp的json设置,就能自动帮你配好了 command和args里面的路径要根据系统内的真实路径调整一下,以下只是示例

```
 #mcp json配置 {   "mcpServers": {     "worldquant-brain-platform": {       "command": "D:\\anaconda\\python.exe",       "args": [         "D:\\anaconda\\Lib\\site-packages\\cnhkmcp\\untracked\\platform_functions.py"       ]     }   } }
```

都弄好之后,应该会显示Using: 1 mcp server

![图片](images/img_1ce7d851a7.jpeg)

看到这个界面就大功告成了,使用方法和电脑上几乎没有差别,只是读论坛时不能创建浏览器,目前还没有好的解决方法,可以挂在手机后台自动挖掘alpha, 基本上不用管,偶尔看一下ai有没有陷入神志不清的状态就行了

---

## 讨论与评论 (12)

### 评论 #1 (作者: YH25030, 时间: 6个月前)

厉害了，大佬！以前用安卓手机跑回测，现在可以用安卓手机训练AI了。谢谢分享。

---

### 评论 #2 (作者: PZ64174, 时间: 6个月前)

国区大佬就是多，大多是深藏不露！手机上安装mcp都研究出来了，我现在都是用远程软件看电脑，操作起来有些许的不方便，但是现在有手机上安装教程了，学习一下学习一下！

====================================================================

一年一个台阶，一步一个脚印

====================================================================

---

### 评论 #3 (作者: MZ45384, 时间: 6个月前)

大佬，我失败好几次了，安装gemini-cli的时候老是报错：

gyp ERR! configure error
gyp ERR! stack Error: `gyp` failed with exit code: 1
gyp ERR! stack at ChildProcess.<anonymous> (/data/data/com.termux/files/usr/lib/node_modules/node-gyp/lib/configure.js:317:18)
gyp ERR! stack at ChildProcess.emit (node:events:508:28)
gyp ERR! stack at ChildProcess._handle.onexit (node:internal/child_process:294:12)
gyp ERR! System Linux 4.19.152-perf+
gyp ERR! command "/data/data/com.termux/files/usr/bin/node" "/data/data/com.termux/files/usr/lib/node_modules/node-gyp/bin/node-gyp.js" "rebuild"
gyp ERR! cwd /data/data/com.termux/files/usr/lib/node_modules/@google/gemini-cli/node_modules/tree-sitter-bash
gyp ERR! node -v v24.9.0
gyp ERR! node-gyp -v v12.1.0
gyp ERR! not ok
npm error code 1
npm error path /data/data/com.termux/files/usr/lib/node_modules/@google/gemini-cli/node_modules/tree-sitter-bash
npm error command failed
npm error command sh -c node-gyp-build
npm error A complete log of this run can be found in: /data/data/com.termux/files/home/.npm/_logs/2025-12-11T04_06_00_018Z-debug-0.log

能帮我看一下是什么原因吗，deepseek也问了好几次了，还是没能解决

---

### 评论 #4 (作者: MZ45384, 时间: 6个月前)

感谢大佬，我成功build gemini cli了，安装nodejs的时候需要扩充一下仓库，还有其他麻烦的过程。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值
======================================================================================

---

### 评论 #5 (作者: LD27384, 时间: 6个月前)

@MZ45384

​看报错你应该是直接在 Termux 的原生环境里安装 Gemini 的吧？Termux 虽然轻量，但它毕竟不是标准的完整 Linux 发行版，它的底层库（主要是 libc）和文件系统路径与常规 Linux 有很大区别。这会导致很多依赖 C++ 编译的 Node.js 模块（特别是涉及 node-gyp 的）在构建时找不到对应的头文件或工具链，从而频频报错。

​强烈建议你按照帖子在 Termux 里装一个 Linux 子系统。子系统提供了一个完整的、标准化的 Linux 开发环境，GCC、Make 等编译工具链非常完善，不仅能完美解决这种编译依赖缺失的问题，后续安装其他复杂的包也会舒服很多，能省去大量排查环境问题的时间。

---

### 评论 #6 (作者: LG87838, 时间: 6个月前)

happy + claude code, 然后claude里面配置好自己的api，比如iflow等免费的api，也是一种方法。

------------------------------------------------------------------------------------------------------------------

慢就是快，相信时间的力量。

-------------------------------------------------------------------------------------------------------------------

---

### 评论 #7 (作者: PX70901, 时间: 6个月前)

直接用termux有什么区别?相对于Ubuntu

---

### 评论 #8 (作者: PX70901, 时间: 6个月前)

保安在做，只能碰手机。用termux跑machine_lib熄屏后会卡主不跑，亮屏后会快，而且pip各种报错cmake err...很多库都不完整。试下Ubuntu看看会不会好一点。

---

### 评论 #9 (作者: ML28213, 时间: 6个月前)

这是真大佬，termux 里装一个 Linux 子系统真是一个很好的想法。。在很多不方便使用电脑的环境中也可以很从容的和 CLI 进行研究。长见识了

---

### 评论 #10 (作者: DS48533, 时间: 6个月前)

可能是系统问题？我手机体验起来，每次回复都需要手动往下拉上下文，才能看到最新的内容，很不方便，回车也没有，要有输入法的回车

---

### 评论 #11 (作者: PX70901, 时间: 4个月前)

我成功了，在手机上用app

---

### 评论 #12 (作者: JL33484, 时间: 24天前)

gemini 一致授权不成功是什么鬼

---

