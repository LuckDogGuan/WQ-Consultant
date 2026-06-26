# 通过Performance Comparison减少Check Submission

- **链接**: [Commented] 通过Performance Comparison减少Check Submission.md
- **作者**: HZ76661
- **发布时间/热度**: 1年前, 得票: 4

## 帖子正文

大家都有Check Submission慢的困扰，论坛上有好多帖子介绍了如何在本地检查Self Correlation 来减少Check，但不能避免 Prod Correlation 高check不通过而浪费时间，当然我想介绍的这种方法也不能从根本上解决 Prod Correlation 问题。也只是减少 Check Submission
思路：

先 Performance Comparison 如下图：

![图片](images/img_060fefd3b0.png)

可通过 [https://api.worldquantbrain.com/users/self/alphas/e3MwdWJ/before-and-after-performance接口获取相应数据](https://api.worldquantbrain.com/users/self/alphas/e3MwdWJ/before-and-after-performance%E6%8E%A5%E5%8F%A3%E8%8E%B7%E5%8F%96%E7%9B%B8%E5%BA%94%E6%95%B0%E6%8D%AE)  如下，

"stats":{
  "before": {
"bookSize": 20000000,
    "pnl": 10964998,
    "longCount": 199,
    "shortCount": 198,
    "drawdown": 0.0652,
    "turnover": 0.0823,
    "returns": 0.1059,
    "margin": 0.002573,
    "sharpe": 3.02,
    "fitness": 2.78
  },
  "after": {
    "bookSize": 20000000,
    "pnl": 10881501,
    "longCount": 205,
    "shortCount": 197,
    "drawdown": 0.0633,
    "turnover": 0.0916,
    "returns": 0.1051,
    "margin": 0.002296,
    "sharpe": 3.11,
    "fitness": 2.85
  }
}

图片上的 sharpe 值是通过 3.11 - 3.02，其他数据同理

若计算出值不符合自身提交的要求，那么check通过也不会提交。目前想法是开10个线程，专项 Performance Comparison 操作，如果达到要求在进入 Check Submission 阶段。

问题：

1. 手动Performance Compariso很快感觉没有限制，是否多线程开启之后也会向Check Submissio一样被限制？（若有尝试过的小伙伴请告知一下）

2.Performance Compariso 的结果是什么样子才是符合进入 Check Submission 阶段，或者说符合提交的？

举几个例子：

已知sharpe、fitness、margin、returns增加好（若有此alpha直接提交就好），turnover和drawdown减少或增加影响不大，那下图sharpe、fitness增加，margin、returns减少，像这样的Performance Compariso的alpha是否该提交呢？或者harpe、fitness、margin增加returns减少的情况？

![图片](images/img_91089b66ed.png)

希望和这方面有经验的小伙伴一起讨论一下，thanks！

---

## 讨论与评论 (2)

### 评论 #1 (作者: MZ45384, 时间: 1年前)

Great, same idea as you

---

### 评论 #2 (作者: CO94068, 时间: 6个月前)

[1. 我试了下，
users/self/alphas/e3MwdWJ/before-and-after-performance](https://api.worldquantbrain.com/users/self/alphas/e3MwdWJ/before-and-after-performance%E6%8E%A5%E5%8F%A3%E8%8E%B7%E5%8F%96%E7%9B%B8%E5%BA%94%E6%95%B0%E6%8D%AE)  这个接口的频率限制似乎是和alpha_detail ,

/alphas/{id}/recordsets` 等是一样的，header 给的limit都是1小时2000次。而且我自己获取，感觉速度也挺快的。1秒内就有结果了，和check肯定不是一个限制量级的。可以放心调用，注意瞬间别同时发太多个就好，我是每隔2秒串行发送请求。
2. 最近刚好也在思考Performance 这个指标，我的思路是，把自己看中的指标先列出来，然后赋予权重。接着根据自己赋予的权重对指标进行归一化，归一化用的sigmoid,center和slope就是要根据个人情况来定了。然后加权求一个总的分数，然后按分数排序。

3. 这个顺序和减少/check 的思路学到了~

⌬ SYSTEM DETECTED: OVERTHINKING...
[██████░░░░] Loading Action...

⚠️ 警告：犹豫只会增加内耗成本。
❝ 细 想 全 是 问 题 ❞
❝ 去 做 全 是 答 案 ❞

>> Execute: Just_Do_It.exe
>> Status: Running... ⚡
━━━━━━━━━━━━━━━━━━━━━━

---

