# 筛选可优化RA进阶版

- **链接**: 筛选可优化RA进阶版.md
- **作者**: MZ45384
- **发布时间/热度**: 6天前, 得票: 16

## 帖子正文

之前发过一个IND区域筛选LOW_ROBUST_UNIVERSE_SHARPE的代码，现在有进阶版了！！！IND区域Regular Alpha通不过的大部分原因都是ROBUST_UNIVERSE_SHARPE不过关，但其他区域没有这个指标，通常可能是SUB_UNIVERSE_SHARPE，2Y_SHARPE，IS_LADDER_SHARPE。尤其是IS_LADDER_SHARPE，在非ATOM RA中出现地最频繁。遂有此优化版本：def wait_get(sess, url: str, max_retries: int = 10) -> "Response":retries = 0while retries < max_retries:while True:simulation_progress = sess.get(url)if simulation_progress.headers.get("Retry-After", 0) == 0:breaktime.sleep(float(simulation_progress.headers["Retry-After"]))if simulation_progress.status_code < 400:breakelse:time.sleep(2 ** retries)retries += 1return simulation_progressdef target_check(s, alpha_list, target, cutoff):may_list = []for alpha_id in tqdm(alpha_list, total=len(alpha_list), desc=f'Checking {target}', colour='#00ff00'):metrics = wait_get(s, f'https://api.worldquantbrain.com/alphas/{alpha_id}').json()for i in metrics['is']['checks']:if i['name'] == target:delta = i['value'] - i['limit']if delta >= cutoff:may_list.append([alpha_id, delta])breakdf = pd.DataFrame(may_list, columns=['alpha_id', target]).set_index('alpha_id')may_df = df.sort_values(target, ascending=False)print('阈值之上：', len(may_df))return may_dfiron_df = target_check(s, stone_bag, 'LOW_2Y_SHARPE', -0.2)  # 这里的阈值（value-limit）设为-0.2，可以根据自己的选择调整iron_bag = iron_df.index.tolist()iron_df另外，常用的四个target值也都在这里展示一下：LOW_SUB_UNIVERSE_SHARPELOW_2Y_SHARPELOW_ROBUST_UNIVERSE_SHARPEIS_LADDER_SHARPE如果有其他指标，稍微修改一下target和cutoff即可。效果展示：最后祝大家都能消除所有的fail或者warning。

---

## 讨论与评论 (0)

