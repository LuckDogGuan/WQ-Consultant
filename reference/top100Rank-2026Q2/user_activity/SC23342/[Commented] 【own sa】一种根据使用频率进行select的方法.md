# 【own sa】一种根据使用频率进行select的方法

- **链接**: [Commented] 【own sa】一种根据使用频率进行select的方法.md
- **作者**: DQ66419
- **发布时间/热度**: 9个月前, 得票: 57

## 帖子正文

以下近2个月自用的一套own sa的select方法，目的是在保证sharpe和fitness>5的基础上，方便做出更多的own sa，甚至pc0.5以下的因子。

大家如果有瓶颈，不妨尝试下。如有雷同，纯属巧合。

先看下2个月的基本情况，我基本上是隔天做一个own sa。根据柱子的长短，可以看出部分own sa是满足35要求的。
 ![图片](images/img_b06617fc9e.png) 
下面是select的方法：
1、准备工作：把自己交过的RA\PPA筛选一遍，保留自己认为质量较好的且self corr在0.5以下的因子（这里并不关心prod_corr），进行favorite打标。这一步是保证sa的质量及低相似度的基础。
2、选择本次需要select的RA进行GREEN标记，具体代码在最下面。大致逻辑是，本次需要select的ra(比如30个)，被使用过的次数要尽可能的低，并且至少要有一部分因子(比如10个)是跟之前own sa不一样的。
3、固定使用这个selection expression来跑。limit数量根据第2个步自己想选择的数量设置。

```
own&&favorite&&color=="GREEN"
```

4、risk neut比较容易低corr，所以我一般只遍历这几个risk neut。
5、combo我没有什么特别的，都是之前游戏王等大佬们分享的技巧。
6、回测并check prod corr。如果本身自己的ra质量不高，可以考虑多select几个。

以下是select并打GREEN标识的代码，本人代码基础不好，仅供参考：

```
import asynciofrom collections import Counterfrom wqb import printimport src.common.common as commonregion = 'EUR'select_count = 35    #sa需要的ra个数diff_count = 10  #与已提交过的sa不重复的ra个数'''查询已提交过的own sa所select的ra'''wqbs = common.login(f'{common.get_file_name(__file__)}')submitted_alphas = wqbs.filter_alphas(    others=['status!=UNSUBMITTED%1FIS-FAIL'],    order='-dateSubmitted',    type='SUPER',    region=region,)saList = []for resp in submitted_alphas:    saList.extend(resp.json()['results'])selectedRaList = []for sa in saList:    if 'not(own)' in sa['selection']['code']:        continue    raList = asyncio.run(common.list_ra_of_sa(wqbs, sa['id']))    selectedRaList.append([ra['id'] for ra in raList])'''取出所有favorite的ra'''regular_alphas = wqbs.filter_alphas(    others=['status!=UNSUBMITTED%1FIS-FAIL'],    order='-dateSubmitted',    type='REGULAR',    favorite='true',    region=region,)favoriteRaList = []for resp in regular_alphas:    favoriteRaList.extend(ra['id'] for ra in resp.json()['results'])'''选择ra'''# 统计 selectedRaList 中每个id的出现频率all_id_in_selectedRaList = [id for row in selectedRaList for id in row]frequency = Counter(all_id_in_selectedRaList)# 对favoriteRaList 按频率升序排序（出现次数少的优先）sorted_favoriteRaList = sorted(favoriteRaList, key=lambda x: frequency.get(x, 0))selected = []  # 最终选中的for id in sorted_favoriteRaList:    if len(selected) >= select_count:        break    trial_selected = selected + [id]    valid = True    for row in selectedRaList:        row_set = set(row)        trial_set = set(trial_selected)        intersection_size = len(row_set & trial_set)        max_allowed_intersection = len(row) - diff_count        if max_allowed_intersection < 0:            continue        if intersection_size > max_allowed_intersection:            valid = False            break    if valid:        selected.append(id)    if len(selected) == select_count:        breakif len(selected) < select_count:    print(f"警告：只选出了 {len(selected)} 个，未能达到 {select_count} 个。")else:    print(selected)    '''颜色标记'''    for ra in favoriteRaList:        wqbs.patch_properties(alpha_id=ra, color='BLUE')    for ra in selected:        wqbs.patch_properties(alpha_id=ra, color='GREEN')
```

```
async def list_ra_of_sa(self, alpha_id):    resp = await self.retry(        'GET', wqb_urls.URL_ALPHAS + f'/{alpha_id}/alphas?limit=100&offset=0&status=ACTIVE%1DECOMMISSIONED', max_tries=600    )    return resp.json()['results']
```

---

## 讨论与评论 (26)

### 评论 #1 (作者: AL13375, 时间: 9个月前)

很棒！

感谢大佬的分享！

原来还能用这种方法进行组自己的alpha，大开眼界了！

从逻辑上来说，很合理，而且从大佬的base也能看出来，这样做出来的sa确实拿到了不错的base！

期待大佬更多的分享！

==========路漫漫其修远兮，吾将上下而求索==========

---

### 评论 #2 (作者: MY49971, 时间: 9个月前)

大佬好厉害啊，own 的35还能出这么多，学习学习~~

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #3 (作者: SJ65808, 时间: 9个月前)

跟大佬学习如何组own的35~~~

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #4 (作者: DA98440, 时间: 9个月前)

感谢分享，好方法，通过打tag的方式可以实现自己去select到自己想要的alpha，灵活度和自主性更高了。

---

### 评论 #5 (作者: QP72475, 时间: 9个月前)

谢谢分享，SA又有新的学习方向了。

---

### 评论 #6 (作者: YH25030, 时间: 9个月前)

仔细阅读了帖子，对我来说One point take way就是“ **self corr在0.5以下的因子进行favorite打标** ”。这个我还没有尝试过。到现在为止，我都是截取turnover和遍历中心化，所以找不到好的own SA。感谢你的分享。

---

### 评论 #7 (作者: MS51256, 时间: 9个月前)

感谢大佬的分享，手动挑选一部分打标签颜色或者喜好都是较为好的一个做sa的方法，但是就是存在耗时较长的情况，如果可以开发一个自动化选取一部分没选取过的因子来自动打标签应该是个非常好的想法。

========================================================================================================================================================================

---

### 评论 #8 (作者: BL72197, 时间: 9个月前)

太好了 之前都在尝试组sa都是sc和pc不过关，现在可以根据大佬的方法来组，感谢大佬分享！

---

### 评论 #9 (作者: GY71341, 时间: 9个月前)

感谢大佬的分享，目前只用来颜色来筛选，确实感觉有点不够用，做出own的三五感觉好难，这就去打tag，试试效果

==================================================================================================================早日当上master==========================================

---

### 评论 #10 (作者: SC23342, 时间: 9个月前)

前段时间经过其他大佬的点拨，也构思过类似的方法，但是不清楚代码上要如何实现这个想法。现在就可以马上投入实践啦，大佬这篇帖子可谓是雪中送炭及时雨啊！

=================================赛博炼丹，其乐无穷====================================

---

### 评论 #11 (作者: AH18340, 时间: 9个月前)

感谢大佬分享，原来还能这样组own的sa,给alpha打上color再选，这就去试试。

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #12 (作者: JX14975, 时间: 9个月前)

感谢大佬，10月份要来了，现在许多gold都能够升到expert，这篇文章对我们来说真是及时雨。

========================================================================================================================================================================

---

### 评论 #13 (作者: AM12075, 时间: 9个月前)

这套方法的逻辑清晰，核心思想是通过 favorite 打标保证因子质量，再结合使用频率和差异度控制，降低 self corr 与重复度，从而在 Sharpe 和 Fitness 约束下更容易构建出低 pc 的 own sa。代码实现思路也比较实用：先统计历史 sa 已用过的 RA，再优先选择出现次数少的 favorite RA，并用 diff_count 来保证一定的新鲜度，避免过度重叠。整体设计兼顾稳定性和多样性，能有效突破瓶颈。

不过个人认为这种方法对 favorite 的依赖较大，如果初期筛选不够严格，后续结果可能受限，另外 diff_count 参数的设定也需要不断调试。

---

### 评论 #14 (作者: DT40395, 时间: 9个月前)

哇，感谢大佬分享，这个思路倒是很清晰，不过很依赖自身之前提交的RA和PPA因子质量。我也来试试看，看看自己的因子搓出来的SA如何! 也祝大佬VF0.9+和GM

---

### 评论 #15 (作者: JB53978, 时间: 9个月前)

很好的想法啊，之前看sa的贴子都没有这个，你的这个心仪的想法不错，我vf高了也要去实践一下看看效果咋样，非常感谢你的分享！！！！！！！！！！！
========================================================================================================================================================================

---

### 评论 #16 (作者: ST61360, 时间: 8个月前)

感谢分享，对于创建super Alpha正处于无想法的状态，看到楼主分享的方法，思路豁然开朗，这个selection方法很新奇。今天实践了一下，时隔多天之后，又交了一个super alpha。

---

### 评论 #17 (作者: RM49262, 时间: 8个月前)

=====================================评论区=======================================

感谢大佬分享，虽然我目前交的alpha数量不多还不太能产出SA，但技巧先码住了哈哈，希望到时候也能拿到大佬这种base

=================================================================================

---

### 评论 #18 (作者: YP44571, 时间: 8个月前)

非常好的分享！想想也是，选别人的alpha是没办法掌握太多，只好用公式去筛选，而自己的alpha能一手掌握，利用自己的修改权利做出有利于自己的选择这个逻辑太棒了！

---

### 评论 #19 (作者: SZ20589, 时间: 8个月前)

这个方法主要是靠标记  **favorite**  来保证因子质量，再用使用频率和差异度来控制重复，降低自相关，让在 Sharpe 和 Fitness 限制下构建低 PC 的自有 SA 更容易。实现上就是先看历史用过的 RA，再优先选出现少的 favorite，同时用  **diff_count**  保持新鲜感。整体设计兼顾稳定和多样，不过对 favorite 依赖比较大，diff_count 也需要反复调, 很依赖自身之前提交的RA和PPA因子质量。

=============================================================================

=============================== HOPE HIGH VF ==================================

=============================================================================

---

### 评论 #20 (作者: HC14446, 时间: 8个月前)

===================================持续学习========================================

先筛选质量好、自相关 0.5 以下的 RA/PPA 打 favorite 标保证基础质量，再优先选使用频率低的，还特意留 10 个和之前不一样的避免重复，三五的机会大大提升。

==================================================================================

感谢大佬分享这套 own SA 的 select 方法，之前一直卡在瓶颈期，看了这个思路确实清晰多了。我这就整理自己的 RA/PPA 试着操作，也希望大佬之后能出更多优质 SA，VF 一直涨。

---

### 评论 #21 (作者: PY32536, 时间: 8个月前)

很棒！

感谢大佬的分享！

原来还能用这种方法进行组自己的alpha，大开眼界了！

从逻辑上来说，很合理，而且从大佬的base也能看出来，这样做出来的sa确实拿到了不错的base！

期待大佬更多的分享！

==========路漫漫其修远兮，吾将上下而求索==========

---

### 评论 #22 (作者: XY20037, 时间: 7个月前)

感谢大佬的分享，学习到了自己组sa的方法，通过自己筛选好的ra然后通过代码选择SP小的，使用频率小的优先。从大佬的base可以看出这样做出来的sa确实拿到了不错的base，向大佬学习

---

### 评论 #23 (作者: YZ54944, 时间: 7个月前)

太赞了！！最近的SA有着落了，感谢大佬的分享

---

### 评论 #24 (作者: JX28185, 时间: 7个月前)

感谢，记录一下自己的学习笔记

**工作流步骤**：

1.  **准备工作：建立优质Alpha池**

*   首先，筛选出自己所有已提交的、质量较好且自身相关性较低（如 `self_corr < 0.5`）的常规alpha。

*   通过API或UI，将这些alpha统一标记为`favorite`。这个收藏夹将作为后续所有`own sa`的候选池。

2.  **程序化筛选与标记**

*   运行一个Python脚本，执行以下自动化操作：

*   **a. 获取历史数据**：获取所有已提交的`own sa`，并遍历它们，提取出每一个`own sa`所包含的常规alpha ID列表。

*   **b. 统计使用频率**：统计在所有历史`own sa`中，每一个常规alpha（来自你的`favorite`池）被使用了多少次。

*   **c. 排序与选择**：根据“使用频率”对`favorite`池中的alpha进行**升序**排序（使用次数越少，排名越靠前）。

*   **d. 迭代构建新组合**：从排序后的列表中，逐一选择alpha来构建一个新的组合。同时，确保这个新组合满足“新颖度”要求（例如，与任何一个历史`own sa`相比，至少有`diff_count = 10`个不同的alpha）。

*   **e. API颜色标记**：将上一步最终选出的alpha组合，通过API调用，统一标记为`GREEN`。同时，可以将池中其他alpha标记为`BLUE`以作区分。

3.  **运行Super Alpha模拟**

*   在模拟页面，使用一个极其简洁的`SELECTION`表达式：

```

own && favorite && color == "GREEN"

```

*   这个表达式的含义是：选择“我自己的、被我标记为`favorite`的、且在本轮程序化筛选中被标记为`GREEN`的”alpha。

*   `Selection Limit`的值应设为你在脚本中期望选出的alpha数量（如 `select_count = 35`）。

---

### 评论 #25 (作者: HJ88260, 时间: 6个月前)

楼主分享的Own SA selection方法确实很实用！不过有几个疑问想请教下：

1. 这个方法对历史RA质量要求很高，如果自己之前提交的RA质量参差不齐，会不会影响最终效果？有没有什么补救措施？
2. 代码里用Counter统计使用频率，但实际运行时会不会因为RA数量多导致处理速度变慢？有没有更高效的方式？
3. diff_count参数设置10是经验值，如果想进一步降低PC到0.5以下，这个值需要怎么调整？
4. 除了打favorite标签，有没有其他筛选RA质量的技巧？比如看回测的夏普比率还是换手率？
5. 最后颜色标记部分，如果同时做多个SA，会不会出现标签冲突？需要手动复核吗？

之前看到有大佬提到"游戏王"的combo技巧，和这套方法结合的话，会不会更容易出高质量SA？期待楼主后续分享更多实战案例！

---

### 评论 #26 (作者: JX14975, 时间: 6个月前)

[HJ88260](/hc/zh-cn/profiles/30760371939095-HJ88260)

1，这不是要你设置favorate来确定哪些ra参与组sa吗？不过有一说一，不推荐这么筛选，毕竟之前出现过精准地选出表现不好的那部分ra来组sa的情况，还比较普遍。

2，不会啊，建议复习线程的概念

4，这个在游戏王的select贴子都讲烂了。

6，combo技巧建议右上角搜索 combo，绝对不少。

---

