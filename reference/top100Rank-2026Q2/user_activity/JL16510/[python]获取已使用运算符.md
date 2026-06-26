# [python]获取已使用运算符

- **链接**: [python]获取已使用运算符.md
- **作者**: JL16510
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

论坛里已有获取个人可使用操作符的代码和获取个人已提交因子的代码，这里就不展示。假设都已保存在本地，格式csv，以下代码仅提供示例。

import pandas as pd
import re
#读取文件
dt_oper=pd.read_csv('xxx.csv')
dt_alpha=pd.read_csv('xxx.csv')
#分别把个人可使用操作符和个人已提交因子装入列表
oper_list=dt_oper.iloc[1:,1].tolist()
alpha_list=dt_alpha.iloc[1:,1].tolist()
#利用正则全局匹配
pattern = re.compile('|'.join(map(re.escape, oper_list)))
all_matched_regex = set()
for s in alpha_list:
    all_matched_regex.update(pattern.findall(s))

print(all_matched_regex)  
print(len(all_matched_regex))

---

## 讨论与评论 (1)

### 评论 #1 (作者: HQ17963, 时间: 1年前)

感谢分享，楼主是正则匹配大佬[手动狗头]

@ [WL27618](/hc/en-us/profiles/29059197295767-WL27618)  最近分享了一篇用ast解析操作符和字段的帖子，参见 [用python ast提取表达式中operator和datafield的方法 – WorldQuant BRAIN](../MS51256/[Commented] 用python ast提取表达式中operator和datafield的方法代码优化.md) ，这样可以不用手动维护dt_oper和dt_alpha了

---

