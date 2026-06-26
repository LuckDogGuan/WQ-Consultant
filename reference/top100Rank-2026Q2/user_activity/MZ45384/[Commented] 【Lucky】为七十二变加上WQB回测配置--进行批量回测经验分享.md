# 【Lucky】为七十二变加上WQB回测配置--进行批量回测经验分享

- **链接**: [Commented] 【Lucky】为七十二变加上WQB回测配置--进行批量回测经验分享.md
- **作者**: ML28213
- **发布时间/热度**: 6个月前, 得票: 12

## 帖子正文

72 变是一个十分好用的工具，但是生成的 json 是没有回测配置的

> e.g.

> ![图片](images/img_e732ed8d06.png)

为了提升回测效率，设计了一个脚本，将七十二变生成的 json转换成成 WQB 能直接回测的带回测配置的json

> e.g.
> ![图片](images/img_58dc1a88aa.png)

设置好回测配置 & 文件输入输出的路径之后，即可生成可直接在 WQB 回测的 JSON。即可批量回测七十二变输出的变体了。

以下是实现代码

```
import jsondef convert_expressions(input_file, output_file, custom_settings):try:withopen(input_file, 'r') asf:expressions=json.load(f)output_data= []forexprinexpressions:alpha_object= {"type": "REGULAR","settings": custom_settings,"regular": expr}output_data.append(alpha_object)withopen(output_file, 'w') asf:json.dump(output_data, f, indent=2)print(f"Successfully converted {len(expressions)} expressions.")print(f"Output saved to '{output_file}'")exceptFileNotFoundError:print(f"Error: Input file not found at '{input_file}'")exceptjson.JSONDecodeError:print(f"Error: Could not decode JSON from '{input_file}'")exceptExceptionase:print(f"An unexpected error occurred: {e}")if __name__ == "__main__":# --- 请在这里自定义参数 ---# --- 以下为示例参数 ---default_settings= {"instrumentType": "EQUITY","region": "IND","universe": "TOP500","delay": 1,"decay": 5,"neutralization": "FAST","truncation": 0.08,"pasteurization": "ON","testPeriod": "P0Y0M","unitHandling": "VERIFY","nanHandling": "OFF","language": "FASTEXPR","visualization": False}INPUT_JSON_PATH='七十二变/输出/文件.json'OUTPUT_JSON_PATH='加上回测配置/文件/的输出路径.json'convert_expressions(INPUT_JSON_PATH, OUTPUT_JSON_PATH, default_settings)
```

---

## 讨论与评论 (6)

### 评论 #1 (作者: PZ64174, 时间: 6个月前)

感谢大佬分享！很简洁很实用的功能！值得大家来点赞！已get，待会就去试一试！

====================================================================

一年一个台阶，一步一个脚印

====================================================================

---

### 评论 #2 (作者: XG98059, 时间: 6个月前)

学习了，感谢大佬。

---

### 评论 #3 (作者: YQ84572, 时间: 6个月前)

便捷的操作，为快速研究做了基础设施的建设

---

### 评论 #4 (作者: AH18340, 时间: 6个月前)

有代码基础可以直接改七十二变的代码，没有的可以尝试这个脚本

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #5 (作者: MZ45384, 时间: 6个月前)

非常棒的工具代码。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值
======================================================================================

---

### 评论 #6 (作者: SY36032, 时间: 6个月前)

感谢大佬的分享

---

