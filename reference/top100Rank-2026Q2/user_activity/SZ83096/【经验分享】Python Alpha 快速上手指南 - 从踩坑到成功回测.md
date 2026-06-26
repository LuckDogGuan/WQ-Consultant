# 【经验分享】Python Alpha 快速上手指南 - 从踩坑到成功回测

- **链接**: 【经验分享】Python Alpha 快速上手指南 - 从踩坑到成功回测.md
- **作者**: SZ83096
- **发布时间/热度**: 21天前, 得票: 21

## 帖子正文

## 背景

最近在学习 Python Alpha，通过阅读官方文档和论坛前辈的经验帖，成功完成了第一个 Python Alpha 的回测。本文整理了学习过程中的关键经验和踩过的坑，希望对后来者有帮助。

## 参考资料

感谢以下资料的作者：

- 官方文档： [Getting Started with Brain Python Alphas](https://platform.worldquantbrain.com/learn/documentation/consultant-information/getting-started-brain-python-alphas)
- [Python Alpha 平台限制粗略小结，请大佬指正](../RM49262/[Commented] Python Alpha 平台限制粗略小结请大佬指正.md)  - 非常详细的限制总结
- [经验分享-尝试Python alpha](/hc/en-us/community/posts/40737593669911)  - 包含完整的代码示例

## 核心限制（踩坑重点！）

### 1. 参数限制 - 最容易踩的坑

**unitHandling 和 nanHandling 必须省略！**  这是我踩的第一个大坑。

```
# ❌ 错误写法 - 会导致 400 错误
settings = {
    "unitHandling": "OFF",
    "nanHandling": "OFF",
    ...
}

# ✅ 正确写法 - 不要传这两个参数
settings = {
    "lookback": 110,
    "language": "PYTHON",
    ...
}
```

### 2. lookback 限制

- 必须 ≤ 115，超过直接 FAIL
- 建议用  **110** （115 偶发 FAIL）
- 与 FastExpr 无限历史窗口不同，Python 只能看到 lookback+1 行数据

### 3. 数据类型限制

- 支持：MATRIX 类型 ✅
- 不支持：VECTOR 类型 ❌（需要 vec_avg 聚合，Python 无法处理）
- 不支持：GROUP 类型 ❌
- int32 字段有 sentinel 值（-2147483648），需要手动替换为 NaN

### 4. 代码限制

```
# ✅ 允许
from brain.alphas import alpha
import numpy as np

# ❌ 不允许 - 服务器端不可用
from brain import Brain, BrainCache
from brain.models import SimulationSettings
```

其他要点：

- 数据数组 **只读** ，修改前必须  `.copy()`
- 返回必须是  **float32 ndarray** ，形状  `[n_instruments]`

## 完整的 Python Alpha 模板

```
from brain.alphas import alpha
import numpy as np
import numpy.typing as npt

def pasteurize(a, u):
    a = a.copy()
    a[~u.astype(bool)] = np.nan
    return a

def neutralize(a):
    a0 = np.nan_to_num(a, nan=0, posinf=0, neginf=0)
    return a - np.mean(a0)

def scale(a):
    a0 = np.nan_to_num(a, nan=0, posinf=0, neginf=0)
    norm = np.linalg.norm(a0, ord=1)
    return a / norm if norm > 0 else a

@alpha(data=["returns"], store=[])
def my_alpha(data, store) -> npt.NDArray[np.float32]:
    signal = -np.nanmean(data.returns, axis=0)
    signal = pasteurize(signal, data.universe[-1])
    signal = scale(neutralize(signal))
    return signal.astype(np.float32)
```

## 验证结果

使用上述模板成功完成回测：

- Alpha ID: d5Qp1GWv
- Sharpe: 0.63
- Turnover: 0.25

## 总结

Python Alpha 虽然有一些限制，但灵活性更高。关键要点：

1. **unitHandling 和 nanHandling 不要传**
2. **lookback ≤ 115**
3. **只 import alpha**
4. **数据只读，返回 float32**

希望这篇分享对大家有帮助！欢迎交流讨论。

---

## 讨论与评论 (1)

### 评论 #1 (作者: ZH41150, 时间: 11天前)

Python Alpha 上手帖里的 lookback / store 注意点和 Weijie 里 multisim 踩坑帖互相印证：Python 不能 multisim 数组提交，要 asyncio 单条并发；嵌套 ts 用 store 或中间序列，否则 lookback 拉很长仍超时。我本地 batch 已改成 partial CSV 续跑，和 Python 长回测的等待策略是配套的。

对刚转 Python 的同学，这篇值得和 Store 实战帖一起读。

---

