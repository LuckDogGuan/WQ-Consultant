# 【Community Leader -因子构造 💎 】点赞50有奖 教你如何不用自己写代码，用Claude Skill + Subagent复刻Kunqi老师的Gem工作流经验分享

- **链接**: 【Community Leader -因子构造  】点赞50有奖 教你如何不用自己写代码用Claude Skill  Subagent复刻Kunqi老师的Gem工作流经验分享.md
- **作者**: RM49262
- **发布时间/热度**: 6个月前, 得票: 23

## 帖子正文

如果你没看过昨晚Kunqi老师的直播分享，这里就先简单介绍一下：- Kunqi老师对Gem的定义是**寻找基于数据含义的Idea**- 大体的研究流程就是1. 通过数据集的定义/数据字段的定义进行聚类2. 基于各个类别的数据字段创建idea(比如通过多数据字段及其之间的关系来提供新的信息)3. 通过Lab观察数据的特征分布4. 基于上述结果创建具体的模板并开始回测目前论坛里已经有非常多MCP相关的AI工作流优化贴，通过提示词优化可以一定程度上复刻上述流程，这里不再赘述。Kunqi老师昨天分享的时候介绍的貌似是基于Langchain的多agent工作流。我本人最近在使用的工具是Claude。因此我尝试通过claude skill + subagent架构复刻了Kunqi老师的这套工作流，这里把经验也分享给大家1.为什么要用Skill？Claude Skill MCP的区别在哪里？Claude Skill 是一种轻量级的、基于文件的指令包。它通常由 Markdown 文件（包含指令 Prompt）和脚本文件（如 Python/Bash）组成。核心作用： 它用来教 Claude 如何执行特定的、可重复的任务流程。MCP 是一个开放的通信协议标准（类似 USB-C 接口标准）。它规定了 AI 模型如何连接外部的数据源和工具。核心作用： 它用来让 Claude 连接外部世界的数据和工具。具体到我们的AI辅助alpha生成的工作流中，当我们尝试用MCP和Skill时最大的区别就是上下文占用问题。通常对于MCP，我们需要将大量的指令放在md文档中一次性全部传给LLM，占用较多Context (工具定义通常常驻上下文)。而对于Skill，Claude说它是可以做到随用随取的，Context占用较少 (按需加载，节省 Token，避免LLM注意力分散)。同时，claude还支持sub-agent，可以有独立的context来执行某些任务。这也和Kunqi老师工作流中的'Seperate specialized verifier agent'的理念不谋而合。但目前Claude Skill只支持Claude/Codex生态，不支持其他LLM。因此，若要尝试，只能采用这两个模型。下文介绍的以Claude为例2.Claude Skill如何创建关于安装Claude Cli的部分请自行查阅，和安装别的工具(比如Gemini Cli)区别不大。Claude Skill的官方说明文档地址是：https://code.claude.com/docs/en/skills我们需要在项目文件夹的.claude文件夹中创建一个skill文件夹，在skill内部再创建我们所需的各类具体skill。比如你想创建一个叫做my-skill，那么只要它的文件夹架构符合以下标准即可：my-skill/├── SKILL.md (required)├── reference.md (optional documentation)├── examples.md (optional examples)├── scripts/│   └── helper.py (optional utility)└── templates/└── template.txt (optional template)可以看到，根据官方说明我们最主要需要的就是Skill.md这个文档。它就是整个Skill的核心。Skill.md的内部格式要求为：---name: safe-file-readerdescription: Read files without making changes. Use when you need read-only file access.allowed-tools: Read, Grep, Glob---# Safe File ReaderThis Skill provides read-only file access.## Instructions1. Use Read to view file contents2. Use Grep to search within files3. Use Glob to find files by pattern看到这里，你可能会怀疑，为什么要说零代码就能复刻呢？明明还需要自己搞这么多复杂的内容，我一点代码都不懂啊那是因为Claude为了方便我们从零开始创建Skill，他自己写了个Skill，功能就是帮我们来创建我们自己所需Skill详见https://github.com/anthropics/skills简单来说，你只需要如下操作即可：1.在Claude Cli中输入 /plugin marketplace add anthropics/skills  按回车2.在Claude中输入/plugin 按回车3.选择那个 anthropic-agent-skills 按回车4.进一步选择example-skills 再按回车，就安装好了example skills中就包括了 'skill-creator'  这个帮助我们从零创建Skill的skill3.借助skill creator 一键复刻kunqi老师的Gem工作流看到这里，如果你已经安装好了这个'skill creator'，你就可以直接通过prompt 一键生成skill了。这里只需要在提示词中告诉他，请调用'skill creator'，为我创建一个新的skill，要求它可以做到1/2/3哪些内容即可。甚至你都不用自己写具体的说明文档，把昨晚kunqi老师在直播中展示的流程图截图一下，放在文件夹里，告诉他按照截图的工作流一步步复刻就好。在这里简单说明一下，claude subagent大概就是一个'拥有独立大脑（上下文窗口）、独立角色设定和特定权限的“分身”，它由主 Agent 指挥去完成某项具体的“脏活累活”。因此，假如我们想要通过sub-agent来实现Kunqi老师工作流中的'Seperate specialized verifier agent'的话，在prompt中注明就好。claude会自动帮我们实现。4.查看并调用我们创建好的Skill当上一步运行完成时，你可以在prompt 框中输入：what skills are available如果你的skill被正确创建，你就可以看到它了那么此时，你就解锁了一键运行Gem工作流的方法比如在prompt中输入'请你调用gem-workflow,为我分析一下IND TOP500 delay1的model77 dataset'它就会自动开始一键运行了！5.初步成果展示6.总结上述内容都只是我2个小时初步实现的效果，还有待进一步打磨。这里只是把创建的流程分享给大家，做个参考，和论坛其他内容完全可以互补起来一起使用。在目前LLM的帮助下，我们很容易的就可以将idea转化为代码。所以不妨大胆地用起来，把idea转化为源源不断的base pay。7.点赞有奖环节本来想直接分享我做好的这个初步的skill，但貌似昨晚会议的精神是鼓励大家自己行动起来。所以这里本人只能尽绵薄之力鼓励一下大家把新工具用起来了：我有三张claude pass，每张可以兑换一周的Claude Pro会员资格，假如点赞超过50我就放在评论区供有缘人自取吧哈哈哈（要是点赞点的速度太慢ticket过期了我也没办法了）看到这里，希望大家点个赞，祝大家一起早日GM！

---

## 讨论与评论 (7)

### 评论 #1 (作者: JG15244, 时间: 5个月前)

20 days ago ..........帖子这么久才被放出来呀。。。过期了吗佬

---

### 评论 #2 (作者: PF50988, 时间: 5个月前)

刚收到邮箱推送，一看20days ago

---

### 评论 #3 (作者: LL87164, 时间: 4个月前)

实际生成的 GEM 的信号怎么样？产出比？

---

### 评论 #4 (作者: JR57542, 时间: 4个月前)

实际上产出比不高，我这两周一直在用，可能是不太会用的缘故

---

### 评论 #5 (作者: MZ45384, 时间: 4个月前)

产出如何，过了两个月了。======================================================================================知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%# sys.setrecursionlimit(α∞)# PnL = ∑(Robustness * Creativity)#无限探索、鲁棒性优先，创新性增值#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。======================================================================================

---

### 评论 #6 (作者: JZ38399, 时间: 2个月前)

大佬，对于这套流程非常好奇，想问下目前产出率如何，在这段使用过程中，有哪些可以提升的地方，可以分享下么。另外在使用这套流程之后，多字段的alpha提交，对vf和combine影响如何，对比之前一二三阶或者说单字段，有提升么，非常期待大佬的再次分享！！！祝大佬vf1

---

### 评论 #7 (作者: JL33484, 时间: 16天前)

牛🐮

---

