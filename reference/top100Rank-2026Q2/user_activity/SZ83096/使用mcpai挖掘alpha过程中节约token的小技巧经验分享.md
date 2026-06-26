# 使用mcp+ai挖掘alpha过程中节约token的小技巧经验分享

- **链接**: 使用mcpai挖掘alpha过程中节约token的小技巧经验分享.md
- **作者**: SZ83096
- **发布时间/热度**: 4个月前, 得票: 63

## 帖子正文

在AI对话/API调用中，Token的消耗由三部分组成，形成一个“上下文窗口”：

**总消耗Token = [输入Token] + [输出Token]**

1. **输入Token** ：
   - 你提交给AI的所有内容： **系统提示词 + 对话历史 + 本次问题/指令** 。
   - 这些都会被模型“阅读”和处理。
2. **输出Token** ：
   - AI根据你的输入 **新生成** 的回复内容。
   - 你要求AI生成的文字越多，输出Token就越多。

输入的token，我观察过AI调用 mcp的过程中，函数返回的内容，有一些是不必要的，比如

get_simulate_result函数，回测完成时，请求后返回给AI 的内容如下：

![图片](images/img_322807202e.png)

可以修改函数返回的内容， 如下图： 这样，AI 获得的输入内容，应该是会减少的，而且，也不会缺少关键信息

![图片](images/img_ff68df00c1.png)

get_alpha_details 的返回内容，也可以进行裁剪，比如，只返回下面的内容

```
{  "id": "xxx",  "settings": {    "region": "GLB",    "universe": "MINVOL1M",    "delay": 1,    "decay": 8,    "neutralization": "REVERSION_AND_MOMENTUM",    "truncation": 0.01,    "pasteurization": "ON",    "unitHandling": "VERIFY",    "nanHandling": "ON",    "maxTrade": "ON"  },  "regular": {    "code": "xxx",    "operatorCount": xx  },  "dateCreated": "2026-01-29T04:14:53-05:00",  "classifications": [    {      "id": "DATA_USAGE:SINGLE_DATA_SET",      "name": "Single Data Set Alpha"    }  ],  "is": {    "longCount": 4448,    "shortCount": 4466,    "turnover": 0.0614,    "returns": 0.0474,    "drawdown": 0.0921,    "margin": 0.001543,    "sharpe": 0.97,    "fitness": 0.6,    "glbAmer": {      "sharpe": 0.97    },    "glbApac": {      "sharpe": 0.32    },    "glbEmea": {      "sharpe": 0.52    },    "checks": [      {        "name": "LOW_SHARPE",        "result": "FAIL",        "limit": 1.58,        "value": 0.97      },      {        "name": "LOW_FITNESS",        "result": "FAIL",        "limit": 1,        "value": 0.6      },      {        "name": "LOW_GLB_AMER_SHARPE",        "result": "FAIL",        "limit": 1,        "value": 0.97      },      {        "name": "LOW_GLB_EMEA_SHARPE",        "result": "FAIL",        "limit": 1,        "value": 0.52      },      {        "name": "LOW_GLB_APAC_SHARPE",        "result": "FAIL",        "limit": 1,        "value": 0.32      },      {        "name": "LOW_TURNOVER",        "result": "PASS",        "limit": 0.01,        "value": 0.0614      },      {        "name": "HIGH_TURNOVER",        "result": "PASS",        "limit": 0.7,        "value": 0.0614      },      {        "name": "CONCENTRATED_WEIGHT",        "result": "PASS"      },      {        "name": "LOW_SUB_UNIVERSE_SHARPE",        "result": "PASS",        "limit": 0.34,        "value": 0.98      },      {        "name": "LOW_2Y_SHARPE",        "result": "FAIL",        "value": 1.48,        "limit": 1.58      },      {        "name": "MATCHES_PYRAMID",        "pyramids_name": [          "GLB/D1/OTHER"        ]      }    ]  }}
```

同理，get_operators, get_datasets, get_datafields  这些函数可以优化下输出，只返回你认为需要给AI的内容

我观察过优化输出后，相同的时间内，token消耗的速度确实会慢一些（可能是错觉？）

小伙伴们可以试试，前后对比下token的消耗情况

---

## 讨论与评论 (8)

### 评论 #1 (作者: YZ64617, 时间: 4个月前)

如何节省token，的确是未来需要考虑的情况。有免费的模型使用，可以无视token花销，prompt可以很长。一旦真金白银了，真的不便宜。卯足劲儿用，一天烧100刀都是轻轻松松的。

为了节省token，除了去除没必要的信息，还可以通过把json转化为markdown或者text格式去节省。json格式几乎是最消耗token的格式。

我使用楼主的get_alpha_details 剪辑之后的json数据做了下面的比较。token统计使用的是openai的tiktoken，编码方式是cl100k_base，GPT-4模型使用的编码。

格式
字符数
Token数
字符/Token
节省Token
节省比例

 **JSON (原始)** 
2173
 **764** 
2.84
0
0.0%

 **Markdown** 
1289
 **507** 
2.54
257

 **33.6%**  ⬇️

 **Text (结构化)** 
1083
 **440** 
2.46
324

 **42.4%**  ⬇️

 **Text (极简)** 
818
 **348** 
2.35
416

 **54.5%**  ⬇️

结论：

json格式转化为markdown格式，text格式，可以大幅节省token

---

### 评论 #2 (作者: YH55729, 时间: 4个月前)

学到了，感谢分享，最近用打工人做因子，token花的肉疼。

------------------------------------------------------------------------------------------------------------------------

---

### 评论 #3 (作者: JX39934, 时间: 4个月前)

是个宝藏帖子，最近正好在AI的比赛中，token的加剧消耗确实让钱包受不了，的确要采取一些方案去节省token了，楼主的方案给了我很大的启发，我准备这就搞起来，还有1楼的转markdown也是一个不错的思路

=============================================================================

The only thing permanent is change. What we need to do is to constantly improve ourselves.

=============================================================================

---

### 评论 #4 (作者: QL50442, 时间: 4个月前)

个人用的话没有必要，token很便宜，大规模使用才有必要

---

### 评论 #5 (作者: WT70694, 时间: 4个月前)

一楼JSON转markdown省token的思路太实用了，54%的节省量很可观。mark一下回头改改自己的返回格式。

---

### 评论 #6 (作者: XY20037, 时间: 3个月前)

这篇分享的核心是 **MCP+AI 挖 Alpha 时的 Token 节约方法** ：

1. Token 消耗由输入和输出两部分构成，输入里 MCP 函数返回的冗余信息是主要浪费点。
2. 裁剪 MCP 接口返回字段：只保留关键配置、收益、夏普、换手率、边际、适应度等核心指标，去掉多余字段和校验信息。
3. 适用函数包括 get_simulate_result、get_alpha_details、get_operators、get_datasets、get_datafields。
4. 补充优化方式：将返回的 JSON 格式转为 Markdown 或纯文本，可大幅降低 Token 使用，最高能节省一半以上。

---

### 评论 #7 (作者: YX50005, 时间: 3个月前)

谢谢橘子姐的分享，其实除了可以节约token，省一些小钱钱之外，更重要的是，减少一些无意义的上下文，也可以减少对模型的干扰，模型会更聪明，挖掘因子更高效

---------------------If you come to the forum to study hard every day, you will get a GM---------------------------------

---------------------------------------------------------------------------------------------------------------------------

---

### 评论 #8 (作者: CZ39633, 时间: 2个月前)

====================================================================================                        感谢橘子姐怎么节省tokens的分享 ,很有用                                                                        ================================自信人生两百年，会当水击三千里==========================

---

