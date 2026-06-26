# 📢 AI Alpha 竞赛：提交前最终自查清单 (Final Self-Check List)

- **链接**: [Commented] AI Alpha 竞赛提交前最终自查清单 Final Self-Check List.md
- **作者**: WL13229
- **发布时间/热度**: 4个月前, 得票: 13

## 帖子正文

各位参赛选手请注意：
本次比赛评审采用  **严格标准** 。为确保您的作品能被正确受理，提交前请务必完成以下  **四项强制性自查** 。❌  **任何不符项都可能导致作品无效。**

#### ✅ 1. 环境依赖 (Dependency Management)

比赛基准环境见 requirements.txt。

- **强制要求** ：如果您的代码中使用了任何  **非标准库** （不在 requirements.txt 中）， **必须**  在 Notebook 靠前的单元格中显式包含安装命令。
- ```
  pandas
  ```
- **示例** ： `!pip install <your_package_name>`
- **自查标准** ：假设在一台全新的机器上运行您的 Notebook，它必须能自动安装依赖并跑通全流程。请特别注意，标准库中没有

#### ✅ 2. 输出文件格式 (Strict Output Schema)

程序运行结束后，必须在当前目录下生成名为 alphas.json 的文件。该文件必须是一个  **JSON 对象列表** ，且每个对象  **严格包含**  以下 5 个字段（拼写区分大小写）：

1. `"alpha_expression"`
2. `"economic_rationale"`
3. `"data_fields_used"`
4. `"operators_used"`
5. `"alpha_settings"`

- **自查标准** ：请用文本编辑器打开生成的 alphas.json，确保 Keys 与上述 5 项完全匹配，无多余字段，无拼写错误。

#### ✅ 3. LLM 使用与运行记录 (Execution Trace)

- **核心逻辑** ：Notebook 中必须明显包含调用 LLM（大语言模型）生成或优化策略的代码/提示词。
- **保留输出** ：提交的  `.ipynb`  文件  **必须保留所有单元格的运行输出 (Cell Outputs)** 。
- **自查标准** ：提交前  **切勿**  点击 "Clear All Outputs"。确保评审能看到代码执行日志和中间结果。

#### ✅ 4. 提交物与语言要求 (Submission & Language)

- **提交内容** ：必须同时提交  **演示文稿 (PPT)**  和  **Jupyter Notebook (.ipynb)** 。
- **语言要求** ：所有提交材料（包括 PPT 内容、Notebook 中的注释及 Markdown 说明） **必须使用英语** 。
- **自查标准** ：检查您的 PPT 和 Notebook，确保所有文本均为英文且表达清晰。

---

## 讨论与评论 (10)

### 评论 #1 (作者: WL13229, 时间: 4个月前)

如果你是使用AI帮你打代码，可以用以下提示词让AI帮助你自查。请注意，AI可能会出错

```
Please act as a Competition Submission Judge. I have attached my competition notebook (.ipynb). Please verify it against these strict rules:1. **Dependencies**:    - The standard environment includes only: [pandas, requests, seaborn, matplotlib, tqdm, nest_asyncio, openai, pydantic, tabulate, ace_lib].   - If my code imports ANY other package (like sklearn, numpy, etc.), verify that I have a `!pip install` command for it.2. **Output File**:    - Verify the code generates a file named exactly `alphas.json`.   - Verify the JSON structure contains a list of objects with these exact 5 keys:      "alpha_expression", "economic_rationale", "data_fields_used", "operators_used", "alpha_settings".3. **Execution & LLM**:    - Confirm LLM usage logic is present.   - Confirm cell outputs are likely preserved (no "clear output" commands).4. **Language**:    - Confirm all text (markdown/comments) is in English.Report PASS or FAIL for each item. Answer in Chinese with explain.
```

---

### 评论 #2 (作者: AM12075, 时间: 4个月前)

已经提交的无法删除，再次提交最新版的吗？

---

### 评论 #3 (作者: RM49262, 时间: 4个月前)

=====================================评论区=========================================

感谢weijie老师的贴心提醒

自己看了是符合要求的  AI也说全PASS了  那就交上去把

===================================================================================

---

### 评论 #4 (作者: JR57542, 时间: 4个月前)

如果我本来的流程全部是claude code cli里面实现的（还带有subagent，纯api没法调用subagent），还带有claude skills 。那我需要改装成纯ipynb脚本+ai的apikey实现吗？有点懵了

---

### 评论 #5 (作者: WL13229, 时间: 4个月前)

[AM12075](/hc/en-us/profiles/30421958512663-AM12075)

评委只看最后提交的版本

---

### 评论 #6 (作者: WL13229, 时间: 4个月前)

[JR57542](/hc/en-us/profiles/34782588698007-JR57542)

需要

---

### 评论 #7 (作者: QX52484, 时间: 4个月前)

======================================================================
补充一下不能携带账号密码和api key
======================================================================

---

### 评论 #8 (作者: WX87649, 时间: 4个月前)

weijie老师，我好像不能同时提交PPT跟notebook.应该怎么办呢?

---

### 评论 #9 (作者: YQ51506, 时间: 4个月前)

摸鱼了，最终关头PPT和代码都写好了，alpha没交够

---

### 评论 #10 (作者: CZ39633, 时间: 3个月前)

====================================================================================                        感谢老师的提醒！！！                                                                                                                        ================================自信人生两百年，会当水击三千里==========================

---

