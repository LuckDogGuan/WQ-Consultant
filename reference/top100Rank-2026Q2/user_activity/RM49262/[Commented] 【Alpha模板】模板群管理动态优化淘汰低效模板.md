# 【Alpha模板】模板群管理——动态优化淘汰低效模板

- **链接**: [Commented] 【Alpha模板】模板群管理动态优化淘汰低效模板.md
- **作者**: SY43349
- **发布时间/热度**: 6个月前, 得票: 8

## 帖子正文

## 引言

大家好我是sy。最近社区一直在缩减回测量想必大家可能会遇到很多困难。我是11月中旬成为条件顾问，到目前刚好一个半月了，这期间我总共提交了122个alpha，点了27个塔，平均每日回测大概2500左右，目前大概每天能稳定提交2-4个alpha（中间断交主要是临时有事。。）  我想跟大家分享一下目前我在实现低回测高产出方面的核心经验——动态管理模板群。  不过需要注意⚠️的是，由于代码和我自身的框架非常绑定无法单独抽离，以下内容主要以思路为主，希望能对大家有所帮助。

![图片](images/img_72b1c372b3.png)

![图片](images/img_4efa3c7aab.png)

## 模板群管理

想必大家手里都有很多模板，但是实际上不知道大家有没有进行过统计，不同模板的产出效率完全不同，甚至相差数百倍，长期在低效模板上的回测是没有意义的。因此，我想到了能不能多各个模板的产出结果进行统计，实现对低效模板的发现和剔除，从而提升这个模板群的效率。

### 抽象模板生成方法

#### alpha funcs 库

要实现动态的模板库管理需要对模板库进行一层抽象，它接受给定的模板库

```
ALPHA_FUNCS = [   "func1", "func2"]
```

#### 动态alpha 生成

随后generator根据给定的alpha funs生成所有的对应的alpha

```
    def generate_random_alphas(self, count):        """        🎲 使用多种策略生成指定数量的随机 Alpha。        使用多种生成器（fundamental, technical, sentiment 等），并按权重抽样。        """        print(f"\n🎲 正在生成 {count} 个随机 Alpha...")        # 所有可用的 Alpha 生成函数列表（涵盖基本面、技术面、情绪面、随机结构等）        all_alphas = []        alpha_funcs = []        generators = get_func_call_info().keys()        # 从每个生成器中随机抽取部分结果        for gen in tqdm(generators):            try:                gen = eval(f'{gen}')                result = gen()                result = list(set(result))                if result and len(result) > 0:                    # 每个生成器抽取 1 ~ min(建议数量, 实际数量) 个                    sample_size = min(count // len(generators) + 5, len(result))                    sample_size = max(1, sample_size)                    selected = ALPHA_SELECTOR.rng.sample(result, sample_size)                    tmp_selected = []                    # 去重                    for s in selected:                        if s not in all_alphas:                            tmp_selected.append(s)                                        all_alphas.append(tmp_selected)                    alpha_funcs.append([gen.__name__] * len(tmp_selected))            except Exception as e:                print(f"⚠️ 生成器 {gen.__name__} 出错: {e}")                continue        all_alphas = [alpha for sublist in all_alphas for alpha in sublist]        alpha_funcs = [func for sublist in alpha_funcs for func in sublist]        print(f"✅ 成功生成 {len(final_alphas)} 个随机 Alpha！")        return final_alphas, final_funcs
```

#### 模板标记

要做到跟踪统计首先是，做到准确的来源标记。这里我采用dataclass的方式在生成时就标记了alpha的来源。

```
@dataclassclass AlphaRecord:    """Data class for storing alpha information, extends evaluation result"""    expression: str    alpha_func: str    alpha_link: str = None    sharpe: float = None    subsharpe: float = None    fitness: float = None    turnover: float = None
```

#### 统计分析

通过上述步骤我们就可以追踪每个alpha 模板的表现，随后可以自己制定规则动态淘汰一些模板。我自己采用的是通过率淘汰的方式。以下是效果展示：

![图片](images/img_e8ce7db7b1.png)

目前经过我对模板群的不断优化，现在每日平均可提交alpha已经可以做到1%的水平（最好2%，最差0.07%），每天只需要挑选其中最好的进行进一步优化和提交即可。

![图片](images/img_034af3087e.png)

---

## 讨论与评论 (4)

### 评论 #1 (作者: RM49262, 时间: 5个月前)

=====================================评论区=========================================

感谢大佬分享，之前有积累一些模板，确实没想到还可以动态淘汰模板

学到了！

===================================================================================

---

### 评论 #2 (作者: ZZ44620, 时间: 5个月前)

大佬能补充一下吗， *alpha funs生成所有的对应的alpha，* 是对所有类别数据集都尝试一下这个模板的效率才得出的低效然后剔除吗？

---

### 评论 #3 (作者: SY43349, 时间: 5个月前)

我目前是自己动态指定一系列数据集测试，如果一段时间后发现一个模板持续产出效率很低就给剔除掉了。当然我觉得你说的有道理，可以进一步进行细化到数据集层次，进一步减少低效回测。

---

### 评论 #4 (作者: XW83124, 时间: 4个月前)

新人问一下，多少个模板就算是模板群了，大佬们都积累了多少个模板了。多少个模板去做这个模板群管理算是比较高效。

---

