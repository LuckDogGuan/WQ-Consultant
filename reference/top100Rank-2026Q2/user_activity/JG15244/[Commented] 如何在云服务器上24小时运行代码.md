# 如何在云服务器上24小时运行代码

- **链接**: [Commented] 如何在云服务器上24小时运行代码.md
- **作者**: JT84734
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

在成为顾问之后我们可以进行大量的回测，最好是24小时不停的回测，这个时候代码还放在本地运行就不是那么方便了。所以接下来我会介绍如何将代码移动到云服务器上运行。

## 1. 购买服务器

如何购买服务器这个这论坛上已经有介绍了，可以直接跳转：
 [💻如何使用天翼云主机进行云端程序挂载](/hc/en-us/community/posts/25891396254231--%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8%E5%A4%A9%E7%BF%BC%E4%BA%91%E4%B8%BB%E6%9C%BA%E8%BF%9B%E8%A1%8C%E4%BA%91%E7%AB%AF%E7%A8%8B%E5%BA%8F%E6%8C%82%E8%BD%BD) 
 [💻如何免费领取阿里无影云电脑使用](../SD17531/[Commented] 如何免费领取阿里无影云电脑使用.md) 
 [💻如何设置云电脑之京东云？](/hc/en-us/community/posts/25880682394263--%E5%A6%82%E4%BD%95%E8%AE%BE%E7%BD%AE%E4%BA%91%E7%94%B5%E8%84%91%E4%B9%8B%E4%BA%AC%E4%B8%9C%E4%BA%91)

我之前分享过一篇免费领取华为服务器的文章，不过近期有同学反应不能领取了，我没有去验证，感兴趣的小伙伴可以再去尝试一下 [华为云沃土云创计划——领取401元代金券（可免费购买Flexus服务器）](/hc/en-us/community/posts/28322890747799-%E5%8D%8E%E4%B8%BA%E4%BA%91%E6%B2%83%E5%9C%9F%E4%BA%91%E5%88%9B%E8%AE%A1%E5%88%92-%E9%A2%86%E5%8F%96401%E5%85%83%E4%BB%A3%E9%87%91%E5%88%B8-%E5%8F%AF%E5%85%8D%E8%B4%B9%E8%B4%AD%E4%B9%B0Flexus%E6%9C%8D%E5%8A%A1%E5%99%A8)

在购买服务器之后，需要使用ssh远程连接上服务器，使用命令行进行操作。简单软件可以直接使用Windows的powershell，专业一些的软件收费的有xshell，免费的可以使用windTerm。连接上服务器后的操作的需要使用命令行进行，如果对命令行不熟悉的同学可以借助kimi，豆包，deepseek等大语言模型的帮助，发送自己的需求，让AI把命令写出来。

## 2. 安装python环境

我这里使用的是debian系统，首先安装 `pyenv，` 这是一个python版本管理工具，可以方便的管理和切换多个python环境。如果存在网络问题可以先换源：

```
sudo sed -i 's|http://deb.debian.org|http://mirrors.aliyun.com|g' /etc/apt/sources.list
sudo apt update

```

1. **安装依赖** ： `pyenv` 需要一些依赖来正常工作，包括 `git` 、 `make` 、 `build-essential` 和 `libssl-dev` 。在Debian系统中，你可以使用以下命令安装这些依赖：

```
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
   libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git   

```

1. **安装 `pyenv`** ：通过 `git` 克隆 `pyenv` 的仓库到你的根目录：
   ```
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv
   ```
2. **配置环境变量** ：将 `pyenv` 的初始化脚本添加到你的shell配置文件（如 `.bashrc` 或 `.zshrc` ）中：
   ```
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
   ```
3. 重新加载配置文件：

```
source ~/.bashrc

```

1. **安装指定版本的Python** ：使用 `pyenv` 安装Python 3.12(这个过程需要几分钟)：
   ```
   pyenv install 3.12.0
   ```

请注意，你需要指定具体的版本号，因为 `3.12` 不是一个有效的版本号，需要具体的版本号，如 `3.12.0` 。
2.  **设置全局Python版本** ：如果你想将Python 3.12设置为全局默认版本，可以使用以下命令：

```
 pyenv global 3.12.0

```

#### pyenv常用命令：

1. 查看可用的Python版本：

```
pyenv install --list

```

1. 安装特定版本的Python：

```
pyenv install 版本号

```

1. 查看当前激活的Python版本：

```
pyenv version

```

1. 列出已安装的Python版本：

```
pyenv versions

```

1. 切换Python版本：

```
pyenv local 版本号 

```

1. 卸载Python版本：

```
 pyenv uninstall 版本号

```

## 安装zellij

安装好服务器后，我们可以使用vscode 上的remote-ssh插件进行开发和调试代码。
 ![图片](images/img_f696978734.png) 
这个时候你可能会发现当运行代码后，关闭vscode后服务器那边的代码还是会终止，为了避免这种情况，让程序一直的运行下去我们需要一个终端复用器。这里我推荐使用zellij，这个相对于tumx，用起来会简单易用很多。

这里先安装x-cmd,然后使用x-cmd安装zellij

```
eval "$(curl https://get.x-cmd.com)"        # 安装 x-cmd
x env use zellij                            # 使用 x-cmd 安装 zellij

```

接下来输入 `zellij --version`  来查看是否安装成功

![图片](images/img_db216197b5.png)

zellij的常用命令：

```
zellij -s <session name>            # 创建新的会话
zellij ls                           # 列出活动的会话
zellij a <session name>             # 连接到指定会话
zellij k <session name>             # 杀死指定会话
zellij d <session name>             # 删除指定会话
zellij ka                           # 杀死所有会话

```

zellij 常用快捷键

```
- `Ctrl-g`：锁定或界面，主要用于缓解快捷键冲突的情况。
- `Ctrl-p` + `n`：分割生成新窗口
- `Ctrl-p` + `x`：关闭当前聚焦的窗口
- `Ctrl-p` + `←`：切换到左侧的窗口
- `Ctrl-t` + `n`：创建新的标签页
- `Ctrl-t` + `x`：关闭当前聚焦的标签页
- `Ctrl-t` + `←`：切换到左侧的标签页 

```

使用方法非常简单，例如使用  `zellij -s worldquant`  创建一个一个名字为worldquant的会话。创建成功之后会自动进入会话。

![图片](images/img_2be9bc7d90.png)

快捷键直接显示在最下面，在这里可以进入对应的文件夹，直接运行已经编写好的代码，然后使用快捷键 `ctrl +o`  +  `d`  即可退出当前会话，再命令行使用  `zellij a worldquant`  就可以恢复会话，也可以看见程序的运行情况。

![图片](images/img_a82a4db398.png)

完成上面的工作之后，就能让代码在云服务器上一直运行了。这里没有涉及到代码，我现在使用的还是上课提供的代码，这里是代码放在云服务器上24小时运行。看到论坛有同学分享修改代码加入微信通知的，后面修改代码加入这个功能，就可以做到代码运行后就不需要管，等微信收到通知后再来处理。

---

## 讨论与评论 (2)

### 评论 #1 (作者: GL61467, 时间: 1年前)

又多了一个工具 zellij， 谢谢分享

---

### 评论 #2 (作者: JG15244, 时间: 1年前)

你好，我在使用zellij的时候，有些快捷键跟vscode快捷键冲突了，请问你是怎么解决的。

---

