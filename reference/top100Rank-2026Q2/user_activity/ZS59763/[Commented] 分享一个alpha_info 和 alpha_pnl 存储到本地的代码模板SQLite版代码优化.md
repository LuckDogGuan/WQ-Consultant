# 分享一个alpha_info 和 alpha_pnl 存储到本地的代码模板（SQLite版）代码优化

- **链接**: [Commented] 分享一个alpha_info 和 alpha_pnl 存储到本地的代码模板SQLite版代码优化.md
- **作者**: LH94963
- **发布时间/热度**: 1年前, 得票: 61

## 帖子正文

分享一个基于SQLite的缓存alpha类，专门用于缓存Alpha info、yearly_stats 和 PnL 数据。

主要包含两个 SQLite 库：

1. AlphaInfoCache - Alpha因子信息缓存
- 基础缓存：存储Alpha因子的基本信息（表达式、设置、性能指标等）
- 年度统计缓存：独立存储Alpha的年度统计数据
- 条件筛选：支持基于JSON字段的复杂查询
- 表达式搜索：支持模糊匹配Alpha表达式

2. AlphaPnlCache - PnL数据缓存
- 原始数据存储：缓存Alpha的损益数据
- 快速检索：基于alpha_id的高效查询

一些使用示例：

- JSON查询

```
cache = AlphaInfoCache()# 复杂条件筛选conditions = {    "pfm.fitness": (">", 1.5),      # fitness > 1.5    "pfm.turnover": ("<", 30),       # turnover < 30    "pfm.sharpe": (">", 0.8)         # sharpe > 0.8}# 可选择特定alpha进行筛选alpha_ids = ["123456", "789012"]filtered_alphas = cache.filter(conditions, alpha_ids)
```

- 表达式搜索

```
# 搜索包含特定操作符的Alpharesults = cache.search_by_expression("rank")# 搜索特定数据字段results = cache.search_by_expression("close")
```

完整代码如下

```
import sqlite3import jsonfrom typing import Optional, Dictimport loggingfrom pathlib import Pathimport osclass AlphaInfoCache:    def __init__(self):        root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")        db_path = os.path.join(root_path, "results", "alpha_info.db")        self.db_path = Path(db_path)        self._init_db()    def _init_db(self):        with sqlite3.connect(self.db_path) as conn:            conn.execute('''                CREATE TABLE IF NOT EXISTS alpha_info (                    alpha_id TEXT PRIMARY KEY,                    data TEXT NOT NULL,                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP                )            ''')            conn.execute('''                CREATE TABLE IF NOT EXISTS alpha_yearly_stats (                    alpha_id TEXT PRIMARY KEY,                    data TEXT NOT NULL,                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP                )            ''')            conn.commit()    def get(self, alpha_id: str) -> Optional[Dict]:        try:            with sqlite3.connect(self.db_path) as conn:                cursor = conn.execute(                    'SELECT data FROM alpha_info WHERE alpha_id = ?',                    (alpha_id,)                )                result = cursor.fetchone()                return json.loads(result[0]) if result else None        except Exception as e:            logging.error(f"Cache get error: {str(e)}")            return None    def set(self, alpha_id: str, data: Dict) -> bool:        try:            with sqlite3.connect(self.db_path) as conn:                conn.execute(                    '''INSERT OR REPLACE INTO alpha_info                     (alpha_id, data) VALUES (?, ?)''',                    (alpha_id, json.dumps(data))                )                conn.commit()                return True        except Exception as e:            logging.error(f"Cache set error: {str(e)}")            return False        def get_yearly_stats(self, alpha_id: str) -> Optional[Dict]:        try:            with sqlite3.connect(self.db_path) as conn:                cursor = conn.execute(                    'SELECT data FROM alpha_yearly_stats WHERE alpha_id = ?',                    (alpha_id,)                )                result = cursor.fetchone()                return json.loads(result[0]) if result else None        except Exception as e:            logging.error(f"Yearly stats cache get error: {str(e)}")            return None    def set_yearly_stats(self, alpha_id: str, data: Dict) -> bool:        try:            with sqlite3.connect(self.db_path) as conn:                conn.execute(                    '''INSERT OR REPLACE INTO alpha_yearly_stats                     (alpha_id, data) VALUES (?, ?)''',                    (alpha_id, json.dumps(data))                )                conn.commit()                return True        except Exception as e:            logging.error(f"Yearly stats cache set error: {str(e)}")            return False        def filter(self, conditions: Dict[str, tuple], alpha_ids: Optional[list] = None) -> list:        """        根据条件筛选数据。        :param conditions: 筛选条件字典，格式为 {"字段路径": (操作符, 值)}。                           例如：{"is.fitness": (">", 1), "is.turnover": ("<", 30)}        :param alpha_ids: 可选参数，指定 alpha_id 数组进行筛选。        :return: 符合条件的数据列表。        """        try:            # 构建查询条件            query_conditions = []            params = []            # 添加 JSON 字段条件            for field_path, (operator, value) in conditions.items():                query_conditions.append(f"json_extract(data, '$.{field_path}') {operator} ?")                params.append(value)            # 添加 alpha_id IN (...) 条件            if alpha_ids:                placeholders = ", ".join(["?"] * len(alpha_ids))  # 动态生成占位符                query_conditions.append(f"alpha_id IN ({placeholders})")                params.extend(alpha_ids)            # 拼接完整的 SQL 查询            where_clause = " AND ".join(query_conditions)            query = f"SELECT data FROM alpha_info WHERE {where_clause}"            # 执行查询            with sqlite3.connect(self.db_path) as conn:                cursor = conn.execute(query, params)                results = cursor.fetchall()            # 解析结果            return [json.loads(row[0]) for row in results]        except Exception as e:            logging.error(f"Filter error: {str(e)}")            return []        def search_by_expression(self, pattern: str) -> list:        """        根据表达式模式在alpha信息中进行模糊搜索                Args:            pattern: 要匹配的表达式模式                Returns:            匹配到的alpha信息列表        """        try:            pattern_with_wildcards = f"%{pattern}%"                        with sqlite3.connect(self.db_path) as conn:                cursor = conn.execute(                    "SELECT data FROM alpha_info WHERE json_extract(data, '$.exp') LIKE ?",                    (pattern_with_wildcards,)                )                # 与filter方法保持一致的返回格式                return [json.loads(row[0]) for row in cursor.fetchall()]        except Exception as e:            logging.error(f"搜索表达式时出错: {e}")            return []class AlphaPnlCache:    def __init__(self):        root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")        db_path = os.path.join(root_path, "results", "alpha_pnl.db")        self.db_path = Path(db_path)        self._init_db()    def _init_db(self):        with sqlite3.connect(self.db_path) as conn:            conn.execute('''                CREATE TABLE IF NOT EXISTS alpha_pnl (                    alpha_id TEXT PRIMARY KEY,                    raw_data TEXT NOT NULL,                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP                )            ''')            conn.commit()    def get(self, alpha_id: str) -> Optional[dict]:        try:            with sqlite3.connect(self.db_path) as conn:                cursor = conn.execute(                    'SELECT raw_data FROM alpha_pnl WHERE alpha_id = ?',                    (alpha_id,)                )                result = cursor.fetchone()                return json.loads(result[0]) if result else None        except Exception as e:            logging.error(f"Pnl cache get error: {str(e)}")            return None    def set(self, alpha_id: str, raw_data: dict) -> bool:        try:            with sqlite3.connect(self.db_path) as conn:                conn.execute(                    '''INSERT OR REPLACE INTO alpha_pnl                     (alpha_id, raw_data) VALUES (?, ?)''',                    (alpha_id, json.dumps(raw_data))                )                conn.commit()                return True        except Exception as e:            logging.error(f"Pnl cache set error: {str(e)}")            return False
```

---

## 讨论与评论 (4)

### 评论 #1 (作者: TQ88961, 时间: 1年前)

非常好。不知道用mongo数据库是不是会更好呢？它原生支持json

---

### 评论 #2 (作者: ZS59763, 时间: 1年前)

很有用的代码，感谢分享，我的sql水平仅限于select* from，看来要好好练一下了

===生活就像海洋，只有意志坚强的人才能到达彼岸===

===This is an apple, I like apples, apples are good for our health===

---

### 评论 #3 (作者: FL39657, 时间: 1年前)

对管理自己的alpha有很大帮助

---

### 评论 #4 (作者: HW93328, 时间: 1年前)

很好的分享，感谢大佬！想问下楼主将alpha保存在sqlite数据库中的存储空间占用如何，大量存储alpha的话感觉云服务器上的空间会不够用（配置太低），感觉后续可以尝试下云端+本地的数据库方案。总之感谢大佬提供的数据库部署思路，祝alpha多多！！

==================================================================================================

---

