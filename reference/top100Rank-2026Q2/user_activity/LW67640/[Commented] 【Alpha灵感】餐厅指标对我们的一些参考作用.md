# 【Alpha灵感】餐厅指标对我们的一些参考作用

- **链接**: [Commented] 【Alpha灵感】餐厅指标对我们的一些参考作用.md
- **作者**: ML42552
- **发布时间/热度**: 1年前, 得票: 1

## 帖子正文

文章链接： [[2501.03862] Rendezfood: A Design Case Study of a Conversational Location-based Approach in Restaurants](https://arxiv.org/abs/2501.03862)

# Rendezfood: A Design Case Study of a Conversational Location-based Approach in Restaurants

# 假设我们有以下“餐厅指标”作为输入（这些在真实的WorldQuant环境中需要被替换为金融数据）：
# restaurant_rating: 餐厅评分（可以视为某种“价格”指标）
# customer_flow: 顾客流量（可以视为“交易量”指标）
# menu_price_change: 菜品价格变化率（可以视为某种“动量”指标）

# 注意：以下表达式是概念性的，并不是真正的WorldQuant代码。

# 步骤1: 定义基础变量
# 这些变量将代表我们的“餐厅指标”，并需要在每个时间点进行更新。

# 步骤2: 计算策略信号
# 我们可以构建一个策略信号，该信号基于餐厅评分的变化、顾客流量的增加或减少，以及菜品价格的变化率。
# 例如，一个可能的策略是：当餐厅评分上升且顾客流量增加时，我们认为这是一个积极的信号；而当菜品价格急剧上涨时，我们可能认为这是一个消极的信号。

![图片](images/img_75a0c6feca.png)

模板：

A=ts_corr(close, volume, 20) > 0.5;

B=group_backfill(winsorize(ts_backfill({data},5),std=4),market,22, std=4.0);

trade_when(A, B, -1)

![图片](images/img_5ac3eebd82.png)

![图片](images/img_24f0d20f40.png)

GLB 的表现

![图片](images/img_5f58b8d4cd.png)

![图片](images/img_d33d7721b6.png)

读论文系列目前对自己来说还是有点难度，最大的难点在找到有效的论文，其次是对自己operators 的熟悉程度，这几天刚把自己所有的operators借助大语言模型学习了一番，想要创造自己的模板还是任重而道远呀

---

## 讨论与评论 (1)

### 评论 #1 (作者: LW67640, 时间: 1年前)

为什么要使用group_backfill呢？

---

