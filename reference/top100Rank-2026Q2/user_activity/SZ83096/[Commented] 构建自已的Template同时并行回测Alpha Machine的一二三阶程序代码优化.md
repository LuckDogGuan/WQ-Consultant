# 构建自已的Template同时，并行回测Alpha Machine的一二三阶程序代码优化

- **链接**: [Commented] 构建自已的Template同时并行回测Alpha Machine的一二三阶程序代码优化.md
- **作者**: LG37773
- **发布时间/热度**: 1年前, 得票: 19

## 帖子正文

## 一、背景：

在顾问的培训课程中，老师讲解到如何构建自已的Template。采用Template将自己的想法泛化为多个alpha。

那么我们构建好了自已的Template之后，会产生很多个由Template生成的alpha。 这些alpha和Alpha Machine生成的alpha混在一起，如何区分哪些是Template生成的alpha呢？

由于Template生成是由多个operator组成的，本身有点复杂，又如何避免Alpha Machine将这些alpha进行二阶和三阶的处理呢？而不去生成过于重叠的alpha表达式。

## 二、解决方案：

### 2.1、方案原理：

需要找到template 独特的区分方式，我们采用的方案是在alpha表达式中添加标识。标识是以/* 开始，以 */ 结束，可以包含多行文本。比如：/*T1*/   这是注释代码，不影响alpha表达式的正常运行。其中T1是代表第一个自已的Template的含义，这是自由定义的标识，可以写成自已喜欢的字符。以方便自己日后查询，精确定位到这个alpha。当有第二个Template时，可以将T1改成T2，从而无限地扩展下去，支持无穷多个Template。

### 2.2、实现步骤

#### **第一步：如何添加标识？**

在表达式的最前面，添加标识。以/* 和*/框住。如下图，在第一行添加/*T1*/。

![图片](images/img_d34973153f.png)

在程序中书写注释代码，和写表达式是一样的，非常简单，这里就省略。

- **添加标识有什么不好的影响？**

对于顾问评级中的一项指标（单个alpha中operator个数），我特意做过测试，添加标识和不添加标识是一样多的operator个数。所以添加标识对单个alpha中operator个数没有影响。

#### **第二步：做好了标识之后，接下来就是“**  **查询”**

为了精确地查询到由Template生成的alpha，创建一个新的函数get_template_alphas ()，函数中大部分代码与machine lib中的get_alphas()相同。添加了新的参数template_name，调用时传入自定义模板的名称，比如我们例子中的 /*T1*/

为了节省阅读的时间，只把改进的部分代码贴出来，有编程基础的同学复制即可。如果需要完整的函数代码，欢迎点赞留言。

```
def get_template_alphas(start_date, end_date, sharpe_th, fitness_th, region, alpha_num,template_name):  #新增参数template_name
```

```
            alpha_list = response.json()["results"]            for j in range(len(alpha_list)):                exp = alpha_list[j]['regular']['code']   #得到alpha中的表达式                if template_name in exp:           #判断表达式中是否包括标识                    alpha_id = alpha_list[j]["id"]                    name = alpha_list[j]["name"]
```

调用get_template_alphas ()的代码：

```
    output = get_template_alphas('03-09','03-10',1.2, 1,'EUR',100,'/*T1*/')    print(output)
```

#### 

#### **第三步：将Template**  **生成的alpha**  **隔离出来**

对Alpha Machine进行一点小的改进，就可以实现隔离。我们在运行Alpha Machine.ipynb时，添加如下代码：

```
#定义一个列表，存放需要隔离的标识excluded_alpha_expressions  = ['/*T']
```

```
#在first order的程序中，实现隔离for alpha in first_order:    if any(char in alpha for char in excluded_alpha_expressions): continue   # added by new version    fo_alpha_expression_list.append((alpha, init_decay))
```

```
#在second order的程序中，实现隔离for expr, decay in fo_layer:    if any(char in expr for char in excluded_alpha_expressions): continue   # added by new version    for alpha in get_group_second_order_factory([expr], group_ops, "USA"):        so_alpha_list.append((alpha,decay))
```

```
for expr, decay in so_layer:    if any(char in expr for char in excluded_alpha_expressions):continue   # added by new version    for alpha in trade_when_factory("trade_when",expr,"USA"):        th_alpha_list.append((alpha,decay))
```

- 小贴士:

excluded_alpha_expressions的列表中，没有将T1,T2,T3…每个template都列示出来，而是采用/*T来作为标识。这样处理的好处是：每次增加新的Template，可以不用修改程序。

## **三、增强的扩展功能：**

采用这个代码，可以扩展使用在其他地方。比如：可以避免三阶的表达式又重复地被二阶factory进行组装。

我们只需要在excluded_alpha_expressions的列表中添加trade_when即可。

```
excluded_alpha_expressions  = ['/*T','trade_when']
```

```
#在second order的程序中，实现隔离for expr, decay in fo_layer:    if any(char in expr for char in excluded_alpha_expressions): continue   # added by new version    for alpha in get_group_second_order_factory([expr], group_ops, "USA"):        so_alpha_list.append((alpha,decay))
```

就可以轻松将二阶factory和三阶factory进行隔离。

*我们不断地扩展alpha machine的功能，更好地生成alpha。希望能够帮助到大家，欢迎大家在评论区留言。*

---

## 讨论与评论 (10)

### 评论 #1 (作者: CL63008, 时间: 1年前)

好用！！！特别是二阶factory和三阶factor隔离的程序，代码简洁实用

---

### 评论 #2 (作者: BY28155, 时间: 1年前)

我想要完整代码。非常有用。

---

### 评论 #3 (作者: SZ83096, 时间: 1年前)

新思路，在alpha 表达式层面对alpha进行区别，挺好的

---

### 评论 #4 (作者: LL87164, 时间: 1年前)

换一个思路怎么样，把excluded换成included？

即：在一二阶的组装代码里加个标注（如/*fo*/  ），在后续的组装中按这个标注来过滤出要操作的alpha。

---

### 评论 #5 (作者: DZ31817, 时间: 1年前)

不错，在代码中添加注释标识也是我一直采用的方法，这比设置属性更快。关于隔离的做法，我是反过来的，我是在需要跑二或三阶时，筛选出我需要的标识的alpha再来组装二三阶，这样可能更直观一些。

---

### 评论 #6 (作者: LL62621, 时间: 1年前)

wq 提供了tag功能，完全没必要添加注释去实现

如图

![图片](images/img_1aff6c94c6.png)

machinelib中也有相应的方法

```
def set_alpha_properties(    s,    alpha_id,    name: str = None,    color: str = None,    selection_desc: str = "None",    combo_desc: str = "None",    tags: str = ["ace_tag"],):    """    Function changes alpha's description parameters    """     params = {        "color": color,        "name": name,        "tags": tags,        "category": None,        "regular": {"description": None},        "combo": {"description": combo_desc},        "selection": {"description": selection_desc},    }    response = s.patch(        "https://api.worldquantbrain.com/alphas/" + alpha_id, json=params    )
```

同时，我觉得只用name去分隔其实就差不多了，足够使用

---

### 评论 #7 (作者: ZR63005, 时间: 1年前)

楼主的IDEA非常实用，这里给出两个自己的想法：

一、兼容get_alphas的代码修改

首先给出一个能够兼容原始get_alphas使用的修改，可直接替换machine_lib中原有的get_alphas方法。
在不需要使用template_name的时候可以直接空白

```
def get_alphas(    start_date,    end_date,    sharpe_th,    fitness_th,    region,    alpha_num,    usage,    template_name=None,  # template_name = "/*T_XXXXXX*/"):    s = login()    output = []    # 3E large 3C less    count = 0    for i in range(0, alpha_num, 100):        print(i)        url_e = (            "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"            % (i)            + "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=2025-"            + start_date            + "T00:00:00-04:00&dateCreated%3C2025-"            + end_date            + "T00:00:00-04:00&is.fitness%3E"            + str(fitness_th)            + "&is.sharpe%3E"            + str(sharpe_th)            + "&settings.region="            + region            + "&order=-is.sharpe&hidden=false&type!=SUPER"        )        url_c = (            "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d"            % (i)            + "&status=UNSUBMITTED%1FIS_FAIL&dateCreated%3E=2025-"            + start_date            + "T00:00:00-04:00&dateCreated%3C2025-"            + end_date            + "T00:00:00-04:00&is.fitness%3C-"            + str(fitness_th)            + "&is.sharpe%3C-"            + str(sharpe_th)            + "&settings.region="            + region            + "&order=is.sharpe&hidden=false&type!=SUPER"        )        urls = [url_e]        if usage != "submit":            urls.append(url_c)        for url in urls:            response = s.get(url)            # print(response.json())            try:                alpha_list = response.json()["results"]                # print(response.json())                for j in range(len(alpha_list)):                    if (                        template_name != None                        and template_name not in alpha_list[j]["regular"]["code"]                    ):                        continue                    alpha_id = alpha_list[j]["id"]                    name = alpha_list[j]["name"]                    dateCreated = alpha_list[j]["dateCreated"]                    sharpe = alpha_list[j]["is"]["sharpe"]                    fitness = alpha_list[j]["is"]["fitness"]                    turnover = alpha_list[j]["is"]["turnover"]                    margin = alpha_list[j]["is"]["margin"]                    longCount = alpha_list[j]["is"]["longCount"]                    shortCount = alpha_list[j]["is"]["shortCount"]                    decay = alpha_list[j]["settings"]["decay"]                    exp = alpha_list[j]["regular"]["code"]                    count += 1                    # if (sharpe > 1.2 and sharpe < 1.6) or (sharpe < -1.2 and sharpe > -1.6):                    if (longCount + shortCount) > 100:                        if sharpe < -sharpe_th:                            exp = "-%s" % exp                        rec = [                            alpha_id,                            exp,                            sharpe,                            turnover,                            fitness,                            margin,                            dateCreated,                            decay,                        ]                        print(rec)                        if turnover > 0.7:                            rec.append(decay * 4)                        elif turnover > 0.6:                            rec.append(decay * 3 + 3)                        elif turnover > 0.5:                            rec.append(decay * 3)                        elif turnover > 0.4:                            rec.append(decay * 2)                        elif turnover > 0.35:                            rec.append(decay + 4)                        elif turnover > 0.3:                            rec.append(decay + 2)                        output.append(rec)            except:                print("%d finished re-login" % i)                s = login()    print("count: %d" % count)    return output
```

使用方法如下：

```
first_order_alphas = get_alphas(        "03-14",        "03-16",        1.2,        1,        region,        100,        "track",        template_name="/*T_GLB_TOP3000_ANL14_1_FIRST*/",    )
```

二、注释标识的管理

楼主提到可以通过屏蔽的方式避免/*T_XXX*/的多次出现。但实际上经过多次迭代后，很容易出现一个代码中包含多个/*T_XX*/的情况，导致难以管理。因此可以考虑每次在上一个阶段的alpha基础上生成新一阶alpha时，都删除原有标识，从而保证管理的便捷。可以通过编写类似于如下代码的程序实现

```
first_order_alphas = get_alphas(        "03-14",        "03-16",        1.2,        1,        region,        100,        "track",      template_name="/*T_GLB_TOP3000_ANL14_1_FIRST*/",    )ALPHA_LIST = []    for expr in first_order_alphas:        for alpha in get_group_second_order_factory([expr[1]], group_ops, region):            alpha = alpha.replace("/*T_GLB_TOP3000_ANL14_1_FIRST*/", "") # 删除上一阶段的注释标识            # 如果会使用正则表达式，可以直接使用/\*T_(?:[^*]*\*[^/])*\*/替换全部注释            ALPHA_LIST.append([f"/*T_GLB_TOP3000_ANL14_1_SECOND*/{alpha}", expr[-1]]) # 在alpha头部加入新的注释标识
```

通过这种方式，能够保证每次注释标识都在alpha最开始的地方，便于查找。同时避免了后续进行更多层生成时注释标识混乱的问题。
进一步的，也可以通过不同的开头，不同的结尾，标记不同类型，例如T1_XXX代表使用template的一阶，H_代表通过论文自己写的alpha等等。

以上是两点建议，若您觉得有用，欢迎给我以及楼主点赞评论。

---

### 评论 #8 (作者: ZR63005, 时间: 1年前)

[LL62621](/hc/en-us/profiles/27135159800727-LL62621) 
properties的设置需要在alpha生成之后，使用alpha_id发送新的请求。
在目前使用multi-simulation的情况下，其实只能在check的时候，用multi-simulation的id，遍历其children实现。
如果代码在未接收到simulation运行结束的情况下，很容易导致properties未被设置（如name、tag等），从而“跟丢”这些alphas。

上述是我暂时没有使用properties来为alpha打标签的原因。非常希望听到您是如何对alpha进行可靠跟踪的，谢谢！

---

### 评论 #9 (作者: MG22853, 时间: 1年前)

感谢楼主！！很好用的功能。

同时在代码能力不是很强的情况下，我是在前两轮使用get_alphas之后添加以下语句：把exp（表达式）中不含有“trade_when”（含有“trade_when”个数为0）的筛选出来

二阶前：

```
fo_tracker = [alpha_info for alpha_info in fo_tracker if alpha_info[1].count('trade_when') == 0]
```

三阶前：

```
so_tracker = [alpha_info for alpha_info in so_tracker if alpha_info[1].count('trade_when') == 0]
```

---

### 评论 #10 (作者: WC53907, 时间: 7个月前)

我是定义了一个辅助函数，作为对exp检索的补充条件。

辅助函数代码：

```
def _contains_data_field(self, exp, required_data_fields, match_all=False):    """    辅助函数，支持模糊查询    exp 待匹配的表达式    required_data_fields 要匹配的字符串关键词列表    match_all  False表示满足任一即可(OR)，True表示必须全部包含(AND)    """    if not required_data_fields:        return True    matched_count = 0    for field in required_data_fields:        pattern = re.escape(field)        if re.search(pattern, exp, re.IGNORECASE):            if not match_all:  # OR模式，匹配到一个就返回                return True            matched_count += 1    # AND模式，需要全部匹配    return matched_count == len(required_data_fields) if match_all else False
```

同时对get_alpha()进行了微调，更新部分如下：

```
def get_alphas(self, start_date, end_date,               sharpe_th, fitness_th,               delay, region,               search_deepth, usage,               required_data_fields=None,               match_all=False):
```

```
exp = alpha_list[j]['regular']['code']# 对关键字列表中的字符串进行模糊查找# 全部匹配，match_all为Trueif not self._contains_data_field(exp, required_data_fields, match_all):  # 全部匹配，match_all    continue
```

但从使用体验而言，还是你的方法好，直接从源头解决问题。

补充：我把alpha相关功能定义为类的方法，有代码基础的同学应该很容易搞定，我就不单独修改了。

---

