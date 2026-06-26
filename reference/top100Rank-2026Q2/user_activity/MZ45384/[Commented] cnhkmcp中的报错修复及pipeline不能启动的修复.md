# cnhkmcp中的报错修复，及pipeline不能启动的修复

- **链接**: [Commented] cnhkmcp中的报错修复及pipeline不能启动的修复.md
- **作者**: YQ83381
- **发布时间/热度**: 3个月前, 得票: 5

## 帖子正文

cnhkmcp，最近3.1.5以后的版本，运行的时候总是启动不了，发现一个报错，不知道有没有同学也遇到了同样问题。ace_lib.py脚本中有一处报错：

```
if parsed["remaining_minute"] <= 1:    # logger.info(f"Rate limit {parsed["limit_minute"]} reached (per minute). Sleeping for a minute...")    time.sleep(60)
```

那么，我们只要在1184行这里，给他注释掉就可以了。
同样的问题，也出现在pipeline，上面的ace_lib.py脚本是在APP的根目录，而这个脚本位置是在：APP\trailSomeAlphas\skills\brain-feature-implementation\scripts\ace_lib.py
也就是Skill中的脚本中，也是在1184行，给他注释掉，pipeline就能正常启动了。
PS：不知道是不是只有我才有这个问题，如果是通用问题，麻烦作者大大、把这行删掉吧，否则每次获取新版本都要去注释下。

---

## 讨论与评论 (6)

### 评论 #1 (作者: CA85280, 时间: 3个月前)

我也有这个问题，我的解决方法是改成：

```
f'Rate limit {parsed["limit_minute"]} reached (per minute). Sleeping for a minute..."'
```

也就是把"改成'

---

### 评论 #2 (作者: CW94093, 时间: 3个月前)

怎么更新的 我还是3.0

---

### 评论 #3 (作者: XY20037, 时间: 3个月前)

太感谢大佬分享这个关键的修复方案！最近升级 cnhkmcp 3.1.5 版本后确实遇到了 pipeline 启动失败的问题，排查了很久都没找到原因，没想到是 ace_lib.py 1184 行的 remaining_minute 判断逻辑导致的。你不仅精准定位了报错位置，还明确了根目录和 Skill 目录下两处需要注释的脚本路径，直接解决了启动卡点，太实用了！这个问题应该是通用的，希望作者能尽快修复，也感谢你帮大家节省了大量排查时间，收藏备用～

---

### 评论 #4 (作者: BW14163, 时间: 3个月前)

一般遇到这类问题，直接让ai接手，告诉他，帮忙配置一下cnhkmcp

---

### 评论 #5 (作者: CL96463, 时间: 3个月前)

这个不用注释也可以，把里面的双引号改成单引号就好啦

---

### 评论 #6 (作者: MZ45384, 时间: 3个月前)

感谢提醒，我这就去cnhkmcp里的APP\trailSomeAlphas\skills\brain-feature-implementation\scripts\ace_lib.py注释掉1184这一行。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

