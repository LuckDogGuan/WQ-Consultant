# 【Community Leader -因子构造】mcp我想运行多久, 就运行多久经验分享

- **链接**: [Commented] 【Community Leader -因子构造】mcp我想运行多久 就运行多久经验分享.md
- **作者**: QQ68782
- **发布时间/热度**: 6个月前, 得票: 66

## 帖子正文

目前大家在使用各种编程cli调用mcp, mcp执行一段时间后就会暂停, 只能手动在cli界面输入"继续"后让AI继续执行;

能否用编程的方式输入"继续", 而不用自己手动输入呢?

这正是SDK的作用, 用编程的方式和cli通信; 目前claude code、qwen code、iflow等cli都支持SDK

下面演示iflow sdk的用法

**## demo** 
首先安装 iFlow CLI: 0.2.24 或更高版本

安装 iflow-cli-sdk
```
pip install iflow-cli-sdk
```

**### 最简单例子** 
```python
import asyncio
from iflow_sdk import IFlowClient, AssistantMessage, TaskFinishMessage

async def main():
    # SDK 自动处理：
    # 1. 检测 iFlow 是否已安装
    # 2. 启动 iFlow 进程（如果未运行）
    # 3. 查找可用端口并建立连接
    # 4. 退出时自动清理资源
    async with IFlowClient() as client:
        await client.send_message("你好，iFlow！")

        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                print(message.chunk.text, end="\n", flush=True)
            elif isinstance(message, TaskFinishMessage):
                break

asyncio.run(main())
```

**### 持续运行的例子** 
下面的例子, 任务结束时自动"继续", 一共执行3次
```python
import asyncio
from iflow_sdk import IFlowClient, AssistantMessage, TaskFinishMessage

async def dotask():
    async with IFlowClient() as client:
        prompt = '''当我说你好或继续时, 你回复"靓仔好+n", 其中的n是回复次数, 如果明白回复"收到"
        '''
        await client.send_message(prompt) 
        loop_limit = 3
        loop_index = 0
        while loop_index <= loop_limit:
            print(f'loop_index: {loop_index}')
            loop_index+=1
            async for message in client.receive_messages():
                if isinstance(message, AssistantMessage):
                    print(f'ai: {message.chunk.text}', end="", flush=True)
                elif isinstance(message, TaskFinishMessage):
                    print()  # 换行
                    user_input = "继续"
                    print(f"user: {user_input}", end="\n", flush=True)
                    await client.send_message(user_input) 
                    break
                else: 
                    print(f'message: {message}', end="", flush=True)
        print("done")
if __name__ == "__main__":
    asyncio.run(dotask())
```

输出示例: 
```
loop_index: 0
ai: 收到
user: 继续
loop_index: 1
ai: 靓仔好+1
user: 继续
loop_index: 2
ai: 靓仔好+2
user: 继续
loop_index: 3
ai: 靓仔好+3
user: 继续
done
```

**### 资料** 
更多用法、常见问题参考官方文档
 [https://platform.iflow.cn/cli/sdk/sdk-python](https://platform.iflow.cn/cli/sdk/sdk-python)

---

## 讨论与评论 (5)

### 评论 #1 (作者: YL27037, 时间: 6个月前)

```
我这运行十几分钟会报错,不知道是不是sdk没跟上iflow的更新DEBUG:websockets.client:< TEXT '{"jsonrpc":"2.0","method":"session/update","par...lization":false}}]}}}\n' [46420 bytes]DEBUG:iflow_sdk._internal.transport:Received message: {"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"a7d99eed-1d62-4c9c-8e93-9d2ae5408b99","update":{"sessionUpdate":"tool_call_update","toolCallId":"call_00_czaaOCU7jp90tz4iyCQdy16W","to...DEBUG:websockets.client:< TEXT '{"jsonrpc":"2.0","id":4,"error":{"code":-32603,...3db49b38265fba-01"}}}\n' [650 bytes]DEBUG:iflow_sdk._internal.transport:Received message: {"jsonrpc":"2.0","id":4,"error":{"code":-32603,"message":"Internal error","data":{"details":"生成数据错误: HTTP 错误！状态：400，响应：{\"error\":{\"message\":\"Bad request!: {\\\"error\\\":{\\\"message\\\":\\\"This ...DEBUG:iflow_sdk._internal.protocol:Received response for unknown request ID: 4
```

---

### 评论 #2 (作者: JW12369, 时间: 6个月前)

这个好啊， 让他优化不要停，然后自己用代码检查

---

### 评论 #3 (作者: HY20507, 时间: 5个月前)

大佬们真是太强了，针对不同的痛点甚至是小小的不便都有解决和优化方案🎉

---

### 评论 #4 (作者: MZ45384, 时间: 5个月前)

大佬，Gemini-cli行吗

---

### 评论 #5 (作者: HW93328, 时间: 5个月前)

============================HW93328============================

太强了，解决了一个困扰已久的问题，感谢大佬～～

============================HW93328============================

---

