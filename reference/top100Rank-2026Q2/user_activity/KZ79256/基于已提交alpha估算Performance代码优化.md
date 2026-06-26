# 基于已提交alpha估算Performance代码优化

- **链接**: 基于已提交alpha估算Performance代码优化.md
- **作者**: KZ79256
- **发布时间/热度**: 11个月前, 得票: 73

## 帖子正文

在alpha界面有一个Performance Comparison, 一个自然而然的问题就是这个Performance是怎么计算的. 这里通过已提交的alpha计算before Performance.结果展示首先是本地计算(local)和云端计算(cloud)的每日盈亏, 整体来看本地估算和云端计算的结果比较相近接下来是估算的各个指标和线上指标的对比以及相对误差整体来看除了个别区域以外, 大部分地区都比较符合代码如下已提交因子的数据采集这里不在赘述, 最后形成这样的一个dataframe, 必须包含以下几列, 包含RA和SA核心估算函数如下pnl是每个pnl的均值sharpe和drawdown是基于pnl计算的turnover, returns, margin都是近似所有alpha的相应值的均值fitness 是基于公式计算的def estimate_performance_func(tmp_data, max_date=None):local_pnls = pd.json_normalize(tmp_data['pnl']).Tlocal_pnls.columns = tmp_data['alphaId'].valueslocal_pnls.index = pd.to_datetime(local_pnls.index)local_pnls = local_pnls.sort_index()local_rets = local_pnls - local_pnls.ffill().shift(1)local_ret = local_rets.mean(1).dropna()ret = local_retif max_date is not None:ret = ret[ret.index <= max_date]ret.dropna(inplace=True)pnl = ret.cumsum()metric_pnl = pnl[-1]metric_sharpe = np.mean(ret) / np.std(ret) * np.sqrt(252)metric_drawdown = ((pnl.cummax() - pnl) / 10000000).max()metric_turnover = tmp_data['turnover'].mean()metric_returns = tmp_data['returns'].mean()metric_fitness = metric_sharpe * np.sqrt(np.abs(metric_returns) / max(metric_turnover,0.125))metric_margin = metric_pnl/(local_pnls.apply(lambda col: col.loc[col.last_valid_index()])/pd.Series(tmp_data['margin'].values,index=tmp_data['alphaId'])).mean()metric = {'turnover': metric_turnover,'pnl': metric_pnl,'sharpe': metric_sharpe,'returns': metric_returns,'margin': metric_margin,'drawdown': metric_drawdown,'fitness': metric_fitness,}return local_pnls, local_ret, metric绘图函数如下from scipy.stats import gaussian_kdefrom mpl_toolkits.axes_grid1.inset_locator import inset_axesdef plot_ret(compare_ret):xy = np.vstack([compare_ret['local'], compare_ret['cloud']])z = gaussian_kde(xy)(xy)sc = plt.scatter(compare_ret['local'], compare_ret['cloud'], c=z, s=10, cmap='viridis')plt.axline((0, 0), slope=1, color='red', linestyle='--', lw=2)plt.xlabel('Alpha')plt.ylabel('PingTai')plt.xlabel(r'Local Ret', fontproperties=font_prop20)plt.ylabel(r'Cloud Ret', fontproperties=font_prop20)# plt.legend(loc='lower right', frameon=False, prop=font_prop20, bbox_to_anchor=(1.05, 0))plt.legend(loc='upper left', frameon=False, prop=font_prop20, bbox_to_anchor=(0, 1), title=f'{region}-D{delay}\nNum={local_pnls.shape[1]}\n'+rf'$\rho={compare_ret.corr().iloc[0,1]:.2f}$', title_fontproperties=font_prop20)plt.xticks(fontproperties=font_prop18);plt.yticks(fontproperties=font_prop18);plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=5))plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=5))plt.gca().xaxis.set_ticks_position('both')  # 在x轴的上下两边都显示刻度plt.gca().yaxis.set_ticks_position('both')  # 在y轴的左右两边都显示刻度for spine in plt.gca().spines.values():spine.set_linewidth(2)plt.gca().tick_params(direction='in', length=6, width=2)  # length是刻度的长度，width是刻度的宽度plt.gca().tick_params(direction='in', length=4, width=1.4, which='minor')# 在主图内部空白处添加水平colorbaraxins = inset_axes(plt.gca(),width="50%",   # colorbar宽度height="5%",   # colorbar高度loc='lower right',bbox_to_anchor=(-0.05, 0.15, 1, 1),bbox_transform=plt.gca().transAxes,borderpad=0)cbar = plt.colorbar(sc, cax=axins, orientation='horizontal')# 1. 统一刻度样式（与主图保持一致）cbar.ax.tick_params(direction='in',  # 刻度向内length=6,        # 主刻度长度width=2,         # 主刻度宽度which='major')cbar.ax.tick_params(direction='in',length=4,        # 次刻度长度width=1.4,       # 次刻度宽度which='minor')# 2. 去除colorbar所有ticklabelcbar.ax.set_xticklabels([])# 3. 在最左和最右分别标记low和highvmin, vmax = cbar.ax.get_xlim()cbar.ax.text(vmin, -0.8, 'low', va='center', ha='left', fontproperties=font_prop18, transform=cbar.ax.transData)cbar.ax.text(vmax, -0.8, 'high', va='center', ha='right', fontproperties=font_prop18, transform=cbar.ax.transData)# 4. 美化colorbar边框for spine in cbar.ax.spines.values():spine.set_linewidth(2)  # 边框线宽与主图一致# 5. 优化colorbar标签cbar.set_label('Density',fontproperties=font_prop20,  # 标签字体与坐标轴标题统一labelpad=10  # 标签与colorbar的间距)需要一个可以获得performence的alpha_idalpha_id_maps = {'USA':{0:'K28bJV1', 1:'VRaOVKY'},'AMR':{1:'l5ROaLn'},'ASI':{1:'J2pl86W'},'CHN':{1:'kYoQoxz'},'EUR':{1:'G7vve1O'},'GLB':{1:'OzzENXb'},'HKG':{1:'xjvwmZp'},'JPN':{1:'PPdpArW'},'KOR':{1:'K7v9XQz'},'TWN':{1:'zL8X50X'},}绘图函数如下region_delay = [(region, delay) for region, delays in alpha_id_maps.items() for delay in delays]plt.figure(figsize=(5*2,5*math.ceil(len(region_delay) / 2)))estimate_data = {}for idx, (region, delay) in enumerate(tqdm(region_delay)):item_estimate_data = {}tmp_res = wait_get(f'https://api.worldquantbrain.com/users/self/alphas/{alpha_id_maps[region][delay]}/before-and-after-performance').json()cloud_pnl = tmp_res['pnl']cloud_pnl = pd.DataFrame(cloud_pnl['records'], columns=[item['name'] for item in cloud_pnl['schema']['properties']])cloud_pnl.set_index('date', inplace=True)cloud_pnl = cloud_pnl['beforePnL']tmp_data = data.query(f'region=="{region}" and delay=={delay} and dateSubmitted >= "{date_beg}"')local_pnls, local_ret, item_metric = estimate_performance_func(tmp_data, max_date=cloud_pnl.index.max())cloud_pnl.index = pd.to_datetime(cloud_pnl.index)cloud_pnl = cloud_pnl.sort_index()cloud_ret = cloud_pnl - cloud_pnl.ffill().shift(1)compare_ret = pd.merge(local_ret.rename("local"),cloud_ret.rename("cloud"),left_index=True,right_index=True)compare_ret.sort_index(inplace=True)compare_ret.dropna(inplace=True)plt.subplot(math.ceil(len(region_delay) / 2), 2, idx+1)plot_ret(compare_ret)item_estimate_data['true'] = tmp_res['stats']['before']item_estimate_data['pred'] = item_metricestimate_data[region + '-' + str(delay)] = item_estimate_data# breakplt.tight_layout()

---

## 讨论与评论 (4)

### 评论 #1 (作者: LZ63459, 时间: 10个月前)

thanks, 如果能够根据历史提交的alpha去总结fields特征,是不是可以更进一步了解到数据集的字段有效性

---

### 评论 #2 (作者: KZ79256, 时间: 9个月前)

经过别人提醒，正文的误差大概率来源于 PPA和RA在performence里是分开的。

---

### 评论 #3 (作者: KZ79256, 时间: 9个月前)

LZ63459如果能够根据历史提交的alpha去总结fields特征,是不是可以更进一步了解到数据集的字段有效性这是一个庞大的工程，而且可能不具有通用性

---

### 评论 #4 (作者: MM38095, 时间: 3个月前)

厉害了，试试看

---

