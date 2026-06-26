# 一键获取GLB ASI 11月RA提交数量，200积分轻松拿！

- **链接**: 一键获取GLB ASI 11月RA提交数量200积分轻松拿.md
- **作者**: JR23144
- **发布时间/热度**: 7个月前, 得票: 22

## 帖子正文

十月的Prod Corr大战硝烟未散，十一月的增补活动又悄然而至！这次官方特别为Combine在1.5以上的大佬们推出了专属福利，目标明确，奖励诱人。

你是否还在手动筛选，或者凭记忆估算自己提交了多少个GLB和ASI的Regular Alpha？为了不再“心中没底”，今天，我再带来一个“开箱即用”Python脚本，助你实时追踪活动进度，精准冲击200积分！

#### **活动规则速览**

在贴上代码之前，我们先重温一下这次的“夺分”要点：

- **面向用户** : 当前Combine Alpha Performance >= 1.5的顾问。
- **活动时间** : 11月1日至11月30日。
- **奖励规则** :
  1. **GLB区域** : 11月提交  **≥ 10个**  Regular Alpha，可获得  **100积分** 。
  2. **ASI区域** : 11月提交  **≥ 20个**  Regular Alpha，可获得  **100积分** 。
  3. 两项奖励可 **叠加** ，最多可获得 **200积分** ！

#### **制胜法宝：新一代“进度查询”脚本**

**核心功能升级：**

- **精准定位** : 专门统计带有Regular Alpha Tag的提交。
- **区域划分** : 可按GLB和ASI区域分别进行查询。
- **实时计数** : 告别手动，一键获取两个区域的已提交数量。

```
from machine_lib import *# 首先，登录你的BRAIN账户s = login()def get_submit_regular_alphas(s, start_date, end_date, region, alpha_num_to_check=500):    """    获取指定日期范围和区域内提交的Regular Alpha数量。    - alpha_num_to_check: 你预估的本月可能提交的总alpha数，可以设大一些以确保覆盖。    """    regular_alpha_num = 0    # 使用分页查询，每次拉取100个，直到检查完所有alpha    for i in range(0, alpha_num_to_check, 100):        # 构造查询URL        url = (f"https://api.worldquantbrain.com/users/self/alphas?limit=100&offset={i}"               f"&status!=UNSUBMITTED%1FIS_FAIL&dateSubmitted%3E={start_date}T00:00:00-04:00"               f"&dateSubmitted%3C={end_date}T23:59:59-05:00&settings.region={region}"               f"&order=-dateSubmitted&hidden=false&type!=SUPER")        try:            response = s.get(url)            response.raise_for_status()  # 如果请求失败则抛出异常            alpha_list = response.json().get('results', [])            # 如果当前页没有alpha了，说明已经拉取完毕            if not alpha_list:                break            for alpha in alpha_list:                # 检查classifications中是否包含Regular Alpha标签                classifications = alpha.get('classifications', [])                for c in classifications:                    if c.get('id') == 'REGULAR:REGULAR':                        regular_alpha_num += 1                        break  # 找到后就不用再检查这个alpha的其他标签了        except Exception as e:            print(f"查询{region}区域时发生异常: {e}")            # 可以在这里增加重试逻辑或直接返回            return f"查询出错"    return regular_alpha_num# --- 主程序运行 ---# 设置查询日期为11月start_date = "2025-11-01"  end_date = "2025-11-30"  # 分别查询GLB和ASI区域的数量glb_alpha_num = get_submit_regular_alphas(s, start_date, end_date, "GLB")asi_alpha_num = get_submit_regular_alphas(s, start_date, end_date, "ASI")# 打印结果print(f"11月活动进度追踪：")print(f"  - GLB区域已提交Regular Alpha数量: {glb_alpha_num} (目标: 10)")print(f"  - ASI区域已提交Regular Alpha数量: {asi_alpha_num} (目标: 20)")
```

运行结果如图所示：

![图片](images/img_e3d8f631c8.png)

（注：这是我本人的当前进度，一目了然！GLB区域还差3个，ASI区域则需要继续努力。）

有了这个工具，我们就能精准规划自己的提交策略，不再盲目“刷量”。

希望这个升级版的小工具能帮助到每一位正在为11月积分奋斗的顾问。特别感谢wordquant 的这些活动，能让我赚到积分换取周边！

祝大家11月积分满满，年底再冲一波高峰！

---

## 讨论与评论 (1)

### 评论 #1 (作者: YH25030, 时间: 6个月前)

程序相当简洁，学到了！多谢

---

