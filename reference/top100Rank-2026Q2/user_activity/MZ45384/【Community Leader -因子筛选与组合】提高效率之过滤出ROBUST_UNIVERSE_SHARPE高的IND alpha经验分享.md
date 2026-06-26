# 【Community Leader -因子筛选与组合】提高效率之过滤出ROBUST_UNIVERSE_SHARPE高的IND alpha经验分享

- **链接**: 【Community Leader -因子筛选与组合】提高效率之过滤出ROBUST_UNIVERSE_SHARPE高的IND alpha经验分享.md
- **作者**: MZ45384
- **发布时间/热度**: 6个月前, 得票: 34

## 帖子正文

这个月开启了IND区域alpha探索之旅，由于IND只能交Regular Alpha，且大多时候会因为ROBUST_UNIVERSE_SHARPE不达标而卡住，因此不得不优化，如果我们选择该指标高于一定阈值的alpha，就能大大提高优化难度和出货效率。于是我写了一个函数，可以帮助筛选过滤符合一定要求的alpha。def wait_get(sess, url: str, max_retries: int = 10) -> "Response":retries = 0while retries < max_retries:while True:simulation_progress = sess.get(url)if simulation_progress.headers.get("Retry-After", 0) == 0:breaktime.sleep(float(simulation_progress.headers["Retry-After"]))if simulation_progress.status_code < 400:breakelse:time.sleep(2 ** retries)retries += 1return simulation_progressdef ind_probe(s, alpha_list, cutoff):# s即session# alpha_list是上一步过滤出来的alpha_id列表# cutoff是选择过滤的阈值，建议初始选择0.8，可以上下调整may_list = []for alpha_id in tqdm(alpha_list, total=len(alpha_list), desc='Checking ROBUST_UNIVERSE_SHARPE', colour='#00ff00'):metrics = wait_get(s, f'https://api.worldquantbrain.com/alphas/{alpha_id}').json()for i in metrics['is']['checks']:if i['name'] == 'LOW_ROBUST_UNIVERSE_SHARPE':if i['value'] > cutoff:may_list.append([alpha_id, i['value']])breakdf = pd.DataFrame(may_list, columns=['alpha_id', 'ROBUST_UNIVERSE_SHARPE']).set_index('alpha_id')may_df = df.sort_values('ROBUST_UNIVERSE_SHARPE', ascending=False)return may_df最后返回的是一个按ROBUST_UNIVERSE_SHARPE倒序的dataframe:一轮搜索过滤下来选择第一个最高的，通常只有weight concentration的问题，优化难度肉眼可见地减小。在经过几天的空档期后，终于有alpha交了。

---

## 讨论与评论 (8)

### 评论 #1 (作者: JX28185, 时间: 6个月前)

这个是搭配AI优化的利器啊

---

### 评论 #2 (作者: LJ85703, 时间: 6个月前)

好好看，好好学

---

### 评论 #3 (作者: FF65210, 时间: 6个月前)

你好大佬，请问这个东西是怎么用的呢，有没有完整版代码，我最近也在做IND地区的，

---

### 评论 #4 (作者: YQ84572, 时间: 6个月前)

好用的工具，ind最近一直没有思路，感谢大佬的分享====================================================================================祝大佬base多多，vf0.9+====================================================================================

---

### 评论 #5 (作者: MZ45384, 时间: 6个月前)

FF65210用上一步过滤出的alpha_id（比如get_alphas)用该方法做下一步筛选即可。======================================================================================知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%# sys.setrecursionlimit(α∞)# PnL = ∑(Robustness * Creativity)#无限探索、鲁棒性优先，创新性增值 Where there is a will, there is a way.======================================================================================

---

### 评论 #6 (作者: WX84677, 时间: 6个月前)

很棒的方法，感谢分享。最近也是在跟 IND 地区死磕，结合大佬给出的工具，找待优化种子 alpha 的效率大大提升了~=========================== 积跬步，至千里 ============================

---

### 评论 #7 (作者: ZF97721, 时间: 6个月前)

看起来代码是用来筛选出来ROBUST_UNIVERSE_SHARPE差距相对比较小的那些失败因子，再去调整和优化，可能因为差距小的话好调整一些。不知道大佬具体优化ROBUST_UNIVERSE_SHARPE的方法有哪些，是否方便分享一下呢？IND确实好多这种失败的因子，调过几个也没有成功。

---

### 评论 #8 (作者: JY55846, 时间: 3个月前)

==============================================================================实测很有用，还会标注那些是用了robust的，祝大家早日vf1，加油加油==============================================================================

---

