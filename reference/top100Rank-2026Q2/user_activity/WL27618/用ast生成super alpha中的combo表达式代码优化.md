# 用ast生成super alpha中的combo表达式代码优化

- **链接**: 用ast生成super alpha中的combo表达式代码优化.md
- **作者**: WL27618
- **发布时间/热度**: 1年前, 得票: 63

## 帖子正文

出于以下两点:

1. 我发现写combo表达式的问题(输入有限, operator有限-> 表达式) 可以完整的表达成ast的格式

2. (这是我个人看法)虽然可以人工挑选有经济学意义的表达式, 但 除非明确知道selection得到的alpha pool中有某种经济学意义没得到充分表达, 这对于combo来说不过是bias, 我相信selection中的alpha全都有意义, 没理由认为某个意义要比其他高级. 在combo中, 我们应该放下偏见, 更无情的, 向着一个明确的指标优化(比如sharpe), 用机器的方法挖掘selection没有顾虑到的地方.

---

我们输入combo表达式是字符串格式的, 我觉得一个可以解析的ast是遍历或者机器学习的基础.
希望有更多同学向这个方向探索. 目前我还没得到一套行之有效的算法.

---

下面是我实现的大概结果和代码.

表达式: expression_node和worldquant识别的字符串

```
└── reduce_count    ├── ts_quantile        │   ├── ts_delta    │       │   │   ├── combo_a(alpha,nlength=500,mode='algo3')    │       │   │   └── 66        │   └── 22    └── 22 reduce_count(self_corr(ts_quantile(ts_delta(combo_a(alpha,nlength=500,mode='algo3'), 66), 22), 22),threshold=0) └── ts_covariance    ├── combo_a(alpha,nlength=252,mode='algo3')    ├── combo_a(alpha,nlength=66,mode='algo1')    └── 66 ts_covariance(ts_zscore(combo_a(alpha,nlength=252,mode='algo3'),66),ts_zscore(combo_a(alpha,nlength=66,mode='algo1'),66),66) └── signed_power    └── subtract            ├── 1/                │   └── stats.returns            └── stats.long_value signed_power(subtract(1/(1+signed_power(2.7182, -stats.returns)),stats.long_value), 0.5) └── {data}    └── ts_av_diff            ├── reduce_stddev                │   ├── combo_a(alpha,nlength=66,mode='algo1')                │   └── 240            └── 120 ts_av_diff(reduce_stddev(self_corr(combo_a(alpha,nlength=66,mode='algo1'), 240)),120) ---代码:
```

```
leaf_nodes = superstates + days + numbers + eventsregular_nodes = (arithmetic_lambda_factory+ compare_lambda_factory+ logical_lambda_factory+ control_lambda_factory+ ts_lambda_factory+ ts_relation_lambda_factory+ corr_lambda_factory+ cross_section_dist_lambda_factory)class ExpressionNode:def__init__(self, op: Union[str, Callable], children: Optional[List[Union['ExpressionNode', str]]] =None, value: Optional[str] =None):self.op = opself.children = children if children else []self.value = valueself.return_type =self._infer_return_type()def_infer_return_type(self):ifself.op =='leaf':# 假设叶节点的类型是从 leaf_nodes 中获取的for leaf in leaf_nodes:ifself.value == leaf:returntype(leaf)return'unknown'elifcallable(self.op):type_hints = get_type_hints(self.op)return type_hints.get('return', 'unknown')else:return'unknown'def__str__(self):returnself._to_tree_str()def_to_tree_str(self, indent: str="", is_last: bool=True) -> str:connector = "└── " if is_last else "├── "ifself.op =='leaf':line = f"{connector}{self.value}"elifcallable(self.op):op_name = self.op.__name__ if hasattr(self.op, "__name__") else str(self.op)line = f"{connector}{op_name}"else:line = f"{connector}{self.op}"# 递归渲染子节点lines = [line]for i, child inenumerate(self.children):is_last_child = i == len(self.children) - 1ifisinstance(child, ExpressionNode):lines.append(child._to_tree_str(indent + (" " if is_last else "│ "), is_last_child))else:leaf_line = f"{' ' if is_last else '│ '}{'└── ' if is_last_child else '├── '}{child}"lines.append(indent + leaf_line)return'\n'.join([indent + l for l in lines])defto_expression(self) -> str:ifself.op =='leaf':returnstr(self.value)elifcallable(self.op):# 关键：直接执行 op 本身传入 child 表达式args = [child.to_expression() if isinstance(child, ExpressionNode) else str(child) for child in self.children]returnself.op(*args)else:returnstr(self.op)defmutate(self):"""变异：用相同类别的其他操作符替换当前操作符"""ifself.op =='leaf':candidates = [node for node in leaf_nodes if isinstance(node, type(self.value))]if candidates:self.op = random.choice(candidates)elifcallable(self.op):category = self.op.categorycandidates = [op for op in regular_nodesifhasattr(op, 'category') and op.category == category and op.__name__!=self.op.__name__]if candidates:self.op = random.choice(candidates) # 随机选择同类别同返回类型的操作符else:passdef random_expression(depth=4, required_type=None, is_root=True):# print('depth', depth, 'required_type:', required_type, 'is_root:', is_root)if depth ==0:# 强制只选 leaf nodesvalid_leaves = [leaf for leaf in leaf_nodesif (required_type is None ortype(leaf) == required_type or(hasattr(required_type, '__origin__') andrequired_type.__origin__ is Union andtype(leaf) in get_args(required_type)))]ifnot valid_leaves:raiseValueError(f"No leaf node found with type: {required_type}")chosen_leaf = random.choice(valid_leaves)return ExpressionNode('leaf', value=chosen_leaf)else:regular_candidates = []leaf_candidates = []for node in regular_nodes + leaf_nodes:ifcallable(node):# print(get_type_hints(node))return_type = get_type_hints(node).get('return')else:return_type = type(node)if (required_type is None orreturn_type == required_type or(hasattr(required_type, '__origin__') andrequired_type.__origin__ is Union andreturn_type in get_args(required_type))):ifcallable(node):regular_candidates.append(node)else:leaf_candidates.append(node)if is_root:# 根节点禁止 leaf和logical operatorscandidates = [node for node in regular_nodes if 'logical' not in node.category]else:# 非根节点允许 leaf，但降低权重（例如只加权重为 0.2）candidates = regular_candidates + random.choices(leaf_candidates, k=max(1, len(regular_candidates)//4))ifnot candidates:raiseValueError(f"No valid node found with return type: {required_type}")node = random.choice(candidates)ifnotcallable(node):# 被选中的是 leaf nodereturn ExpressionNode('leaf', value=node)# 被选中的是 regular nodesig = inspect.signature(node)children = []for name, param in sig.parameters.items():param_type = param.annotation if param.annotation != inspect.Parameter.empty else Nonechild = random_expression(depth - 1, required_type=param_type, is_root=False)children.append(child)return ExpressionNode(node, children)
```

---

## 讨论与评论 (1)

### 评论 #1 (作者: LJ12230, 时间: 2个月前)

感谢大佬！深受启发！

---

