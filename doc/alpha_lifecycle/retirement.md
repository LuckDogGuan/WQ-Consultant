# Alpha Retirement 因子退休规则

对于系统评估质量过低的因子（如触发致命缺陷、停牌或夏普比偏低），为了减少列表噪音，本系统整合了远程自动物理退休机制。

---

## C 级因子自动退休流程

当定级重估触发 C 级（包含原 C 级和合并后的原 D 级）时，会触发以下逻辑：
1. **远程平台物理退休**: 封装 WQ API，向云端服务器发送 DELETE 退休指令，从用户云端账户中物理下线该垃圾因子，隐藏其记录。
2. **本地标记与隐藏**: 在本地 SQLite 数据库中，将该因子的 `is_garbage` 属性更新为 `1`，使得它不再会进入 `/alphas` 主页面及被后续优化任务选为候选。

---

## 核心组件与代码映射

* **远程退休 WQ 调用包装**: `_run_retire` 通过 `retire_wq_alpha` 进行接口交互。
  * 源码位置: [background_inspector.py:L443](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/background_inspector.py#L443)
* **重估评级后的退休逻辑分支**: `_update_alpha_grade_and_status` 对重估评级为 C 等级的因子进行自动退休判定。
  * 源码位置: [background_inspector.py:L670](file:///d:/code/WorldQuant%20Brain/consultant/gui/app/services/background_inspector.py#L670)
