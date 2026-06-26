# [Agent skills] 枪在手跟我走，AI工作流大进化，Skills开箱即用！经验分享

- **链接**: [Commented] [Agent skills] 枪在手跟我走AI工作流大进化Skills开箱即用经验分享.md
- **作者**: VC17729
- **发布时间/热度**: 5个月前, 得票: 75

## 帖子正文

1、项目链接

各位道友好，我是白嫖党的最爱 Vincent，终于轮到我来回馈社区了。话不多说，先上项目链接： [https://github.com/tythe86/Three-Fire-Fan](https://github.com/tythe86/Three-Fire-Fan)

2、快速使用

如果你已经对 Agent Skills 的概念非常了解，并且高强度地在使用 roo code、claude code、geminicli 等工具，那么你可以直接拉取代码后，按照 README 指引配置好环境开始运行（特别注意各 md 文档中的

`/opt/miniconda3/bin/python3`  请统一替换成你的 Python 解释器路径）。

此处以 geminicli 为例，输入 ' `.agent/START_HERE.md'` ，后续可跟上 Region、Universe、Datasets 等参数。如果不写，则以  `run_config.json`  中的信息作为默认值开始执行。第一次运行需要对各项命令进行授权，建议第一次使用时统一选择“单次授权”，借此了解它对各个文件的读取顺序和触发条件。

![图片](images/img_985b5f073c.png)

![图片](images/img_08eeb49cdc.png)

3、Agent Skills 基础

Agent Skills 本质上就是一段大模型可以随时翻阅的、实现某项功能的说明文档。

![图片](images/img_0e7e41037b.png)

做一个不太全面的比喻：

- 之前的工作流，相当于  `def`  了一个超大的函数，把所有执行内容都塞进去，需要在里面一点点修改，从上到下执行，并且每次都要读取整个工作流。
- 现在使用 Agent Skills，就相当于按功能把它封装成一个个具有独立职能的“抽象类”，便于维护和复用，也更便于大模型理解，并在工作流中按需调用。

4、Agent Skills 的渐进式披露

LLM 在读取 Agent Skills 时，并不会一次性读完文档中的所有内容，而是先只看 description 部分的信息。如果与当前任务无关，就会跳过；只有在确实需要使用这个 Agent Skill 时，才会继续读取更进一步的提示内容。

这样既可以节约 token，又能减少注意力涣散，从而降低产生幻觉的概率。

5、Agent Skills 的拓展性与进阶使用

每个独立的 Agent Skills 都可以接入知识库（knowledge）和运行库（script），并按照该 Agent Skills 中 description 以下的规则进行调用。

举一个本项目中的例子：

> Guardian（守卫）：负责策略准入检查、自相关性计算以及筛选标准把控。

这个 Agent Skills 挂载了两个脚本：

- 一个通过 API 接口验证 alpha 是否通过所有检测
- 一个在本地进行自相关计算

只有两者都通过的情况下，才会继续下一步的 prod-corr 检测。

LLM 只会按照 Agent Skills 中的规则去调用并执行脚本、获取返回信息，而不会去“阅读”脚本本身，从而避免上下文压力并节省 token 消耗。

在整个工作流调度的总控 Agent Skills  `skill-research-master`  中，我同样使用了 Python 脚本做验证，可以在一定程度上避免 LLM“放飞自我”、随意跳步骤运行的情况。

后续执行的各个环节都可以创建 Agent Skills 技能库。建议把思路和想法直接交给 Claude 大模型，让它帮你生成 Agent Skills。我的 Agent Skills 技能库基本都是 Claude Opus 参考 Claude 官方的 Agent Skills 范式写出来的。

同样要特别注意各个 Agent Skills 之间的数据传递。相比 LangChain、DeepAgent 等方案，Agent Skills 算是非常简单易上手的了，期待看到国区各位大佬把 Agent Skills 玩出花来。

6、局限性与不足

这里还是要先叠个甲： **Agent Skills 只是一套框架，只是“术”的层面** 。不同的人用出来的效果可能天差地别，更多还是取决于个人的理解和洞察力，这些会直接体现在各个 Agent Skills 的知识库和脚本搭建上。

本项目仅作为示例，做不出 alpha 可不要来找我，就算能无脑做出 alpha，也很快会因为 PC 而失效。

只要整个 Agent 是由 LLM 驱动，幻觉就是不可避免的，只能尽量想办法去降低它出现的概率。

7、结语

前前后后从了解概念、学习、构建到验证，大概花了接近一周时间。开年后做的第一件事就是它了。后面会重点考虑两个方向：

- 一方面，如何沉淀可复用的知识库、RAG，让整个工作流产生复利
- 另一方面，如何拓展思路，获取更多 idea

最后，希望大家多多使用，也希望能把这套框架打磨成国区的一套基础设施。如果你搓出了好用的 Agent Skills，欢迎联系我一起加到仓库中。

祝新年快乐！

---

## 讨论与评论 (16)

### 评论 #1 (作者: JR57542, 时间: 5个月前)

哈哈哈哈，感谢，作为一个新兵刚入门就有大炮用了，感觉再套上迭代系统会如何，给skills也自我迭代

---

### 评论 #2 (作者: TL32287, 时间: 5个月前)

非常厉害的思路，目前遇到的问题就是繁琐修改基础的内容，现在有了agent skill之后就可以快速的找寻自己能够得到的技能，这样才投入训练的时候可以很快的产出产物。

---

### 评论 #3 (作者: JX54288, 时间: 5个月前)

大佬，github链接404呢

---

### 评论 #4 (作者: JZ76850, 时间: 5个月前)

项目网站打开是404，不知道是不是我打开的方式不太对 ![图片](images/img_5b69ac1ddb.png)

---

### 评论 #5 (作者: YG48815, 时间: 5个月前)

项目打不开

---

### 评论 #6 (作者: LW29329, 时间: 5个月前)

哥，你这私有库吗，我看怎么404

---

### 评论 #7 (作者: SM90987, 时间: 5个月前)

您好，大佬，您这个guthub项目地址打开是空的，麻烦更新下，谢谢

---

### 评论 #8 (作者: KQ43044, 时间: 5个月前)

[https://github.com/tythe86/Three-Fire-Fan](https://github.com/tythe86/Three-Fire-Fan)  链接失效了可以重新放下链接吗

---

### 评论 #9 (作者: ML28213, 时间: 5个月前)

大佬！把编程那一套搬到因子挖掘上了。非常新非常棒的思路！感谢指路，这就拉下来玩玩

---

### 评论 #10 (作者: ML28213, 时间: 5个月前)

链接直接点进去好像没有访问权限

---

### 评论 #11 (作者: ZY23886, 时间: 5个月前)

[https://github.com/tythe86/Three-Fire-Fan](https://github.com/tythe86/Three-Fire-Fan)  开不开啊 大佬

---

### 评论 #12 (作者: LY52969, 时间: 5个月前)

思路又打开了，用skill是不是可以进行组合做更复杂的事情了

---

### 评论 #13 (作者: VC17729, 时间: 5个月前)

为避免一些不必要的麻烦已将原先github仓库关闭，请移步gitee拉取。
 [https://gitee.com/vincent0226/Three-Fire-Fan](https://gitee.com/vincent0226/Three-Fire-Fan)

---

### 评论 #14 (作者: FF56620, 时间: 5个月前)

开源大佬，感谢分享

-------------------------------------

Pursue scalable, repeatable opportunities rooted in probability.

---

### 评论 #15 (作者: MZ45384, 时间: 5个月前)

原来skills跟mcp这么不同，看起来确实更有结构性和逻辑性，可以避免不必要的操作。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #16 (作者: SL19872, 时间: 5个月前)

效果怎么样？

---

