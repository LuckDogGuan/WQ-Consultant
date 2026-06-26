# [Gemini大王]同时调取多个Gemini Cli完成不同工作经验分享

- **链接**: [Commented] [Gemini大王]同时调取多个Gemini Cli完成不同工作经验分享.md
- **作者**: HZ58133
- **发布时间/热度**: 5个月前, 得票: 7

## 帖子正文

在使用AI改进Alpha时，我每次都需要打开terminal，然后输入提示词开始任务，颇为繁琐。于是想到是否可以有更高效的办法，比如用代码同时唤起多个Gemini Cli大模型然后完成不同的任务。

经过学习发现有多种方法可以实现，比如可以多任务调度”Python 脚本(需要api)如果有需要我之后也可都介绍一下，我们现在主要介绍使用  **PowerShell 并行脚本(免费)。**

### **第一步:安装Gemini Cli**

Terminal中输入

```
npm install -g @google/gemini-cli
```

### **第二部:VS Code里安装Powershell**

点开VS code左侧的小方块(Extensions)，搜索PowerShell并下载，

![图片](images/img_f0c73387e2.png)

### **第三步:编写 ps1. 文档调用Gemini Cli执行任务**

```
$OutputEncoding = [System.Text.Encoding]::UTF8[Console]::OutputEncoding = [System.Text.Encoding]::UTF8chcp 65001 | Out-Null  # 强制切换当前终端代码页为 UTF-8$tasks = @(    @{ File = "C:\Users\dujid\Desktop\WORLDQUANT\Learn\Gemini\总结.txt"; Hint = "总结一下这段话" };    @{ File = "C:\Users\dujid\Desktop\WORLDQUANT\Learn\Gemini\math.txt"; Hint = "输出结果" };    @{ File = "C:\Users\dujid\Desktop\WORLDQUANT\Learn\Gemini\翻译.txt"; Hint = "翻译成中文" })Write-Host "--- 正在启动并行任务 ---" -ForegroundColor Yellowforeach ($task in $tasks) {    if (Test-Path $task.File) {        Start-Job -ScriptBlock {            param($f, $h)            # 在子任务中也要确保编码环境            [Console]::OutputEncoding = [System.Text.Encoding]::UTF8            Get-Content -Path $f -Raw | gemini $h        } -ArgumentList $task.File, $task.Hint        Write-Host "已启动任务: $($task.File | Split-Path -Leaf)" -ForegroundColor Green    } else {        Write-Warning "找不到文件: $($task.File)"    }    # 稍微停顿，防止 API 触发频率限制（Rate Limit）    Start-Sleep -Milliseconds 600}Write-Host "`n所有任务已在后台运行，正在回收结果...`n" -ForegroundColor Cyan# 2. 等待并回收结果Write-Host "`n所有任务已在后台运行，正在回收结果...`n" -ForegroundColor Cyan$allJobs = Get-Jobforeach ($job in $allJobs) {    Wait-Job $job | Out-Null       # 打印一个简单的分割线    Write-Host ">> 任务 [ID: $($job.Id)] 的处理结果:" -ForegroundColor Cyan -BackgroundColor DarkBlue       # 接收结果    Receive-Job -Job $job -ErrorAction SilentlyContinue       Write-Host "------------------------------------`n"}# 清理任务缓存Remove-Job *
```

### **使用说明:**

```
@{ File = "C:\xx\xx\xx\这里写你需要Gemini阅读的提示词.txt"; Hint = "这里写执行任务的命令" }
```

**现在先简单演示一下效果**

一共设置了三个不同任务

**![图片](images/img_81893796c8.png)**

输入文件路径和指令

![图片](images/img_8a1572dfbd.png)

成功运行，返回结果 ![图片](images/img_4c828a5aad.png)

## **现在进入实战环节:**

为了方便观察，我们使用Gemini Cli对三个不同地区(EUR, USA, IND)不合格Alpha进行改进。

**由于调用Gemini Cli进行回测时需要调用工具，因此我们要对代码做出相应修改。**

```
# 1. 环境编码设置$OutputEncoding = [System.Text.Encoding]::UTF8[Console]::OutputEncoding = [System.Text.Encoding]::UTF8chcp 65001 | Out-Null# 明确你的工作目录路径$workDir = "C:\Users\dujid\Desktop\WORLDQUANT\Learn\Gemini"$tasks = @(    @{ File = "$workDir\ImproveEUR.md"; Hint = "获取ID为`xxx`的Alpha的数据,在其原有表达式的基础上对其进行改进提升。阅读ImproveEUR.md" };    @{ File = "$workDir\ImproveUSA.md"; Hint = "获取ID为`xxx`的Alpha的数据,在其原有表达式的基础上对其进行改进提升。阅读ImproveUSA.md" };    @{ File = "$workDir\ImproveIND.md"; Hint = "获取ID为`xxx`的Alpha的数据,在其原有表达式的基础上对其进行改进提升。阅读ImproveIND.md" })Write-Host "--- 正在启动并行任务 (全授权模式) ---" -ForegroundColor Yellowforeach ($task in $tasks) {    if (Test-Path $task.File) {        Start-Job -ScriptBlock {            param($f, $h, $d)            # A. 必须在子任务内部切换到文件所在目录，否则 Gemini 找不到 .md 文档            cd $d            [Console]::OutputEncoding = [System.Text.Encoding]::UTF8                       # B. 使用 --yolo 标志直接授权所有工具调用（回测、平台连接等）            Get-Content -Path $f -Raw | gemini $h --yolo        } -ArgumentList $task.File, $task.Hint, $workDir        Write-Host "已启动任务: $($task.File | Split-Path -Leaf)" -ForegroundColor Green    } else {        Write-Warning "找不到文件: $($task.File)"    }    Start-Sleep -Milliseconds 800 # 稍微延长停顿，给工具初始化留时间}Write-Host "`n任务已全部提交，正在回收结果 (由于涉及 BRAIN 回测，可能需要较长时间)...`n" -ForegroundColor Cyan# 2. 等待并回收结果$allJobs = Get-Jobforeach ($job in $allJobs) {    Wait-Job $job | Out-Null    Write-Host ">> 任务 [ID: $($job.Id)] 处理结果:" -ForegroundColor Cyan -BackgroundColor DarkBlue       # 使用 -ErrorAction SilentlyContinue 过滤登录等杂音    Receive-Job -Job $job -ErrorAction SilentlyContinue       Write-Host "------------------------------------`n"}# 清理任务Remove-Job *
```

任务成功启动

![图片](images/img_8708524582.png)

查看Alpha界面，成果回测并取得了结果，以下是EUR地区的示例

改进前: ![图片](images/img_4b44d2a4db.png)

成功改进:

![图片](images/img_fc1db2ddb9.png)

三个任务也都在同时进行: ![图片](images/img_1888bcd03b.png)

---

## 讨论与评论 (3)

### 评论 #1 (作者: JX39934, 时间: 5个月前)

感谢大佬的分享，这招并发任务直接解决了AI回测效率的问题，顺便想问下，gemini cli的并发数量最大是3个吗，还有就是开了3个对电脑硬件性能的占比如何呢，望大佬解答一下

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #2 (作者: HZ58133, 时间: 5个月前)

您好，Gemini cli并发数量理论上来讲是可以无限多的，开五个十个都可以。单个cli大概占200-500MB的内存，电脑内存16GB+的话完全可以胜任5个cli同时开。

---

### 评论 #3 (作者: MZ45384, 时间: 5个月前)

看起来比直接多开更便捷，但是要是遇到socket hung up, keep try或者potential loop detected怎么处理。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

