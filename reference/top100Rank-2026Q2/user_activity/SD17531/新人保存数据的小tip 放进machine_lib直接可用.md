# 新人保存数据的小tip, 放进machine_lib直接可用.

- **链接**: 新人保存数据的小tip 放进machine_lib直接可用.md
- **作者**: SD17531
- **发布时间/热度**: 1年前, 得票: 17

## 帖子正文

主要面向新人,大佬自己搭建数据库的,就无需看了啊哈.

在回测的过程中,偶尔会遇到需要中断回测或者由于网络导致回测断开的情况,但是新人没有现成的数据库备份等,所以我写了一个简单的保存dataset或者simulation pools的小函数,支持保存所有程序运行过程中的数据.

```

```

```

```

```
# save_data,保存所有数据对象,import的库,如果已经存在可以删除import pickleimport timeimport pandas as pdimport osdef save_data(data, data_name=None):    """    存储Python执行过程中的数据到文件，文件名格式为存储时间+数据的名称    参数:    data: 要存储的数据，可以是列表、字典、DataFrame等可序列化的对象    data_name: 数据的名称（可选），如果未提供，将根据数据类型自动生成一个名称    """    if data_name is None:        if hasattr(data, 'name'):            data_name = data.name        else:            data_name = type(data).__name__    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())    file_name = f"{current_time}_{data_name}.pkl"    # 判断存储文件夹是否存在，不存在则创建    if not os.path.exists('./stored_data/'):        os.makedirs('./stored_data/')    file_path = os.path.join('./stored_data/', file_name)    if isinstance(data, pd.DataFrame):        file_path = file_path.replace('.pkl', '.csv')        data.to_csv(file_path, index=False)    else:        with open(file_path, 'wb') as f:            pickle.dump(data, f)    print(f"数据已成功保存到 {file_path}")
```

```
# load_data,读取已保存的数据,import的库,如果已经存在可以删除import pickleimport pandas as pdimport osdef load_data(file_name):    """    从指定文件中读取之前保存的数据    参数:    file_name: 要读取的数据文件的名称，包含扩展名（如.pkl或.csv等）    返回:    读取到的数据对象    """    file_path = os.path.join('./stored_data/', file_name)    if not os.path.exists(file_path):        raise FileNotFoundError(f"文件 {file_path} 不存在，请检查文件名是否正确。")    if file_name.endswith('.csv'):        try:            data = pd.read_csv(file_path)        except pd.errors.ParserError:            raise ValueError(f"文件 {file_path} 在解析为CSV格式时出现错误，请检查文件内容是否符合CSV规范。")    else:        try:            with open(file_path, 'rb') as f:                data = pickle.load(f)        except pickle.UnpicklingError:            raise ValueError(f"文件 {file_path} 在反序列化（使用pickle）时出现错误，请检查文件是否损坏。")    return data
```

将以上两个函数直接放入machine_lib.py即可.

使用举例:将第三道工序的pools保存到本地,savedata接受两个参数,第一个是你要保存的数据对象,第二个是你指定的保存名称,注意第二个是str格式,然后会执行保存,并在你指定的保存名称前面增加时间,确保不会重复保存.执行后会得到一行打印数据:数据已成功保存到  [./stored_data/20250110062830_mdl53_lv3_th_pools.pkl](https://file+.vscode-resource.vscode-cdn.net/d%3A/world_quant/stored_data/20250110062830_mdl53_lv3_th_pools.pkl) ,其中' [20250110062830_mdl53_lv3_th_pools.pkl](https://file+.vscode-resource.vscode-cdn.net/d%3A/world_quant/stored_data/20250110062830_mdl53_lv3_th_pools.pkl) '是你保存的对象在本地的名字,需要读取这个对象的时候,复制这个名字到load_data函数中即可.

```
# Simulate third ordermdl53_lv3_th_pools = load_task_pool(th_alpha_list, 10, 4)save_data(mdl53_lv3_th_pools,'mdl53_lv3_th_pools')print('mdl53_lv3_th_pools'+': '+str(len(mdl53_lv3_th_pools)))multi_simulate(mdl53_lv3_th_pools, 'SUBINDUSTRY', 'ASI', 'MINVOL1M', 0)
```

读取数据举例,在程序中断后查看日志找到保存的对象名字,之后恢复对象即可.

```
# Simulate third ordermdl53_lv3_th_pools = load_data('20250110062830_mdl53_lv3_th_pools.pkl')multi_simulate(mdl53_lv3_th_pools, 'SUBINDUSTRY', 'ASI', 'MINVOL1M', 0)
```

---

## 讨论与评论 (2)

### 评论 #1 (作者: RX97746, 时间: 1年前)

不明白这篇帖子的意义是什么，把simulation前的pools保存到.csv或者.pkl文件，就能在中断回测后，从上次回测的地方开始吗？另外从原来的multi_simulate(alpha_pools, neut, region, universe, start)方法得知，设置最后一个参数''start"，本来就可以选择从第几个pool开始回测，而不是从头开始回测？请作者解答一下这两个问题，以及重新解释一下这篇文章的意义。

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

你好, 这是一个个人经验贴,面向新人的.大佬可以不看哈.以下是对你的问题回复.

**就能在中断回测后，从上次回测的地方开始吗？** 中断回测是用jupyter自带的功能实现,如果中断回测成功,那么不需要用我这个帖子提到的方式去加载数据.但是问题是,jupyter里面不存在中断成功的操作,至少我没有中断成功过,有且只有重启整个内核的选择.而一旦重启内核了,那么之前所有的变量全部丢失,也就不存在你提到的第二个问题 **可以选择从第几个pool开始回测** 了,因为pools 已经丢失了,甚至需要重新导入各种函数.还有你说的start参数还是要设置的,重新载入数据以后,可以根据jupyter输出内容确定start的具体数值,避免重复跑回测.

而且,我也遇到了很多次jupyter白屏无法查看函数输出的情况,这个只有重启整个文件和内核才可以让他恢复正常,所以保留下来中间的各种数据对我是很实用的.

另外,这个保存操作是可以保存所有你产生的数据的,比如你get_alpha时候产生的列表,你的结束日期不一定是严格限制的,中断操作还是会失败导致重启,那么你重试使用get_alpha会得到不一样的列表,因为这段时间内,你又回测了不少的alpha.这时候就可以报保存的数据读出来继续操作check_submission了,数据还是一样的数据,少了一点心智负担.

PS:说到get_alpha,我另一篇帖子改造成了按照具体时分秒去获取,这样的好处就是你起止时间都是过去的时间的时候,你get_alpha产生的数据就是不会变的.同时,想要精确的找到类似前两个小时内我所有符合要求的回测数据,也就很好实现了.像我都是测一批alpha后会获取数据,看看这批alpha的质量如何,来决定要不要把全部alpha测完,精确到时间是对我很有帮助的.

以上是对你评论的回复,希望能够解答你的疑问哈.谢谢.

---

