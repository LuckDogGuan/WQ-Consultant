# Python alpha 提交经验分享经验分享

- **链接**: Python alpha 提交经验分享经验分享.md
- **作者**: RM49262
- **发布时间/热度**: 1个月前, 得票: 31

## 帖子正文

Python alpha推出有一段时间了，本人昨天第一次尝试提交了Python alpha，这里简单分享一下相关的经验：1.Python alpha 是否影响六维/点塔/d0 quota/ppa quota？提交Python alpha不会影响六维中的Operators per Alpha/Operators used。但六维中的Fields per Alpha以及Fields used这两项还是会变动的。同时，提交Python alpha会正常点亮所使用字段的Pyramid。若提交的Python alpha是D0 alpha，也会正常占用每月30个的D0 alpha quota。但鉴于Python alpha不直接使用Fast Expression中的操作符，系统无法判断使用的操作符数量是否符合PPA上限8个的要求，从而无法判断某个alpha是否属于PPA。因此，目前无法使用Python alpha来提交PPA，只能提交RA。2.Python alpha 有base加成吗？上周双周会培训的时候Kunqi老师有提到说Python alpha的加成已经写在了Base的算法中。但就目前本人实测情况来看，上面这个alpha的prod corr为0.38，在vf0.88+os rank0.5的情况下，拿到的Base是8.86刀。这个Base水平和相同水平的Fast Expression alpha的base收益基本一致。此外，在check的时候，目前也没有看到针对Python Alpha的额外加成系数。因此就个人体感而言，没有明显的感受到Python alpha存在额外Base 加成系数。当然这一点还需要大家更多样本的对比验证。3.Python alpha 现阶段的限制(大家可以在评论区继续补充)目前并不是所有区域都可以提交Python alpha(比如GLB就不可以)。Python alpha现阶段不可以被SA Selection选到。目前Python alpha不支持Vector类型的字段。现阶段Python alpha也不支持多重回测。只能单个回测。现阶段Python alpha功能并不稳定，有些时候报错的Python alpha在原封不动重新回测之后又能正常出结果。这一点只能靠官方进一步优化了。4.Python alpha 的基础格式具体细节请参考说明文档：https://platform.worldquantbrain.com/learn/documentation/consultant-information/getting-started-brain-python-alphas简单的说的话目前Python alpha的需要由这么几部分组成：a. import部分：from brain.alphas import alphaimport numpy as npimport numpy.typing as npt此外培训的时候提到还支持scipy/scikit-learn之类的包，但本人还没进一步尝试b. 定义所需的各类操作符def _signed_power(x, n):return np.sign(x) * np.power(np.abs(x), n)c. 装饰器@alpha(data=["field1", "field2", ...],   # 声明输入字段store=[],                   # 跨时间步持久化的状态（一般不用）)d. 最终alphadef alpha_func(data, store) -> npt.NDArray[np.float32]:# ... 计算逻辑 ...return signal.astype(np.float32)   # 必须 float32，shape [n_instruments]```即使你不会也没有关系，把说明文档喂给AI，让他帮你分析/转化即可5.Python alpha 的回测设置Python alpha回测时的Payload需要修改一下：def build_payload() -> dict:return {"type": "REGULAR","settings": {"instrumentType": "EQUITY","region": "EUR","universe": "TOP2500","delay": 1,"decay": 1,"neutralization": "REVERSION_AND_MOMENTUM","truncation": 0.07,"lookback": 0,"pasteurization": "ON","maxTrade": "OFF","maxPosition": "OFF","language": "PYTHON","visualization": False,"startDate": "2014-01-01","endDate": "2023-12-31",},"regular": PYTHON_CODE,}最主要的加粗的这三处地方：a. lookback假设你的alpha中用到了ts相关的时序操作符，那就一定要修改lookback这个值。要让lookback大于你的ts操作符中的days的最大值。举个例子：假设你的原alpha是ts_mean(ts_max(ts_decay_linear(returns,5),10),3)这个alpha中用到了三个不同的days: 3/5/10那你的lookback就要设置为大于等于10的值，否则Python回测就会报错。同时，增加lookback这个值似乎会增加计算的复杂度，因此假如你习惯性把这个值设置的很大，个人感觉报错会更频繁。因此，最合理的就是根据你所需的时间长度合理设置这个值。b. language要改成PYTHONc. regularregular中要完整的放上前面基础格式里提到的需要的全部代码即可6.Python alpha 操作符复刻示例这里简单放一个我用到的group_normalize操作符的复刻方法：def _int_group_to_float(g_raw):if np.issubdtype(g_raw.dtype, np.integer):sentinel = np.iinfo(g_raw.dtype).ming = g_raw.astype(np.float64)g[g_raw == sentinel] = np.nanreturn greturn g_raw.astype(np.float64)def _group_normalize(values, groups, scale=1.0):out = values.astype(np.float64, copy=True)valid = ~np.isnan(values) & ~np.isnan(groups)if not valid.any():return outfor g in np.unique(groups[valid]):mask = valid & (groups == g)denom = np.abs(values[mask]).sum()out[mask] = scale * values[mask] / denom if denom > 0 else 0.0return out@alpha(data=["country"],store=[],def alpha_func(data, store) -> npt.NDArray[np.float32]:country = _int_group_to_float(data.country[-1])normalized = _group_normalize(alpha, country)return result.astype(np.float32)需要注意的是，鉴于现在操作符如何处理数据都是我们自己定义，因此像如何处理Nan值这样的问题其实重要性不容忽视，这一点在写代码的时候一定要考虑好。以上就是本人提交Python alpha的初步分享，希望能帮到大家！祝大家下个月Python alpha比赛都能取得好成绩

---

## 讨论与评论 (13)

### 评论 #1 (作者: LL81909, 时间: 1个月前)

看了一下，好像比regular alpha更复杂，也更难。官方搞这个的目的是什么？从操作符上降低相关性？但是投入的时间更高，也更需要专业性。

---

### 评论 #2 (作者: MY82844, 时间: 1个月前)

感谢分享，对于六维的影响，终于找到了实战数据：==============================================================1. 提交Python alpha不会影响六维中的Operators per Alpha/Operators used2. 六维中的Fields per Alpha以及Fields used这两项还是会变动的3. 提交Python alpha会正常点亮所使用字段的Pyramid

---

### 评论 #3 (作者: QL68122, 时间: 1个月前)

正好派上用场，之前各种函数报错试了好一整子

---

### 评论 #4 (作者: XB37939, 时间: 1个月前)

mark一下 ，希望下个月Python alpha比赛可以用到#========= WORLDQUANT BRAIN CONSULTANT ========== ##每天进步一点点，加油# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%# sys.setrecursionlimit(α∞)# PnL = ∑(Robustness * Creativity)#无限探索、鲁棒性优先，创新性增值#=================加油每一天=======================#

---

### 评论 #5 (作者: EL15829, 时间: 1个月前)

确实是这样，深有同感！我之前在跑 MEA 区的时候也发现没法正常使用 Python Alpha，跑到中途系统直接报错，直接弹窗提示我‘WorldQuant is experiencing some difficulties’。现阶段限制确实挺多的，等官方后续慢慢优化放开权限。

---

### 评论 #6 (作者: WL58980, 时间: 1个月前)

感谢分享，可以尝试做Python alpha了！！！============================================================================Study hard — quality over quantity, no room for mediocrity. Cherish every learning opportunity, stay focused, and learn from the experts. Keep pushing!============================================================================

---

### 评论 #7 (作者: TL53163, 时间: 29天前)

我还没有开始python alpha，看了楼主的贴子启发很大。楼主的alpha还是借助ai做的么？ 用python不限制op的话，应该更容易做出RA了。============================================================================

---

### 评论 #8 (作者: XW23690, 时间: 28天前)

赞。复刻现有的fast expression运算符是学习python expression的第一步！---------------------------------------------------------------------------α≠运气 |α=Edge E [PnL]=∑(E [r_i]×w_i) σ↓→Sharpe↑Factor=Signal-Noise Backtest→Live→Repeat βNeutral|αMaxWin>Loss|Risk<Reward InSample→OutOfSample---------------------------------------------------------------------------

---

### 评论 #9 (作者: RM49262, 时间: 21天前)

=====================================评论区====================================另外再补充一条，有时网页Python回测会疯狂报错，但有时按加号创建一个新的回测栏，然后把Python code再复制进去回测，似乎偶尔能成功=============================================================================

---

### 评论 #10 (作者: RM49262, 时间: 21天前)

=====================================评论区====================================另外关于多时间窗口的问题，我正文里写的有误，对于多时间窗比如ts_mean(ts_decay_linear(x,5),5)这种，lookback应该是两个值加起来才对，不是简单取最大值。=============================================================================

---

### 评论 #11 (作者: XY20037, 时间: 19天前)

这份首测 Python Alpha 实战总结干货详实，把配额规则、收益、平台约束、代码规范、payload 配置五大关键要点全部梳理透彻，对初次上手编写代码提交的顾问参考价值极高。明确 Python 不计算子占用、仅统计字段用量、无法生成 PPA 只可提交 RA，D0 名额照常占用，帮大家避开配额规划误区；Base 实测和传统表达式因子收益持平，破除网传额外加成的误区。同时列明 GLB 不可提交、暂不支持 SA 入选与 Vector 字段、无法多重回测等现存限制，提前规避踩坑。代码模板、lookback 按需配置逻辑、group_normalize 自定义算子示例清晰易懂，尤其是整型空值哨兵值转换处理细节切中 Python 高频报错痛点，照着规范喂给 AI 生成代码、按需设置回溯周期就能大幅提升回测通过率，非常适配当下 Python 专项赛事赛前打磨因子。

---

### 评论 #12 (作者: VG70621, 时间: 17天前)

感谢大佬提供的示例和解释 我一直没做出 python alpha====================================================================================================================================================================

---

### 评论 #13 (作者: HL84989, 时间: 15天前)

感谢分享，我也遇到以上错误，一直不知道原因，只能一步步试试了========================================================================================================================================================================

---

