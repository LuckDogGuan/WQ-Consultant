# 有趣的项目分享：网页版Gemini转API调用（Gemini-API）代码优化

- **链接**: [Commented] 有趣的项目分享网页版Gemini转API调用Gemini-API代码优化.md
- **作者**: ZL35633
- **发布时间/热度**: 6个月前, 得票: 60

## 帖子正文

Gemini-API（项目地址： [https://github.com/HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) ）是一款基于 Google Gemini 网页应用逆向工程开发的异步 Python 库，它绕开了官方 API 的限制，以简洁的接口实现了与 Gemini 模型的全功能交互，支持多轮对话、图像生成、模型自定义等特性，且全程基于 asyncio 实现异步操作，性能更高效。

## 核心示例：交互式命令行对话程序

以下是基于 Gemini-API 实现的完整交互式对话示例，可直接运行实现与 Gemini 的长对话交互：

```
#!/usr/bin/env python3
"""
Gemini 交互式命令行对话程序
使用 gemini-webapi 库与 Google Gemini 进行长对话
"""

import asyncio
import sys
from gemini_webapi import GeminiClient, set_log_level

class GeminiChat:
    """Gemini 交互式聊天类"""

    def __init__(self, verbose: bool = False):
        """
        初始化 Gemini 客户端

        Args:
            verbose: 是否显示详细日志
        """
        # 设置日志级别
        set_log_level("DEBUG" if verbose else "INFO")
        self.client = GeminiClient()  # 初始化Gemini客户端
        self.chat = None  # 对话会话对象
        self.conversation_count = 0  # 对话轮次计数
        self.model = "gemini-3.0-pro"  # 指定使用的Gemini模型

    async def initialize(self):
        """初始化客户端并启动聊天"""
        try:
            print("正在初始化 Gemini 客户端...")
            await self.client.init()  # 客户端初始化（自动获取浏览器Cookie认证）
            self.chat = self.client.start_chat(model=self.model)  # 启动对话会话
            print(f"✓ Gemini 客户端初始化成功！使用模型: {self.model}")
            print("=" * 60)
            return True
        except Exception as e:
            print(f"✗ 初始化失败: {e}\n")
            print("提示：请确保已安装 browser-cookie3 并在浏览器登录Google账号")
            print("安装命令: pip install browser-cookie3")
            print("需先访问：https://gemini.google.com/")
            return False

    async def send_message(self, message: str) -> str:
        """发送消息并获取回复"""
        if not self.chat:
            return "错误：聊天未初始化"
        try:
            self.conversation_count += 1
            print(f"\n[轮次 {self.conversation_count}] 正在思考...")
            response = await self.chat.send_message(message)  # 发送消息
            return response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            return f"错误：{e}"

    def print_reply(self, reply: str):
        """格式化打印回复"""
        print("\n" + "=" * 60)
        print("Gemini 回复：")
        print("-" * 60)
        print(reply)
        print("=" * 60)

    async def run_interactive(self):
        """运行交互式对话循环"""
        if not await self.initialize():
            return

        print("\n欢迎使用 Gemini 交互式对话！")
        print("输入 'quit/exit/q' 退出 | 'clear/reset' 重置对话 | 'model' 查看模型 | 'help' 帮助")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n你: ").strip()
                if not user_input:
                    continue
                # 处理核心指令
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n再见！")
                    break
                elif user_input.lower() in ['clear', 'reset']:
                    self.chat = self.client.start_chat(model=self.model)
                    self.conversation_count = 0
                    print("✓ 对话已重置")
                elif user_input.lower() == 'model':
                    print(f"当前模型: {self.model}")
                elif user_input.lower() == 'help':
                    print("可用命令：quit/exit/q(退出)、clear/reset(重置对话)、model(查看模型)、help(帮助)")
                else:
                    reply = await self.send_message(user_input)
                    self.print_reply(reply)
            except (KeyboardInterrupt, EOFError):
                print("\n\n程序退出...")
                break
            except Exception as e:
                print(f"\n✗ 发生错误: {e}")

async def main():
    """主函数"""
    chat = GeminiChat(verbose=False)
    await chat.run_interactive()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已退出")
        sys.exit(0)

```

## 关键功能代码片段

除了基础对话，Gemini-API 还支持以下核心功能，以下是简洁的代码示例：

### 1. 多轮对话会话恢复

```
import asyncio
from gemini_webapi import GeminiClient

async def restore_chat():
    client = GeminiClient()
    await client.init()
    # 启动第一个对话并发送消息
    chat1 = client.start_chat(model="gemini-3.0-pro")
    await chat1.send_message("记住：我喜欢编程")
    # 保存对话元数据
    session_meta = chat1.metadata
    # 恢复之前的对话
    chat2 = client.start_chat(metadata=session_meta, model="gemini-3.0-pro")
    response = await chat2.send_message("我喜欢什么？")
    print(response.text)  # 会回复“你喜欢编程”

asyncio.run(restore_chat())

```

### 2. 图像生成与保存

```
import asyncio
from gemini_webapi import GeminiClient

async def generate_image():
    client = GeminiClient()
    await client.init()
    # 生成图像
    response = await client.generate_content("生成一张可爱的猫咪图片")
    # 保存图片到本地
    for i, img in enumerate(response.images):
        await img.save(path="./", filename=f"cat_{i}.png")

asyncio.run(generate_image())

```

### 3. 自定义模型与 Gem 提示

```
import asyncio
from gemini_webapi import GeminiClient

async def custom_model_and_gem():
    client = GeminiClient()
    await client.init()
    # 创建自定义Gem（系统提示）
    python_tutor = await client.create_gem(
        name="Python导师",
        prompt="你是专业的Python编程导师，回答简洁易懂",
        description="Python编程助手"
    )
    # 使用自定义Gem和模型提问
    response = await client.generate_content(
        "解释列表推导式",
        model="gemini-2.5-flash",
        gem=python_tutor
    )
    print(response.text)

asyncio.run(custom_model_and_gem())

```

### 总结

1. **Gemini-API** 是一款异步 Python 库，通过逆向工程实现了 Google Gemini 的全功能交互，无需官方 API 密钥。
2. 核心优势包括支持多轮对话、图像生成、自定义模型 / 系统提示，且接口简洁易用。
3. 上述代码可直接运行，仅需提前安装 `browser-cookie3` 并在浏览器登录 Google 账号即可完成认证。

---

## 讨论与评论 (8)

### 评论 #1 (作者: NL80893, 时间: 6个月前)

啊啊啊啊，太好了，感恩作者，这就去试！

====================================================================================
祝大佬base多多，vf高高，分享更多小妙招～～
====================================================================================

---

### 评论 #2 (作者: JX14975, 时间: 6个月前)

楼主，有几个问题想问，可否解答：
1，这个库绕开api意味着难以被限流吗？这是api运用中的常见痛点

2，脚本的运用是否有联用mcp的方法？感觉很多人对ai的运用还是主要借助了mcp。

---

### 评论 #3 (作者: YQ84572, 时间: 6个月前)

很有趣的办法，网页版的还能转api来使用，可以试试看能否直接用在ide上
====================================================================================
祝大佬base多多，vf0.9+
====================================================================================

---

### 评论 #4 (作者: ZL35633, 时间: 6个月前)

@ [JX14975](/hc/en-us/profiles/29548387470487-JX14975)

这个项目是使用浏览器中的cookie模拟web的api访问gemini的，理论上与网页版的功能是一致的，只不过比起web端使用会更自由一点。

虽然mcp不能用，但是wq的api是能用的。

另外，我再给个思路，可以找弱一点的AI通过api来控制mcp，困难的问题交给gemini网页版。

---

### 评论 #5 (作者: MY49971, 时间: 6个月前)

感谢大佬分享，会有token限制吗？

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #6 (作者: CL86067, 时间: 6个月前)

太强了，这和Gemini cli 转api那个项目有得一拼呀，如果真的能结合mcp手搓就无敌了，感谢大佬的分享，顺便蹲一下大家的使用反馈

====================================================================================

行动是一切问题的答案，加油

---

### 评论 #7 (作者: XZ35933, 时间: 6个月前)

太好了，正好手上有白嫖的gemini，正好拿来试试。感谢！

---

### 评论 #8 (作者: JL40454, 时间: 6个月前)

好思路, 收藏了

---

