# 向BRAIN Labs里粘贴代码的一个方法代码优化

- **链接**: [Commented] 向BRAIN Labs里粘贴代码的一个方法代码优化.md
- **作者**: QQ68782
- **发布时间/热度**: 1年前, 得票: 75

## 帖子正文

brain labs逐步开放了, 但是没法复制粘贴代码进去, 网络也不通, 只能手动敲字进去

这里提供一种方法, 能快速『敲』字进去

核心思路是用模拟键盘按键, 发送文本, 借助python的keyboard包实现

**注意: 模拟按键有风险, 谨慎尝试**

**## 使用示例**

1.在本机安装keyboard包: 
pip install keyboard

2.保存代码到py文件, 比如: send_key.py
其中的text是要复制的内容
```
import keyboard
import time

print('start')
# 等待2秒, 把鼠标光标切换到labs的输入框
time.sleep(2)

# 要输入的文本
text = '''
The quick brown fox jumps over the lazy dog
The quick brown fox jumps over the lazy dog
The quick brown fox jumps over the lazy dog
'''.strip()

# 每个字符之间的时间间隔, 单位秒
delay = 0.01

keyboard.write(text=text,delay= delay, exact= False)

```

3.执行脚本
python sned_key.py

4.把鼠标光标定位到labs里, 把浏览器里的输入法改为英文, 等待自动输入完成

**## 效果**

![图片](images/img_7d929e48ad.png)

**## 改进思路**

可以指定一个快捷键, 执行快捷键后调用python脚本, 脚本读取剪贴板、发送文字, 实现更丝滑的复制粘贴体验

---

## 讨论与评论 (13)

### 评论 #1 (作者: WL13229, 时间: 1年前)

需要把浏览器变成英文语言，不然有下划线的输入可能会输入错误

---

### 评论 #2 (作者: YQ51506, 时间: 1年前)

很好的分享，给大佬点赞，使用自动化包去模拟手动输入

---

### 评论 #3 (作者: QQ68782, 时间: 1年前)

[WL13229](/hc/en-us/profiles/12285040305687-WL13229)  是的, 已经更新到正文了

---------------------------------------------------------------------------------------------------
知识就是力量 Knowledge is power.

---

### 评论 #4 (作者: YX23928, 时间: 1年前)

感谢QQ哥分享的黑科技

===================================================================================

---

### 评论 #5 (作者: ZY77039, 时间: 1年前)

下面的代码可以实现ctrl+shift+a的快捷输入（快捷键可以自己改），且可以多次输入，有需要可以自取：

```
import keyboardimport time# 定义要输入的文本text_to_input = '''blablabla'''.strip()# 定义每个字符之间的时间间隔，单位秒delay_between_keys = 0.01def input_text():    print('开始输入文本...')    # 等待2秒, 把鼠标光标切换到labs的输入框    time.sleep(2)    # 使用keyboard库输入文本    keyboard.write(text=text_to_input, delay=delay_between_keys, exact=False)    print('文本输入完成')# 设置快捷键为Ctrl+Shift+Akeyboard.add_hotkey('ctrl+shift+a', input_text)# 保持程序运行，监听快捷键print('等待快捷键Ctrl+Shift+A组合键...')keyboard.wait()
```

---

### 评论 #6 (作者: FL39657, 时间: 1年前)

很有用的工具，对在lab里研究数据提供了很大的便利

---

### 评论 #7 (作者: JL16510, 时间: 1年前)

感谢分享，没想到还有这样的操作，还没试过，先mark回头去搞起来。

-------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #8 (作者: QQ68782, 时间: 1年前)

[ZY77039](/hc/en-us/profiles/22255214618775-ZY77039)

感谢你的分享, 有了快捷键方便了很多, 可用性大大增强

---------------------------------------------------------------------------------------------------
知识就是力量 Knowledge is power.

---

### 评论 #9 (作者: XC66172, 时间: 1年前)

谢谢分享，最近也开始在学习BRAIN LABS, 这个很实用~~

========================================================

FIGHTING LABUBU! ~  每天醒来就搓搓因子，总有一个是好的

========================================================

---

### 评论 #10 (作者: WF37935, 时间: 1年前)

我的需求是把剪切板东西复制到lab，参考 [ZY77039](/hc/zh-cn/profiles/22255214618775-ZY77039)  写了个方法，方便把字段名什么的复制进去。

```
def paste_from_clipboard():    print('正在读取剪贴板内容...')        # 1. 先读取剪贴板内容（尽早获取，避免后续操作污染剪贴板）    try:        clipboard_text = pyperclip.paste()        print(f"剪贴板内容: {clipboard_text[:50]}...")  # 只打印前50字符避免过长    except Exception as e:        print(f"读取剪贴板失败: {e}")        return    # 2. 提示用户切换窗口    print('请2秒内切换到目标输入框...')    time.sleep(2)    # 3. 模拟键盘输入    try:        keyboard.write(text=clipboard_text, delay=delay_between_keys, exact=False)        print('输入完成！')    except Exception as e:        print(f"输入失败: {e}")
```

---

### 评论 #11 (作者: JX28185, 时间: 10个月前)

向大佬学习

---

### 评论 #12 (作者: HL64570, 时间: 5个月前)

很好用，谢谢大佬的分享，另外，发现可以输入中文字符。

---

### 评论 #13 (作者: LY67324, 时间: 3个月前)

大佬，太强了，很好用的工具

---

