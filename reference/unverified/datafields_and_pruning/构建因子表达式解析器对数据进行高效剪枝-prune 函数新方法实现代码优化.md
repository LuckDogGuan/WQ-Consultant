# 构建因子表达式解析器对数据进行高效剪枝-prune 函数新方法实现代码优化

- **Author**: DM89198
- **Date**: 2025年03月12日 08:30
- **Votes**: 11
- **Article ID**: 30584578183063

## Content

剪枝对我们的因子挖掘是十分重要的，高效的剪枝能大大提高我们的生产质量。
论坛里有不少人也发过对prune函数的改进贴子，我这里也提供一种剪枝的方法供大家参考。
为什么要剪枝？
按我理解是为了去自相关。我们提交因子都会遇到过SelfCorrelation 大于0.7的失败。
也就是说没有经过有效的剪枝，前面做的很多工作都是无用功。
那么如何降低自相关？
我们的一阶表达式是通过遍历时间窗口产生大量的因子表达式，或者二阶表达式是通过遍历不同的分组来产生大量因子表达式。
如果你的表达式组合结构都是一样的，只是参数不同。那么必然是只能有一个能成功提交的
比如  ts_op(op(x), d1), ts_op(op(x), d2) , 如果只有d1和d2不同，即使是都达到提交标准，那必然是只会有一个能成功

根据上面的分析，那么对于数据字段我们只需保留它一个相同表达式组合结构的因子去进行迭代就可以了。

1 首先需要识别出表达式里的数据字段 x
平台提供的通用模板 x 都是通过填充来进行预处理。 那么我们可以根据此进行正则匹配，把数据字段取出来

```python
regtx = r'ts_backfill\s*\(\s*(\w+)\s*,\s*'    p = re.compile(r'ts_backfill\s*\(\s*(\w+)\s*,\s*')  exp = "ts_backfill(AAbbccdd_123_XXxx, 66)"  match = p.search(exp)  if match:    x = match.group(1)
```

经过我的观测，一阶表达式或二阶表达式，数据字段x的位置只会有两种情况
1: (x,  2: (x)

于是我的通用型正则匹配是(这方法不会受到 ts_backfill 的制约)

```python
def get_regular_field(expression: str) -> str:    field_regular = [r'\(\s*(\w+)\s*,\s*', r'\(\s*(\w+)\s*\)\s*']    field_patterns = [re.compile(regular) for regular in field_regular]      for p in field_patterns:        math = p.search(expression)        if math:            return math.group(1)
```

p.search()  会返回第一个匹配到的数据。所以你只需要保证在多个(x)这种结构的出现，数据字段是在最前面就没有问题。

2 识别出表达式所用到的操作符及其顺序
cross_ops 代表你用到的所有横截面操作符列表
ts_ops 代表你用到的所有时序操作符列表
group_ops 代表你用到的所有分组操作符列表

```python
def parse_expression(expression: str) -> List[str]:   ops = cross_ops + ts_ops + group_ops   field = get_regular_field(expression)       elements = set(op for op in ops if op in expression)    elements.add(field)   pattern = '|'.join(re.escape(element) for element in elements)   return re.findall(pattern, expression)
```

3 关于三阶表达式的解析
三阶表达式用到的操作符结构是 trade_when(x, y, z)   其中y 就是我们的组合的二阶表达式。x, z 是可变策略条件。
y 是这个因子的主要信号来源，通常只要y 相同，x, z 无论怎样变化，他们的自相关都会很高。
因此，我们只需要把y解析出来，用来分组，就能对相同结构的alpha进行剪技

```python
def get_regular(trade_when_expression: str) -> str:    # 把表达式 trade_when(x, y, z) 转换为  x, y, z    expr_clean = trade_when_expression.split('trade_when', 1)[1].strip(' ()')    params = []    stack = 0    current = []     for char in expr_clean:      if char == '(':        stack += 1      elif char == ')':        stack -= 1      if char == ',' and stack == 0:        params.append(''.join(current).strip())        current = []      else:        current.append(char)      if current:  # 最后一个参数        params.append(''.join(current).strip())        # params  就是 [x, y, z]      return params[1]  # 把y取出来
```

4 prune 剪枝函数优化
有了上面的认识，我们就可以构建一个表达式解析器。运用这个解析器对数据进行剪枝。
我的数据用到 DataFrame 做排序合并等操作，建议大家使用DataFrame

```python
def prune(df: DataFrame) -> DataFrame:    print(f"剪枝前：{len(df)}")      df = df.copy()     rb = RegularBuilder()   # 创建一个解析器，后面会给出这个解析器的完整代码      # regular 列就是你的alpha的表达式，我是提取出来放在一个列上处理      # exp 列就是把alpha的表达式通过解析器提取出表达式的结构，再转成字符串    df.loc[:,"exp"] = df["regular"].apply(rb.parse_expression).astype(str)     df.loc[:,"abs_sharpe"] = df["sharpe"].abs()    df.loc[:,"abs_fitness"] = df["fitness"].abs()      # 按照'abs_sharpe'降序和'abs_fitness'降序进行排序    df_sort = df.sort_values(by=['abs_sharpe', 'abs_fitness'], ascending=[False, False])    # 排序后重置索引    df = df_sort.reset_index(drop=True)    # 使用groupby按exp列分组，exp 存的是表达式的结构，同一个数据字段相同结构的会放在一起    grouped = df.groupby('exp')      # 创建一个列表以存储每个组的Top1    group_list = []        for name, group in grouped:        group_list.append(group.head(1))   # 由于前面排序过，head(1) 就是sharpe，fitness 最高的那一条      df = concat(group_list).reset_index(drop=True)    print(f"剪枝后：{len(df)}")    return df
```

5 完整解析器代码

```python
import reclass RegularBuilder:   def __init__(self):       field_regular = [r'\(\s*(\w+)\s*,\s*', r'\(\s*(\w+)\s*\)\s*']       self.field_patterns = [re.compile(regular) for regular in field_regular]         first_op_regular = r'(\w+)\s*\('       self.first_op_pattern = re.compile(first_op_regular)       self.ops = list(set(ts_ops + cross_ops + group_ops + decay_ops))   def _extract_parameters(self, trade_when_expression: str) -> List[str]:       """       示例输入: "trade_when(x, y, z)"       输出: [x, y, z]       """       expr_clean = trade_when_expression.split('trade_when', 1)[1].strip(' ()')       params = []       stack = 0       current = []        for char in expr_clean:         if char == '(':            stack += 1         elif char == ')':            stack -= 1         if char == ',' and stack == 0:            params.append(''.join(current).strip())            current = []         else:             current.append(char)        if current:  # 最后一个参数         params.append(''.join(current).strip())      return params[:3]  # 保证x,y,z三个参数    def get_regular(self, trade_when_expression: str) -> str:      params = self._extract_parameters(trade_when_expression)      return params[1]    def get_regular_field(self, expression: str) -> str:      if "trade_when" in expression:          expression = self.get_regular(expression)        for p in self.field_patterns:          math = p.search(expression)          if math:              return math.group(1)      else:          return ""    # 取表达式的第一个操作符    def get_first_op(self, expression: str) -> str:      if "trade_when" in expression:          expression = self.get_regular(expression)        if expression.startswith("-"):          expression = expression[1:]        math = self.first_op_pattern.search(expression)      if math:          return math.group(1)      return ""    def parse_expression(self, expression: str) -> List[str]:      """      示例输入: "group_op(ts_op(x, d), group)"      输出: [group_op, ts_op, x]      解析一阶、二阶、三阶 表达式，返回组合结构列表      :param expression:      :return:      """      if "trade_when" in expression:         expression = self.get_regular(expression)         return ["trade_when", expression]        field = self.get_regular_field(expression)      elements = set(op for op in self.ops if op in expression)      elements.add(field)      pattern = '|'.join(re.escape(element) for element in elements)        return re.findall(pattern, expression)
```

## Comments

### Comment 1
- **Author**: JL16510
- **Date**: 2025年03月13日 03:56

点赞。一二三阶跑出数据相关性确实很大，这也是一种减少check的办法。

---

### Comment 2
- **Author**: HJ33503
- **Date**: 2025年03月30日 11:05

====================================================================================

确实一二三阶很多时候会出现同一字段很多类似表现的alpha，提交一个后面的都不能提交的情况，我也是使用re去限制了每个field抓取的alpha数量，尽量去提升回测效率。

====================================================================================

---

