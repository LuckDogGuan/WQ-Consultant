import re
import pandas as pd
from typing import List

# Default operators to make the pruner self-contained or extensible
DEFAULT_TS_OPS = [
    "ts_rank", "ts_zscore", "ts_delta", "ts_sum", "ts_delay", 
    "ts_std_dev", "ts_mean", "ts_arg_min", "ts_arg_max", "ts_scale", 
    "ts_quantile", "ts_backfill", "ts_std"
]

DEFAULT_CROSS_OPS = [
    "reverse", "inverse", "rank", "zscore", "quantile", "normalize",
    "scale", "truncate", "winsorize"
]

DEFAULT_GROUP_OPS = [
    "group_neutralize", "group_rank", "group_zscore", "group_mean"
]

DEFAULT_DECAY_OPS = [
    "ts_decay_linear", "ts_decay_exp_window", "ts_weighted_decay"
]

class RegularBuilder:
    def __init__(self, ts_ops: List[str] = None, cross_ops: List[str] = None, 
                 group_ops: List[str] = None, decay_ops: List[str] = None):
        field_regular = [r'\(\s*(\w+)\s*,\s*', r'\(\s*(\w+)\s*\)\s*']
        self.field_patterns = [re.compile(regular) for regular in field_regular]
        
        first_op_regular = r'(\w+)\s*\('
        self.first_op_pattern = re.compile(first_op_regular)
        
        t_ops = ts_ops if ts_ops is not None else DEFAULT_TS_OPS
        c_ops = cross_ops if cross_ops is not None else DEFAULT_CROSS_OPS
        g_ops = group_ops if group_ops is not None else DEFAULT_GROUP_OPS
        d_ops = decay_ops if decay_ops is not None else DEFAULT_DECAY_OPS
        
        self.ops = list(set(t_ops + c_ops + g_ops + d_ops))

    def _extract_parameters(self, trade_when_expression: str) -> List[str]:
        """
        示例输入: "trade_when(x, y, z)"
        输出: [x, y, z]
        """
        if 'trade_when' not in trade_when_expression:
            return [trade_when_expression, "", ""]
            
        expr_clean = trade_when_expression.split('trade_when', 1)[1].strip(' ()')
        params = []
        stack = 0
        current = []
        
        for char in expr_clean:
            if char == '(':
                stack += 1
            elif char == ')':
                stack -= 1
                
            if char == ',' and stack == 0:
                params.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
                
        if current:  # 最后一个参数
            params.append(''.join(current).strip())
            
        # Ensure at least 3 elements
        while len(params) < 3:
            params.append("")
            
        return params[:3]

    def get_regular(self, trade_when_expression: str) -> str:
        params = self._extract_parameters(trade_when_expression)
        return params[1]

    def get_regular_field(self, expression: str) -> str:
        if "trade_when" in expression:
            expression = self.get_regular(expression)
            
        for p in self.field_patterns:
            math = p.search(expression)
            if math:
                return math.group(1)
        return ""

    def get_first_op(self, expression: str) -> str:
        if "trade_when" in expression:
            expression = self.get_regular(expression)
            
        if expression.startswith("-"):
            expression = expression[1:]
            
        math = self.first_op_pattern.search(expression)
        if math:
            return math.group(1)
        return ""

    def parse_expression(self, expression: str) -> List[str]:
        """
        示例输入: "group_neutralize(ts_rank(close, 20), sector)"
        输出: ['group_neutralize', 'ts_rank', 'close']
        """
        if "trade_when" in expression:
            # For trade_when, extract its core signal (the second parameter)
            core_expr = self.get_regular(expression)
            return ["trade_when"] + self.parse_expression(core_expr)
            
        field = self.get_regular_field(expression)
        elements = set(op for op in self.ops if op in expression)
        if field:
            elements.add(field)
            
        pattern = '|'.join(re.escape(element) for element in elements)
        if not pattern:
            return []
            
        return re.findall(pattern, expression)

def prune_expressions(df: pd.DataFrame, regular_col: str = "regular", 
                      sharpe_col: str = "sharpe", fitness_col: str = "fitness") -> pd.DataFrame:
    """
    通过解析表达式结构并按分组去重进行因子剪枝。
    对于结构相同（即操作符顺序和字段相同，仅参数不同）的因子，仅保留 Sharpe 和 Fitness 最高的那个。
    """
    if df.empty:
        return df
        
    df = df.copy()
    rb = RegularBuilder()
    
    # 提取表达式结构，转为字符串表达作为分类Key
    df["exp_structure"] = df[regular_col].apply(lambda x: str(rb.parse_expression(x)))
    
    # 计算 Sharpe 与 Fitness 绝对值，排序用
    df["abs_sharpe"] = df[sharpe_col].abs()
    df["abs_fitness"] = df[fitness_col].abs()
    
    # 按照 abs_sharpe 降序和 abs_fitness 降序进行排序
    df_sort = df.sort_values(by=['abs_sharpe', 'abs_fitness'], ascending=[False, False])
    df_reset = df_sort.reset_index(drop=True)
    
    # 按结构分组并保留每组的第一条（即 Sharpe 最高的那条）
    grouped = df_reset.groupby('exp_structure')
    group_list = []
    for name, group in grouped:
        group_list.append(group.head(1))
        
    # 合并结果并清理临时列
    res_df = pd.concat(group_list).reset_index(drop=True)
    res_df = res_df.drop(columns=["exp_structure", "abs_sharpe", "abs_fitness"])
    
    return res_df
