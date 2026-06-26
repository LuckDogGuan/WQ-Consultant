# 【新人向】是否还在对华子哥数据WebDataRAW不会解压而感到苦恼！即插即用代码来了，仅需Excel就可以进行数据分析！代码优化

- **链接**: [Commented] 【新人向】是否还在对华子哥数据WebDataRAW不会解压而感到苦恼即插即用代码来了仅需Excel就可以进行数据分析代码优化.md
- **作者**: LX57490
- **发布时间/热度**: 2个月前, 得票: 24

## 帖子正文

### **本帖子展示了如何将华子哥前辈（ [KZ79256](/hc/en-us/profiles/13609593802263-KZ79256) ）制作的WebDataRAW解压成Excel进行数据分析！**

**注：内存要求极高，请清空电脑目前全部其他打开的应用再进行运行代码！！！！**

**运行内存10G+可尝试！！！！**

**一、配置**

**1.  解压完WebDataRAW_20250219_V0.10.9在图示位置随便创建一个.py文件 ！   ![图片](images/img_f02b6639cd.png)**

**2.  复制代码到这个.py文件里面**

```
import pandas as pdimport msgpackimport zlibimport pickleimport osfrom collections.abc import Iterable# 数据加载函数 (保持原样)def load_obj(name: str) -> object:    with open(name + '.pickle', 'rb') as f:        return pickle.load(f)# 数据解码函数 (稍作优化)def decode_from_bin(file_path):    try:        with open(file_path, 'rb') as f:            compressed_data = f.read()        decompressed_data = zlib.decompress(compressed_data)        # 解决msgpack未导入的问题        import msgpack        data = msgpack.unpackb(decompressed_data, raw=False)        print(f"数据已从 {file_path} 成功解码")        return data    except Exception as e:        print(f"解码过程出错: {str(e)}")        return Nonedef merge_datasets(res_df, settings_df, is_df, os_df):    """合并四个具有相同ID的数据集"""    # 逐步合并数据（类似SQL JOIN）    merged = res_df.merge(settings_df, on='id', how='left', suffixes=('', '_settings'))    merged = merged.merge(is_df, on='id', how='left', suffixes=('', '_is'))    merged = merged.merge(os_df, on='id', how='left', suffixes=('', '_os'))    # 清理可能的重复列（保留原始列）    return merged.loc[:, ~merged.columns.duplicated()]def flatten_dict(d, parent_key='', sep='_'):    items = []    for k, v in d.items():        new_key = f"{parent_key}{sep}{k}" if parent_key else k        if isinstance(v, dict):            items.extend(flatten_dict(v, new_key, sep=sep).items())        elif isinstance(v, Iterable) and not isinstance(v, str):            items.append((new_key, ', '.join(map(str, v))))        else:            items.append((new_key, v))    return dict(items)def save_to_csv(data, filename, max_depth=3):    """    智能保存数据到CSV    """    # 创建输出目录    output_dir = 'data_csv'    os.makedirs(output_dir, exist_ok=True)    filepath = os.path.join(output_dir, filename)    if isinstance(data, dict):        # 展平嵌套字典        flat_data = flatten_dict(data)        pd.DataFrame([flat_data]).to_csv(filepath, index=False)        print(f"字典数据已保存到 {filepath}")    elif isinstance(data, list) and all(isinstance(item, dict) for item in data):        # 处理字典列表        flat_data = []        for item in data:            try:                # 只展平前max_depth层嵌套                flat_data.append(flatten_dict(item, sep='_'))            except:                flat_data.append(item)  # 回退到原始数据        df = pd.DataFrame(flat_data)        df.to_csv(filepath, index=False)        print(f"列表数据({len(data)}条)已保存到 {filepath}")    else:        # 其他类型直接创建DF        try:            pd.DataFrame(data).to_csv(filepath, index=False)            print(f"数据已保存到 {filepath}")        except Exception as e:            print(f"无法保存 {filename}: {str(e)}")            with open(filepath.replace('.csv', '.txt'), 'w') as f:                f.write(str(data))def convert_to_dataframe(data):    """智能转换为DataFrame"""    if isinstance(data, dict):        return pd.DataFrame([flatten_dict(data)])    elif isinstance(data, list) and data and isinstance(data[0], dict):        return pd.DataFrame([flatten_dict(x) for x in data])    return pd.DataFrame(data)# 主处理函数def export_all_to_csv():    # 1. 加载全局数据    all_data = load_obj('all_data')  # 加载pickle数据    info_data = decode_from_bin('info_data.bin')  # 加载bin数据    # 2. 单独保存info_data（保持原功能）    save_to_csv(info_data, 'info_data.csv')    # 3. 配置所有需处理的地区和延迟    regions = ['USA', 'EUR', 'IND', 'ASI', 'GLB', 'JPN', 'KOR', 'HKG', 'TWN', 'CHN']    delays = [0, 1]    # 4. 为每个地区/延迟生成合并文件    for region in regions:        for delay in delays:            key = f"{region}_{delay}"            if key not in all_data:                continue            print(f"\n处理地区: {region}, 延迟: {delay}")            res, settings, is_data, os_data = all_data[key]            # 将各数据集转换为DataFrame            df_res = convert_to_dataframe(res)            df_settings = convert_to_dataframe(settings)            df_is = convert_to_dataframe(is_data)            df_os = convert_to_dataframe(os_data)            # 添加ID列（如果不存在）            for df, name in zip([df_res, df_settings, df_is, df_os],                                ['res', 'settings', 'is_data', 'os_data']):                if 'id' not in df.columns:                    df.insert(0, 'id', range(1, len(df) + 1))            # 合并数据集并保存            merged = merge_datasets(df_res, df_settings, df_is, df_os)            filename = f"merged_{region}_{delay}.csv"            save_to_csv(merged, filename)if __name__ == "__main__":    export_all_to_csv()
```

二、结果

1.   **解压比较慢，请耐心等待！！！！**

在data_csv里面会得到如下内容！
 ![图片](images/img_b2f1252169.png)

2. 效果图

在这里你可以找到alpha的ID，数据标签，数据集类型，具体数据字段，具体数据集类型，操作符数量，IS数据，Risk数据，max trade数据，23 OS数据，2023年~2026.2月提交时间，制作alpha时间等等！

当然这只是一个小小的解压代码，你可以改进成更好的可视化等等！进行顶级的数据分析！

**最后祝各位顾问月月VF1.0！RA60刀！SA60！日日120刀！！！！**

**高筑墙！广积粮！缓称王！**

![图片](images/img_a64a5378ff.png)

---

## 讨论与评论 (25)

### 评论 #1 (作者: RM49262, 时间: 2个月前)

=====================================评论区====================================

尼克太强了吧

这个新人向系列实在太实用了 学到了很多

给尼克大佬点赞

=============================================================================

---

### 评论 #2 (作者: GZ60647, 时间: 2个月前)

来学习尼克总的帖子了。非常实用，马上搭起来搞上。电脑内存有32G，跑这个还是足够的。

基于这些数据确实能在动手挖掘前就得到充足的信息，可以少走弯路。

********************   高质量，多样性，做好量化每一天   *******************

---

### 评论 #3 (作者: FZ60707, 时间: 2个月前)

这个解压方案太实用了，直接解决了WebDataRAW的解析痛点，代码清晰又贴心，感谢分享！

====================================================================================================================================================================

---

### 评论 #4 (作者: CZ78575, 时间: 2个月前)

==================================================================================

感谢大佬分享

----------    好东西，快把这个代码给我啊==================================================================================

---

### 评论 #5 (作者: PY58917, 时间: 2个月前)

谢谢nick哥的教程，我前些天没看论坛和群聊使得我在下载插件后一头雾水，不知道如何下手，就搁置在一旁。谢谢nick哥的教程，解决了我很大的问题。
========================================================================
知难行易，知易行难，都是要做下去的
==============================================
成本损耗 ≈ 换手 ≈ 信号变化速度 ≈ 1 / Half-life
====================================
Retention=AC/BC
============================================================
==============================================================

---

### 评论 #6 (作者: YH25030, 时间: 2个月前)

谢谢分享。刚才在云电脑上运行了一下程序，跑得时间有点长。的确对内存有要求（笑）

---

### 评论 #7 (作者: CZ39633, 时间: 2个月前)

====================================================================================  感谢大佬的关于怎么解决华子哥数据分析工具对于内存要求高的痛处                                                                      ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #8 (作者: MH33969, 时间: 2个月前)

一直都不知道 **WebDataRAW_20250219_V0.10.9这个压缩包是干什么用的！现在终于知道了！万分感谢！**

---

### 评论 #9 (作者: FF65210, 时间: 2个月前)

感谢大佬，分享，新人非常缺好东西，又拿到一个好代码了。

===============================================================================
守正心，戒浮躁，恒复盘，危中机。“复利是世界第八大奇迹，关键在于找到可长期重复的正确策略，日复一日、不疾不徐地执行。”—— 爱因斯坦 / 查理・芒格
Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
sys.setrecursionlimit(α∞)
PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值# 有志者事竟成，苦心人天不负。千淘万漉虽辛苦，吹尽狂沙始到金。
=================================================================================

---

### 评论 #10 (作者: JJ69164, 时间: 2个月前)

===================================================================================================================我也来写评论了=====================================

感谢nick佬的教程，我正在为看不懂WebDataRAW数据而发愁呢，及时雨解决了我很大的困惑，别的也不太熟悉，Excel功能还用的算可以，话不多说赶紧去转换数据用起来。
找到alpha的ID，数据标签，数据集类型，具体数据字段，具体数据集类型，操作符数量，IS数据，Risk数据，max trade数据，23 OS数据，2023年~2026.2月提交时间，制作alpha时间等等：原来有这么多可以用啊，ID都有但我这没想到咋用呢，哪位大佬说说咋用这个ID呗很想要不知道咋用~

====================================================================================================================点赞的大佬高OS====================================

---

### 评论 #11 (作者: JD13815, 时间: 2个月前)

内存无所谓的，我内存管够，这么本地跑一遍挺好的，因为华子哥插件时不时就抽风，一阵有一阵没有的。

没有的时候就十分抓瞎，这个脚本拉到本地就不会受插件抽风的影响了。

---

### 评论 #12 (作者: YX50005, 时间: 2个月前)

谢谢大佬分享！太酷了！迫不及待要试一下！想再进一步问一下，大佬后面是如何利用这份数据的呢，如果全部传给AI会不会太大了

---------------------If you come to the forum to study hard every day, you will get a GM---------------------------------

---------------------------------------------------------------------------------------------------------------------------

---

### 评论 #13 (作者: FF45555, 时间: 2个月前)

刚刚试了一下，会提示“    import msgpack
ModuleNotFoundError: No module named 'msgpack'”

因为没有安装msgpack module，

提供一下安装代码：-m pip install msgpack

在终端输入安装完之后再运行就不会报错了

====================================================================================== # Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100% # sys.setrecursionlimit(α∞) # PnL = ∑(Robustness * Creativity) #无限探索、鲁棒性优先，创新性增值 #Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。

---

### 评论 #14 (作者: AK76468, 时间: 2个月前)

==================================================================================

感谢分享！ 程序跑一会就好了，就是csv文件打开是得等一会😂，这下选择性的跑一跑字段了!

==================================================================================

---

### 评论 #15 (作者: BW14163, 时间: 2个月前)

感谢分享，非常有用

**********************************
紧跟大佬的脚步，每天坚持至少学一个知识点，尽量不混信号，不过拟合。
Prioritize diversity, strong margin, low correlation, stable diversification; strictly control costs and overfitting.
**********************************

---

### 评论 #16 (作者: XY20037, 时间: 2个月前)

太感谢大佬分享这个 WebDataRAW 一键解压代码！完美解决新人最头疼的数据解析难题，代码优化得很干净，直接复制运行就能导出 Excel 可读取的 CSV，内存提醒和步骤也写得特别清晰，对新手极度友好。终于能轻松分析全量数据、挖掘有效因子了，实用度拉满，祝大佬 VF 长虹、收益节节高！

---

### 评论 #17 (作者: CZ26433, 时间: 2个月前)

非常有用，内存大好解决，国区人才辈出啊

---

### 评论 #18 (作者: XW25488, 时间: 2个月前)

小内存只能先学习思路了，谢谢老师分享！！！

---

### 评论 #19 (作者: MY82844, 时间: 2个月前)

太强了，多谢分享！

是说可以看到alpha的使用字段信息了吗？有alpha的使用算符信息吗？

====================================================================

"Pain + Reflection = Progress"

====================================================================

---

### 评论 #20 (作者: HK79942, 时间: 2个月前)

# 数据加载函数 (保持原样)

def load_obj(name: str) -> object:

"""Load a pickled object with compatibility for numpy internal module moves.

Some pickles reference internal numpy modules like 'numpy._core.numeric'

which may not exist on newer numpy versions. This function first tries a

normal load, and if that fails due to ModuleNotFoundError, it uses a

custom Unpickler that remaps 'numpy._core' -> 'numpy.core' during lookup.

"""

path = name + '.pickle'

with open(path, 'rb') as f:

try:

return pickle.load(f)

except ModuleNotFoundError:

f.seek(0)

class CompatUnpickler(pickle.Unpickler):

def find_class(self, module, name):

# Remap old numpy internal module names to current ones

if module.startswith('numpy._core'):

module = module.replace('numpy._core', 'numpy.core')

return super().find_class(module, name)

return CompatUnpickler(f).load()
解决numpy版本兼容问题

---

### 评论 #21 (作者: XC66172, 时间: 2个月前)

谢谢佬分享，之前下载了一直不知道如何使用。现在可以解压看一下数据~~

=====================================

FIGHTING LABUBU!

=====================================

---

### 评论 #22 (作者: WT26072, 时间: 1个月前)

不愧是尼克大佬，不仅热心，还有实力，还无私分享自己写的代码，感谢大佬们

---

### 评论 #23 (作者: MZ45384, 时间: 1个月前)

nick大佬太强了。这样可以查看以前交过哪些塔的数据，更方便横向点塔了。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #24 (作者: JX84394, 时间: 1个月前)

感谢尼克大佬！非常好用！

---

### 评论 #25 (作者: WW11235, 时间: 24天前)

请问华子哥的WebDataRAW_20250219_V0.10.9在哪里下载，找了github和华子哥的帖子，还是没有找到。新手问题，感谢指导

---

