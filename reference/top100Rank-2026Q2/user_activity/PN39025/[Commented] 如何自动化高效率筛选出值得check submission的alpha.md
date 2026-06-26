# 如何自动化高效率筛选出值得check submission的alpha

- **链接**: [Commented] 如何自动化高效率筛选出值得check submission的alpha.md
- **作者**: KY86095
- **发布时间/热度**: 1年前, 得票: 16

## 帖子正文

*TIPs: 老师给的模版我没有做太大改动，而是另外在其上重构了一套自己的python库文件。我也建议大家维护一套自己的库，不断的去完善优化。*

## 基本思路：

- 每一批回测都按照自己的标准起个名字： 比如我的格式“SUBINDUSTRY_USA_TOPSP500_241229_1717_mdl25_matrix_top60”，这个name需要在回测时注入到每个alpha信息里面，我的建议是放在name，而不是tag，因为tag是固定的列表，如果做了很多批次，tag列表选取是个大麻烦，而name是可以自己填入的信息，不存在选取问题。
- 抓取alpha列表信息时，按照上面的name去筛选。
- 不要一个一个去locate查询，而是批量查看
- 查询的时候检查是否有FAIL的项目，如果有，直接过滤掉，不需要做check submission动作
- 将过滤后的结果直接写入到一个Alpha List里面
- 最后在Alpha List里面直接查看结果，选取几个手动执行check即可。

## 实现细节：

1. get_alphas增加了一个exclude_fail参数，如果为False，可以作为三阶模版使用。如果为True，可以作为check submission阶段的抓取alpha列表信息。

```
def get_alphas(start_date, end_date, sharpe_th, fitness_th, region, usage='', alpha_num_end=10000, alpha_num_start=0,               name='', full_tag='', exclude_fail=False):    positive_output = get_alphas_operator(start_date, end_date, sharpe_th, fitness_th, region, usage,                                          True, alpha_num_end, alpha_num_start,                                          name, full_tag, exclude_fail)    negative_output = get_alphas_operator(start_date, end_date, sharpe_th, fitness_th, region, usage,                                          False, alpha_num_end, alpha_num_start,                                          name, full_tag, exclude_fail)    output = positive_output    output.extend(negative_output)    lh.info("total_count: %d" % len(output))    return output
```

2. 在get_alphas_operator函数中，有关exclude_fail的使用

```
try:    alpha_list = response.json()["results"]    # lh.debug(response.json())    for j in range(len(alpha_list)):        alpha_id = alpha_list[j]["id"]        name = alpha_list[j]["name"]        dateCreated = alpha_list[j]["dateCreated"]        sharpe = alpha_list[j]["is"]["sharpe"]        fitness = alpha_list[j]["is"]["fitness"]        turnover = alpha_list[j]["is"]["turnover"]        margin = alpha_list[j]["is"]["margin"]        longCount = alpha_list[j]["is"]["longCount"]        shortCount = alpha_list[j]["is"]["shortCount"]        decay = alpha_list[j]["settings"]["decay"]        exp = alpha_list[j]['regular']['code']        if exclude_fail:            # 额外获取是否已经有fail的项目            checks_df = pd.DataFrame(alpha_list[j]["is"]["checks"])            if any(checks_df["result"] == "FAIL"):                continue
```

3. 最终收集可以提交的alpha，并直接保存到一个TAG里。

```
FULL_NAME_LIST = [    'SUBINDUSTRY_USA_TOPSP500_241229_1717_mdl25_matrix_top60',    'SUBINDUSTRY_KOR_TOP600_241229_2323_star_matrix_top60',]FULL_NAME = FULL_NAME_LIST[-1]##############################################################################################################################################################################################################################################################################(_, REGION, _UNIVERSE, DATE_START, prefix, _) = extract_info_from_full_name_str(FULL_NAME)PREFIX_LIST = [prefix]DATE_END = '12-31'ALPHA_LIST_TAG_NAME = '_'.join([REGION, _UNIVERSE, prefix, 'success']).lower()# 1.58 sharpe, 1 fitness, "submit"参数th_tracker = get_alphas(DATE_START, DATE_END, 1.58, 1, REGION, "submit", name=FULL_NAME, exclude_fail=True)print('th_tracker:', th_tracker)def get_unique_data_field(top_sharpe_count=5):    full_field_list = []    for alpha_info in th_tracker:        alpha = alpha_info[1]        for prefix in PREFIX_LIST:            if prefix in alpha:                field_appendix = alpha.split(prefix)[-1].split(",")[0]                full_field = prefix + field_appendix                full_field_list.append(full_field)    new_full_field_list = list(set(full_field_list))    def _pick_full_field_from_exp(exp):        for full_field in full_field_list:            if full_field in exp:                return full_field        return ''    # top_sharpe_alpha_info_list = []    full_field_to_alpha_infos_map = {}    for field in new_full_field_list:        full_field_to_alpha_infos_map[field] = {            'count': 0,            'list': []        }    for alpha_info in th_tracker:        alpha = alpha_info[1]        full_field = _pick_full_field_from_exp(alpha)        # if full_field != 'oth176_lmt_close_eq_score':        #     continue        if len(full_field) == 0:            continue        if full_field_to_alpha_infos_map[full_field]['count'] < top_sharpe_count:            full_field_to_alpha_infos_map[full_field]['count'] += 1            full_field_to_alpha_infos_map[full_field]['list'].append(alpha_info)            # top_sharpe_alpha_info_list.append(alpha_info)        else:            continue    print('full_field_to_alpha_infos_map:', full_field_to_alpha_infos_map)    return full_field_to_alpha_infos_map
```

```
def add_alphas_to_existing_list(s, tag_id, list_name, alpha_list):    payload = {        'op': 'add',        'name': list_name,        'alphas': alpha_list    }    try:        response = s.patch('https://api.worldquantbrain.com/tags/%s' % tag_id, json=payload)        print('add_alphas_to_existing_list: response:', response, response.content, response.reason, response.json())    except:        lh.warning("content: %s" % response.content)        sleep(10)        s = login()
```

```
def add_alphas_to_new_list(s, list_name, alpha_list):payload = {'type': 'LIST','name': list_name,'alphas': alpha_list}try:response = s.post('https://api.worldquantbrain.com/tags', json=payload)except:lh.warning("content: %s" % response.content)sleep(1)s = login()finally:if 'detail' in response.json() and response.json()['detail'] == 'Conflict':tag_id = get_get_tag_id_by_name(s, list_name)print('tag_id:%s is found for name %s' % (tag_id, list_name))if len(list_name) == 0:print('Error: Tag name %s not found' % list_name)returnadd_alphas_to_existing_list(s, tag_id, list_name, alpha_list)
```

```
if __name__ == '__main__':    result = get_unique_data_field(30)    print(json.dumps(result, indent=4))    alpha_id_list = []    for field, val in result.items():        for alpha_info in val['list']:            alpha_id_list.append(alpha_info[0])    if len(alpha_id_list) > 0:        add_alphas_to_new_list(s, ALPHA_LIST_TAG_NAME, alpha_id_list)
```

## 执行的效果展示

下面的信息表示这三个字段出现了可以提交的alpha

```
unique_field_list: ['mdl25_is_61v', 'mdl25_73v', 'mdl25_is_13v', 'mdl25_34v']
```

上面每个data field都会按照Sharpe值从高到低排序，供你优先选择

![图片](images/img_f0a9322576.png)

最后只需要在Alpha List上直接去查看结果即可

---

## 讨论与评论 (7)

### 评论 #1 (作者: MH14654, 时间: 1年前)

感谢！很有用

---

### 评论 #2 (作者: PN39025, 时间: 1年前)

感谢您的分享！您关于重构Python库文件、标准化命名以及高效管理Alpha的经验非常实用，对优化流程有很大帮助。您的建议为我们提供了宝贵的参考，非常感谢！

---

### 评论 #3 (作者: KP26017, 时间: 1年前)

非常有用，谢谢你的分享！

---

### 评论 #4 (作者: SR30962, 时间: 1年前)

求问大佬第一步如何实现？

- 每一批回测都按照自己的标准起个名字： 比如我的格式“SUBINDUSTRY_USA_TOPSP500_241229_1717_mdl25_matrix_top60”，这个name需要在回测时注入到每个alpha信息里面，我的建议是放在name，而不是tag，因为tag是固定的列表，如果做了很多批次，tag列表选取是个大麻烦，而name是可以自己填入的信息，不存在选取问题。

---

### 评论 #5 (作者: RX97746, 时间: 1年前)

- 每一批回测都按照自己的标准起个名字： 比如我的格式“SUBINDUSTRY_USA_TOPSP500_241229_1717_mdl25_matrix_top60”，这个name需要在回测时注入到每个alpha信息里面，我的建议是放在name，而不是tag，因为tag是固定的列表，如果做了很多批次，tag列表选取是个大麻烦，而name是可以自己填入的信息，不存在选取问题。

请问这一步应该是在回测的时候注入，还是在回测结束后拉取时注入

---

### 评论 #6 (作者: SZ83096, 时间: 1年前)

RX97746 : 应该是回测结束时，获取回测alpha id后，注入name

---

### 评论 #7 (作者: LL87164, 时间: 1年前)

[RX97746 SZ83096](/hc/en-us/profiles/27071748433815-RX97746) : 应该是执行回测时注入的。

[KY86095](/hc/en-us/profiles/27705933874071-KY86095) : 想知道注入name和不做这一步对执行效率有多大影响。

---

