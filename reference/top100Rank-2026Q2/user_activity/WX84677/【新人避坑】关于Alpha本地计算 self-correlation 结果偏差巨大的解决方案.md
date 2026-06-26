# 【新人避坑】关于Alpha本地计算 self-correlation 结果偏差巨大的解决方案

- **链接**: 【新人避坑】关于Alpha本地计算 self-correlation 结果偏差巨大的解决方案.md
- **作者**: WX84677
- **发布时间/热度**: 1年前, 得票: 14

## 帖子正文

首先感谢 XZ23611 分享的帖子：“【提升Check Submission效率】一些可以提升Check Submission的Tips，效率提高10倍以上”其中分享的代码非常实用。一般情况下，使用这套代码本地计算self-correlation值与Brain 平台计算的结果值，一般只会有 0.02~0.05 的差异，对于实战完全够用。但有个场景下，计算结果与平台结果天差地别：看以下案例：Alpha_id1 的pnl曲线：Alpha_id2 的pnl曲线：关键点就是alpha 的pnl数据日期不一致，且批量获取 pnl 时先获取了数据日期较少的alpha.这种情况下，get_pnl_panel( ) 函数中，对多个alpha的pnl_df 进行合并时，由于行数不一致，合并后的 pnl_df 会出现 Date 索引乱序。而后续计算自相关性时，pnl 数据的时序性是非常关键的，如果非时序结果自然完全不同。pnl_df 只包含 alpha1 时，print(pnl_df.index):pnl_df 合并 alpha2 后，print(pnl_df.index):解决方案：修改get_pnl_panel() 函数即可：希望遇到相同场景的伙伴，能节省调试时间，少走弯路。最后祝愿所有顾问伙伴，2025年都能收获满满~

---

## 讨论与评论 (1)

### 评论 #1 (作者: HQ17963, 时间: 1年前)

感谢分享！注意到截图中Date列的类型为object，即str储存的，可以转换为datetime64类型，再merge就没问题了。附转换代码：pnl_df=pnl_df.assign(Date=lambda x:pd.to_datetime(x.Date,format='%Y-%m-%d')).set_index('Date')改：我是用concat实现合并的，不知道是否影响final_df = pd.concat(pnl_dfs, axis=1)

---

