# MCP 工具优化实践:create_multiSim 函数重构

- **链接**: MCP 工具优化实践create_multiSim 函数重构.md
- **作者**: SZ83096
- **发布时间/热度**: 27天前, 得票: 21

## 帖子正文

在使用pip安装 cnhkmcp MCP 脚本进行 WorldQuant BRAIN 平台的 Alpha 研究时，我发现 create_multi_simulation 函数存在一些设计上的不足，影响了批量研究效率。下面记录了我对该函数的重构优化过程。

## 原始函数的五大问题

#### 1. 阻塞式等待设计

原始函数提交后会阻塞等待所有子模拟完成才返回结果：

# 原始函数会阻塞等待所有子模拟完成

return await _wait_for_multisimulation_completion(location, len(alpha_expressions))

问题：提交后必须等待 8+ 分钟才能返回，容易导致客户端响应超时

#### 2. 缺乏参数校验（无效配置直接发送）

原始默认参数：

```
    neutralization: str = "NONE"    truncation: float = 0.0    nan_handling: str = "OFF"    max_trade: str = "OFF"
```

问题：neutralization="NONE" 几乎不使用；无 decay 值校验；无 truncation 校验，模型可能陷入循环微调。

#### 3. 无表达式校验机制（浪费请求配额）

问题：语法错误的表达式直接发送到平台；无法提前发现算术运算符违规；错误信息不友好。

#### 4. 无去重机制（资源浪费）

问题：同一批次内重复的表达式会重复提交；历史已回测的表达式无法识别；无法区分"回测中"和"已完成"状态。

#### 5. 缺乏可追溯性（难以排查问题）

问题：无日志记录，难以追踪回测历史，无法快速定位失败的回测任务。

---

## 重构后的核心改进

#### 改进一：非阻塞返回设计

立即返回 location，由客户端轮询：

# 立即返回 location，由客户端轮询

```
    result = {        "success": True,        "message": "Multisimulation created. Please poll with get_simulate_result.",        "multisimulation_location": location,        "submitted_count": len(new_expressions),        ...    }    return result
```

优点：支持并行提交多个批次，轮询间隔可由客户端控制。

#### 改进二：参数合法性校验

```
    # 禁止 NONE neutralization     if neutralization.upper() == "NONE":        return {"error": "INVALID_NEUTRALIZATION", ...}    # decay 值白名单校验    if decay not in [0,5,10,14,20,60] or truncation != 0.08:        param_warning = f"⚠️ decay={original_decay}, truncation={original_truncation} 非法..."        decay = 0        truncation = 0.08
```

优点：提前拦截无效配置，自动修正为合法默认值。

#### 改进三：表达式多层校验

第一层 - 禁止算术运算符校验：

```
    arithmetic_check = check_expressions_no_arithmetic_batch(alpha_expressions)    if not arithmetic_check["valid"]:        return {            "error": "FORBIDDEN_ARITHMETIC_OPERATORS",            "message": f"❌ {len(arithmetic_check['invalid_expressions'])}个表达式包含禁止的算术运算符",            "hint": "规则禁止使用加法(+)、乘法(*)运算。",            ...        }
```

第二层 - 语法合法性校验：

```
    if _HAS_EXPRESSION_VALIDATOR:        for expr in alpha_expressions:            result = _expression_validator.check_expression(expr)            if not result.get('valid', False):                invalid_results.append({                    'expression': expr,                    'errors': result['errors']                })
```

优点：提交前发现语法错误，错误信息附带正确用法示例。

#### 改进四：智能去重机制

批次内去重：

# 同批次内重复的表达式只保留一个

```
    unique_expressions = list(dict.fromkeys(alpha_expressions))    duplicates_in_batch = len(alpha_expressions) - len(unique_expressions)
```

哈希数据库去重（区分 pending 和 completed）：

```
    check_results = check_expressions_batch(settings_dict, unique_expressions)    for exists, _, expr, status in check_results:        if not exists:            new_expressions.append(expr)        elif status == "pending":            pending_expressions.append(expr)        else:            completed_expressions.append(expr)
```

优点：避免重复提交相同表达式，区分"回测中"和"已完成"状态。

#### 改进五：完整的日志追溯

# 记录 location 到文件
    with open(location_file, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {location}\n")

# 记录表达式
    with open(exp_file, "a") as f:
        for expr in new_expressions:
            f.write(f"{datetime.now().isoformat()} | {location} | {expr}\n")

# 保存哈希到数据库

save_expression_hash(settings_dict, expr, status="pending")

优点：完整记录回测历史，便于问题排查。

---

---

## ExpressionValidator 实现来源

_expression_validator 来自项目本地的 Alphas/get_self_corr/check_expression.py，参考了原始 cnhkmcp 包中的 cnhkmcp/untracked/APP/Tranformer/validator.py 并进行优化。

核心特性：
- 基于 PLY (Python Lex-Yacc) 构建词法分析器和语法分析器
- 支持 200+ 函数的参数规则校验
- 支持命名参数、Group 字段校验、分号表达式处理

使用方式：

```
    from check_expression import ExpressionValidator #自定义导入路径    validator = ExpressionValidator()    result = validator.check_expression("ts_mean(close, 20)")    # result = {'valid': True, 'errors': [], ...}    result = validator.check_expression("ts_mean(close)")  # 缺少参数    # result = {'valid': False, 'errors': ['Function ts_mean Requires at least 2 Arguments...'], ...}---
```

### **哈希去重的先决条件**

此功能需要以下先决条件才能正常工作：

#### 1. MongoDB 数据库

需要运行 MongoDB 服务，通过环境变量配置：

```
    export MONGO_HOST="localhost"    export MONGO_PORT="27017"    export MONGO_USER="xxx"    export MONGO_PASSWORD="xxx"    export MONGO_DB="alpha_db"
```

使用 expressions_done 集合存储表达式哈希，文档结构：

```
    {      "hash": "sha256哈希值",      "expression": "原始表达式",      "alpha_id": "alpha ID（可选）",      "status": "pending 或 completed",      "settings": {"region": "USA", "universe": "TOP3000", ...},      "created_at": "ISO时间戳"    }
```

#### 2. 哈希生成函数

```
    def generate_simulation_hash(settings: Dict[str, Any], expression: str) -> str:        key = {            'region': settings.get('region', ''),            'universe': settings.get('universe', ''),            'delay': int(settings.get('delay', 1)),            'neutralization': settings['neutralization'],            'decay': int(settings.get('decay', 0)),            'maxTrade': settings.get('maxTrade', 'ON'),            'truncation': float(settings['truncation'])        }        return hashlib.sha256((json.dumps(key, sort_keys=True) + '||' + expression).encode()).hexdigest()
```

规则：同一个表达式 + 同一个 settings = 同一个哈希；不同 settings 会产生不同哈希。

#### 3. 辅助函数实现

# 批量检查表达式是否已存在

```
    def check_expressions_batch(settings, expressions):        hashes = [(generate_simulation_hash(settings, e), e) for e in expressions]        client = get_mongo_client()        existing_docs = {d["hash"]: d.get("status", "completed")                        for d in client[MONGO_DB]["expressions_done"].find(                            {"hash": {"$in": [h for h, _ in hashes]}},                            {"hash": 1, "status": 1}                        )}        client.close()        return [(h in existing_docs, h, e, existing_docs.get(h)) for h, e in hashes]
```

如果没有 MongoDB，可以使用 JSON 文件存储替代或直接禁用哈希去重功能。

---

状态流转说明

pending：回测中，create_multiSim 提交成功后立即设置
completed：回测完成，get_simulate_result 获取到 alpha_id 后更新
删除：回测出错时清理，避免脏数据

---

总结

通过这次重构，create_multiSim 函数从一个简单的"提交并等待"工具，变成了一个具备完整校验、去重、追溯能力的生产级工具。

主要收益：
- 效率提升：非阻塞设计 + 去重机制，大幅提升批量研究效率
- 资源节约：前置校验避免无效请求，哈希去重避免重复回测
- 错误友好：详细的错误信息和正确用法示例，降低调试成本
- 可追溯性：完整日志记录，便于问题排查和历史分析
- 合规性：强制执行业务规则，确保提交的表达式符合要求

---

## 讨论与评论 (0)

