# 【MCP WorkFlow】AI排障手册经验分享

- **链接**: [Commented] 【MCP WorkFlow】AI排障手册经验分享.md
- **作者**: FF56620
- **发布时间/热度**: 6个月前, 得票: 85

## 帖子正文

在使用AI时，总是会遇到一些问题，在每次遇到问题，我都让AI记录了下来，方便后续进行快速排查，分享给大家，希望有所帮助。

```
    ## 🔍 错误诊断流程

    ### 快速诊断检查表

    遇到错误时，按以下顺序检查：

    1. **参数层面** (80%的错误原因)
    - [ ] region/delay/universe组合是否合法？
    - [ ] 参数命名是否正确？  
    - [ ] ASI地区是否设置了max_trade="ON"？

    2. **表达式层面** (15%的错误原因)
    - [ ] 字段名是否存在且拼写正确？
    - [ ] VECTOR字段是否先用vec_*()处理？
    - [ ] 操作符是否支持该输入类型？

    ## 🚨 常见错误类型及解决方案

    ### 1. 数据类型错误 (最高频)

    #### 错误现象
    ```
    Operator rank/zscore/scale does not support event/vector inputs
    Operator ... does not support event inputs  
    ```

    #### 错误原因
    VECTOR/EVENT类型字段直接用于截面操作符

    #### 解决方案
    ```python
    # ❌ 错误写法
    "rank(anl69_best_eps_4wk_up)"

    # ✅ 正确写法  
    "rank(vec_avg(anl69_best_eps_4wk_up))"
    "rank(vec_sum(anl69_best_net_chg_pct))"

    # EVENT类型处理
    "if_else(earnings_announce_date == today, 1, 0)"
    ```

    #### 诊断工具
    ```python
    # 查看字段数据类型
    mcp_tool("worldquant-brain-platform", "get_datafields", {
        "search": "anl69",
        "region": "USA", "delay": 1, "universe": "TOP1000"
    })
    # 关注返回结果中的 "type" 字段: MATRIX/VECTOR/EVENT
    ```

    ### 2. 配置参数错误

    #### 错误现象
    ```
    Invalid parameter combination
    400 Bad Request
    Parameter validation failed
    ```

    #### 解决方案
    ```python
    # 1. 获取合法配置组合
    valid_configs = mcp_tool("worldquant-brain-platform", "get_platform_setting_options", {})

    # 2. 常见合法组合参考
    usa_config = {"region": "USA", "delay": 1, "universe": "TOP1000"}
    glb_config = {"region": "GLB", "delay": 1, "universe": "TOP3000"}  
    eur_config = {"region": "EUR", "delay": 1, "universe": "TOP1200"}
    asi_config = {"region": "ASI", "delay": 1, "universe": "MINVOL1M", "max_trade": "ON"}
    chn_config = {"region": "CHN", "delay": 1, "universe": "TOP2000U"}
    ```

    #### 常见错误配置
    ```python
    # ❌ 这些组合不存在
    {"region": "GLB", "delay": 0}           # GLB没有D0
    {"region": "ASI", "universe": "TOP3000"} # ASI没有TOP3000
    {"region": "USA", "universe": "MINVOL1M"} # USA常用TOP系列
    ```

    ### 3. ASI地区特殊错误

    #### 错误现象
    ```
    Simulation failed  
    400 error in ASI region
    Max trade limit exceeded
    ```

    #### 解决方案
    ```python
    # ASI地区必须设置
    asi_params = {
        "region": "ASI",
        "delay": 1,
        "universe": "MINVOL1M",  # 或 "ILLIQUID_MINVOL1M"
        "max_trade": "ON"        # ⭐ 必须设置
    }
    ```

    ### 4. MultiSim使用错误

    #### 错误现象
    ```  
    Invalid alpha_expressions count
    Need 2-8 expressions for multiSim
    ```

    #### 解决方案
    ```python
    # ❌ 错误：只有1个表达式
    create_multiSim({
        "alpha_expressions": ["rank(close/delay(close,5))"]  # 只有1个
    })

    # ✅ 正确：2-8个表达式
    create_multiSim({
        "alpha_expressions": [
            "rank(close/delay(close,5))",
            "rank(-returns)",  
            "rank(roe)"
        ]
    })
    ```

    ### 5. 参数命名错误

    #### 错误现象  
    ```
    Unknown parameter: nanHandling
    Unknown parameter: unitHandling  
    Parameter ignored
    ```

    #### 解决方案
    ```python
    # ❌ 错误：驼峰命名
    {
        "nanHandling": "OFF",
        "unitHandling": "VERIFY",
        "maxTrade": "ON"
    }

    # ✅ 正确：snake_case命名
    {
        "nan_handling": "OFF",
        "unit_handling": "VERIFY", 
        "max_trade": "ON"
    }
    ```

    ### 6. 中性化参数错误

    #### 错误现象
    ```
    Invalid neutralization value
    Neutralization not supported for this region  
    ```

    #### 解决方案
    ```python
    # ❌ 错误：试图设置多个值
    {"neutralization": "COUNTRY+SECTOR"}

    # ✅ 正确：只能设置一个值  
    {"neutralization": "SECTOR"}

    # 地区推荐中性化
    region_neutralization = {
        "USA": "SECTOR",      # 或 INDUSTRY/SUBINDUSTRY
        "GLB": "COUNTRY",     # 或 SECTOR  
        "EUR": "COUNTRY",     # 或 SECTOR
        "ASI": "COUNTRY",      # 或去他
        "CHN": "SECTOR"       # 或 INDUSTRY
    }
    ```

    ### 7. 表达式语法错误

    #### 常见错误类型

    **未来数据泄露**:
    ```python
    # ❌ 错误：负数delay
    "rank(delay(close, -1))"

    # ✅ 正确：使用历史数据
    "rank(delay(close, 1))"
    ```

    **硬编码阈值**:
    ```python
    # ❌ 错误：绝对阈值
    "rank(close > 100.5 ? 1 : 0)"

    # ✅ 正确：相对阈值
    "rank(close > ts_mean(close, 20) ? 1 : 0)"
    ```

    ## 🛠️ 调试工具和技巧

    ### 渐进式调试法

    #### Step 1: 最小可行表达式
    ```python
    # 从最简单开始
    test_expressions = [
        "rank(close)",           # 最基础
        "rank(returns)",         # 加入收益率
        "rank(close/delay(close,1))"  # 加入时序操作
    ]
    ```

    #### Step 2: 逐步增加复杂度
    ```python
    # 确认基础版本work后再增加
    progressive_test = [
        "rank(close/delay(close,5))",                    # 基础动量
        "rank(winsorize(close/delay(close,5), 3))",      # 加入截尾
        "rank(zscore(winsorize(close/delay(close,5), 3)))"  # 加入标准化
    ]
    ```

    ### 参数敏感性测试

    #### 关键参数影响测试
    ```python
    # 测试decay的影响
    decay_test = [
        {"decay": 0, "truncation": 0.08},   # 基准
        {"decay": 2, "truncation": 0.08},   # 轻度平滑
        {"decay": 4, "truncation": 0.08},   # 中度平滑  
        {"decay": 8, "truncation": 0.08}    # 重度平滑
    ]

    # 测试truncation的影响
    truncation_test = [
        {"decay": 0, "truncation": 0.05},   # 低权重上限
        {"decay": 0, "truncation": 0.08},   # 中等权重上限
        {"decay": 0, "truncation": 0.12}    # 高权重上限
    ]
    ```

    ### 性能诊断

    #### 异常低性能诊断
    ```python
    # 性能异常低时检查清单
    performance_checklist = {
        "sharpe_low": {
            "possible_causes": [
                "信号太弱或噪音太多",
                "中性化过度消除了有效信号", 
                "参数设置不当",
                "数据质量问题"
            ],
            "solutions": [
                "尝试不同的neutralization",
                "调整decay和truncation参数",
                "检查数据覆盖率",
                "简化表达式逻辑"
            ]
        },
        "turnover_too_high": {
            "solutions": [
                "增加decay值(0→4→8)",
                "使用hump()或ts_decay_linear()平滑",
                "降低truncation阈值", 
                "增加信号稳定性"
            ]
        },
        "turnover_too_low": {
            "solutions": [
                "检查是否信号过度平滑",
                "减少decay值",
                "检查数据新鲜度",
                "确认表达式逻辑正确性"
            ]
        }
    }
    ```

    ### 常见错误快速查表

    | 错误关键词 | 可能原因 | 快速解决 |
    |-----------|---------|---------|
    | `does not support event/vector` | VECTOR字段直接rank | 加vec_avg() |
    | `Invalid parameter combination` | 地区/宇宙不匹配 | 用get_platform_setting_options检查 |
    | `400 Bad Request` | 参数错误 | 检查命名和类型 |
    | `Simulation failed` | ASI地区或表达式错误 | 加max_trade="ON"或简化表达式 |
    | `Authentication failed` | 认证问题 | 重新authenticate |
    | `Large number of NaN` | 数据覆盖率低 | 换高覆盖率字段 |
    | `Low turnover warning` | 信号过度平滑 | 减少decay或检查逻辑 |
    | `High correlation` | 策略相似度高 | 调整逻辑或换数据源 |

    ## 🎯 预防性最佳实践

    ### 开发前检查清单
    - [ ] 先运行get_platform_setting_options 
    - [ ] 从简单表达式开始测试
    - [ ] 使用标准化的参数模板
    - [ ] 准备2-8个表达式做对比

    ### 成功检查清单
    - [ ] Sharpe ≥ 1.0, Fitness ≥ 1.0
    - [ ] Turnover在0.01-0.7范围内
    - [ ] 相关性检查通过
    - [ ] get_submission_check全部PASS
    - [ ] Alpha描述完整，格式正确

    ### 长期维护建议
    - 定期检查策略性能衰减
    - 监控相关性漂移
    - 关注市场环境变化对策略的影响
    - 建立策略性能异常的预警机制

    ---

    **其他**: 
    - 使用MCP工具的官方错误信息作为诊断起点
    - 保持简单原则：复杂问题往往有简单原因
```

---

## 讨论与评论 (2)

### 评论 #1 (作者: LW67640, 时间: 6个月前)

感谢分享，很实用。

mcp逐渐复杂起来了，等精简下来的时候，就离不开mcp了。

=======================================================

AI时代，改变自己的工作习惯，适应新的生产力。

=======================================================

---

### 评论 #2 (作者: ZH12413, 时间: 6个月前)

快速诊断检查表到常见错误类型、解决方案，再到调试工具和最佳实践，覆盖得全面又细致。分类清晰，每个错误都配了具体现象、原因和可直接复制的代码示例，还整理了快速查表，遇到问题能快速定位解决。不管是新手还是有经验的顾问，都能避开很多坑，大幅提升开发效率。感谢这么用心的整理分享，这份指南值得收藏常备，后续开发时肯定能频繁用到～

---

