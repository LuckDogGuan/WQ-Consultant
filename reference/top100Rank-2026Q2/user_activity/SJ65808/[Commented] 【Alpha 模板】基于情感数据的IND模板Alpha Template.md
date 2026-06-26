# 【Alpha 模板】基于情感数据的IND模板Alpha Template

- **链接**: [Commented] 【Alpha 模板】基于情感数据的IND模板Alpha Template.md
- **作者**: LZ29996
- **发布时间/热度**: 6个月前, 得票: 26

## 帖子正文

S1=ts_mean(ts_backfill({sentiment},250),22);# 月平均情感分数

R1=ts_product(1+returns,22); # 月度收益率，本来应该是ts_product(1+returns,22)-1，没有-1不影响结果。

alpha=ts_quantile(S1-R1,5,driver=’cauchy’);# 归一化并加重极端值的权重，使用gaussian也可以。

// alpha idea:做多情感分数相对于收益高的股票，反之亦是。

// 初始setting:Region=IND,Universe=TOP500,Decay=10,Delay=1,Truncation=0.01,Neu=Industry,

// Pasteurization=On,NaN Handing=Off

// 迭代:{sentiment}使用与sentiment相关的datafiled。

和sentiment相关的datafiled可以通过以下代码获得：

def get_datafields(s,searchScope,dataset_id:str='',search:str=''):

instrument_type=searchScope['instrumentType']

region=searchScope['region']

delay=searchScope['delay']

universe=searchScope['universe']

if len(search)==0:

url_template=" [https://api.worldquantbrain.com/data-fields?"+\](https://api.worldquantbrain.com/data-fields?%22+\)

f"&instrumentType={instrument_type}"+\

f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50"+\

"&offset={x}"

count=s.get(url_template.format(x=0)).json()['count'] #.json()将response 转为字典

else:

url_template=" [https://api.worldquantbrain.com/data-fields?"+\](https://api.worldquantbrain.com/data-fields?%22+\)

f"&instrumentType={instrument_type}"+\

f"&region={region}&delay={str(delay)}&universe={universe}&search={search}&limit=50"+\

"&offset={x}"

count=s.get(url_template.format(x=0)).json()['count']

datafields_list=[]

for x in range(0,count,50):

while True:

try:

datafields=s.get(url_template.format(x=x))

datafields_list.append(datafields.json()['results'])

break

except:

time.sleep(1)

datafields_list_flat=[item for sublist in datafields_list for item in sublist]

datafields_df=pd.DataFrame(datafields_list_flat)

return datafields_df

dataFields=get_datafields(s=sess,searchScope=searchScope,search=’sentiment’)

目前我只使用了非RISK neutralization的setting，自从IND有RISK之后，或许还有其他alpha可以提交。不过该模板一般需要两个datasets，听论坛的大神说这是在混信号。所以，大家可以在新手阶段，断粮，或者点塔的时候使用。以下是一些模板的结果。

![图片](images/img_48e5f9f4a5.png)  ![图片](images/img_7ce17129ae.png)

![图片](images/img_c08f676a43.png)

![图片](images/img_fbd19f2862.png)

---

## 讨论与评论 (17)

### 评论 #1 (作者: PZ64174, 时间: 6个月前)

感谢大佬分享！是我很需要的IND模板了！自己用ai做出来的模板总是差一点意思，robust test fail从0.5-0.8都有，有了这篇贴子让ai学习下，应该可以完善一下流程！

====================================================================

一年一个台阶，一步一个脚印

====================================================================

---

### 评论 #2 (作者: SJ65808, 时间: 6个月前)

两个不同量纲的指标相减确实有混信号的嫌疑，指标看着都挺不错的，不知道开了maxtrade之后咋样

====================================================================================
==================纸上得来终觉浅，绝知此事要躬行======================================

---

### 评论 #3 (作者: FX25214, 时间: 6个月前)

能不能详细解释一下这个R1是怎么选出来的呢？

---

### 评论 #4 (作者: LK12887, 时间: 6个月前)

IND开通ppa了吗

---

### 评论 #5 (作者: MY82844, 时间: 6个月前)

个人感觉S1-R1这步是核心，原始信号减去市场price in的部分，非常合理的想法，赞

严格来说，类似回归，可能需要拟合一个参数 S1-k*R1，否则可能和R1部分的mean reversion有些相关性

---

### 评论 #6 (作者: YZ29225, 时间: 6个月前)

respect

---

### 评论 #7 (作者: MZ35432, 时间: 6个月前)

学习了，但经济学意义是什么呢？能解释下不

---

### 评论 #8 (作者: LZ29996, 时间: 6个月前)

具体经济学意义可以看一下这篇文章：Tomorrow’s Fish and Chip Paper? Slowly incorporated  News and the Cross-section of Stock Returns。还有IND目前还未开通PPA（我之前的帖子写错了），目前我已修改帖子内容。

---

### 评论 #9 (作者: JX14975, 时间: 6个月前)

能否展示一下该模板在sentiment这个datacategory的应用，毕竟标题叫基于情感数据的模板？看举例都是analyst，请问是作者只跑了analyst这个数据类别吗？

---

### 评论 #10 (作者: MY49971, 时间: 6个月前)

看截图都是analyst数据，和sentiment数据集好像没啥关系

===================================================================================
===================Talk is cheap,show me the alpha=================================

---

### 评论 #11 (作者: HL86751, 时间: 6个月前)

感谢大佬的模板，很急需

=======================================

句有可削，足见其疏；字不得减，乃知其密。

=======================================

---

### 评论 #12 (作者: XG98059, 时间: 6个月前)

确实属于混信号。

---

### 评论 #13 (作者: AH18340, 时间: 6个月前)

学到了，感谢大佬分享

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #14 (作者: MZ45384, 时间: 6个月前)

模板捕捉：

S1=ts_mean(ts_backfill({sentiment},<d1/>),<d2/>);

R1=ts_product(1+returns,22);

alpha=ts_quantile(S1-R1,<d3/>,driver=’cauchy’)

不过sentiment数据大多都是日更吧，回填天数250是不是太长了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值
======================================================================================

---

### 评论 #15 (作者: CW62372, 时间: 5个月前)

======================================================================================

S1=ts_mean(ts_backfill({sentiment},<d1/>),<d2/>);

R1=ts_product(1+returns,22);

alpha=ts_quantile(S1-R1,<d3/>,driver=’cauchy’)

如果把ts_backfill去掉能行不？我试一试

======================================================================================

---

### 评论 #16 (作者: XW23690, 时间: 5个月前)

学习到了。模板似乎也是一个量价的模板，我看最后几个alpha的margin不是特别高。量纲不一致直接相减感觉会混信号，R1=ts_product(1+returns,22); # 月度收益率，这一步作为if_else条件是否也可以筛选掉这部分影响？

---------------------------------------------------------------------------
α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑
Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMax
Win>Loss|Risk<Reward InSample→OutOfSample
---------------------------------------------------------------------------

---

### 评论 #17 (作者: WA25180, 时间: 3个月前)

学习了

---

