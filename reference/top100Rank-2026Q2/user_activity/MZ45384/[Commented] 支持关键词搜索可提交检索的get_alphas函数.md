# 支持关键词搜索/可提交检索的get_alphas函数

- **链接**: [Commented] 支持关键词搜索可提交检索的get_alphas函数.md
- **作者**: WC53907
- **发布时间/热度**: 7个月前, 得票: 3

## 帖子正文

我从7月下旬接触世坤的顾问项目，到10月中旬获得顾问权限，从论坛上学习到了很多知识和技巧，非常感谢各位前辈大佬的经验和分享。

今天我分享一下我重构后的get_alphas函数。我重构后的函数现在支持表达式关键词搜索，根据返回的json文件中的is下面checks的fail数量判断是否具备提交条件，顺带自动标成绿色，方便在官网快速查看。整个搜索过程支持进度条显示。以下是具体功能介绍。

### **关键词搜索**

通过required_fields传入需要的关键词列表，match_mode为"all"是全部符合，"any"是任一匹配。

### **可提交搜索**

通过submittable传入True,可以实现提提交初步搜索。如果 auto_color传入True，则开启自动标色，我设置的是绿色，在辅助函数里可以自行修改。

### **隐藏状态搜索**

如果hidden传入true，则搜索范围为已隐藏alpha。

### **函数输出**

通过output_file_name传入需要输出的csv文件名，我默认的是"alpha_search_list.csv"。输出顺序是按fitness降序排列。如果输入模式mode为w为全新输入，如果是a则为追加输入。有时需要批量查PC时用得着。

### **日志显示**

如果觉得麻烦，可以直接删除！

### **其他**

1. 如果region、universe传入空白字符串，submittable为True,auto_color为True则为搜索全部可提交alpha。
2. 按日期排列最新的10000个Alpha，其实可以根据sharpe或fitness进行降序排列，改下url就可以。
3. 这个函数我是放在类里的方法，大家借鉴的时候注意把self去掉！

### 特别说明

可提交检索没有考虑相关因素！！

## 必要库

pandas tqdm requests pathlib

安装命令如下：

```
pip install pandas tqdm requests
```

## 函数代码

```
def get_alphas(        self,        total_alphas=5,        limit=100,        delay=1,        region="USA",        universe="TOP3000",        required_fields=None,        match_mode="all",        min_sharpe=None,        min_fitness=None,        hidden="false",        submittable=False,        auto_color=False,        color="GREEN",        output_file_name="alpha_search_list.csv",        mode="w",    ):        # 按生成日期，根据操作符或特定数据字段， 从最新的1万alpha中搜索        # 支持 /*T */ 的格式搜索特定批次的alpha        # required_fields包含的字符串不要过多，否则搜索很慢很慢        # submittable设为True，筛选可提交函数，并标为绿色方便PC、SC检查        # 其实也可以根据sharpe，fitness的阈值进行标色        # submittable判断依据['is']['checks']['results']中FAIL数为0        # submittable未涉及PC、SC等相关因素！！        # color 值为NONE为无色        # 支持查询进度显示        # 最后输出为fitness降序        # hidden默认为false，如果是true则已隐藏alpha中查找        # 验证颜色参数        valid_colors = [None, "GREEN", "YELLOW", "RED", "BLUE", "PURPLE", "ORANGE"]        if color not in valid_colors:            raise ValueError(f"颜色必须是以下之一: {valid_colors}")        fetched_alphas = []        offset = 0        total_accessed = 0        colored_count = 0  # 记录标记数量        # 先获取总数        count_url = (            f"https://api.worldquantbrain.com/users/self/alphas?stage=IS&hidden={hidden}"            f"&limit=1&settings.delay={delay}&settings.region={region}&status=UNSUBMITTED%1FIS_FAIL&settings.universe={universe}"        )        count_response = self.sess.get(count_url)        total_available = count_response.json()["count"]        pbar = tqdm(total=total_available, desc="扫描Alpha", unit="条")        while len(fetched_alphas) < total_alphas:            # 构建请求URL            url = (                f"https://api.worldquantbrain.com/users/self/alphas?stage=IS&limit={limit}"                f"&offset={offset}&settings.delay={delay}&settings.region={region}&hidden={hidden}&status=UNSUBMITTED%1FIS_FAIL&settings.universe={universe}"            )            response = self.sess.get(url)            if response.status_code == 400:                self.logger.warning(                    f"遇到API限制 (offset过大)，停止获取更多数据。URL: {url}"                )                break  # 停止循环                   response_data = response.json()            if not isinstance(response_data, dict) or "results" not in response_data:                self.logger.error(f"API返回了意外的数据: {response_data}")                self.logger.error(f"请求的URL是: {url}")                self.logger.error(f"HTTP状态码是: {response.status_code}")                break            alphas = response.json()["results"]            if not alphas:                break            total_accessed += len(alphas)                   if required_fields:                if match_mode == "all":                    filtered_alphas = [                        alpha                        for alpha in alphas                        if all(                            field in alpha["regular"]["code"]                            for field in required_fields                        )                    ]                elif match_mode == "any":                    filtered_alphas = [                        alpha                        for alpha in alphas                        if any(                            field in alpha["regular"]["code"]                            for field in required_fields                        )                    ]                else:                    raise ValueError("match_mode 必须是 'all' 或 'any'")            else:                filtered_alphas = alphas            # 进一步筛选夏普比率和fitness            final_filtered = []            for alpha in filtered_alphas:                sharpe = alpha.get("is", {}).get("sharpe", 0)                fitness = alpha.get("is", {}).get("fitness", 0)                # 检查是否满足阈值条件                sharpe_ok = (min_sharpe is None) or (                    sharpe is not None and abs(sharpe) >= min_sharpe                )                fitness_ok = (min_fitness is None) or (                    fitness is not None and abs(fitness) >= min_fitness                )                if sharpe_ok and fitness_ok:                    # 如果启用了submittable，检查checks状态                    if submittable:                        checks = alpha.get("is", {}).get("checks", [])                        # 统计各种状态数量                        status_counts = {                            "PASS": 0,                            "FAIL": 0,                            "WARNING": 0,                            "PENDING": 0,                        }                        for check in checks:                            result = check.get("result", "UNKNOWN")                            if result in status_counts:                                status_counts[result] += 1                        # 检查fail数量是否为0                        fail_count = status_counts["FAIL"]                        # 如果fail数为0且启用了自动标记，标记为指定颜色                        if fail_count == 0 and auto_color:                            alpha_id = alpha.get("id")                            if alpha_id:                                success = self.update_alpha_color(alpha_id, color)                                if success:                                    colored_count += 1                                    # self.logger.info(f"已将Alpha {alpha_id} 标记为{color}")                        if fail_count == 0:  # 只保留fail数为0的                            final_filtered.append(alpha)                    else:                        final_filtered.append(alpha)            fetched_alphas.extend(final_filtered)            # 更新进度条            pbar.update(len(alphas))            pbar.set_postfix(                {                    "Region": region,                    "Delay": delay,                    "universe": universe,                    "required_fields": required_fields,                    "match_mode": match_mode,                    "已扫描": total_accessed,                    "找到": len(fetched_alphas),                    "本次": len(final_filtered),                    "标记": colored_count,                    "进度": f"{total_accessed}/{total_available}",                }            )            if len(alphas) < limit:                break            offset += limit        pbar.close()        # 输出标记统计        if auto_color and colored_count > 0:            self.logger.info(f"共标记了 {colored_count} 个Alpha颜色为{color}")            self.wechat_check_corr_message(                f"共标记了 {colored_count} 个Alpha颜色为{color}"            )        alpha_list = fetched_alphas[:total_alphas]        if not alpha_list:            self.logger.warning(                f"未找到任何符合条件的Alpha！请检查筛选条件是否过于严格。"            )        else:            df = pd.DataFrame(alpha_list)            # 先创建一个临时的fitness列，用于排序            df["temp_fitness"] = df.apply(                lambda row: (                    row["is"].get("fitness", 0)                    if isinstance(row.get("is"), dict)                    else 0                ),                axis=1,  # axis=1 表示按行操作            )                  df_sorted = df.sort_values(by="temp_fitness", ascending=False)                  df_sorted = df_sorted.drop("temp_fitness", axis=1)                     output_file_name = self.base_path / output_file_name            if mode == "w":                df_sorted.to_csv(output_file_name, index=False)            elif mode == "a":                df_sorted.to_csv(output_file_name, mode="a", index=False, header=False)            # 从排序后的DataFrame中获取前5个进行浏览            top_5_alphas = df_sorted.head(5).to_dict("records")            self.logger.info(                f"批量回测初步检测结果已经下载！共{len(alpha_list)}条记录！"                f"\n{output_file_name}文件名保存！"            )            # self.logger.info("为节省篇幅，现浏览前5个表达式（已按fitness降序排列）：")            # for item in top_5_alphas:            #     self.logger.info(            #         [            #             item["id"],            #             item["regular"]["code"],            #             item["is"]["sharpe"],            #             item["is"]["fitness"],            #         ]            # )            return alpha_list
```

 **辅助函数**

颜色标注函数

```
   def update_alpha_color(self, alpha_id, color):        update_data = {"color": color}        response = self.sess.patch(            f"https://api.worldquantbrain.com/alphas/{alpha_id}", json=update_data        )        return response.status_code == 200
```

会话sess获取我就省略，论坛有。

## 函数运行

我是在jupyter里运行的，具体如下

```
# region、universe保留空白为搜索全部region = "USA"delay = 1universe = "TOP3000"required_fields = ['put']match_mode = "all"total_alphas = 500min_sharpe = Nonemin_fitness = Nonehidden = "false"submittable = Trueauto_color = Truecolor = "GREEN"output_file_name = "alpha_to_prune_list.csv"mode = "w"alpha.high_get_alphas(    total_alphas=total_alphas,    region=region,    delay=delay,    universe=universe,    required_fields=required_fields,    match_mode=match_mode,    min_sharpe=min_sharpe,    min_fitness=min_fitness,    hidden=hidden,    submittable=submittable,    auto_color=auto_color,    color=color,    output_file_name=output_file_name,    mode=mode,)
```

### 运行截图

![图片](images/img_b569f09f60.png)

如果大家有不清楚不明白的，欢迎留言指正！

---

## 讨论与评论 (1)

### 评论 #1 (作者: MZ45384, 时间: 3个月前)

非常强大的方法。太厉害了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

