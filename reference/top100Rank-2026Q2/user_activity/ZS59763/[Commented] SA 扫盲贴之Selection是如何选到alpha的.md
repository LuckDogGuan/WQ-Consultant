# SA 扫盲贴之Selection是如何选到alpha的

- **链接**: [Commented] SA 扫盲贴之Selection是如何选到alpha的.md
- **作者**: QZ67721
- **发布时间/热度**: 1年前, 得票: 27

## 帖子正文

简单来说,Selection就是你通过你的表达式,从你个人(own)拥有的或者你顾问等级所能触达的所有active alpha做一个筛选, 选择你需要的alpha.

选择表达式通过根据 SuperAlpha 设置对所有 Alpha 进行排名，并选择排名最高的 Alpha 来组建SA。这里是关键.你必须要非常清楚你的Selection里面为什么出现的是这样的alpha,而非那样的alpha.同时,如果你的Selection设置限制很小,那么很有可能挑到的alpha非常同质化,因为他们的权重是一致的.尤其是你设置几十个alpha的limit,但是又有几千个alpha符合条件的时候.

具体权重如何确定?

其实这里把你的Selection表达式类比成alpha即可,同时,alpha里面的每一个股票就对应你的Selection里面的每一个alpha. 从我们普通组建alpha的角度来说,经过alpha运算以后,每一个股票都有一个alpha权重,这表示这个alpha占用你的多空投资额的比例.比如今天满足你alpha表达式的有100个股票, 50做多,50做空, 权重是-1到+1之间,两者算数相加和为0.代表多空投资总额相等.

而Selection里面的alpha也会经过Selection表达式的计算,获得这个alpha的权重,在选中的alpha数量大于你settings里面设置的alpha数量时,就按照权重从高到低取出你设置数量的alpha作为你最终选中的alpha.

举例如下: in(competitions, "HCAC2025")&&not(own) &&(self_correlation <= 0.5) *  (prod_correlation < 0.5) * (long_count + short_count) *(operator_count < 8)

可以看到上一行是选择的alpha的范围,主要是判断符组成,在设置Positive的情况下,不在范围内的alpha直接赋值为0,就无法选中了.后面*号开始计算权重.这里有个关键点需要注意.后续的部分权重条件,比如乘以(longcount+shortcount)-universe_size（universe）/2,或者作者活跃天数等,都会极大增加原先alpha的权重,使用的时候可能导致选到的因子几乎来自一个作者,这些权重的量级跟prod_corr差了几个量级.

---

## 讨论与评论 (1)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

感谢分享

学到了很多，对于sa都是比较迷茫的状态，这篇帖子教会了我很多

。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。

---

