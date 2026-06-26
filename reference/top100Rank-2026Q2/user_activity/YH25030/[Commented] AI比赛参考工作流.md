# AI比赛参考工作流

- **链接**: [Commented] AI比赛参考工作流.md
- **作者**: WL13229
- **发布时间/热度**: 8个月前, 得票: 34

## 帖子正文

千万不能思维受限

![图片](images/img_3861a4408b.png)

如果觉得阅读有困难，可以复制下面代码，到 [https://mermaid.live/](https://mermaid.live/)  生成高清流程图

```
graph TDA[Start - user provides seed alpha id] --> B[Authenticate with BRAIN and LLM gateway]subgraph AnalysisPhase [Analysis phase]  direction TB  C1[1. Fetch alpha details - code and settings]  C2[2. Identify operators and data fields used]  C3[3. Fetch context for each component from BRAIN API]  C4[4. Call LLM to generate economic rationale]  C1 --> C2 --> C3 --> C4endB --> C1subgraph CoreLoop [Core research loop]  direction TB  I{Step 3 - AI powered ideation}  I --> V1[3.1 Operator variation]  I --> V2[3.2 Data field variation]  I --> V3[3.3 Settings variation]  V1 --> G[Generate new alpha expressions]  V2 --> G  V3 --> G  subgraph SimEvalTag [3. Simulate evaluate and tag for each generated expression]    direction TB    S1[a. Simulate on BRAIN]    S2[b. Tag with parent id]    S3[c. Retrieve performance results]    S1 --> S2 --> S3  end  G --> SimEvalTag  S3 --> R[Performance results]  subgraph ReflectViz [4. AI powered reflection and visualization]    direction TB    N1[a. LLM experiment summary and next steps]    N2[b. Query API for all related alphas by tag]    N3[c. Generate performance comparison graphs]  end  R --> ReflectViz  ReflectViz --> CH[5. Select new champion for next iteration]  CH --> IendC4 --> ICH --> OUT[Output - group of variation alphas - End result - family of optimized alphas - SuperAlpha]
```

---

## 讨论与评论 (15)

### 评论 #1 (作者: BY28155, 时间: 8个月前)

Thanks ! Teacher !

---

### 评论 #2 (作者: XX81632, 时间: 8个月前)

感谢老师的分享，让我受益匪浅

---

### 评论 #3 (作者: ZY88181, 时间: 8个月前)

请问老师工作流怎么转成python代码？调用mcp可以实现吗？

---

### 评论 #4 (作者: AA39361, 时间: 8个月前)

昨天会议上,真是让人大开眼界

---

### 评论 #5 (作者: LR93609, 时间: 8个月前)

感谢分享，学到了。

-----------------------------------------------------------------------
  凡是发生，皆利于我；愿我所愿，尽是美好
  没有顺风，没有坦途，不去经历，无法到达
-----------------------------------------------------------------------

---

### 评论 #6 (作者: FF56620, 时间: 8个月前)

感谢老师的分享，我实际跑了一下，大概搞懂流程了，不过有一个小疑问

AI每次优化的结果，我可能只是提交一个alpha，甚至没有提交，我需要每次都把代码保存下来，最后进行一并的上传吗，还是应该怎么提供代码

=========================================================
Pursue scalable, repeatable trades rooted in probabilistic edge.
=========================================================

---

### 评论 #7 (作者: WD55783, 时间: 8个月前)

感觉借这次比赛能搭建起这个工作流对以后挖掘alpha有很大好处

---

### 评论 #8 (作者: DY53343, 时间: 8个月前)

感谢老师！

---

### 评论 #9 (作者: MY82844, 时间: 8个月前)

感谢分享，非常有启发

---

### 评论 #10 (作者: LW52547, 时间: 8个月前)

感谢分享，一定好好研究研究

---

### 评论 #11 (作者: CM48632, 时间: 8个月前)

千万不能思维受限。老师每次分享都感觉受益匪浅呀

---

### 评论 #12 (作者: WL13229, 时间: 7个月前)

[FF56620](/hc/en-us/profiles/29176848908951-FF56620)

确保您的代码中可以复现一些alpha即可

---

### 评论 #13 (作者: WD55783, 时间: 7个月前)

感谢分享，虽然还没有解锁sa的权限，但是这个工作流的思路是很值得学习的，一个好的工作流对搭建自动化程序都有很大的价值

---

### 评论 #14 (作者: YH25030, 时间: 7个月前)

谢谢老师分享。其实刚开始并没有搞懂这个流程，结合其他的论坛帖子，终于对工作流有点理解了。争取提交10个因子。

---

### 评论 #15 (作者: JJ69164, 时间: 7个月前)

点赞，高清图没搞定，哪位大佬有分享一下呗

---

