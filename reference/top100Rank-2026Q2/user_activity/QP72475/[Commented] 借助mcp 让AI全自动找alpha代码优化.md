# 借助mcp, 让AI全自动找alpha代码优化

- **链接**: [Commented] 借助mcp 让AI全自动找alpha代码优化.md
- **作者**: QQ68782
- **发布时间/热度**: 1年前, 得票: 69

## 帖子正文

大家平时可能会让AI解释字段、写alpha表达式, 然后手动回测、调试, 这个过程能不能让AI自动完成呢?

借助mcp可以大大简化这个过程的实现

下面演示一个demo, 展示这个过程

**## demo示例**

安装 fastmcp

```

pip install fastmcp

```

mcp server代码:

```

from fastmcp import FastMCP

# from test_mongo_lib import *

import ai.tools as ai_tools

from pydantic import BaseModel, Field

from typing import Optional, Literal

class AlphaSettings(BaseModel):

instrumentType: Literal["EQUITY"] = Field(description="交易品种类型")

region: Literal["USA"] = Field(description="交易区域")

universe: Literal["TOP3000", "TOP1000", "TOP500", "TOP200", "ILLIQUID_MINVOL1M", "TOPSP500"] = Field(description="交易标的范围")

delay: Literal[1] = Field(description="延迟")

decay: int = Field(description="衰减天数", ge=0)

neutralization: Literal["STATISTICAL", "CROWDING", "FAST", "SLOW", "MARKET", "SECTOR", "INDUSTRY", "SUBINDUSTRY", "SLOW_AND_FAST"] = Field(description="中性化方式")

truncation: float = Field(description="截断比例", ge=0, le=1)

pasteurization: Literal["ON", "OFF"] = Field(description="是否进行数据清洗")

unitHandling: Literal["VERIFY"] = Field(description="单位处理方式")

nanHandling: Literal["ON", "OFF"] = Field(description="空值处理方式")

language: Literal["FASTEXPR"] = Field(description="表达式语言")

visualization: bool = Field(description="是否可视化")

class AlphaConfig(BaseModel):

type: Literal["REGULAR"] = Field(description="Alpha类型")

settings: AlphaSettings = Field(description="Alpha配置参数")

regular: str = Field(description="Alpha表达式")

mcp = FastMCP("Demo 🚀")

@mcp.tool()

def add(a: int, b: int) -> int:

"""Add two numbers"""

return a + b

@mcp.tool()

def simulate(alpha_config: AlphaConfig) -> str:

"""回测alpha

Args:

alpha_config (AlphaConfig): 回测配置

Returns:

str:  返回查询回测进度的 simulation_progress_url

"""

data = alpha_config.model_dump()

print(data)

result = ai_tools.simulate(data)

return result

# tasks = [data]

# process_simulation4(0, tasks)

# return f"sim_id: {alpha_id}"

@mcp.tool()

def get_simulate_result(simulation_progress_url:str):

"""查询回测进度/结果

预计等待2-5分钟, 建议每过一分钟轮询一次

Args:

simulation_progress_url (str): 查询url

Returns:

json: 进度或回测完成的结果, 返回结果包含"alpha"字段表示回测完成, "alpha"字段表示alpha_id

"""

result = ai_tools.get_simulate_result(simulation_progress_url)

return result

@mcp.tool()

def get_alpha_detail(alpha_id:str):

"""查询alpha详情, 包括详细指标信息, 如longCount、shortCount、turnover、returns、drawdown、margin、sharpe、fitness等

Args:

alpha_id (str): id

"""

result = ai_tools.get_alpha_detail(alpha_id)

return result

@mcp.resource(

uri="resource://tool_use_flow",

)

def tool_use_flow() -> str:

"""工具的使用流程说明"""

return """

第一步: 调用simulate工具提交回测, 得到simulation_progress_url用于查询回测进度/结果

第二步: 调用get_simulate_result获取回测进度/结果

第三步: 调用get_alpha_detail获取alpha详细指标信息

"""

if __name__ == "__main__":

# mcp.run()

mcp.run(

transport="sse",

host="0.0.0.0",  # Override default host

port=8000,         # Override default port

log_level="debug"  # Set logging level

)

```

启动服务:

```

fastmcp run mcp_server.py

```

配置到mcp客户端, 如trae、cursor

```

{

"mcpServers": {

"brain-tools": {

"url": "http://localhost:8000/sse"

},

}

```

**## 效果**

**![图片](images/img_ba00d1db7f.png)**

![图片](images/img_ce1bec8e9e.png)

**## 总结**

demo实现了最核心的流程, 但找出的alpha效果一般, token消耗量也很大, 还有许多需要继续优化的地方

---

## 讨论与评论 (11)

### 评论 #1 (作者: QP72475, 时间: 1年前)

进阶知识，离全自动化又进一步了。

---

### 评论 #2 (作者: QZ67721, 时间: 1年前)

大佬能不能搞出一个自动写PPA描述的脚本啊， 每天写这个东西要用AI，给他传文件，重新给他提示词，非常的麻烦。而且电脑配置不行，卡的一笔。
+++++++++++++++++++++++++++++++++++++++萌新想要Genius ++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

---

### 评论 #3 (作者: LG87838, 时间: 1年前)

感谢楼主的分享，论坛里还缺少mcp相关的内容，这下补上了。

如果不看结果，这个demo其实已经很完美了，实现了我们想象中的样子。消耗Token等我觉得不是问题的本质，干活需要投入成本，如果活干得漂亮，再优化成本即可，而且IT领域的成本总体是下降趋势。

说点个人观点：从大模型的角度看，也许不是demo的问题，而是大模型在专业领域的能力欠缺。如果继续优化，可能又需要绕回到大模型的微调里了。这个门槛一下子又高了起来。

现阶段可能还是LLM的初级阶段，尽管隔一段时间就会看到一些惊喜的创新，LLM确实也可以完成很多的任务。大家对LLM即有期望，但用起来又是各种嫌弃批评。总之，这个帖子不应该这么少的讨论，积极拥抱新技术，只会有好的收获，不会浪费时间。

又或许在量化领域，也许有我们还不知道的LLM已经实盘了。。。

---

### 评论 #4 (作者: QQ68782, 时间: 1年前)

[LG87838](/hc/en-us/profiles/26968783514775-LG87838)

老哥的分析很到位

作为一个最小化的、可行性验证的demo, 充分验证了思路的可行性

想要进一步优化效果, 可能需要调整提示词、工程化优化、甚至微调, 但这需要专业的量化研究的知识, 是我的大短板

LLM有很多的问题, 也有很多的可能性, 让我们一起拥抱新技术

---------------------------------------------------------------------------------------------------
知识就是力量 Knowledge is power.

---

### 评论 #5 (作者: QQ68782, 时间: 1年前)

[QZ67721](/hc/en-us/profiles/31819531107479-QZ67721)

老师希望我们熟悉字段和操作符, 无脑全自动可能不是老师希望看到的, 帖子可能发不出来😂😂

---------------------------------------------------------------------------------------------------
知识就是力量 Knowledge is power.

---

### 评论 #6 (作者: EL94401, 时间: 1年前)

感谢分享。正要学习研究，marked。

---

### 评论 #7 (作者: BJ10003, 时间: 1年前)

MCP（Model Context Protocol）是一种标准化协议，旨在为大语言模型（LLMs）提供上下文信息传递方式，从而实现AI智能体与外部数据及工具的无缝结合。其核心功能包括资源访问、工具调用和提示管理，通过客户端与服务器之间的标准化通信，使AI模型能够执行具体操作，如查询API、生成图表、访问数据库等。帖子这个尝试太前沿了。

---

### 评论 #8 (作者: YQ51506, 时间: 1年前)

很好的实践，对于后期AI自动化工程有很大的借鉴意义

---

### 评论 #9 (作者: JL67084, 时间: 1年前)

感谢分享，熟悉操作符数据集后会用的更好

---

### 评论 #10 (作者: CL64349, 时间: 8个月前)

谢谢分享，对我小白有很大的帮助！

---

### 评论 #11 (作者: LL40122, 时间: 4个月前)

向大佬学习，AI全流程自动化~

---

