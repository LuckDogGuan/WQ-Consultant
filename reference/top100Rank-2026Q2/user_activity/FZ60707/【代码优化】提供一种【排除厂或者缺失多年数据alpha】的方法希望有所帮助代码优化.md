# 【代码优化】提供一种【排除厂或者缺失多年数据alpha】的方法，希望有所帮助代码优化

- **链接**: 【代码优化】提供一种【排除厂或者缺失多年数据alpha】的方法希望有所帮助代码优化.md
- **作者**: FZ60707
- **发布时间/热度**: 1年前, 得票: 41

## 帖子正文

问题背景：在check的时候由于只设置了相关性低的条件，同时因为【厂或者缺失多年数据】的alpha本身就与其他alpha的相关性低，所以经常check出来的alpha点进去一看是厂或者缺失数据的，又需要再一次人工去筛选，加大了人工的时间。解决思路：通过观察注意到，厂或者缺失多年数据的alpha拥有共同特点，就是有很多年份的sharpe值都为0，比如：那么解决的方式就是，获取到上述表格每年的shapre，然后通过判断等于0的年份有几年即可。常听到说最好交8年有数据的alpha，那么判断条件就是sharpe不等于0的年份大于8就可以了。最终代码：def check_alpha_sharpe_conditions(s, alpha_id):# Get the yearly stats dataa = wait_get(s, f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats").json()data = a['records']# Extract sharpe values (7th parameter in each record, index 6)sharpe_values = [float(record[6]) for record in data]# Check conditions:# 1. At least 8 years with sharpe != 0non_zero_sharpe = sum(1 for sharpe in sharpe_values if sharpe != 0)condition1 = non_zero_sharpe >= 8# Return True if both conditions are metreturn condition1上面代码先获取每年的sharpe数据，然后保存到列表中，最后判断sharpe不为0的年份是否大于8即可。代码扩展：除了拥有8年数据外，一般还可以要求至少6年的shapre大于1，从而保证alpha的稳健性。也可以要求2022年shapre大于1，从而保证近几年的情况良好，不至于说sharpe高是只是因为旧年份导致的。代码改进：def check_alpha_sharpe_conditions(s, alpha_id):# Get the yearly stats dataa = wait_get(s, f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets/yearly-stats").json()data = a['records']# Extract sharpe values (7th parameter in each record, index 6)sharpe_values = [float(record[6]) for record in data]# Check conditions:# 1. At least 8 years with sharpe != 0non_zero_sharpe = sum(1 for sharpe in sharpe_values if sharpe != 0)condition1 = non_zero_sharpe >= 8# 2. At least 6 years with sharpe > 1sharpe_above_1 = sum(1 for sharpe in sharpe_values if sharpe > 1)condition2 = sharpe_above_1 >= 6print(alpha_id+":sharpe检测:"+str(condition1 and condition2 and  data[9][6]>0.8))# Return True if both conditions are metreturn condition1 and condition2 and  data[9][6]>1  #2022年的sharpe大于1第一个条件依然是8年shapre不为0，第二个条件是至少有6年的shapre大于1。最终的data[9][6]>1的意思是2022年的sharpe大于1。2013-2023年中2022年的是第10年，索引是9，sharpe数据在api的['records']的索引是6，所以是data[9][6]。你也可以扩展自己的条件。补充：获取api的方式可以按【f12-网络-然后刷新网页-名称列表-标头】进行查询。比如上述代码中的api来源如下：然后通过【响应】来看获取到的数据结构是如何的：代码补充：代码中用到了wait_get方法，是其他顾问提供的，用session基本的get方法也可以有同样的效果，该方法是进行了一些改进，增加了等待时间的get。def wait_get(s,url: str, max_retries: int = 10) -> "Response":"""发送带有重试机制的 GET 请求，直到成功或达到最大重试次数。此函数会根据服务器返回的 `Retry-After` 头信息进行等待，并在遇到 401 状态码时重新初始化配置。Args:url (str): 目标 URL。max_retries (int, optional): 最大重试次数，默认为 10。Returns:Response: 请求的响应对象。"""retries = 0while retries < max_retries:while True:simulation_progress = s.get(url)if simulation_progress.headers.get("Retry-After", 0) == 0:breaktime.sleep(float(simulation_progress.headers["Retry-After"]))if simulation_progress.status_code < 400:breakelse:time.sleep(2 ** retries)retries += 1return simulation_progress希望对大家有所帮助，一起进步！！

---

## 讨论与评论 (5)

### 评论 #1 (作者: BW14163, 时间: 11个月前)

学习了，很有帮助，刚到达consult，每天人工去找alpha，最怕碰到厂字，非常浪费时间，根据本贴大佬的代码，很好的解决了这个问题

---

### 评论 #2 (作者: BW14163, 时间: 10个月前)

3个条件感觉挺好的，实现了一下，准备加到二阶回测之前的条件判断里面，没有别的大佬评论，感觉有点心慌慌啊At least 8 years with sharpe != 0At least 6 years with sharpe > 1data[9][6]>1  #2022年的sharpe大于1

---

### 评论 #3 (作者: FZ60707, 时间: 10个月前)

@BW14163别的大佬都有自己的妙招，^_^哈哈。有用就好，有用就好。我后面又加了一些条件，把return,turnover,drawdown也纳入了。可以给个参考：return/turnover > 0.75 .return > drawdown 的年份大于7年.后面我感觉22年sharpe 大于1有点太严格了，改成0.8了。或者是2020-2022三年的平均sharpe 大于1，看一个平均值也可以。 这里就可以自由发挥了。不过这新的条件是在给ppa打tag的时候才用的，因为想提高一下每月的那个成绩，平常交alpha还是没有那么严格。====================================================================================================================================================================================================================================================================================================================================

---

### 评论 #4 (作者: LZ14923, 时间: 9个月前)

太感谢了，最近正好碰到一堆好几年sharpe数据为0的alpha，一个个手动排查太麻烦了！

---

### 评论 #5 (作者: WC64477, 时间: 6个月前)

虽然不是那么严谨，但确实比识别pnl要简单，计算量要小，比较实用

---

