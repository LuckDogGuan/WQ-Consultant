# 待优化拯救因子的分类体系与检索规范 (Factor Optimization & Categorization Guide)

为了对评级优良（S/A/B/C 级）但存在仿真异常/校验报错的因子进行精细化管理与挽救，本系统引入了**“本地双重分类标注机制”**。我们在 SQLite 数据库的记录中，以及 `payload` JSON 的属性中，对这些因子的故障根源进行了归类。

---

## 1. 待优化拯救因子分类定义 (TODO Categories)

| 类别代码 (Category Code) | 故障场景与描述 (Failure Scenario) | 诊断依据 (Diagnostic Criteria) | 推荐挽救优化手段 (Rescue Actions) |
| :--- | :--- | :--- | :--- |
| **`TODO_SYNTAX`** | **语法或不支持算子错误** | 表达式语法结构错、算子拼写错或该区域/该板块不支持的算子。 | 校验并替换区域不支持算子；修复嵌套括号错。 |
| **`TODO_DATAFIELD`** | **数据字段受限或不可用** | 使用了非本区域、未订阅或不可公开的数据源字段。 | 查找同义替代字段或用基础量价字段重构。 |
| **`TODO_DECAY`** | **高相关性或衰退期不足** | 表现极好但本地自相关性超标，或者 Decay 导致回测报错。 | 引入行业/概念中性化消偏；使用截断/消偏算子拯救。 |
| **`TODO_CONSTRAINTS`** | **多空单侧归零或股票数少** | 活跃股票数少于 30 只，或任一完整年度多空不平衡导致仿真 Fail。 | 调整选股过滤阈值，扩宽流动性覆盖。 |
| **`TODO_GENERIC`** | **其他通用/偶发仿真异常** | 接口超时、网络闪退或 WQ 平台临时故障报错。 | 直接保留，在网络顺畅时重新提交校验。 |

---

## 2. 数据库标注技术细节

在巡检流程判定因子由于 Error/Fail 无法 Checks 时，除了将 `status` 设为 `ERROR` 或 `FAIL` 外，还会在 `payload` 属性中追加存储类别：

```json
{
  "todo": "optimize_later",
  "todo_category": "TODO_SYNTAX",
  "error_message": "Mismatched parentheses at index 14"
}
```

---

## 3. 极速检索 SQL 规范 (SQLite Queries)

在未来进行因子改写或大批量优化（例如消偏算法上线）时，您可以通过如下 SQL 命令瞬间筛选出需要拯救的特定类别因子：

### 3.1 检索所有待优化但未退休的优质因子
```sql
SELECT alpha_id, name, sharpe, alpha_type, status,
       json_extract(payload, '$.todo_category') AS category
FROM alpha_records
WHERE is_garbage = 0 
  AND status IN ('ERROR', 'FAIL')
  AND json_extract(payload, '$.todo') = 'optimize_later';
```

### 3.2 针对自相关（Decay）问题大批量提取因子
```sql
SELECT alpha_id, name, sharpe, expression
FROM alpha_records
WHERE is_garbage = 0
  AND json_extract(payload, '$.todo_category') = 'TODO_DECAY';
```

### 3.3 针对语法算子错误大批量提取因子
```sql
SELECT alpha_id, name, sharpe, expression,
       json_extract(payload, '$.error_message') AS err_msg
FROM alpha_records
WHERE is_garbage = 0
  AND json_extract(payload, '$.todo_category') = 'TODO_SYNTAX';
```
