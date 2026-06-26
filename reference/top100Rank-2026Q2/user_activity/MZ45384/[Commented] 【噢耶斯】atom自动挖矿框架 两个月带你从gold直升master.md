# 【噢耶斯】atom自动挖“矿”框架 (两个月带你从gold直升master)

- **链接**: [Commented] 【噢耶斯】atom自动挖矿框架 两个月带你从gold直升master.md
- **作者**: WS29639
- **发布时间/热度**: 8个月前, 得票: 43

## 帖子正文

先截个上赛季的提交情况～

![图片](images/img_86405a8647.png)

![图片](images/img_c34d8ec978.png)

![图片](images/img_80ca735ead.png)

从成为条件顾问开始，用了两个月成为master还是有点小激动的。本来早就想写写自动挖掘框架分享，不过因为之前代码太垃圾早就看不下去了，从10.1到今天断断续续一直在重构，昨天终于完成了！由于第二版针对性地进行了大幅度改进，包括大量减少人工成本 & 提高回测速度 & 提高回测效率，在这里就不分享第一版的工作了。

先看个整体的流程示意图

![图片](images/img_6be6045e77.png)

## 一、字段库

存储权限下的所有字段，由于region和delay影响较大，在这里进行了拆分。此外为了保存历史回测信息即方便后续的筛选，保存的kv如下：

```
key = datafield#region#delayvalue = {  "simu_times": 0,  "simu_templates": [],  "good_alphas": [],   "better_alphas": [],     "best_alphas": [],     }
```

其中的simu_times指的是回测次数，simu_templates是记录回测的模板ids，good_alphas表示的是用该字段的有潜力的alpha_ids，better_alphas表示的是可以进一步优化的alpha_ids，best_alphas表示的是能提交的优秀alpha_ids。记录的alpha_id全部是在不考虑sc和pc的条件下，这里纠结了挺久，不过留了一个接口即存储的是alpha_id，因此后续考虑corr的时候可以在这里直接将其删除。

## 二、回测模块1

### 字段&模版筛选

1. 字段筛选：

考虑到alpha的多样性，可以使用随机字段。但是由于不同的region和category，字段数量差异较大，比如model类的字段很多，那随机的话很有可能全是model字段，丧失多样性。在这里我的选择是五步法：随机region&delay -> 随机category -> 随机dataset -> 随机universe -> 内部优选datafield。

其中优选datafield的逻辑就是10%的概率随机选择即探索，90%概率按照得分的rank概率选择，以防止极端值的影响。得分逻辑如下，其中的max_xxx是计算的同组下即region+delay+category+dataset的最大值

score = 0.3 * (0.5*simu_times/max_simu_times + 0.5*len(simu_templates)/max_simu_templates + 0.7 * (1/6*len(good_alphas)/max_good_alphas + 2/6* len(better_alphas)/max_better_alphas + 3/6* len(best_alphas)/max_best_alphas

此外，在这个阶段还设置了强制使用/不使用region/dataset/datafield的情况，方便在主题、点塔、代码未覆盖的异常字段情况。新增字段ext_infos记录一些信息比如比如template_id、post_hash一类的

2. 模板筛选

设置多个模板，每个模板的空间尽量在1k以内，每个模板的记录结构可以和datafield相同，并按照rank进行挑选。这里可做的东西比较多，可以专门用一个类去处理，什么样的data优先哪几种模板，比如缺失值过多的就用backfill一类的，然后做时间的朋友，哪个出货多让框架自动选择就好了。

目前偷懒，只有几个模板，基本就是像下面这种所有算子大杂烩，反正效果还可以，后面有时间再优化吧～

![图片](images/img_1c85f32602.png)

### 异步请求

没什么好说的，直接async那套，做好异常检测就ok，失败就不纠结，直接报日志 & 跳过！

![图片](images/img_794ee6d63f.png)

![图片](images/img_6ebfc6b16b.png)

### 回测完成记录信息

为了方便，没有用服务的方式，就直接写入到文件了，用豆包搞下多文件&异步下的写锁读不锁逻辑就好了，在这里分享下我的mq消息，包含id、ts即时间戳用来更改alpha_name方便检索，processing字段和processed字段用来仿真mq队列和断点续写功能，注意代码运行的开始需要将所有processed为false的processing强制为也false，不然断点续写的时候会丢失消息。

![图片](images/img_ca84efbf40.png)

![图片](images/img_2eef351f56.png)

## 三、回测模块2

主要针对step2_db（后面介绍）中的，可进一步优化的alpha，进行精细化调优，以后可以考虑用llm接口来做，目前逻辑比较简单。

1. 随机选择一个待优化的alpha_id进行扩展，扩展的alphas都标记为同一个parent。选择的条件为该alpha的自相关较低，sharpe不低，pc如果有则不高，没有parent_alpha即非扩展alpha
2. 如果sharpe小于 -0.8, 构造相同请求，但是 regular = -code，且不设置 parent_alpha
3. 对该alpha的datafield涉及到的所有universe，所有中性化，decay为[5, 20, 60, 250]，进行全扩展，并去掉重复回测（post_hash）后
4. 循环读入10个初始alpha，并随机选择一种region+delay的前8个alpha做multi_simu
5. step1初始回测和step2优化回测，目前设置的并行度是5:3

## 四、记录&评估模块

这里用于存储的db，采用的是python的库aiosqlite，挺好用的。

### 记录模块

记录回测结果，放到step1_db。为了方便后续的分析（并没有），我选择abs(val["is"]["sharpe"]) >0.5的时候就下载pnl，反正也是和回测并行，不影响耗时，也无所谓。最后将这种有pnl的alpha设置为good alpha

### 评估模块1

读取step1_db，评估可以进一步优化的alpha，放到step2_db。在这里什么叫可以进一步优化的呢，以下逻辑依次进行，剩下的就是进入step的alpha。

1. 没有pnl信息，即abs(val["is"]["sharpe"]) <=0.5
2. "厂型"曲线不要，在这里通过解析pnl信息，将last_update_days_to_now <=60的定义为"厂型"曲线，与此同时，删掉之前错误设置的good alpha
3. 年限较短且效果不是特别好的不要，first_update_years_to_now <= 6 and (not (abs(json_data["is"]["sharpe"]) >= 1.58 and abs(json_data["is"]["fitness"]) >= 1.0))，与此同时，删掉之前错误设置的good alpha
4. parent_alpha要删掉之前错误设置的good alpha。这一点比较重要，因为标记parent_alpha的因子都是由同一个父alpha简单扩展而来，当父alpha不错的时候，可能会产生很多不错的扩展alphas，并记录到good/better/best alpha，会严重影响第一步的字段筛选逻辑
5. abs(json_data["is"]["sharpe"]) <= 0.8的不要
6. 满足上述所有条件，且没有parent_alpha的，设置为better_alpha
7. 未检测出faild，且不是parent_alpha，设置为best_alpha
8. 针对region计算self_corr>0.6，则继续优化的空间较低，跳过

### 评估模块2

step2_db每隔一段时间，遍历所有数据，重新计算self corr

```
if alpha_id in 不考虑pc的情况可以展现出来(显示模块):    if 计算了pc and pc >=0.8: pass    elif 未计算pc 或 sc距离上一次有变化:         计算pc        等待4min
```

### 显示模块

在这里我定义的不能交的因子为

1. 高相关性：不满足ppa或者ra的标准（这里不考虑pc不满足但sharpe>10%的情况）
2. 厂型：last_update_days_to_now <=30
3. 有faild
4. 有concentrated_weight的warn
5. 死因子：turnover < 0.05
6. 时间短效果还不是特别好：first_update_years_to_now <= 5 and warning_num != 0
7. 最近两年不行了: low_2y_sharpe < 1.0
8. Margin不够，GLB和ASI为15，USA和EUR为10（为了提高alpha数量，而且也打开了max trade，在这里给了点浮动空间，全部降低20%）
9. 年sharpe>1占总年数比例低于60%，年sharpe>0占总年数比例低于90%
10. 收益低于回撤：return < (0.8) * drawback

我没有写自动提交alpha模块，考虑点有如下：

1. 代码可能写的不完善，放出了一些不合适的alpha。

2. 定义alpha的好坏并没有唯一的指标，我只是按照warn数量、fitness进行排序，给出一个大概的排名，当手头alpha比较多时，可以参考排名并具体情况具体分析。

3. 过去10年和过去2年sharpe>1的比例，要多看看pnl并对比其他alpha

4. alpha的多样性可控

5. 即便排名准确，也不一定要提交最优秀的alpha，因为可能会影响大量的alpha的self corr，要自行斟酌

6. 可能会出现操作符冗余，比如去掉backfill效果更好

另外给大家提供下打印思路，解析字符串，按照region_delay，warn升序，Fitness降序排列

![图片](images/img_818bfc6b90.png)

最后，祝大家早日登上M/GM，走上人生巅峰！

最后附两个工具，python的DB和MQ

```
# async_mq_json.pyimport osimport uuidimport jsonimport asynciofrom datetime import datetimeclass AsyncMQ:    def __init__(self, storage_file="mq_messages.json"):        self.storage_file = storage_file        self._init_storage()            def _init_storage(self):        """初始化消息存储文件"""        if not os.path.exists(self.storage_file):            with open(self.storage_file, 'w') as f:                json.dump([], f)                    async def _read_messages(self):        """异步读取消息列表"""        loop = asyncio.get_event_loop()        return await loop.run_in_executor(None, self._sync_read_messages)        def _sync_read_messages(self):        """同步读取消息列表（用于在异步中执行）"""        try:            with open(self.storage_file, 'r') as f:                return json.load(f)        except (json.JSONDecodeError, FileNotFoundError):            return []        async def _write_messages(self, messages):        """异步写入消息列表"""        loop = asyncio.get_event_loop()        await loop.run_in_executor(None, self._sync_write_messages, messages)        def _sync_write_messages(self, messages):        """同步写入消息列表（用于在异步中执行）"""        with open(self.storage_file, 'w') as f:            json.dump(messages, f, indent=2)    async def reset_processing(self):        messages = await self._read_messages()        for msg in messages:            if "processing" in msg:                msg["processing"] = False        await self._write_messages(messages)        async def enqueue(self, data):        """将JSON数据加入队列"""        # 确保输入是JSON可序列化的        try:            json.dumps(data)        except (TypeError, ValueError) as e:            raise ValueError(f"数据不可序列化为JSON: {e}")                messages = await self._read_messages()                # 创建带ID和时间戳的消息        message = {            "id": str(uuid.uuid4()),            "timestamp": datetime.now().isoformat(),            "data": data,  # 存储JSON数据            "processing": False,            "processed": False        }                messages.append(message)        await self._write_messages(messages)        return message["id"]        async def dequeue(self):        """获取下一个未处理的消息"""        messages = await self._read_messages()                # 找到第一个未处理的消息        for msg in messages:            if not msg.get("processed") and not msg.get("processing"):                msg["processing"] = True                await self._write_messages(messages)                return msg        return None            async def unprocessed_msg_num(self):        """获取剩余未处理的消息数量"""        messages = await self._read_messages()                ret = 0        for msg in messages:            if not msg.get("processed") and not msg.get("processing"):                ret += 1        return ret        async def mark_processed(self, message_id):        """标记消息为已处理"""        messages = await self._read_messages()                for msg in messages:            if msg["id"] == message_id:                msg["processed"] = True                msg["processing"] = False                await self._write_messages(messages)                return True        return False
```

```
# kv_database_json.pyimport aiosqliteimport asyncioimport osimport jsonimport fcntlfrom typing import Any, Optional, List, Dict, AsyncGeneratorimport hashlibfrom .utils import *class KVJsonDatabase:    def __init__(self, db_path: str = "kv_json_database.db", lock_path: Optional[str] = None):        """初始化支持多进程异步操作的KV JSON数据库                Args:            db_path: 数据库文件路径            lock_path: 跨进程锁文件路径，默认在数据库同目录下        """        self.db_path = db_path        self.lock_path = lock_path or os.path.splitext(db_path)[0] + ".lock"                # 单进程内的异步写锁        self.write_lock = asyncio.Lock()        self._initialized = False        # 新增：批量预加载的配置和缓存        self._preload_batch = 20000  # 内部一次预加载多少条（核心调优参数）        self._preload_cache: List[tuple[str, Any]] = []  # 预加载数据的缓存                # 确保锁文件目录存在        if os.path.dirname(self.lock_path):            os.makedirs(os.path.dirname(self.lock_path), exist_ok=True)    async def _acquire_file_lock(self):        """获取跨进程文件锁（异步包装）"""        # 因为fcntl是同步操作，需要在线程池中执行        loop = asyncio.get_event_loop()        self._lock_file = open(self.lock_path, 'w')                # 非阻塞获取锁，避免死锁        try:            await loop.run_in_executor(                None,                 lambda: fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)            )            return True        except BlockingIOError:            # 锁已被其他进程占用，等待后重试            await asyncio.sleep(0.1)            return await self._acquire_file_lock()    async def _release_file_lock(self):        """释放跨进程文件锁"""        if hasattr(self, '_lock_file') and self._lock_file:            loop = asyncio.get_event_loop()            await loop.run_in_executor(                None,                lambda: fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_UN)            )            self._lock_file.close()            delattr(self, '_lock_file')        async def _initialize_db(self):        """异步初始化数据库表结构"""        if self._initialized:            return                    # 确保数据库文件所在目录存在        if os.path.dirname(self.db_path):            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)                    # 初始化表结构（需要加锁确保只有一个进程执行初始化）        async with self.write_lock:            await self._acquire_file_lock()            try:                async with aiosqlite.connect(self.db_path) as conn:                    await conn.execute('''                    CREATE TABLE IF NOT EXISTS key_value (                        key TEXT PRIMARY KEY,                        value TEXT NOT NULL                    )                    ''')                    await conn.commit()            finally:                await self._release_file_lock()                    self._initialized = True        async def get(self, key: str, default: Any = None) -> Any:        """异步读取键对应的值（无读锁）"""        await self._initialize_db()                async with aiosqlite.connect(self.db_path) as conn:            # 启用读未提交隔离级别，允许读取未提交的数据            await conn.execute("PRAGMA read_uncommitted = 1")            async with conn.execute(                "SELECT value FROM key_value WHERE key = ?",                (key,)            ) as cursor:                result = await cursor.fetchone()                if result:            try:                return json.loads(result[0])            except json.JSONDecodeError:                return result[0]        return default        async def get_many(self, keys: List[str]) -> Dict[str, Any]:        """异步批量读取多个键的值（无读锁）"""        if not keys:            return {}                    await self._initialize_db()                placeholders = ', '.join('?' for _ in keys)        query = f"SELECT key, value FROM key_value WHERE key IN ({placeholders})"                async with aiosqlite.connect(self.db_path) as conn:            await conn.execute("PRAGMA read_uncommitted = 1")            async with conn.execute(query, keys) as cursor:                results = await cursor.fetchall()                items = {}        for key, value in results:            try:                items[key] = json.loads(value)            except json.JSONDecodeError:                items[key] = value                return items    async def get_all(self) -> Dict[str, Any]:        """异步获取所有键值对（无读锁）"""        await self._initialize_db()                async with aiosqlite.connect(self.db_path) as conn:            await conn.execute("PRAGMA read_uncommitted = 1")            async with conn.execute("SELECT key, value FROM key_value") as cursor:                results = await cursor.fetchall()                all_items = {}        for key, value in results:            try:                all_items[key] = json.loads(value)            except json.JSONDecodeError:                all_items[key] = value                return all_items                async def iter_all(self, batch_size: int = 5000) -> AsyncGenerator[tuple[str, Any], None]:        """异步生成器，流式返回所有键值对，改进版避免长时间阻塞写入                改进点：        1. 每批数据读取后关闭连接，允许写入操作执行        2. 使用事务隔离级别优化，减少锁竞争        """        await self._initialize_db()                # 先获取总记录数        async with aiosqlite.connect(self.db_path) as conn:            await conn.execute("PRAGMA read_uncommitted = 1")            async with conn.execute("SELECT COUNT(*) FROM key_value") as count_cursor:                count_result = await count_cursor.fetchone()                total = count_result[0] if count_result else 0                # 分页查询所有记录，每批处理完释放连接        offset = 0        while offset < total:            # 每批数据使用新的连接，避免长时间持有连接            async with aiosqlite.connect(self.db_path) as conn:                # 使用更宽松的事务隔离级别                await conn.execute("PRAGMA journal_mode = WAL")  # 启用WAL模式                await conn.execute("PRAGMA synchronous = NORMAL")                await conn.execute("BEGIN TRANSACTION")                                async with conn.execute(                    "SELECT key, value FROM key_value LIMIT ? OFFSET ?",                    (batch_size, offset)                ) as cursor:                    async for row in cursor:                        key, value = row                        try:                            yield key, json.loads(value)                        except json.JSONDecodeError:                            yield key, value                                await conn.rollback()  # 只读操作，回滚释放锁                        offset += batch_size                        # 每批处理后短暂休眠，给写入操作机会            await asyncio.sleep(0.001)        async def set(self, key: str, value: Any):        """异步设置键值对（带双重写锁）"""        await self._initialize_db()        # 将值序列化为JSON字符串        json_value = json.dumps(value)                # 双重锁定：先单进程锁，再跨进程锁        except_time = 1        while True:            if except_time % 10 == 0: logger.error(f"{key} 写入db失败，继续重试！")            async with self.write_lock:                await self._acquire_file_lock()                try:                    async with aiosqlite.connect(self.db_path) as conn:                        await conn.execute(                            "INSERT OR REPLACE INTO key_value (key, value) VALUES (?, ?)",                            (key, json_value)                        )                        await conn.commit()                    test_value = await self.get(key)                    # print(value, test_value)                    if await self.are_nested_dicts_equal(value, test_value):                        return                     else:                        await asyncio.sleep(0.5)                                    except:                    except_time += 1                    await asyncio.sleep(1)                finally:                    await self._release_file_lock()        async def set_many(self, items: Dict[str, Any]):        """异步批量设置键值对（带双重写锁）"""        if not items:            return                    await self._initialize_db()                # 将所有值序列化为JSON        json_items = [(k, json.dumps(v)) for k, v in items.items()]                async with self.write_lock:            await self._acquire_file_lock()            try:                async with aiosqlite.connect(self.db_path) as conn:                    await conn.executemany(                        "INSERT OR REPLACE INTO key_value (key, value) VALUES (?, ?)",                        json_items                    )                    await conn.commit()            finally:                await self._release_file_lock()        async def get_all_key_field_mapping(self, field: str) -> Dict[str, Any]:        """        快速获取所有记录的「key + 目标字段」映射（SQL层直接解析）                Args:            field: 目标字段名（支持嵌套字段，如 "order.total"）        Returns:            Dict[key: 目标字段值]（跳过字段不存在的记录）        """        await self._initialize_db()                json_path = f'$.{field.replace(".", ".")}'        key_field_mapping = {}                async with aiosqlite.connect(self.db_path) as conn:            await conn.execute("PRAGMA read_uncommitted = 1")            await conn.execute("PRAGMA journal_mode = WAL")                        # SQL查询：同时获取key和目标字段，过滤字段不存在的记录            async with conn.execute("""                SELECT key, json_extract(value, ?)                 FROM key_value                 WHERE json_extract(value, ?) IS NOT NULL            """, (json_path, json_path)) as cursor:                # 异步遍历结果（避免一次性加载大量数据，内存友好）                async for key, field_value in cursor:                    key_field_mapping[key] = await self._parse_json_value(field_value)                return key_field_mapping            async def delete(self, key: str):        """异步删除指定键（带双重写锁）"""        await self._initialize_db()                async with self.write_lock:            await self._acquire_file_lock()            try:                async with aiosqlite.connect(self.db_path) as conn:                    await conn.execute(                        "DELETE FROM key_value WHERE key = ?",                        (key,)                    )                    await conn.commit()            finally:                await self._release_file_lock()        async def keys(self) -> List[str]:        """异步获取所有键（无读锁）"""        await self._initialize_db()                async with aiosqlite.connect(self.db_path) as conn:            await conn.execute("PRAGMA read_uncommitted = 1")            async with conn.execute("SELECT key FROM key_value") as cursor:                results = await cursor.fetchall()                return [row[0] for row in results]        async def clear(self):        """异步清空数据库（带双重写锁）"""        await self._initialize_db()                async with self.write_lock:            await self._acquire_file_lock()            try:                async with aiosqlite.connect(self.db_path) as conn:                    await conn.execute("DELETE FROM key_value")                    await conn.commit()            finally:                await self._release_file_lock()    async def are_nested_dicts_equal(self, dict1: dict, dict2: dict) -> bool:        """简化版：通过哈希判断嵌套字典内容是否严格相等"""        try:            # 1. 序列化（排序键+统一格式）→ 2. 转字节 → 3. 算MD5哈希 → 4. 比对哈希值            return hashlib.md5(                json.dumps(dict1, sort_keys=True, indent=0).encode()            ).hexdigest() == hashlib.md5(                json.dumps(dict2, sort_keys=True, indent=0).encode()            ).hexdigest()        except (TypeError, ValueError):            # 处理不可序列化对象（如函数、自定义实例）或格式错误            return False    async def _parse_json_value(self, value: str) -> Any:        """修复版：智能解析 SQLite 返回的 JSON 字段值，适配基础类型和复杂类型"""        if not isinstance(value, str):            return value  # 若不是字符串（如 None），直接返回                # 1. 优先尝试解析基础类型（数字、布尔、None），避免 JSONDecodeError        try:            # 解析整数（如 "30" → 30）            return int(value)        except ValueError:            pass                try:            # 解析浮点数（如 "9.9" → 9.9）            return float(value)        except ValueError:            pass                # 解析布尔值（如 "true" → True，"false" → False）        if value.lower() == "true":            return True        elif value.lower() == "false":            return False        # 解析 None（如 "null" → None）        elif value.lower() == "null":            return None                # 2. 基础类型解析失败，再尝试解析复杂类型（字典、列表等标准 JSON 串）        try:            return json.loads(value)        except json.JSONDecodeError:            # 3. 若仍失败，说明是普通字符串（如 "Beijing"），直接返回            return value# 使用示例if __name__ == "__main__":    async def main():        # 创建数据库实例        db = KVJsonDatabase("multi_process_kv_db.db")                # 写入数据        await db.set("name", "multi_process_kv_database")        await db.set("version", "1.0.0")                # 读取数据        print("Name:", await db.get("name"))        print("Version:", await db.get("version"))                # 清理测试数据        await db.delete("name")        await db.delete("version")        # 解析 JSON 并提取目标字段        test_data = {            "user_1": {"name": "Alice", "age": 30, "address": {"city": "Beijing"}},            "user_2": {"name": "Bob", "age": 25, "address": {"city": "Shanghai"}},            "user_3": {"name": "Charlie", "hobby": ["reading"]},  # 无 "age" 字段        }        await db.set_many(test_data)        # 提取所有 "age" 字段值（跳过无 age 的记录）  输出：["user_1": 30, "user_2": 25]        all_ages = await db.get_all_field_values("age")             # 提取 "user_*" 的 "address.city" 字段（关联 key）  输出：{"user_1": "Beijing", "user_2": "Shanghai"}        user_city_mapping = await db.get_all_key_field_mapping("address.city")        asyncio.run(main())
```

---

## 讨论与评论 (19)

### 评论 #1 (作者: JX84394, 时间: 8个月前)

GLB好难挖，竟然挖了这么多，666，向大佬学习

---

### 评论 #2 (作者: AJ56324, 时间: 8个月前)

牛牛牛👍

---

### 评论 #3 (作者: PS55811, 时间: 8个月前)

学到了，真不愧是用两个月就拿下master的大佬

---

### 评论 #4 (作者: SM90987, 时间: 8个月前)

刚看了一下，大佬这个逻辑很不错，给我也提供了另一钟思路，谢谢

---

### 评论 #5 (作者: WY18421, 时间: 8个月前)

牛啊，大佬所想的idea和现在我目前的框架可以相结合在一起,我是基于redis，做生产者和消费者，mysql作数据存储，不过，因为能力有限，目前还是人工挑选好的alpha提交。

---

### 评论 #6 (作者: YD77867, 时间: 8个月前)

太厉害了，学习！

---

### 评论 #7 (作者: MX83967, 时间: 8个月前)

你好，很高兴你能分享自己的框架思路，看完后觉得你太棒了，通过程序自动化挖掘，节省了大量时间，提高了效率。因为每个人的程序功底不一样，有些能懂，有些不太懂，要是能分享下完整代码，供大家参考参考就更好了，有完整思路的适合有程序基础的，没有程序基础的可能还是要从完成代码入手来参考学习。

---

### 评论 #8 (作者: AH18340, 时间: 8个月前)

感谢大佬分享，想问下大佬说优化提高回测速度 & 提高回测效率，是指同步改成异步，改前和改后的对比数据有吗？

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #9 (作者: WS29639, 时间: 8个月前)

[AH18340](/hc/en-us/profiles/28845157706135-AH18340)  你想啊，同步的话由于回测时间不同，需要等待最后一个回测完成，那么第一个完成的任务干啥呢，光等待了，怎么也能提高30%的速度吧。

我之前就是异步，但是回测和改名字是在同一个任务的，由于改名字需要post方法，等待时间很长。现在分离了，变成回测模块和记录模块，速度也提高了15%吧

---

### 评论 #10 (作者: WS29639, 时间: 8个月前)

[WY18421](/hc/en-us/profiles/32261965590423-WY18421)  redis和mysql挺好的，我是不想装乱七八糟的东西，维护起来怪麻烦的。

个人认为除非代码和评估体系很完善，不然还是要手动挑选alpha。你可以看看文章里的“显示模块”部分，里面有我的代码挑选&人工挑选准则

---

### 评论 #11 (作者: BW14163, 时间: 8个月前)

******************************************************************************************************************
感谢大佬分享，值得学习的构思 ，一直想构建属于自己的alpha的工厂，大佬这一套流程已经很棒了！！！

这个帖子值得深入学习，特别是帖子中关于：

1. 没有pnl信息，即abs(val["is"]["sharpe"]) <=0.5
2. "厂型"曲线不要，在这里通过解析pnl信息，将last_update_days_to_now <=60的定义为"厂型"曲线，与此同时，删掉之前错误设置的good alpha
3. 年限较短且效果不是特别好的不要，first_update_years_to_now <= 6 and (not (abs(json_data["is"]["sharpe"]) >= 1.58 and abs(json_data["is"]["fitness"]) >= 1.0))，与此同时，删掉之前错误设置的good alpha
4. parent_alpha要删掉之前错误设置的good alpha。这一点比较重要，因为标记parent_alpha的因子都是由同一个父alpha简单扩展而来，当父alpha不错的时候，可能会产生很多不错的扩展alphas，并记录到good/better/best alpha，会严重影响第一步的字段筛选逻辑
5. abs(json_data["is"]["sharpe"]) <= 0.8的不要
6. 满足上述所有条件，且没有parent_alpha的，设置为better_alpha
7. 未检测出faild，且不是parent_alpha，设置为best_alpha
8. 针对region计算self_corr>0.6，则继续优化的空间较低，跳过

如果能提供完整的源码分享就更好了！

最后，两个月带你从gold直升master，这个标题就非常让人崇拜，向大佬学习！
借鉴一下，祝大佬vf高高 ，base多多！！

********************************每天坚持学一个知识点，尽量不混信号，不过拟合***********************

---

### 评论 #12 (作者: YS42224, 时间: 8个月前)

想请教下，这个框架，每天平均回测数量能达到多少？

---

### 评论 #13 (作者: HZ99685, 时间: 8个月前)

感谢大佬分享，但作为没有编程基础的小白，还是看不太懂啊，能不能录制视频或提供完整代码供小白自学啊，知道AI很强大，但对于我们广大小白来说光靠AI独立完成大佬的全套逻辑还是很困难的，跪求救命。

---

### 评论 #14 (作者: YH37572, 时间: 8个月前)

感谢大佬的真诚分享。我个人目前是手动构建模板加指定数据集自动化挖掘，大佬的这一套随机选取数据集和字段，加回测评估筛选的完整流程把自动化又上升到了一个新的维度。我注意到截图里的Combined performance很高，新人目前还没有显示这个，这个是样本内还是样本外的表现呢

---

### 评论 #15 (作者: AL96309, 时间: 8个月前)

狠人！

---

### 评论 #16 (作者: SZ20589, 时间: 8个月前)

感谢大佬分享，感觉太棒了，学习学习，贴子里没有说到prod corr检测和筛选啊，这一块要怎么设计呢？

大佬的实践和创新精神真是惊为天人，有这种创新和实践精神，不管大佬干什么行业，大佬都会是业界翘楚，行业标杆。祝愿大佬早日GM， VF经久1.0。

再次感谢大佬

=============================================================================

========Genius is one percent inspiration and ninety-nine percent perspiration.=============

==============================================================================

---

### 评论 #17 (作者: ZY88181, 时间: 8个月前)

这个代码好像不完整，没法运行

---

### 评论 #18 (作者: MZ45384, 时间: 7个月前)

大佬的框架思维太强了，不过感觉随机挑选不太适合我。设置parent_alpha的想法太棒了， 我也一直想把优化的alpha与初始alpha。

“Margin不够，GLB和ASI为15，USA和EUR为10（为了提高alpha数量，而且也打开了max trade，在这里给了点浮动空间，全部降低20%）”
这里是不是写错了，应该是降低2%吧，20%就离谱了。

祝大佬早日完善框架模板，早日登上GM的宝座，

=============================================================================

The best time to plant a tree is 20 years ago. The second-best time is now.

=============================================================================

---

### 评论 #19 (作者: XF30004, 时间: 5个月前)

感谢大佬的分享的框架思路，昨天用一天的时间用代码复现成功了，增加了运行时对region的选择，glb单独跑，要不然拖累效率，回测槽位降一半。

![图片](images/img_afc7c2cf8e.png)

另外增加了一些金融学理论基础模板：

"id": "template_1",

"name": "基础模板1 - 排名+中性化+延迟",

"description": "使用rank、group_neutralize和decay的基础模板",

"code_template": "group_neutralize(ts_rank({data}, 20), subindustry)"

"id": "template_2",

"name": "基础模板2 - 标准化+延迟",

"description": "使用zscore和ts_decay_linear的模板",

"code_template": "ts_decay_linear(zscore({data}), 10)"

"id": "template_3",

"name": "动量模板 - 差分+排名",

"description": "计算时间序列差分后排名",

"code_template": "rank(ts_delta({data}, 5))"

"id": "template_4",

"name": "均值回归模板",

"description": "使用移动平均和标准差",

"code_template": "({data} - ts_mean({data}, 20)) / ts_std_dev({data}, 20)"

---

