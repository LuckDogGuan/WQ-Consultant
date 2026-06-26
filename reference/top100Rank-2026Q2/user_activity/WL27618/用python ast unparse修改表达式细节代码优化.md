# 用python ast unparse修改表达式细节代码优化

- **链接**: 用python ast unparse修改表达式细节代码优化.md
- **作者**: WL27618
- **发布时间/热度**: 10个月前, 得票: 66

## 帖子正文

我在  [**用**  **python ast**  **提取表达式中**  **operator**  **和**  **datafield**  **的方法**](/hc/en-us/community/posts/30870358077463-%E7%94%A8python-ast%E6%8F%90%E5%8F%96%E8%A1%A8%E8%BE%BE%E5%BC%8F%E4%B8%ADoperator%E5%92%8Cdatafield%E7%9A%84%E6%96%B9%E6%B3%95) 这个帖子里写过可以把wq表达式转为python表达式解析. 更进一步, 因为ast的操作性比字符串强得多, 我们可以在ast时期对表达式进行想要的修改, 然后再unparse回wq表达式去进行回测.

举例来说,  **可以对表达式做消融, 去掉实际上对结果没帮助的operator** . 这在字符串上操作千难万难, 不过在ast操作就还好. 下面是一个例子:

signal_t_sep = ts_decay_linear(kth_element(vec_avg(anl69_best_eps_gaap_4wk_chg), 120, k=1), 66);
trade_when(group_rank(ts_std_dev(returns, 60), sector) > 0.7, signal_t_sep, -1)

remove_Call_Call_0_left => 
signal_t_sep = kth_element(vec_avg(anl69_best_eps_gaap_4wk_chg), 120, k=1);
trade_when(group_rank(ts_std_dev(returns, 60), sector) > 0.7, signal_t_sep, -1)

remove_Call_Call_1_left => 
signal_t_sep = ts_decay_linear(vec_avg(anl69_best_eps_gaap_4wk_chg), 66);
trade_when(group_rank(ts_std_dev(returns, 60), sector) > 0.7, signal_t_sep, -1)

remove_Call_Call_3_left => 
signal_t_sep = ts_decay_linear(kth_element(vec_avg(anl69_best_eps_gaap_4wk_chg), 120, k=1), 66);
group_rank(ts_std_dev(returns, 60), sector) > 0.7

remove_Compare_Compare_4_left => 
signal_t_sep = ts_decay_linear(kth_element(vec_avg(anl69_best_eps_gaap_4wk_chg), 120, k=1), 66);
trade_when(group_rank(ts_std_dev(returns, 60), sector), signal_t_sep, -1)

remove_Call_Call_5_left => 
signal_t_sep = ts_decay_linear(kth_element(vec_avg(anl69_best_eps_gaap_4wk_chg), 120, k=1), 66);
trade_when(ts_std_dev(returns, 60) > 0.7, signal_t_sep, -1)

remove_Call_Call_6_left => 
signal_t_sep = ts_decay_linear(kth_element(vec_avg(anl69_best_eps_gaap_4wk_chg), 120, k=1), 66);
trade_when(group_rank(returns, sector) > 0.7, signal_t_sep, -1)

remove_UnaryOp_UnaryOp_7_left => 
signal_t_sep = ts_decay_linear(kth_element(vec_avg(anl69_best_eps_gaap_4wk_chg), 120, k=1), 66);
trade_when(group_rank(ts_std_dev(returns, 60), sector) > 0.7, signal_t_sep, 1)

用到的代码:

class IfExpToCallTransformer(ast.NodeTransformer):
    def visit_IfExp(self, node: ast.IfExp):
        self.generic_visit(node)
        return ast.copy_location(
            ast.Call(
                func=ast.Name(id="if_else", ctx=ast.Load()),
                args=[node.test, node.body, node.orelse],
                keywords=[]
            ),
            node
        )

def wq_expr_2_python_expr(alpha_expression):
    # 运算符预处理
    replacements = [
        (r"\b(or)\b", "logical_or"),  # 保护逻辑函数名
        (r"\b(and)\b", "logical_and"),
        (r"\&\&", " and "),  # 处理逻辑表达式
        (r"\|\|", " or "),  # 处理逻辑表达式
        (r"(?<!\=)\!(?!\=)", " not "),  # 处理逻辑表达式
        (r"\?", " if "),  # 处理三元表达式
        (r"\:", " else "),  # 处理三元表达式
        (r"\bNaN\b", "0"),  # 处理特殊常量
    ]
    for pattern, repl in replacements:
        alpha_expression = re.sub(pattern, repl, alpha_expression)

# 清理注释和字符串
    alpha_expression = re.sub(r"/\*.*?\*/", "", alpha_expression, flags=re.DOTALL)
    alpha_expression = re.sub(r"(?m)^\s*(//|#).*\n?", "", alpha_expression)
    alpha_expression = re.sub(r'"([^"]*)"', "0", alpha_expression)
    # 合并多行没有分号的表达式
    lines = alpha_expression.splitlines()
    merged_lines = []
    temp_line = ""

for line in lines:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.endswith(';'):  # 如果行不以分号结尾
            temp_line += " " + stripped_line  # 合并到上一行
        else:
            if temp_line:  # 如果存在合并的内容
                merged_lines.append(temp_line.strip())  # 添加到结果中
            merged_lines.append(stripped_line)  # 添加当前行
            temp_line = ""  # 清空临时合并内容

# 如果最后一行没有以分号结尾，确保它被处理
    if temp_line:
        merged_lines.append(temp_line.strip())
    alpha_expression = "\n".join(line.strip() for line in merged_lines)
    # 处理缩进错误，尝试修复
    alpha_expression = "\n".join(line.strip() for line in alpha_expression.splitlines())

return alpha_expression

def python_expr_2_wq_expr_v2(py_expr: str) -> str:
    # 1. Parse Python AST
    tree = ast.parse(py_expr)

# 2. Apply transformation
    transformer = IfExpToCallTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

# 3. Unparse back to code
    try:
        py_expr = ast.unparse(new_tree)
    except AttributeError:
        import astor
        py_expr = astor.to_source(new_tree).strip()

# 4. Replace logical ops: and/or/not → && / || / !
    py_expr = re.sub(r"\band\b", "&&", py_expr)
    py_expr = re.sub(r"\bor\b", "||", py_expr)
    py_expr = re.sub(r"\bnot\b", "!", py_expr)

# 5. 按行加分号，最后一行不加
    lines = [line.strip() for line in py_expr.splitlines() if line.strip()]
    if not lines:
        return ""
    result_lines = []
    for line in lines[:-1]:
        result_lines.append(line + ";")
    result_lines.append(lines[-1])  # 最后一行不加分号
    return "\n".join(result_lines)

消融的代码:

import ast
import copy
import astor  # fallback if ast.unparse unavailable
from expression.alpha_ast import wq_expr_2_python_expr, python_expr_2_wq_expr_v2

def _ast_to_source(tree):
    try:
        return ast.unparse(tree)
    except AttributeError:
        return astor.to_source(tree).strip()

class Annotator(ast.NodeVisitor):
    def __init__(self):
        self.targets = []  # list of (kind, tag)
        self.counter = 0

def visit_BinOp(self, node):
        tag = f"BinOp_{self.counter}"
        node._ablation_tag = tag
        self.targets.append(("BinOp", tag))
        self.counter += 1
        self.generic_visit(node)

def visit_UnaryOp(self, node):
        tag = f"UnaryOp_{self.counter}"
        node._ablation_tag = tag
        self.targets.append(("UnaryOp", tag))
        self.counter += 1
        self.generic_visit(node)

def visit_BoolOp(self, node):
        tag = f"BoolOp_{self.counter}"
        node._ablation_tag = tag
        self.targets.append(("BoolOp", tag))
        self.counter += 1
        self.generic_visit(node)

def visit_Compare(self, node):
        tag = f"Compare_{self.counter}"
        node._ablation_tag = tag
        self.targets.append(("Compare", tag))
        self.counter += 1
        self.generic_visit(node)

def visit_Call(self, node):
        tag = f"Call_{self.counter}"
        node._ablation_tag = tag
        self.targets.append(("Call", tag))
        self.counter += 1
        self.generic_visit(node)

class AblationTransformer(ast.NodeTransformer):
    PROTECTED_CALL_KEYWORD = "densify"  # densify 及其内部跳过消融

def __init__(self, target_kind, target_tag):
        super().__init__()
        self.target_kind = target_kind
        self.target_tag = target_tag
        self.replaced = False
        self._in_protected_call = 0  # 记录是否在 densify 里（可以嵌套）

def _is_target(self, node, kind):
        return getattr(node, "_ablation_tag", None) == self.target_tag and kind == self.target_kind

def visit_BinOp(self, node):
        if self._is_target(node, "BinOp"):
            self.replaced = True
            return self.visit(node.left)  # left variant
        return self.generic_visit(node)

def visit_UnaryOp(self, node):
        if self._is_target(node, "UnaryOp"):
            self.replaced = True
            return self.visit(node.operand)
        return self.generic_visit(node)

def visit_BoolOp(self, node):
        if self._is_target(node, "BoolOp"):
            self.replaced = True
            if node.values:
                return self.visit(node.values[0])
        return self.generic_visit(node)

def visit_Compare(self, node):
        if self._is_target(node, "Compare"):
            self.replaced = True
            return self.visit(node.left)
        return self.generic_visit(node)

def visit_Call(self, node):
        # 先识别当前是不是受保护的外层调用（如 densify）
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

is_protected_call = func_name == self.PROTECTED_CALL_KEYWORD

if is_protected_call:
            self._in_protected_call += 1

# 先递归子节点（但如果是 densify，仍要递归进去以保持内部不被替换）
        node = self.generic_visit(node)

# 如果当前在 densify 之内（包括 densify 本身），跳过任何 target 消融
        if self._in_protected_call > 0:
            if is_protected_call:
                self._in_protected_call -= 1
            return node  # 原样返回，不做替换

# 下面是原本针对被标记 target 的消融逻辑
        if self._is_target(node, "Call"):
            # 仍然可以保留你之前的函数保护逻辑，例如 vec_avg 之类
            inner_name = None
            if isinstance(node.func, ast.Name):
                inner_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                inner_name = node.func.attr

if inner_name and 'vec' in inner_name:
                return node  # 护着 vec_* 系列不消融

self.replaced = True
            if node.args:
                return self.visit(node.args[0])  # 用第一个参数替代
            else:
                return ast.Constant(value=0)

return node

class RightVariantApplier(ast.NodeTransformer):
    def __init__(self, target_kind, target_tag):
        super().__init__()
        self.target_kind = target_kind
        self.target_tag = target_tag
        self.replaced = False

def _is_target(self, node, kind):
        return getattr(node, "_ablation_tag", None) == self.target_tag and kind == self.target_kind

def transform_right_variant(self, node: ast.BinOp):
        right = node.right
        if isinstance(node.op, ast.Sub):
            # a - b -> -b
            return ast.copy_location(ast.UnaryOp(op=ast.USub(), operand=right), node)
        elif isinstance(node.op, ast.Div):
            # a / b -> 1 / b
            one = ast.Constant(value=1)
            return ast.copy_location(ast.BinOp(left=one, op=ast.Div(), right=right), node)
        else:
            # 默认退回右边
            return ast.copy_location(right, node)

def visit_BinOp(self, node):
        if self._is_target(node, "BinOp"):
            self.replaced = True
            return self.transform_right_variant(node)
        return self.generic_visit(node)

def generate_ablation_variants(alpha_expression: str):
    """
    返回一个 dict：key 是变体名字，value 是修改后的表达式字符串。
    对每个 BinOp 生成两个（left / right_variant），其余 operator 各一个。
    """
    tree = ast.parse(alpha_expression)
    annotator = Annotator()
    annotator.visit(tree)

variants = {}

for kind, tag in annotator.targets:
        # left / default variant
        tree_copy = copy.deepcopy(tree)
        left_transformer = AblationTransformer(target_kind=kind, target_tag=tag)
        new_tree_left = left_transformer.visit(tree_copy)
        ast.fix_missing_locations(new_tree_left)
        if left_transformer.replaced:
            expr_left = _ast_to_source(new_tree_left)
            variants[f"remove_{kind}_{tag}_left"] = expr_left

# right_variant only for BinOp; others skip
        if kind == "BinOp":
            tree_copy2 = copy.deepcopy(tree)
            right_transformer = RightVariantApplier(target_kind=kind, target_tag=tag)
            new_tree_right = right_transformer.visit(tree_copy2)
            ast.fix_missing_locations(new_tree_right)
            if right_transformer.replaced:
                expr_right = _ast_to_source(new_tree_right)
                variants[f"remove_{kind}_{tag}_right_variant"] = expr_right

return variants

def get_alpha_ablation_list(alpha):
    alpha_expression = wq_expr_2_python_expr(alpha)
    variants = generate_ablation_variants(alpha_expression)
    alpha_ablation_list = [python_expr_2_wq_expr_v2(v) for v in variants.values()]
    return alpha_ablation_list

不过, 我这个代码没有大规模的回测过, 想必有些目前不知道的隐患. 

如果想对表达式自动化简, 光做一步消融也不够...需要收集消融结果重新组合表达式, 这个目前我还没做到. 

还有就是表达式替换, 比如把...group_zscore(...,group)... 换成 ...zscore(...)... . 都是我经常手工操作的化简. 如果能把常用操作换成代码自动实现, 想必回测体验会好很多.

---

## 讨论与评论 (0)

