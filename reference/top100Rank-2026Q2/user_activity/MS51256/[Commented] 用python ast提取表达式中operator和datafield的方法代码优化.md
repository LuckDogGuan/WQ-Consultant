# 用python ast提取表达式中operator和datafield的方法代码优化

- **链接**: [Commented] 用python ast提取表达式中operator和datafield的方法代码优化.md
- **作者**: WL27618
- **发布时间/热度**: 1年前, 得票: 13

## 帖子正文

python ast可以自动解析符合python规范的代码表达式. 因此把我们的alpha转换成python可以理解的方式就能解析了, 这样避免了每次字符串的解析(写正则表达式之类). 可以用来在跑模版的时候检测datafield是否符合规范, 也可以用来统计自己使用的各种datafield, operators频率.

代码如下:

import ast

import re

def parse_alpha(alpha_expression):

"""

Parses an alpha expression and extracts operators and data fields.

This function processes a given alpha expression by converting ternary expressions,

fixing indentation errors, and parsing it into an abstract syntax tree (AST). It then

traverses the AST to extract operators and data fields, while filtering out defined

variables, NaN values, and Python built-in functions and keywords.

Args:

alpha_expression (str): The alpha expression to be parsed.

Returns:

dict: A dictionary containing two lists:

- 'operators': A list of unique operators (function and method names) found in the expression.

- 'data_fields': A list of unique data fields (variable names) found in the expression, excluding defined variables and NaN values.

"""

# 处理三元表达式

alpha_expression = alpha_expression.replace('?',' if ').replace(':',' else ')

# 处理和python内置逻辑表达式冲突

alpha_expression = re.sub(r'\band\b', 'and_', alpha_expression) # 替换独立的 'and'

alpha_expression = re.sub(r'\band\(', 'and_(', alpha_expression) # 替换 'and('

alpha_expression = re.sub(r'\bor\b', 'or_', alpha_expression) # 替换独立的 'or'

alpha_expression = re.sub(r'\bor\(', 'or_(', alpha_expression) # 替换 'or('

# 处理逻辑表达式

alpha_expression = alpha_expression.replace('!',' not ').replace('&&',' and ')

# 处理range="0.1,1,0.1" 类似表达式

alpha_expression = re.sub(r'"([^"]*)"', "0", alpha_expression)

# 处理缩进错误，尝试修复

alpha_expression = "\n".join(line.strip() for line in alpha_expression.splitlines())

# 解析表达式为抽象语法树 (AST)

tree = ast.parse(alpha_expression)

# 提取 operators 和 data fields

operators = set()

data_fields = set()

# 提取过程中定义的变量

defined_variables = set()

# 遍历 AST

for node in ast.walk(tree):

# 提取赋值语句中的变量名

ifisinstance(node, ast.Assign):

for target in node.targets:

ifisinstance(target, ast.Name):

defined_variables.add(target.id) # 记录定义的变量名

# 提取函数调用 (operators)

ifisinstance(node, ast.Call):

ifisinstance(node.func, ast.Name):

operators.add(node.func.id) # 函数名

elifisinstance(node.func, ast.Attribute):

operators.add(node.func.attr) # 方法名

# 提取变量名 (data fields)

ifisinstance(node, ast.Name):

data_fields.add(node.id) # 变量名

# 提取三元条件表达式

ifisinstance(node, ast.IfExp):

# 提取条件部分

ifisinstance(node.test, ast.Compare):

for comparator in node.test.comparators:

ifisinstance(comparator, ast.Name):

data_fields.add(comparator.id)

# 提取 if 部分

ifisinstance(node.body, ast.Name):

data_fields.add(node.body.id)

# 提取 else 部分

ifisinstance(node.orelse, ast.Name):

data_fields.add(node.orelse.id)

# 过滤掉过程中定义的变量

data_fields = data_fields - defined_variables

# 过滤掉特殊变量nan

data_fields = data_fields - set(['nan','true','false'])

# 过滤掉 Python 内置函数和关键字

builtin_functions = set(dir(__builtins__)) # Python 内置函数

operators = operators - builtin_functions # 去掉内置函数

data_fields = data_fields - builtin_functions - operators # 去掉内置函数

return {'operators':list(operators),"data_fields":list(data_fields)}

目前这个版本我自己用着是没发现什么解析错误的问题. 欢迎大家指正.

---

## 讨论与评论 (7)

### 评论 #1 (作者: ZZ44620, 时间: 1年前)

感谢大佬分享，调用时发现如果有注释/*T1*/会报错，需要添加一行

```
    # 预处理: 移除C风格注释    alpha_expression = re.sub(r'/\*.*?\*/', '', alpha_expression)
```

---

### 评论 #2 (作者: WP88606, 时间: 1年前)

或许还有另一种思路，就是在从头生成代码的过程中，把用到的字段和操作符记录到注释里，定义好格式，这样就能保证一定是准确的了，不过之前的代码就只能解析了。

---

### 评论 #3 (作者: HQ17963, 时间: 1年前)

感谢大佬分享，用AI修正了空格，方便大家取用，版权归原作者所有😊

> import ast
> import re
> def parse_alpha(alpha_expression):
> """
> Parses an alpha expression and extracts operators and data fields.
> This function processes a given alpha expression by converting ternary expressions,
> fixing indentation errors, and parsing it into an abstract syntax tree (AST). It then
> traverses the AST to extract operators and data fields, while filtering out defined
> variables, NaN values, and Python built-in functions and keywords.
> Args:
> alpha_expression (str): The alpha expression to be parsed.
> Returns:
> dict: A dictionary containing two lists:
> - 'operators': A list of unique operators (function and method names) found in the expression.
> - 'data_fields': A list of unique data fields (variable names) found in the expression,
> excluding defined variables and NaN values.
> """
> # 预处理: 移除//和#注释
> alpha_expression = re.sub(r'(?m)^\s*(//|#).*\n?', '', alpha_expression)
> # 处理三元表达式
> alpha_expression = alpha_expression.replace('?', ' if ').replace(':', ' else ')
> # 处理和 python 内置逻辑表达式冲突
> alpha_expression = re.sub(r'\band\b', 'and_', alpha_expression)  # 替换独立的 'and'
> alpha_expression = re.sub(r'\band\(', 'and_(', alpha_expression)  # 替换 'and('
> alpha_expression = re.sub(r'\bor\b', 'or_', alpha_expression)  # 替换独立的 'or'
> alpha_expression = re.sub(r'\bor\(', 'or_(', alpha_expression)  # 替换 'or('
> # 处理逻辑表达式
> alpha_expression = alpha_expression.replace('!', ' not ').replace('&&', ' and ')
> # 处理 range="0.1,1,0.1" 类似表达式
> alpha_expression = re.sub(r'"([^"]*)"', "0", alpha_expression)
> # 处理缩进错误，尝试修复
> alpha_expression = "\n".join(line.strip() for line in alpha_expression.splitlines())
> # 解析表达式为抽象语法树 (AST)
> tree = ast.parse(alpha_expression)
> # 提取 operators 和 data fields
> operators = set()
> data_fields = set()
> # 提取过程中定义的变量
> defined_variables = set()
> # 遍历 AST
> for node in ast.walk(tree):
> # 提取赋值语句中的变量名
> if isinstance(node, ast.Assign):
> for target in node.targets:
> if isinstance(target, ast.Name):
> defined_variables.add(target.id)  # 记录定义的变量名
> # 提取函数调用 (operators)
> if isinstance(node, ast.Call):
> if isinstance(node.func, ast.Name):
> operators.add(node.func.id)  # 函数名
> elif isinstance(node.func, ast.Attribute):
> operators.add(node.func.attr)  # 方法名
> # 提取变量名 (data fields)
> if isinstance(node, ast.Name):
> data_fields.add(node.id)  # 变量名
> # 提取三元条件表达式
> if isinstance(node, ast.IfExp):
> # 提取条件部分
> if isinstance(node.test, ast.Compare):
> for comparator in node.test.comparators:
> if isinstance(comparator, ast.Name):
> data_fields.add(comparator.id)
> # 提取 if 部分
> if isinstance(node.body, ast.Name):
> data_fields.add(node.body.id)
> # 提取 else 部分
> if isinstance(node.orelse, ast.Name):
> data_fields.add(node.orelse.id)
> # 过滤掉过程中定义的变量
> data_fields = data_fields - defined_variables
> # 过滤掉特殊变量 nan
> data_fields = data_fields - set(['nan', 'true', 'false'])
> # 过滤掉 Python 内置函数和关键字
> builtin_functions = set(dir(__builtins__))  # Python 内置函数
> operators = operators - builtin_functions  # 去掉内置函数
> data_fields = data_fields - builtin_functions - operators  # 去掉内置函数
> return {'operators': list(operators), "data_fields": list(data_fields)}

---

### 评论 #4 (作者: HQ17963, 时间: 1年前)

[@ZZ44620](/hc/en-us/profiles/28856702901527-ZZ44620) ：

好像不太管用，我改成了

> # 预处理: 移除//和#注释
> alpha_expression = re.sub(r'(?m)^\s*(//|#).*\n?', '', alpha_expression)

经过测试没问题

---

### 评论 #5 (作者: ZS59763, 时间: 1年前)

提供一个新的思路，如果是走一二三阶段的路子，可以试着用backfill来抓取（当然，向量类型每种向量运算符都算一个），详细的可以参考： [如何统计得到的字段数？如何抓取多地区因子一起检验？ – WorldQuant BRAIN](/hc/en-us/community/posts/28754183939351-%E5%A6%82%E4%BD%95%E7%BB%9F%E8%AE%A1%E5%BE%97%E5%88%B0%E7%9A%84%E5%AD%97%E6%AE%B5%E6%95%B0-%E5%A6%82%E4%BD%95%E6%8A%93%E5%8F%96%E5%A4%9A%E5%9C%B0%E5%8C%BA%E5%9B%A0%E5%AD%90%E4%B8%80%E8%B5%B7%E6%A3%80%E9%AA%8C)

---

### 评论 #6 (作者: MS51256, 时间: 1年前)

非常有用的功能，可以实现对op field的统计  从而知道哪些被使用的而去使用别的数据或者操作符
===========================================================================================================================================================================================================================================================

---

### 评论 #7 (作者: DZ31817, 时间: 1年前)

感谢分享，这个代码对于降低六维的op avg和df avg具有重要作用，我可以使用这个代码统计每个候选alpha的op数和df数，然后从中挑选少的来交，从而降低avg。不过原代码中对op和df做了去重处理，而六维统计avg时不会去重，因此如果要用于降avg用途的op、df非去重统计，需要做一定修改，主要是将原代码中用来储存op和df的去重的集合set改为不会去重的列表即可。

---

