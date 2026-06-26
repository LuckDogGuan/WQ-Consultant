# Python调用DeepSeek官方API实现数据集内字段智能组合代码优化

- **链接**: [Commented] Python调用DeepSeek官方API实现数据集内字段智能组合代码优化.md
- **作者**: YX50005
- **发布时间/热度**: 1年前, 得票: 62

## 帖子正文

在3月第二节顾问课上，老师展示了使用网页版大模型来进行字段组合生成具有经济学含义的新字段的流程，如果能把这个流程放在python中自动执行，可以提高一些效率。

- 大语言模型选择DeepSeek-R1
- 输入给大语言模型的信息遵循老师课上给的例子，包括数据集描述和字段名，字段描述

流程如下：

1.输入数据集描述/字段信息形成prompt

```
def _build_prompt(
        self, dataset_desc: str, fields_info: List[Tuple[str, str]]
    ) -> str:
        """
        构建 prompt
        """
        # 如果字段数量超过100，随机选择100个
        if len(fields_info) > 100:
            fields_info = random.sample(fields_info, 100)

        fields_text = "\\n".join(
            [
                f"{field_name}: {field_desc}; "
                for field_name, field_desc in fields_info
            ]
        )

        prompt_system = f"""
你是一位专业的量化金融分析师。现在有一个数据集提供给你：

1. 数据集描述：  
   {dataset_desc}

2. 现有字段信息：  
   {fields_text}
"""

        prompt_user = f"""
请根据以下要求，生成新的字段表达式列表：
(1) 请尽量多样化地生成新的字段表达式，且每个字段都需具有明确的经济学含义。  
(2) 可使用加减乘除等基本运算符。  
(3) 每个字段的经济学含义需有注释说明
(4) 输出格式：仅返回 JSON 数组，数组中每个元素包含 "description" 和 "expression" 两个字段：  
    • description（描述字段含义）  
    • expression（字段的实际表达式）  

请勿输出除 JSON 数组外的任何额外文字或说明。请直接返回最终的 JSON 数组结果。
"""

        return prompt_system, prompt_user

```

2.调用deepseek API

```
def _call_api(self, system_prompt: str, user_prompt: str) -> dict:
        """
        调用 DeepSeek API
        """
        data = {
            "model": "deepseek-reasoner",
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            "temperature": 0.7,
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()

        return response.json()

```

输出的结果类似于

![图片](images/img_2dc1ea80d0.png)

3.解析输出的json，获取生成的字段

```
def _parse_response(self, response: dict) -> List[str]:
        """
        解析 API 响应
        """
        try:
            content = response["choices"][0]["message"]["content"]
            if content.startswith("```json"):
                content = content[len("```json") :]
            if content.endswith("```"):
                content = content[: -len("```")]
            print(content)
            fields = json.loads(content)
            return [field["expression"] for field in fields]
        except Exception as e:
            print(f"解析响应时出错: {e}")
            return []

```

这样在通过API获取数据集的表述、字段的信息后，就可以自动地为各个数据集生成一批具有经济学含义的新的组合字段了。

更进一步

- Deepseek的官方API需要收费，可以探索其他更经济的调用大模型的方式
- 目前取了一个数据集中的随机100个字段，如果大模型本身支持，并且价格不贵，可以取更多的字段进行输入

---

## 讨论与评论 (3)

### 评论 #1 (作者: DZ31817, 时间: 1年前)

感谢分享，很好的实践。我最近也在使用大模型批量生成信号，但也跟你这段prompt一样，目前仅限于使用加减乘除等基本运算符的时候效果还可以接受，一旦涉及高等的运算符，生成的效果就没那么好了。期待进一步的探索研究。

---

### 评论 #2 (作者: ZS59763, 时间: 1年前)

很好的实践，潜在的优化方向是把一些基础的运算符，比如sqrt，tsmean这些也同时扔给ai，供参考。

---

### 评论 #3 (作者: JX14975, 时间: 1年前)

请问你遇到过deepseek无中生有数据字段的情况吗？我用网页版这种情况就特别明显，尤其是在输入的字段多的时候。

---

