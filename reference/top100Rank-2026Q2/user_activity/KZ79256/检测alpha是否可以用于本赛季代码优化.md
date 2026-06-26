# 检测alpha是否可以用于本赛季代码优化

- **链接**: 检测alpha是否可以用于本赛季代码优化.md
- **作者**: KZ79256
- **发布时间/热度**: 1年前, 得票: 59

## 帖子正文

众所周知，还有几天就定级了，到时候运算符和数据集都会重新随机。那么就会导致库存里的alpha报销。因此，我优化了一下 [WL27618](/hc/en-us/profiles/29059197295767-WL27618) 的提供的 [ast解析表达式的代码](../MS51256/[Commented] 用python ast提取表达式中operator和datafield的方法代码优化.md) ，从而可以用于检测alpha是否可以用于本赛季。

原理，使用ast解析表达式里的ops和fields，和自己可用的进行比较

```
import astimport reimport keyworddef parse_alpha(alpha_expression: str) -> dict[str, list[str]]:    """解析表达式并提取操作符和数据字段。    该函数用于解析输入的表达式字符串，进行预处理、AST解析，并提取其中的操作符和数据字段。    它会过滤掉无效的数据字段（如Python关键字、已定义变量等），并保留操作符的顺序和重复项。    Args:        alpha_expression (str): 输入的表达式字符串。    Returns:        Dict[str, List[str]]: 包含操作符和数据字段的字典。            - 'operators': 提取的操作符列表，保留顺序和重复项。            - 'data_fields': 提取的有效数据字段列表，已过滤无效项。    """    # 运算符预处理    replacements = [        (r'\b(or)\b', 'logical_or'),  # 保护逻辑函数名        (r'\b(and)\b', 'logical_and'),        (r'\&\&', ' and '),          # 转换运算符        (r'\|\|', ' or '),        (r'(?<!\=)\!(?!\=)', ' not '),        (r'\?', ' if '),        (r'\:', ' else '),        (r'\bNaN\b', '0')           # 处理特殊常量    ]    for pattern, repl in replacements:        alpha_expression = re.sub(pattern, repl, alpha_expression)    # 清理注释和字符串    alpha_expression = re.sub(r'(?m)^\s*(//|#).*\n?', '', alpha_expression)    alpha_expression = re.sub(r'"([^"]*)"', "0", alpha_expression)    # 处理和 python 内置逻辑表达式冲突    alpha_expression = re.sub(r'\band\(', 'and_(', alpha_expression)  # 替换 'and('    alpha_expression = re.sub(r'\bor\(', 'or_(', alpha_expression)  # 替换 'or('    # 合并多行没有分号的表达式    lines = alpha_expression.splitlines()    merged_lines = []    temp_line = ""    for line in lines:        stripped_line = line.strip()        if stripped_line and not stripped_line.endswith(';'):  # 如果行不以分号结尾            temp_line += " " + stripped_line  # 合并到上一行        else:            if temp_line:  # 如果存在合并的内容                merged_lines.append(temp_line.strip())  # 添加到结果中            merged_lines.append(stripped_line)  # 添加当前行            temp_line = ""  # 清空临时合并内容    # 如果最后一行没有以分号结尾，确保它被处理    if temp_line:        merged_lines.append(temp_line.strip())    alpha_expression = "\n".join(line.strip() for line in merged_lines)    # 解析AST    tree = ast.parse(alpha_expression)       operator_map = {        ast.Add: 'add', ast.Sub: 'subtract',        ast.Mult: 'multiply', ast.Div: 'divide',        ast.Pow: 'power', ast.USub: 'reverse',        ast.Lt: 'less', ast.Gt: 'greater',        ast.LtE: 'less_equal', ast.GtE: 'greater_equal',        ast.Eq: 'equal', ast.NotEq: 'not_equal',        ast.And: 'and', ast.Or: 'or',        ast.Not: 'not'    }    operators = []  # 改为列表    data_fields = [] # 改为列表    defined_vars = set()    for node in ast.walk(tree):        # 变量定义检测        if isinstance(node, ast.Assign):            for target in node.targets:                if isinstance(target, ast.Name):                    defined_vars.add(target.id)        # 函数调用捕获        if isinstance(node, ast.Call):            if isinstance(node.func, ast.Name):                func_name = node.func.id                # 恢复原始函数名                if func_name.lower() == 'logical_or':                    func_name = 'or'                elif func_name.lower() == 'logical_and':                    func_name = 'and'                operators.append(func_name)            elif isinstance(node.func, ast.Attribute):                operators.append(node.func.attr)        # 运算符捕获        if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp)):            ops = []            if isinstance(node, ast.BinOp):                ops = [node.op]            elif isinstance(node, ast.UnaryOp):                ops = [node.op]            elif isinstance(node, ast.Compare):                ops = node.ops            elif isinstance(node, ast.BoolOp):                ops = [node.op]                       for op in ops:                if type(op) in operator_map:                    operators.append(operator_map[type(op)])        # 三元运算符标记        if isinstance(node, ast.IfExp):            operators.append('if_else')        # 变量名收集        if isinstance(node, ast.Name):            data_fields.append(node.id)    # 数据字段过滤    exclude_keywords = set(keyword.kwlist) | {'True', 'False', 'None'}    operators_set = set(operators)  # 用于过滤同名字段    valid_data = [        fieldforfieldindata_fields        iffieldnotindefined_vars        and field not in {'nan', 'true', 'false'}        and field not in exclude_keywords        and field not in operators_set    ]    return {        'operators': operators,           # 保留原始顺序和重复        'data_fields': valid_data          # 已过滤无效项但保留重复    }def identify_state(regular):    res = parse_alpha(regular)    return len(set(res['data_fields'])-set(fields)) + len(set(res['operators'])-set(ops))
```

优化后的代码可以检测到里面所有的运算符，运算符数量可以和wq官方给的完全一致。且经过了我之前提交的非一二三阶复杂的alpha表达式的验证。

之后获取自己的ops和fields，以及alpha的regular。由于我是用mongo数据库管理的alpha

所以代码没法照抄，但是可以经过修改移植到自己的体系

```
    group_datafields, datafields = loadAset_data()    fields = set(datafields['id'].tolist() + group_datafields['id'].tolist())    ops = set(cfg.OPS_LIST)    print(f"{len(fields)} fields, {len(ops)} ops")    print(f"查询到的 的alphas数量 {collection.count_documents({})}")    results = list(collection.find({'genius_state':'Old'}, {"_id":1, "alpha_id":1, 'regular':"$sim_data.regular", 'ops': "$info.operatorCount"}))    results = pd.DataFrame(results)    print(f"查询语句Old待更新的 {results.shape}")    results['notcounts'] = results['regular'].parallel_apply(identify_state)    print(f"notcounts的情况 {results['notcounts'].value_counts()}")    results = results.query('notcounts==0')       batch_size = 10000    total_updated = 0    # 获取 _id 列表    id_list = results['_id'].to_list()    # 分批更新    for i in tqdm(range(0, len(id_list), batch_size)):        batch = id_list[i:i + batch_size]        result = collection.update_many(            {'_id': {'$in': batch}},  # 匹配 _id 在当前批次中的文档            {'$set': {'genius_state': 'Current'}}  # 更新 genius_state 和 user_idx        )        total_updated += result.modified_count
```

---

## 讨论与评论 (1)

### 评论 #1 (作者: KZ79256, 时间: 1年前)

获取某个region，delay，universe组合下的所有fields可以从以下链接获得，不受个数限制

> [https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&region={region}&delay={delay}&universe={universe}](https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&region={region}&delay={delay}&universe={universe})

---

