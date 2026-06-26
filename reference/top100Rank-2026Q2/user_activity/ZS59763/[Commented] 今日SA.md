# 今日SA

- **链接**: [Commented] 今日SA.md
- **作者**: QZ67721
- **发布时间/热度**: 1年前, 得票: 25

## 帖子正文

bool = (

not (own)

&&in(competitions,"HCAC2025")

&&(neutralization == 'FAST')

&&datacategory_count<=3

&& datafield_count <= 4

&&short_count+long_count> universe_size(universe)/2

&& (( self_correlation <0.2) || (self_correlation <0.4 ||self_correlation >0.2)||(self_correlation >0.45) )

# && author_fitness > 0.2

);

weight = (

1

*((long_count+ short_count)/ universe_size(universe))

*if_else(prod_correlation > 0.7, 2, 1.5)

*(1 - self_correlation)

*(1 / datafield_count)

);

bool * weight

combo：1

---

## 讨论与评论 (2)

### 评论 #1 (作者: ZS59763, 时间: 1年前)

很有用的select，感谢分享

但还是有个小问题，为什么会设置    *if_else(prod_correlation > 0.7, 2, 1.5)，按道理来说，prod越高的应该给越小的权重才对？

---

### 评论 #2 (作者: JX14975, 时间: 11个月前)

[ZS59763](/hc/zh-cn/profiles/26858512793111-ZS59763) 

prod_correlation>0.7在3月以前意味着力大砖飞，sharpe>110%原有因子，可能意味着对原有因子产生了非常好的改进。（但我个人建议单独拉出来看看margin，以防在改进sharpe的过程中牺牲margin）

---

