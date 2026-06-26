# 【重复回测&哈希】大家是如何做好避免重复回测的？哈希是否是一个好的方案

- **链接**: [Commented] 【重复回测哈希】大家是如何做好避免重复回测的哈希是否是一个好的方案.md
- **作者**: ZT38415
- **发布时间/热度**: 7个月前, 得票: 3

## 帖子正文

## 问题

在回测过程中，有时候会出现重复回测的情况，这个在之前传统的一二三阶回测方案中，采用了记录断点后，进行断点续跑的方案。但是随着我当前构建的回测系统逐渐复杂，尤其是开始利用冷神的模板群方案后，对于避免重复回测成了一个难题。我当前是构建了一个较为复杂的json

```
{    "塔名": {        "pyramid_info": {            "pyramid_status": "light" | "completed_high_quality" | "completed_all_processed" | "in_progress",            "total_high_quality_signals": 0,            "created_time": "2025-10-03T...",            "last_updated": "2025-10-03T..."        },        "datasets": {            "数据集ID": {                "dataset_info": {                    "dataset_status": "completed" | "no_signal" | "interrupted",                    "current_expression_idx": 0,                    "total_expressions": 0,                    "high_quality_count": 0,                    "yellow_count": 0,                    "created_time": "2025-10-03T...",                    "last_updated": "2025-10-03T..."                },                "templates": {                    "T类型_索引": {                        "template_status": "completed" | "in_progress",                        "current_alpha_idx": 0,                        "high_quality_count": 0,                        "yellow_count": 0,                        "total_alpha_number": 0                    }                }            }        }    }}
```

但是后续我应该会逐渐修改我的回测系统，每次都要做好对之前系统回测记录的兼容，导致代码预发复杂，并且很可能导致记录出错，漏掉一些回测或者重复一些回测。

## 思路

我当前还没有用数据库，现在新的思路是每次的回测数据都提前记录为hash值

```
def generate_task_hash(sim_data):    """    计算 sim_data 的 SHA256 哈希值作为唯一任务 ID (task_id)。    对字典进行规范化排序(sort_keys=True)以确保相同内容的字典得到相同的哈希。    """    # 规范化 JSON 字符串    normalized_json = json.dumps(sim_data, sort_keys=True)    # 计算哈希    return hashlib.sha256(normalized_json.encode('utf-8')).hexdigest()
```

为了节约空间，只在文件中保持哈希数据，并且按照字典序排序。后面回测前，都先计算回测数据的哈希值，并且利用二分（复杂度logN，速度应该还是很快的）进行检索，如果不存在才进行回测，不知这样是否可行。对于可能在利用数据库的大家，是直接把所有回测数据都存在数据库中进行检索避免重复回测吗？我在想这样是不是会占用太大内存？以及大家是否有更好的方案呢

---

## 讨论与评论 (2)

### 评论 #1 (作者: RM49262, 时间: 5个月前)

=====================================评论区=========================================

+1  我目前也是靠哈希来查重 避免重复回测的

之前问AI AI推荐的这个方案，不知道还有没有更好的方案哈哈

===================================================================================

---

### 评论 #2 (作者: ZH87224, 时间: 5个月前)

最简单的方案就是哈希，目前哈希的问题是可能会存在不同的 expr 表示相同的含义，所以语法树+哈希应该是最优解，不过如果本地控制好表达式生成规范，也不需要加语法树解析，我目前是基于以下字段做的哈希：

class Simulation(LocalModel, AlphaSettingsMixin, AlphaMarkingMixin):

__hashkey__ = [

"simulation_type",

"expr",

"combo",

"selection",

"instrument",

"region",

"universe",

"decay",

"delay",

"neutralization",

"truncation",

"pasteurization",

"unit_handling",

"max_trade",

"language",

"nan_handling",

"visualization",

]

应用的时候只需要：

for sim in sim_all:

simhash = sim.hashing()

sim_get = await Simulation.get_or_none(hashcode=simhash)

if sim_get is None:

sim_new.append(sim)

else:

sim_cache.append(sim_get)

就可以只回测新的Simulation

---

