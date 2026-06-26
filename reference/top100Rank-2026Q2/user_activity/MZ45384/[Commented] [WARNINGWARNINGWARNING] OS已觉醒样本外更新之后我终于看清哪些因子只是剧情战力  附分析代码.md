# [WARNING!!!WARNING!!!WARNING] OS已觉醒!!!｜样本外更新之后，我终于看清哪些因子只是“剧情战力” | 附分析代码

- **链接**: [Commented] [WARNINGWARNINGWARNING] OS已觉醒样本外更新之后我终于看清哪些因子只是剧情战力  附分析代码.md
- **作者**: JL40454
- **发布时间/热度**: 5个月前, 得票: 70

## 帖子正文

最近的 OS更新后，我把同一批因子整体重新做了一轮 OS 分布分析。结果非常直观，也非常残酷：很多在 IS 里表现“像主角”的因子，一进 OS 分布，直接暴露出真实定位——剧情强度，不是实战强度。

这次我刻意不看均值、不看单点最优，只看分布。OS 的 Sharpe、Fitness、Returns、Drawdown、Turnover、Margin 全部拆开，按 type、region、delay 做分布图。原因只有一个：均值可以靠运气堆出来，分布不行。分布会明确告诉你，这类因子是在大多数时间里稳定工作，还是偶尔爆发、大多数时候失效。

最明显的感受是：
同一个 type 内，OS 的离散度远高于 IS。也就是说，真正决定因子能不能活下来的，不是“你做了哪一类因子”，而是“你在这一类里抓到的是不是结构性信号”。这一步直接改变了我对模板设计的看法——模板的目标不该是极限 Sharpe，而是让 OS 分布整体右移，同时压住左尾。

当我把 OS 分布进一步按 region 和 delay 的组合展开，很多以前被我视为“稳定模板”的因子直接翻车。不是调参问题，也不是噪声，而是逻辑只在非常狭窄的市场状态下成立。OS 在这里起到的作用，其实是世界线切换器：你换一条时间线，它还能不能站得住，一眼就能看出来。
 ![图片](images/img_ce1f1d164a.png)

现在我越来越把 OS 当成因子研究里真正的分水岭：
IS 只是入场券，证明你确实捕捉到了一点信息；
OS 才是觉醒考核，决定你是不是有资格成为可复用、可扩展的策略组件。

如果说以前做因子有点像抽卡，那 OS 更新之后更像是角色觉醒系统：
没通过 OS 的，再好看的数值也只是皮肤；
能在 OS 分布里稳住形态的，才是真正的本体。

下面我会把这次用来做 OS 分布分析与可视化的完整代码贴出来，包含分组逻辑、分布图构建以及交互式 Plotly 导出。
代码较长，直接粘贴在这里，方便有兴趣的朋友自行复现和改造：

> import pandas as pd
> import numpy as np
> from datetime import datetime, timezone, timedelta
> import time
> import plotly.graph_objects as go
> from plotly.subplots import make_subplots
> from wqb.wqb import WQBSession, print, FilterRange
> # Create `wqbs`
> wqbs = WQBSession((
> "EMAIL",
> "PASSWORD"
> ), logger=None)
> # If `logger` was not created, use the following line instead.
> # wqbs = WQBSession(('<email>', '<password>'))
> # Test connectivity (Optional)
> resp = wqbs.auth_request(log=None)
> print(f'status_code: [{resp.status_code}], success_login: {resp.ok}, user id: {resp.json()["user"]["id"]}')           # 201, True, <Your BRAIN User ID>
> def flatten_dict(d, parent_key='', separator='_'):
> """
> 将嵌套字典扁平化为一层字典，键通过 separator 连接路径。
> 参数:
> d (dict): 要扁平化的字典。
> parent_key (str): 当前递归层级的父键（用于递归，一般不需手动传入）。
> separator (str): 键路径的分隔符，默认为 '_'。
> 返回:
> dict: 扁平化后的字典。
> """
> items = []
> for k, v in d.items():
> new_key = f"{parent_key}{separator}{k}" if parent_key else str(k)
> if isinstance(v, dict):
> items.extend(flatten_dict(v, new_key, separator).items())
> else:
> items.append((new_key, v))
> return dict(items)
> s_t = datetime.now()
> while True:
> try:
> print(f'Waiting...{datetime.now()-s_t}.')
> alphas = []
> resps = wqbs.filter_alphas(
> status='ACTIVE',
> # date_submitted=FilterRange.from_str(f"[{datetime.fromisoformat('2025-11-01T00:00:00-0000').isoformat()}, {datetime.fromisoformat('2026-02-01T00:00:00-0000').isoformat()}]"),
> # date_submitted=FilterRange.from_str(f"[{datetime.fromisoformat('2020-11-01T00:00:00-0000').isoformat()}, {datetime.fromisoformat('2026-01-01T00:00:00-0000').isoformat()}]"),
> # type='REGULAR',
> # delay=1,
> log=None
> )
> for resp in resps:
> alphas.extend(item for item in resp.json()['results'])
> print(f"{len(alphas)} alphas found.")
> break
> except Exception as e:
> print(e)
> time.sleep(5)
> submitted_alphas = [flatten_dict(alpha) for alpha in alphas]
> df = pd.DataFrame(submitted_alphas)
> # =========================
> # Utils
> # =========================
> def _to_numeric_safe(s: pd.Series) -> pd.Series:
> return pd.to_numeric(s, errors="coerce")
> def _ensure_categories(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
> out = df.copy()
> for c in cols:
> out[c] = out[c].astype("string").fillna("NA")
> return out
> def _build_hist_subplots(
> df: pd.DataFrame,
> group_cols: list[str],
> value_cols: list[str],
> nbins: int = 30,
> title: str = "",
> legend_right: bool = True,
> legend_gap: int = 8,
> legend_font_size: int = 10,
> ):
> """
> 每个数值列一个子图；每个分组一个 trace(直方图)。
> 你要的“分布图”就是这里：histnorm 设为 'probability' / 'percent' / None 都行。
> """
> df = _ensure_categories(df, group_cols)
> g = df.groupby(group_cols, dropna=False)
> ncols = 2
> nrows = int(np.ceil(len(value_cols) / ncols))
> fig = make_subplots(
> rows=nrows,
> cols=ncols,
> subplot_titles=value_cols,
> horizontal_spacing=0.08,
> vertical_spacing=0.10,
> )
> # 统一 legend：同一个 group label 在每个子图都出现，但只在第一个子图展示 legend
> group_labels = []
> group_frames = []
> for k, sub in g:
> if not isinstance(k, tuple):
> k = (k,)
> label = " | ".join([f"{col}={val}" for col, val in zip(group_cols, k)])
> group_labels.append(label)
> group_frames.append(sub)
> for i, col in enumerate(value_cols):
> r = i // ncols + 1
> c = i % ncols + 1
> # 每个分组一个 trace
> for j, (label, sub) in enumerate(zip(group_labels, group_frames)):
> x = _to_numeric_safe(sub[col]).dropna()
> if x.empty:
> continue
> show_legend = (i == 0)  # 只在第一个子图显示 legend
> fig.add_trace(
> go.Histogram(
> x=x,
> name=label,
> nbinsx=nbins,
> opacity=0.55,
> histnorm="probability",  # 你要“分布图”，不是mean
> legendgroup=label,
> showlegend=show_legend,
> ),
> row=r,
> col=c,
> )
> fig.update_xaxes(title_text=col, row=r, col=c)
> fig.update_yaxes(title_text="probability", row=r, col=c)
> fig.update_layout(
> title=title,
> barmode="overlay",
> bargap=0.08,
> height=320 * nrows,
> template="plotly_white",
> )
> # ✅ 关键：把 legend 做“高一点”，不要和图混一起 —— 放到右侧图外 + 预留 margin
> if legend_right:
> fig.update_layout(
> legend=dict(
> orientation="v",
> yanchor="middle",
> y=0.5,
> xanchor="left",
> x=1.02,  # 放到绘图区外
> tracegroupgap=legend_gap,  # 让legend项上下更“松”
> font=dict(size=legend_font_size),
> itemsizing="constant",
> ),
> margin=dict(r=280),  # 给legend腾位置（否则会挤在一起）
> )
> else:
> # 备选：放底部
> fig.update_layout(
> legend=dict(
> orientation="h",
> yanchor="top",
> y=-0.25,
> xanchor="center",
> x=0.5,
> tracegroupgap=legend_gap,
> font=dict(size=legend_font_size),
> ),
> margin=dict(b=220),
> )
> return fig
> def _build_count_bar_and_table(
> df: pd.DataFrame,
> count_cols: list[str],
> title: str,
> legend_right: bool = True,
> ):
> """
> 统计数值表：每个分组变量的频数分布
> - 柱状：counts
> - 表：counts 的 DataFrame 展示
> """
> df = _ensure_categories(df, count_cols)
> fig = make_subplots(
> rows=1,
> cols=len(count_cols),
> subplot_titles=[f"Counts: {c}" for c in count_cols],
> horizontal_spacing=0.08,
> )
> tables = {}
> for i, c in enumerate(count_cols):
> vc = df[c].value_counts(dropna=False).sort_index()
> tables[c] = vc.rename("count").to_frame()
> fig.add_trace(
> go.Bar(
> x=vc.index.astype(str),
> y=vc.values,
> name=c,
> showlegend=False,
> ),
> row=1,
> col=i + 1,
> )
> fig.update_xaxes(title_text=c, tickangle=30, row=1, col=i + 1)
> fig.update_yaxes(title_text="count", row=1, col=i + 1)
> fig.update_layout(
> title=title,
> template="plotly_white",
> height=420,
> margin=dict(r=40),
> )
> return fig, tables
> # =========================
> # Main
> # =========================
> def plot_distributions_and_tables(
> df: pd.DataFrame,
> nbins: int = 30,
> ):
> """
> 你提的三种统计需求：
> 1) 仅按 ('type','settings_region','settings_delay') 分组：对其他列做分布图 + 统计表
> 2) 仅按 'type' 分：统计 (settings_region, settings_delay) 的 combo 类
> 3) 仅按 'type' 分：统计 settings_region 和 settings_delay 类
> """
> required = [
> "type",
> "settings_region",
> "settings_delay",
> "os_osISSharpeRatio",
> "os_turnover",
> "os_returns",
> "os_drawdown",
> "os_margin",
> "os_fitness",
> "os_sharpe",
> "os_sharpe60",
> "os_sharpe125",
> ]
> missing = [c for c in required if c not in df.columns]
> if missing:
> raise ValueError(f"df 缺少这些列: {missing}")
> value_cols = [
> "os_osISSharpeRatio",
> "os_turnover",
> "os_returns",
> "os_drawdown",
> "os_margin",
> "os_fitness",
> "os_sharpe",
> "os_sharpe60",
> "os_sharpe125",
> ]
> # -------------------------
> # 1) 按 type/region/delay 分组：分布图（直方） + 统计表（describe）
> # -------------------------
> group_cols = ["type", "settings_region", "settings_delay"]
> fig_dist_1 = _build_hist_subplots(
> df=df,
> group_cols=group_cols,
> value_cols=value_cols,
> nbins=nbins,
> title="(1) Distributions by type × region × delay",
> legend_right=True,   # ✅ legend 右侧变“高”，不挤图
> legend_gap=10,
> legend_font_size=10,
> )
> # 统计表：对每个分组的数值列做 describe（不取 mean 画图；这里只是表）
> df_num = df[value_cols].apply(_to_numeric_safe)
> df_tmp = pd.concat([df[group_cols], df_num], axis=1)
> desc_1 = (
> df_tmp.groupby(group_cols, dropna=False)[value_cols]
> .describe()
> )
> # desc_1 是 MultiIndex columns；你可以按需保存/导出
> # -------------------------
> # 2) 仅按 type 分：统计 (region, delay) combo 类
> # -------------------------
> df2 = df.copy()
> df2["region_delay_combo"] = (
> df2["settings_region"].astype("string").fillna("NA")
> + "|"
> + df2["settings_delay"].astype("string").fillna("NA")
> )
> combo_counts = (
> df2.groupby("type", dropna=False)["region_delay_combo"]
> .value_counts(dropna=False)
> .rename("count")
> .reset_index()
> .sort_values(["type", "count"], ascending=[True, False])
> )
> # 可视化：每个 type 一个子图，展示 topN（你没说要切片，我这里不切片）
> types = df2["type"].astype("string").fillna("NA").unique().tolist()
> fig_combo = make_subplots(
> rows=len(types),
> cols=1,
> subplot_titles=[f"(2) type={t}: (region,delay) combos" for t in types],
> vertical_spacing=0.08,
> )
> for i, t in enumerate(types, start=1):
> sub = combo_counts[combo_counts["type"] == t]
> fig_combo.add_trace(
> go.Bar(
> x=sub["region_delay_combo"],
> y=sub["count"],
> name=str(t),
> showlegend=False,
> ),
> row=i,
> col=1,
> )
> fig_combo.update_xaxes(tickangle=30, row=i, col=1)
> fig_combo.update_yaxes(title_text="count", row=i, col=1)
> fig_combo.update_layout(
> title="(2) Combo counts per type",
> template="plotly_white",
> height=300 * len(types),
> margin=dict(r=40),
> )
> # -------------------------
> # 3) 仅按 type 分：统计 region 类 & delay 类
> # -------------------------
> region_counts = (
> df.groupby(["type", "settings_region"], dropna=False)
> .size()
> .rename("count")
> .reset_index()
> .sort_values(["type", "count"], ascending=[True, False])
> )
> delay_counts = (
> df.groupby(["type", "settings_delay"], dropna=False)
> .size()
> .rename("count")
> .reset_index()
> .sort_values(["type", "count"], ascending=[True, False])
> )
> fig_rd = make_subplots(
> rows=len(types),
> cols=2,
> subplot_titles=sum([[f"(3) type={t}: region", f"(3) type={t}: delay"] for t in types], []),
> horizontal_spacing=0.08,
> vertical_spacing=0.10,
> )
> for i, t in enumerate(types, start=1):
> sub_r = region_counts[region_counts["type"].astype("string").fillna("NA") == t]
> sub_d = delay_counts[delay_counts["type"].astype("string").fillna("NA") == t]
> fig_rd.add_trace(
> go.Bar(x=sub_r["settings_region"].astype(str), y=sub_r["count"], showlegend=False),
> row=i,
> col=1,
> )
> fig_rd.add_trace(
> go.Bar(x=sub_d["settings_delay"].astype(str), y=sub_d["count"], showlegend=False),
> row=i,
> col=2,
> )
> fig_rd.update_xaxes(tickangle=30, row=i, col=1)
> fig_rd.update_xaxes(tickangle=30, row=i, col=2)
> fig_rd.update_yaxes(title_text="count", row=i, col=1)
> fig_rd.update_yaxes(title_text="count", row=i, col=2)
> fig_rd.update_layout(
> title="(3) Region / Delay counts per type",
> template="plotly_white",
> height=320 * len(types),
> margin=dict(r=40),
> )
> # 返回：三个图 + 三个表对象
> tables = {
> "describe_by_type_region_delay": desc_1,        # (1) describe 表
> "combo_counts_by_type": combo_counts,           # (2) combo 计数表
> "region_counts_by_type": region_counts,         # (3) region 计数表
> "delay_counts_by_type": delay_counts,           # (3) delay 计数表
> }
> figs = {
> "fig_dist_1": fig_dist_1,
> "fig_combo": fig_combo,
> "fig_region_delay": fig_rd,
> }
> return figs, tables
> # =========================
> # Usage
> # =========================
> figs, tables = plot_distributions_and_tables(df, nbins=35)
> figs["fig_dist_1"].show()
> figs["fig_combo"].show()
> figs["fig_region_delay"].show()
> print(tables["describe_by_type_region_delay"])  # groupby describe (MultiIndex columns)
> print(tables["combo_counts_by_type"])           # DataFrame
> print(tables["region_counts_by_type"])          # DataFrame
> print(tables["delay_counts_by_type"])           # DataFrame
> import os
> fig = figs["fig_dist_1"]
> # 1) 保存为可交互 HTML（推荐：双击打开即可交互）
> out_html = r"./fig_dist_1.html"
> fig.write_html(
> out_html,
> include_plotlyjs="cdn",   # 或 True(更大但离线可用)
> full_html=True,
> auto_open=False
> )
> print("saved:", os.path.abspath(out_html))
> # 2) 备选：保存为 plotly 的 JSON（以后可用 pio.from_json 恢复）
> out_json = r"./fig_dist_1.json"
> fig.write_json(out_json)
> print("saved:", os.path.abspath(out_json))
> # 读取 JSON 恢复：
> # import plotly.io as pio
> # fig_restored = pio.from_json(open(out_json, "r", encoding="utf-8").read())
> # fig_restored.show()

---

## 讨论与评论 (5)

### 评论 #1 (作者: JR57542, 时间: 5个月前)

这个确实是，is里面很高数值已经os就不行了，往往过拟合的方式提高is导致os都会崩。这个可视化做的好。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ 引擎状态：在线 [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(稳健性 * 创造力)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #2 (作者: FG65608, 时间: 5个月前)

博主文章中的关键行结论："真正决定因子能不能活下来的，不是“你做了哪一类因子”，而是“你在这一类里抓到的是不是结构性信号”。这一步直接改变了我对模板设计的看法——模板的目标不该是极限 Sharpe，而是让 OS 分布整体右移，同时压住左尾"

后半句看懂了，但是前半句中结构性信号，不太理解，可否详细说明下，或者举个例子？

---

### 评论 #3 (作者: JL40454, 时间: 4个月前)

[FG65608](/hc/en-us/profiles/35848484925975-FG65608) 
结构性信号 = 有可重复的经济/行为/制度机制支撑，能在多数时间线、市场结构变化后仍然以“同一种方向”提供信息优势的信号

---

### 评论 #4 (作者: MZ45384, 时间: 4个月前)

这次os更新给了很多人一击大棒，尤其是我，os/is的均值没有过一的，看分布一眼望去红的一块像创伤一样骇人。想要实现真正的high performance，必须学会抓住结构性信号。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #5 (作者: MZ54236, 时间: 4个月前)

感谢提供代码，已经跑过一次了，看上去还是挺惨的，除了图表之外我还挨个点进去看了一下OS，比较意外的是model类的有好几个撑场面的好因子，之前的感觉是model的sharpe逐年走平，OS可能不太好，看来也要分数据集讨论。

Super alpha，原以为10+的IS sharpe就算OS较差也能剩下不少，没想能跌到没信号…

---

