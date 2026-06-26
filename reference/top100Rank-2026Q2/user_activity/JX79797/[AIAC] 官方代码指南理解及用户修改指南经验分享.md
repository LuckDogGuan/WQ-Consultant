# [AIAC] 官方代码指南理解及用户修改指南经验分享

- **链接**: [AIAC] 官方代码指南理解及用户修改指南经验分享.md
- **作者**: JX79797
- **发布时间/热度**: 8个月前, 得票: 95

## 帖子正文

## 详细组件分析

### **1. 核心文件结构**

instructions.md: 竞赛指南和工作流程文档
llm_competition.ipynb: 包含竞赛逻辑的主要Jupyter笔记本
ace_lib.py: 全面的BRAIN API封装库
helpful_functions.py: 数据处理和格式化的工具函数
requirements.txt: Python依赖包规范

### **2. 集成点**

*WorldQuant BRAIN平台集成*

- 身份验证和会话管理
- Alpha模拟和测试
- 数据检索（操作符、数据集、数据字段）
- 性能分析和相关性检查
- 提交管理

*LLM集成*

- 异步OpenAI客户端集成
- 可定制的LLM接口
- Alpha描述和生成的提示工程

### **3. 数据管理**

输入: Alpha ID、BRAIN平台凭证
处理: Alpha表达式、描述、模拟结果
输出: SuperAlphas、标记的子Alpha、性能指标

### **4. 工作流程详解**

**![图片](images/img_fd1fa22b60.png)**

## **结合官方指南和FAQ, 整理用户修改建议**

### 🔴  必须修改的部分

**1. LLM模型配置 (call_llm函数)** 
```python
async def call_llm(prompt):
     🔴 必须修改：替换为自己的LLM
     FAQ明确说明：可以用任何模型，但别改call_llm模版函数结构
```

*修改要点：* 
- ✅ 可以使用任何LLM模型（OpenAI、Claude、本地模型等）
- ❌ 不能改变函数的输入输出结构
- ✅ 可以修改内部实现逻辑

**2. Alpha ID列表** 
```python
alpha_ids = ["..."]  🔴 必须修改：使用比赛期间提交的Alpha ID
```

*重要限制：* 
- ❌ 不能使用比赛前创建的Alpha
- ✅ 仅能使用比赛期间提交的Alpha作为父Alpha

### **🟡 可以修改的部分**

**3. 提示词优化** 
```python
# 在generate_alpha_description中的prompt
prompt = f"""Describe the following alpha in plain English:\n
Alpha: {alpha_expression}. Here you can find used operators {operators[operators['scope']=='REGULAR'].to_json()}
and data {data_fields.to_json()}."""

*🟡 可以优化：改进提示词质量，避免生成不存在的操作符* 
```

**4. 数据源配置** 
```python
dataset_ids = ['pv1', 'shortinterest3']  🟡 可以修改：根据需要调整数据集
```

**5. 生成逻辑优化** 
```python
🟡 可以修改：添加验证逻辑，确保生成的Alpha表达式有效
def validate_alpha_expression(expression, available_operators):
    # 添加验证逻辑
    pass
```

### **🟢 建议增强的部分**

**6. 错误处理和验证**

根据FAQ中提到的"生成的表达式不能直接用，模型会使用你所没有的操作符"，建议添加：

```python
async def generate_new_alphas(alpha_description, brain_session):
    # 获取可用操作符
    operators = ace.get_operators(brain_session)
    available_ops = operators[operators['scope']=='REGULAR']['name'].tolist()

    🟢 建议添加：验证生成的Alpha表达式
    prompt = f"""
    基于描述生成新Alpha，但只能使用以下操作符：
    {available_ops}

    严格要求：
    1. 只使用列表中的操作符
    2. 确保语法正确
    3. 生成{num_alphas}个不同的表达式
    """
    response = await call_llm(prompt)

    🟢 建议添加：验证每个生成的表达式
    validated_alphas = []
    for alpha in response.split('\n'):
        if validate_alpha_syntax(alpha, available_ops):
            validated_alphas.append(alpha)

    return validated_alphas
```

**7. 完整的工作流实现** 
```python
🟢 建议完善：模拟、标记和提交流程
async def complete_workflow(alpha_id, brain_session):
    # 1. 生成描述
    description = await generate_alpha_description(alpha_id, brain_session)

    # 2. 生成新Alpha
    new_alphas = await generate_new_alphas(description, brain_session)

    # 3. 模拟每个新Alpha
    child_alpha_ids = []
    for alpha_expr in new_alphas:
        simulate_data = ace.generate_alpha(regular=alpha_expr)
        result = ace.simulate_single_alpha(brain_session, simulate_data)

        if result['alpha_id']:
            # 4. 标记父Alpha ID
            ace.set_alpha_properties(
                brain_session, 
                result['alpha_id'], 
                tags=[f"parent_{alpha_id}"],
                regular_desc=description
            )
            child_alpha_ids.append(result['alpha_id'])

    return child_alpha_ids
```

### 📋 修改优先级清单

高优先级 (必须完成)
1. ✅ 配置自己的LLM模型
2. ✅ 设置正确的Alpha ID列表
3. ✅ 完善模拟和标记流程

中优先级 (强烈建议)
4. ✅ 优化提示词，避免生成无效操作符
5. ✅ 添加Alpha表达式验证
6. ✅ 完善错误处理

低优先级 (可选优化)
7. ✅ 调整数据源配置
8. ✅ 优化生成数量和策略
9. ✅ 添加性能监控

### 🚨 关键注意事项

1. 提交要求：至少10个SuperAlphas才有津贴资格
2. 标记要求：所有子Alpha必须标记父Alpha ID
3. 时间限制：只能使用比赛期间创建的Alpha
4. 代码提交：最终需要提交Jupyter Notebook（不含API密钥）

---

## 讨论与评论 (6)

### 评论 #1 (作者: AH18340, 时间: 8个月前)

是不是要用大模型生成的alpha回测后组成一个super alpha再提交才算，这样感觉有的难

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #2 (作者: XY53622, 时间: 8个月前)

官方代码下载地址有吗？

---

### 评论 #3 (作者: PX70901, 时间: 7个月前)

伟杰老师讲课的代码有分享吗？

---

### 评论 #4 (作者: LZ63459, 时间: 7个月前)

官方包代码哪里下载呢

---

### 评论 #5 (作者: JD22447, 时间: 7个月前)

文中提到的官方代码在比赛的页面里面，点击Submissions进去就可以下载了。

---

### 评论 #6 (作者: HS29282, 时间: 7个月前)

官方代码下载地址：个人主页：competition 选择 AI Alpha Competition 2025 进入页面后，点击Submissions。然后页面里面有一个下载地址链接。 ![图片](images/img_650fd53442.png)

---

