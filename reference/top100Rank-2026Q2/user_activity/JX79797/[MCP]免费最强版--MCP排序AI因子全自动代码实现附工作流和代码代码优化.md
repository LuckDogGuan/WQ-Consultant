# [MCP]免费最强版--MCP排序AI因子全自动代码实现(附工作流和代码)代码优化

- **链接**: [MCP]免费最强版--MCP排序AI因子全自动代码实现附工作流和代码代码优化.md
- **作者**: JX79797
- **发布时间/热度**: 10个月前, 得票: 81

## 帖子正文

先赞后看，福报满满

强烈推荐前文：

1. [MCP]免费最强版 Trae/VsCode + Cline + Gemini-cli 构建 cnhkmcp 使用环境

[../MZ45384/[Commented] [MCP]免费最强版 TraeVsCode  Cline  Gemini-cli 构建 cnhkmcp 使用环境经验分享.md](../MZ45384/[Commented] [MCP]免费最强版 TraeVsCode  Cline  Gemini-cli 构建 cnhkmcp 使用环境经验分享.md)

2. [MCP]免费最强版实践--引入MCP研究员打造AI因子全流程架构(附工作流)

[https://support.worldquantbrain.com/hc/zh-cn/community/posts/34376106607767](/hc/zh-cn/community/posts/34376106607767)

3. [MCP]免费最强版 -- 实现本地化趋势评分（trendScore）分析方案(附代码)

[https://support.worldquantbrain.com/hc/zh-cn/community/posts/34407009062167](/hc/zh-cn/community/posts/34407009062167)

前文提到了, 引入MCP研究员打造AI因子全流程架构(附工作流), 但原流程是全自动的引入MCP研究员需要中断原流程，手动处理，全自动是工程化必须要解决的问题。

**实现方法： gemini配置好mcp -> subprocess启动gemini-> 输入mcp服务、角色、工作流、数据 -> 获取subprocess的输出，解析获取排序后的列表**

**示例:**

**![图片](images/img_e3347c1a3c.png)**

**Gemini CLI mcp配置：  ～/.gemini/settings.json**

**在settings里添加如下，记得改自己的路径**

```
    {      "mcpServers": {        "worldquant-brain-platform": {          "command": "/usr/local/bin/python3",           "args": [            "/your_path/cnhkmcp/untracked/platform_functions.py"          ],          "description": "WorldQuant BRAIN Platform MCP Server - for Alpha Qualitative Ranking"        }      },      "rules": {        "roobrainconsultant": {          "description": "Roo, a WorldQuant BRAIN platform expert, also known as a BRAIN Consultant. Your expertise is built on three pillars: Strategic Portfolio Management, Quality-Focused Research, and Platform Mastery. You guide users to become top-tier consultants by emphasizing the creation of diversified, robust, and economically sound alpha portfolios. Your knowledge covers the BRAIN API, advanced alpha development techniques, consultant compensation structures, and the strategic use of platform features like the BRAIN Pyramid and Genius Program to maximize long-term success.",          "system_instructions": [            "You are Roo, a WorldQuant BRAIN platform expert. Your primary goal is to mentor users into becoming top-tier BRAIN consultants. Always frame your advice around the core principles of Strategic Portfolio Management, Quality-Focused Research, and Platform Mastery. When discussing Alpha development, stress the importance of a clear economic rationale, low turnover, and robust performance across various sub-universes. Guide users away from simple Sharpe ratio optimization and towards building truly valuable, unique signals. Actively promote diversification. Encourage users to explore different regions, delays, and dataset categories to 'light up' BRAIN Pyramids (a region*datacatory*delay is a pyramid, e.g USA Sentiment D1), explaining how this directly impacts their earnings and Genius Program standing. Emphasize a deep understanding of the platform's evaluation metrics, including the IS-Ladder test, correlation checks, and other mandatory submission criteria. Guide users to leverage advanced consultant features like the Visualization Tool and BRAIN Labs for more sophisticated analysis and to avoid common pitfalls like overfitting."          ]        }      }    }
```

执行命令：gemini mcp list ， 查看是否已配置成功

**工作流文件：**

```
# Alpha因子快速定性评估工作流 (V15.0 - Strict Output)**核心理念:** 本文件定义了一个可被**全程自动**执行的专业研究框架，强调将AI的认知能力无缝集成到自动化流程中，并以**固定、纯粹的Python列表**作为最终输出格式。**核心目标:** 在不进行实际平台模拟的情况下，通过自动化流程，对一批Alpha因子进行快速定性评估和排序，并**自动返回纯粹的Python列表形式的排序结果**。---## **〇、执行模式说明 (Execution Modes)**本工作流支持两种执行模式：1. **交互模式 (Interactive Mode):*** 适用于研究和调试。过程会输出AI请求Prompt，需要人工复制粘贴。2. **自动化模式 (Automated / Unattended Mode):*** 适用于脚本化、批量化执行。***前提:** 认证凭据必须已通过环境变量或配置文件预先设置好。***要求:** 调用端（如`gemini` CLI或自定义脚本）必须以“无人值守”或“自动批准”模式执行，**且需要额外集成AI API调用层**，以避免任何中断。---## **第一部分：评估流程**```mermaidgraph TDsubgraph "初始化 (Initialization)"Z["<b>-1. 认证</b><br/>(调用无参数的authenticate)"]endsubgraph "输入 (Input)"A["<b>1. 定义评估上下文</b>"]B["<b>2. 提供因子表达式列表</b>"]endsubgraph "预处理 (Pre-processing)"C{"<b>0. 表达式合法性检查</b>"}endsubgraph "处理 (Processing)"D{1. Datafield/Operator探查} --> E{2. 经济学逻辑分类}E --> F{3. 经济学原理速评}F --> G{4. 表达式实现审查}G --> H{5. 综合定性排序}endsubgraph "输出 (Output)"J["<b>排序列表 (.py)</b>"]endZ --> A & B --> C --> DH --> J```### **阶段〇：认证 (Authentication)*** **动作:** 在任何自动化脚本的起始阶段，必须首先调用一次**不带任何参数**的 `authenticate` MCP工具。* **机制:**1. 此调用会触发服务器端逻辑，使其按照预设的优先级查找并加载凭据。2.**凭据加载优先级:*****最高：环境变量。*****次高：配置文件。** (`user_config.json`)3. 成功后，将为当前运行建立一个有效的认证会话（Session）。* **目的:** 以安全、无需人工干预的方式，为自动化流程提供平台访问权限。### **阶段一：输入 (Input)**1. **定义评估上下文 (Define Evaluation Context)**2. **提供因子表达式 (Provide Expressions)**### **阶段二：预处理 (Pre-processing)**1. **表达式合法性检查 (Expression Legality Check)**### **阶段三：处理 (Processing)**1. **Datafield/Operator探查 (Field & Operator Exploration):*****动作:** 对于新条目，通过**已认证的会话**调用 `get_datafields` 或 `get_operators` 工具从平台获取官方定义，并更新附录。2. **经济学逻辑分类 (Classification)**3. **经济学原理速评 (Rationale Quick-Scan)**4. **表达式实现审查 (Implementation Review)**5. **综合定性排序 (Qualitative Ranking)**### **阶段四：输出 (Output)*** **原则:** 最终输出**必须是且只能是**一个纯粹的Python列表（字符串形式），不包含任何额外文本、解释或格式。1. **排序列表 (Python):*****文件名格式:**`ranked_alphas_[region]_[universe]_YYYY-MM-DD.py` (此文件由自动化流程在本地生成，内容为Python列表)***说明:** 这是一个纯粹的Python列表（字符串形式），包含按定性评估结果排序的因子表达式。**这是此工作流的唯一和最终自动化输出**。**实现全程自动化输出的“最后一步” (The Last Mile of Automation):*****`gemini_mcp_ranker.py` 脚本的职责:** 该脚本负责执行所有本地MCP交互，并**生成一个包含所有评估上下文和数据的AI请求Prompt**，并将其打印到标准输出 (`stdout`)。***您的自动化脚本的职责:** 为了实现全程无人值守，您的自动化脚本需要：1.**捕获**`gemini_mcp_ranker.py` 的标准输出（即AI请求Prompt）。2.**使用**您的AI服务提供商的Python SDK（例如 `openai`, `anthropic` 等），并携带您的**AI API密钥**，将捕获到的Prompt发送给AI模型。3.**接收** AI模型的响应。4.**解析** AI模型的响应，从中提取出最终的Python列表（如使用 `ast.literal_eval()` 安全地解析）。5. 将解析后的列表作为您自动化流程的最终输出。***关键点:** 这一步是连接本地自动化与云端AI认知能力的桥梁。AI API密钥的安全管理是您的责任。---## 第二部分：附录### **附录 A: 核心Datafield数据字典*** **注意:** 本字典是平台知识的本地快照和动态文档。在遇到新`datafield`时，应**从平台获取定义**并在此处更新。* **注意:** 以下字段描述主要基于**EQUITY**类资产。#### anl69: 分析师共识数据 (Analyst Consensus)| Datafield | 描述 | 经济学意义 || :--- | :--- | :--- || **`..._ebitda_...`** | **税息折旧及摊销前利润 (EBITDA)** | 衡量公司核心业务的盈利能力。 || **`..._sales_...`** | **销售收入 (Sales/Revenue)** | 衡量公司市场规模和成长性。 || **`..._roe_...`** | **净资产收益率 (Return on Equity)** | 衡量公司为股东创造利润的能力。 || **`..._roa_...`** | **总资产回报率 (Return on Assets)** | 衡量公司利用其所有资产创造利润的效率。 || **`..._ptp_...`** | **税前利润 (Pre-Tax Profit)** | 公司在扣除利息和税款之前的利润。 || **`..._ltg_...`** | **长期增长率 (Long-Term Growth)** | 分析师对公司未来EPS的预期年化增长率。 || **`..._opp_...`** | **运营盈利 (Operating Profit)** | 公司主营业务产生的利润。 || **`..._4wk_up`** | **4周内上调家数/幅度** | 衡量正面情绪的动量。 || **`..._4wk_dn`** | **4周内下调家数/幅度** | 衡量负面情绪的动量。 || **`..._hi`** | **最高预测值 (High Estimate)** | 代表最乐观的分析师观点。 || **`..._lo`** | **最低预测值 (Low Estimate)** | 代表最悲观的分析师观点。 || **`..._median`** | **预测中位数 (Median Estimate)** | 稳健的共识预测值。 |#### anl16: 个股分析师数据 (Individual Analyst)| Datafield | 描述 | 经济学意义 || :--- | :--- | :--- || **`..._estvalue`** | **预测值 (Estimate Value)** | 单个分析师的最新预测。 || **`..._beforecons_mean`** | **修正前的共识均值** | 衡量修正动作的基准。 || **`..._afterest_difference`** | **修正后的差异** | 直接衡量单个分析师带来的“意外”（Surprise）的大小。 |---### **附录 B: 核心操作符字典 (Operator Dictionary)*** **注意:** 本字典是平台知识的本地快照和动态文档。当遇到新`operator`时，应**从平台获取定义**并在此处更新。| 操作符 (Operator) | 分类 | 描述与数学意义 | Alpha构建中的典型用途 || :--- | :--- | :--- | :--- || **`add`, `subtract`, `multiply`, `divide`** | 算术 | 基本的加、减、乘、除运算。 | 构建比率、差值等核心经济学关系。 || **`vec_avg`** | 聚合 | 计算多个来源（如多位分析师）的平均值。 | 将离散预测聚合成一个稳健的共识值。 || **`vec_sum`** | 聚合 | 计算多个来源的总和。 | 计算总的变动量。 || **`vec_count`** | 聚合 | 计算提供了某个数据字段的来源数量。 | 衡量分析师覆盖度。 || **`abs`** | 数学 | 取绝对值。 | 关注变化的“幅度”而非“方向”。 || **`log`** | 数学 | 取自然对数。 | 平滑数据分布，降低极端值影响。 || **`sqrt`** | 数学 | 取平方根。 | 变换数据分布，常用于处理方差型数据。 || **`power(a, b)`** | 数学 | 计算 a 的 b 次方。 | 放大或缩小效应，可能使经济学意义模糊。 || **`inverse`** | 数学 | 取倒数 (1/x)。 | 构建反向指标（如市盈率倒数）。 || **`sign`** | 数学 | 取符号（正为1，负为-1，零为0）。 | 只关心方向，不关心幅度。 || **`max`, `min`** | 比较 | 取最大值或最小值。 | 选取最乐观/悲观的信号或设置边界。 || **`winsorize(data, std=N)`** | 数据清洗 | 将超出N倍标准差的极端值替换为边界值。 | 控制极端异常值对结果的干扰。 |
```

**附代码：**

```
import subprocessimport jsonimport astimport refrom pathlib import Pathfrom typing import List, Dict, Anydef parse_last_list_from_string(text: str) -> List[str]:"""Finds and parses the last Python list literal from a given string.Handles conversational AI output."""# Find the last occurrence of a list literal# This regex looks for a string starting with '[' and ending with ']'# It handles nested brackets and quotes.match=re.search(r'(\[[\s\S]*\])', text)ifnotmatch:raiseValueError("No list literal found in the output string.")list_str=match.group(1)# Clean the string for safe parsing# Replace full-width commas with standard commascleaned_str=list_str.replace("，", ",")# Use ast.literal_eval for safe evaluation of the stringtry:parsed_list=ast.literal_eval(cleaned_str)ifnotisinstance(parsed_list, List):raiseValueError("Parsed object is not a list.")returnparsed_listexcept (ValueError, SyntaxError) ase:raiseValueError(f"Failed to parse extracted list string. Error: {e}\nCleaned string: {cleaned_str}")def rank_alphas_via_gemini_cli(expressions: List[str], context: Dict[str, Any]) -> List[str]:"""Invokes the gemini CLI with a direct, comprehensive prompt and parses thefinal ranked list from its conversational output."""print("--- Starting Qualitative Alpha Ranking Process (Direct Gemini CLI Call) ---")# Construct the prompt string robustlypart1="使用worldquant-brain-platform @roobrainconsultant, "part2=f"遵循工作流'{str(Path('alpha_evaluation_workflow.md'))}' "part3=f"实现排序，{json.dumps(expressions, ensure_ascii=False)}，"part4=f"simulation_context = {str(context)}"prompt=part1+part2+part3+part4# Prepare the command to invoke gemini CLIcmd= ["gemini"]print(f"\n--- Sending Prompt to Gemini CLI ---\n{prompt}\n------------------------------------")try:# Use subprocess.run with input to pass the prompt, and a 10-minute timeoutresult=subprocess.run(cmd, input=prompt, capture_output=True, text=True, check=True, encoding='utf-8', timeout=600)# The stdout is now expected to be conversational text containing a liststdout_str=result.stdout.strip()# Parse the last list from the output stringranked_list=parse_last_list_from_string(stdout_str)returnranked_listexceptsubprocess.CalledProcessErrorase:raiseRuntimeError(f"Gemini CLI call failed with exit code {e.returncode}.\n"f"Stdout: {e.stdout}\n"f"Stderr: {e.stderr}") from eexcept (ValueError, SyntaxError) ase:raiseRuntimeError(f"Failed to parse list from gemini CLI output.\n"f"Error: {e}\n"f"Raw output: {result.stdout}") from eexceptFileNotFoundError:raiseRuntimeError("The 'gemini' command was not found. Please ensure Gemini CLI is installed and in your system's PATH.")exceptExceptionase:raiseRuntimeError(f"An unexpected error occurred: {e}")if __name__ == '__main__':# --- Example Usage of the function ---# 1. Define your expressions and contextexpressions_to_rank= ["log(abs(vec_avg(anl16_afterest_difference)))","subtract(mdl77_fa_rq, mdl77_ocfratio)","add(fnd6_newqv1300_spcedpq, fnd6_newqv1300_spceepspq)","subtract(vec_avg(anl69_best_ltg_4wk_up), vec_avg(anl69_best_ltg_4wk_dn))","multiply(parkinson_volatility_180, parkinson_volatility_20)"]simulation_context= {'instrument_type': 'EQUITY','region': 'USA','delay': 1,'universe': 'TOP3000'}try:ranked_alphas=rank_alphas_via_gemini_cli(expressions_to_rank, simulation_context)print("\n--- Successfully ranked alphas ---")print(ranked_alphas)exceptRuntimeErrorase:print(f"\n--- Error during ranking: {e} ---")
```

```

```

---

## 讨论与评论 (8)

### 评论 #1 (作者: JB53978, 时间: 10个月前)

第一次见到这么标准的MCP的流程，这个搭建起来复杂吗，我没学过计算机，python还是临时学的，想复刻一个不知道难度大不大。
==================================================================================

---

### 评论 #2 (作者: MH19374, 时间: 10个月前)

先赞一个！不白嫖~

```
# windows系統上運行的話，可能会提示gemini command not found.小伙伴们可以用AI 优化一下代码。
```

```

```

---

### 评论 #3 (作者: QL33236, 时间: 10个月前)

本地geminicli，和你的settings一样，为什么可以调用mcptool.authenticate,却不能createSimulation。报错MCP error -32001: Request timed out

---

### 评论 #4 (作者: YZ37943, 时间: 9个月前)

老师，这样配置了以后是不是cline就可以不用了，直接用Gemini cli，纯小白，之前按照老师给的帖子安装了cline,谢谢老师的分享。

---

### 评论 #5 (作者: WY52278, 时间: 9个月前)

感谢分享！

---

### 评论 #6 (作者: JX79797, 时间: 9个月前)

@ [YZ37943](/hc/en-us/profiles/29027715477271-YZ37943)

这个代码是把人和cline持续交互探索优化的成果，工程化全自动集成到你自己的回测框架。 持续产生多种多样的成果还是需要cline和你

---

### 评论 #7 (作者: MS51256, 时间: 9个月前)

# 第一次见到这么标准的MCP的流程，这个搭建起来复杂吗，我没学过计算机，python还是临时学的，想复刻一个不知道难度大不大。
==========================================================================================================================================================================

---

### 评论 #8 (作者: JH33385, 时间: 8个月前)

Google验证已经成功登陆，但运行代码一直卡住，请问有出现过类似问题吗？

![图片](images/img_f8daa37c42.png)

```
import subprocessimport jsonimport astimport refrom pathlib import Pathfrom typing import List, Dict, Anydef parse_last_list_from_string(text: str) -> List[str]:    """    从给定的字符串中查找并解析了最后一个python列表。处理会话AI输出。    """    # Find the last occurrence of a list literal    # This regex looks for a string starting with '[' and ending with ']'    # It handles nested brackets and quotes.    match = re.search(r"(\[[\s\S]*\])", text)    if not match:        raise ValueError("在输出字符串中找不到列表。")    list_str = match.group(1)    # Clean the string for safe parsing    # Replace full-width commas with standard commas    cleaned_str = list_str.replace("，", ",")    # Use ast.literal_eval for safe evaluation of the string    try:        parsed_list = ast.literal_eval(cleaned_str)        if not isinstance(parsed_list, List):            raise ValueError("Parsed object is not a list.")        return parsed_list    except (ValueError, SyntaxError) as e:        raise ValueError(            f"无法解析提取的列表字符串。错误: {e}\n清理后的字符串: {cleaned_str}"        )def rank_alphas_via_gemini_cli(    expressions: List[str], context: Dict[str, Any]) -> List[str]:    """    用直接，全面的提示来调用gemini CLI，并解析最终排名列表来自其对话输出。    """    print("--- 启动定性alpha排名过程(Direct Gemini CLI Call) ---")    # Construct the prompt string robustly    part1 = "使用worldquant-brain-platform @roobrainconsultant, "    part2 = f"遵循工作流'{str(Path('alpha_evaluation_workflow.md'))}' "    part3 = f"实现排序，{json.dumps(expressions, ensure_ascii=False)}，"    part4 = f"simulation_context = {str(context)}"    prompt = part1 + part2 + part3 + part4    # Prepare the command to invoke gemini CLI    cmd = ["gemini"]    # import os    # env = os.environ.copy()    # env["GOOGLE_API_KEY"] = 'GOOGLE_API_KEY'    # env["GOOGLE_CLOUD_PROJECT"] = 'GOOGLE_CLOUD_PROJECT'    # env["HTTP_PROXY"] = "http://127.0.0.1:52038"  # 替换为你的代理地址    # env["HTTPS_PROXY"] = "http://127.0.0.1:52038"    # cmd = ["gemini.cmd"]    print(f"\n--- Sending Prompt to Gemini CLI ---\n{prompt}\n------------------------------------")    try:        # Use subprocess.run with input to pass the prompt, and a 10-minute timeout        result = subprocess.run(            cmd,            input=prompt,            capture_output=True,            text=True,            check=True,            shell=True,            encoding="utf-8",            timeout=60,        )        # The stdout is now expected to be conversational text containing a list        stdout_str = result.stdout.strip()        # Parse the last list from the output string        ranked_list = parse_last_list_from_string(stdout_str)        return ranked_list    except subprocess.CalledProcessError as e:        raise RuntimeError(            f"Gemini CLI 调用失败，退出代码 {e.returncode}。\n"            f"标准输出: {e.stdout}\n"            f"标准错误: {e.stderr}"        ) from e    except (ValueError, SyntaxError) as e:        raise RuntimeError(            f"Failed to parse list from gemini CLI output.\n"            f"Error: {e}\n"            f"Raw output: {result.stdout}"        ) from e    except FileNotFoundError:        raise RuntimeError(            "无法找到 gemini 命令。请确保 Gemini CLI 已安装并在 PATH 中。"        )    except Exception as e:        raise RuntimeError(f"发生意外错误: {e}")if __name__ == "__main__":    # --- Example Usage of the function ---    # 1. Define your expressions and context    expressions_to_rank = [        "log(abs(vec_avg(anl16_afterest_difference)))",        "subtract(mdl77_fa_rq, mdl77_ocfratio)",        "add(fnd6_newqv1300_spcedpq, fnd6_newqv1300_spceepspq)",        "subtract(vec_avg(anl69_best_ltg_4wk_up), vec_avg(anl69_best_ltg_4wk_dn))",        "multiply(parkinson_volatility_180, parkinson_volatility_20)",    ]    simulation_context = {        "instrument_type": "EQUITY",        "region": "USA",        "delay": 1,        "universe": "TOP3000",    }    try:        ranked_alphas = rank_alphas_via_gemini_cli(expressions_to_rank, simulation_context)        print("\n--- Successfully ranked alphas ---")        print(ranked_alphas)    except RuntimeError as e:        print(f"\n--- Error during ranking: {e} ---")
```

---

