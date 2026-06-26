# SA实例分析

- **链接**: [Commented] SA实例分析.md
- **作者**: QZ67721
- **发布时间/热度**: 1年前, 得票: 25

## 帖子正文

Selection：

bool = (

not (own) &&

in(competitions,"HCAC2025")&&

(neutralization=='CROWDING')&&

datacategory_count<=3 &&

short_count+long_count > 2000 &&

(( prod_correlation >0.4) || (prod_correlation <0.35 ||prod_correlation >0.25)||(prod_correlation <0.2) )

);

weight = (

1

*((long_count+ short_count)/ universe_size(universe))

*if_else(prod_correlation > 0.7, 2, 1.5)

*(1 - self_correlation)

);

bool * weight

Combo：

combo_a(alpha, nlength = 250, mode = 'algo1')

今天SA prod corr 0.6，租了50个USA的alpha，感觉如果一直都有全部alpha权限的话，我可以天天组。

---

## 讨论与评论 (1)

### 评论 #1 (作者: YH25030, 时间: 1年前)

谢谢分享您宝贵的经验。想请教您一下，您选的limit是多少是1000吗？

---

