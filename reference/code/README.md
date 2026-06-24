# PPA 数据集与字段批量获取脚本使用说明

本目录下的 `fetch_ppa_datasets.py` 脚本源自 WorldQuant Brain 社区官方分享，主要用于批量爬取并导出符合本次 PPA（Predictive Power Alpha）主题的数据集及其全部可用字段。

## 一、 文件结构
* **`fetch_ppa_datasets.py`**: 爬取核心脚本。能够自动通过限制参数（如 `theme=true`）获取关联的数据集，并对每个数据集遍历抓取所有具体字段输出为 CSV 文件。
* **`config.yaml`**: 配置文件。已自动从本地系统配置中提取您的 WorldQuant Brain 账号凭据进行初始化。

## 二、 使用方法
在终端中进入当前目录，直接运行以下命令：
```bash
python fetch_ppa_datasets.py
```

## 三、 输出结果说明
脚本运行完成后，将在当前目录下生成以下内容：
1. **`theme_datasets_USA_1_TOP3000.csv`**: 本次 PPA 主题覆盖的所有数据集元数据列表。
2. **`theme_fields_USA_1_TOP3000/` (目录)**: 存放针对每个数据集单独导出的字段信息 CSV 文件。
3. **`theme_fields_all_USA_1_TOP3000.csv`**: 本次 PPA 筛选出的所有数据集下全部可用字段的汇总列表，方便批量检索和本地因子挖掘。

> [!NOTE]
> 脚本中已预配置 `tenacity` 重试机制，能够自动应对偶发性网络抖动，保障爬取流程的稳健执行。
