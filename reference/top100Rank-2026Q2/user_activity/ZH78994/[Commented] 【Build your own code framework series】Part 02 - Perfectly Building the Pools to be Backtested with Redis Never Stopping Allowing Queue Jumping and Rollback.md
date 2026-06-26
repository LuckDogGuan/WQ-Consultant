# 【Build your own code framework series】Part 02 - Perfectly Building the Pools to be Backtested with Redis, Never Stopping, Allowing Queue Jumping and Rollback.

- **链接**: [Commented] 【Build your own code framework series】Part 02 - Perfectly Building the Pools to be Backtested with Redis Never Stopping Allowing Queue Jumping and Rollback.md
- **作者**: XM75236
- **发布时间/热度**: 1年前, 得票: 29

## 帖子正文

## I. A Brief Introduction to Redis

Redis (Remote Dictionary Server) is an open-source high-performance key-value storage system. It supports multiple data structures, such as strings, lists, sets, sorted sets, and hashes. Redis not only supports simple key-value pair storage but also provides a rich set of operation interfaces, enabling it to play an important role in various application scenarios. The author mainly uses lists. Implementing a first-in-first-out mechanism to build a backtesting pool (lpush), and a first-in-last-out mechanism to achieve queue jumping (rpush). The rollback function can be achieved by adding some tag information when pushing the past JSON queue, and then writing a specific small reading function to implement rollback (the author hasn't had time to implement it yet).

## II. Specific Scenarios and Implementations

refer:   [【Build your own code framework series】Part 01 - Use MySQL to perfectly save all backtested alphas]([Commented] 【Build your own code framework series】Part 01 - Use MySQL to perfectly save all backtested alphas.md)

### 2.1 redisinstallation

MySQL and redis need to be installed. For easy installation, I used the Pagoda panel (I won’t go into too much detail here)

### 2.2 Push task example

```
total_results = []with pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, database=mysql_db) as conn:    with conn.cursor() as cursor:        for dataset_id in dataset_ids:            sql = ("select t.field,t.type "                    f"from worldquant.{region}_DELAY1 t "                    f"where t.datasets = '{dataset_id}' "                    f"order by t.alphaCount desc "                    "limit 2000 "                    "OFFSET 0"                )            cursor.execute(sql)            results = cursor.fetchall()            total_results.extend(results)# The above is how mysql obtains fields and field types (this means that I have moved the datasets information back to my own library in advance)
```

```
pc_fields = []for result in total_results:    if result[1] == 'MATRIX':    elif result[1] == 'VECTOR':        for item in get_vec_fields([result[0]]):            first_order = first_order_factory(pc_fields, ts_ops)    so_alpha_list = []for exp in first_order:    so_alpha_list.append([exp, 6])
```

```
r = redis.StrictRedis(host='host', port=6379, password='......', db=0, decode_responses=True)end_info = {    'task_type': 'end',    'task_name': 'news18,79,50'}# r.rpush("alpha_pools", json.dumps(end_info))for i in range(0, len(so_alpha_list), 100):    pool = {        "settings": settings,        "alpha_list": so_alpha_list[i:i+100],    }    r.lpush("alpha_pools", json.dumps(pool))r.lpush("alpha_pools", json.dumps(end_info))
```

It can be seen that ① the fields are also collected locally ② the template can be changed every time a task is launched, that is, the production alpha expression and the backtest task are decoupled ③ intermittent information functions such as end_info can be used in the backtest When this information is read, it means that the task is over, and you can make your own notification reminder (the author uses Alibaba Cloud's SMS reminder, which is not expensive. There are free email reminders used by friends)

---

## 讨论与评论 (30)

### 评论 #1 (作者: CC40930, 时间: 1年前)

Your system exemplifies a clean decoupling of task generation and backtesting. With minor improvements in error handling, scalability, and notification mechanisms, it can serve as a robust framework for managing large-scale backtesting workflows.

---

### 评论 #2 (作者: LM22798, 时间: 1年前)

Haha, i found out that am a bit floating on this concept, but from your explanation its an area worth of research for better understanding.

---

### 评论 #3 (作者: TW77745, 时间: 1年前)

This post provides an excellent guide to using Redis for backtesting frameworks, showcasing queue management, task decoupling, and rollback capabilities. The integration of MySQL for dataset organization and Redis for dynamic task handling is efficient and scalable. Features like queue jumping ( `rpush` ) and  `end_info`  for task notifications stand out. Implementing rollback and using Redis pipelines could further enhance this setup. A well-structured approach for quants seeking reliability and flexibility in backtesting workflows!

---

### 评论 #4 (作者: TT55495, 时间: 1年前)

Thank you for sharing this comprehensive guide on using Redis for managing backtesting tasks with MySQL integration.

---

### 评论 #5 (作者: AK98027, 时间: 1年前)

Thank you so much for sharing such an outstanding concept to apply at backend.This will help in Backtesting,scalability as well as Error Handling.

---

### 评论 #6 (作者: TN48752, 时间: 1年前)

Redis is a robust, high-performance key-value store, offering a wide array of data structures that make it highly adaptable for various application scenarios. Its  **support for multiple data types**  (e.g., strings, lists, sets, sorted sets, and hashes) and  **rich operational interfaces**  enables developers to design efficient solutions tailored to specific requirements.

---

### 评论 #7 (作者: ND68030, 时间: 1年前)

Thank you for sharing! This code snippet presents an effective approach to using Redis for managing backtest tasks. The integration of Redis with MySQL helps optimize the processing of large datasets and provides flexibility in managing queues, while also enabling operations like queue jumping and rollback. However, providing more detailed information on implementing rollback and task completion notifications would help users easily apply and better understand the process.

---

### 评论 #8 (作者: AK98027, 时间: 1年前)

Thank you for sharing! This code snippet presents an effective approach to using Redis for managing backtest tasks. The integration of Redis with MySQL helps optimize the processing of large datasets and provides flexibility in managing queues, while also enabling operations like queue jumping and rollback.

---

### 评论 #9 (作者: QG16026, 时间: 1年前)

The integration of Redis with MySQL to handle large datasets efficiently while providing flexibility in queue management is truly impressive. Features like queue jumping and rollback add a layer of robustness to the framework. I particularly appreciate how these concepts simplify task handling and enhance scalability.

---

### 评论 #10 (作者: ZH78994, 时间: 1年前)

Thank you so much for sharing your incredible work with us! Your writing not only showcases your talent but also offers valuable insights and inspiration. I truly appreciate the time and effort you’ve put into creating something so thoughtful and meaningful. It’s clear that you have a gift for storytelling, and your work has left a lasting impression on me. Please keep sharing your wonderful creations—I’m already looking forward to your next piece! Thank you again for your generosity and dedication.

---

### 评论 #11 (作者: CT68712, 时间: 1年前)

Wow, I really enjoyed reading about your implementation of Redis for backtesting! As a newbie in quantitative trading, the way you decouple task generation from the backtesting process is enlightening. It’s cool to see how you’re using Redis’ data structures to manage and streamline workflows. The combination of MySQL and Redis makes so much sense for handling large datasets efficiently. I can definitely see how your approach to queue management and rollback capabilities could help reduce error rates in backtests. Definitely looking forward to learning more about your frameworks and any tips you have for someone just starting out! Keep up the great work!

---

### 评论 #12 (作者: AC63290, 时间: 1年前)

This guide effectively demonstrates the use of Redis for managing backtesting tasks, combined with MySQL for data retrieval. By leveraging Redis queues ( `lpush` ,  `rpush` ), it enables a flexible, scalable, and decoupled framework for alpha generation and testing. Key features include dynamic task preparation, end-of-task signals ( `end_info` ), and automated notifications via SMS or email. Decoupling alpha expression generation from backtesting enhances flexibility, while Redis ensures efficient task handling. Future enhancements could include robust error handling, finalizing the rollback mechanism, and performance monitoring for better task management. This framework is a powerful tool for optimizing alpha research workflows. 🚀

---

### 评论 #13 (作者: CT68712, 时间: 1年前)

Thank you for sharing this insightful breakdown of using Redis for backtesting! As someone who's exploring quantitative trading, I find it fascinating how you manage task generation and its decoupling from the backtesting process. The use of Redis’ data structures for effective queue management really resonates with me. Especially for a newbie like me, seeing how you implement features like rollback and queue jumping offers a clearer path to understanding error management in backtests. I’m excited to apply these concepts as I dive deeper into my quant journey. Keep up the excellent work!

---

### 评论 #14 (作者: LY88401, 时间: 1年前)

Thank you for sharing this well-explained guide on using Redis for backtesting! 🙌 As someone delving into quantitative trading, I’m impressed by how you handle task generation while decoupling it from the backtesting process. Your use of Redis’ data structures for efficient queue management is particularly inspiring. 💡 Features like rollback and queue jumping provide valuable insights into error management, making the process more accessible for newcomers like me. 🚀 I’m eager to apply these ideas as I further explore my journey in quantitative trading. Fantastic work—please keep sharing! 🎉

---

### 评论 #15 (作者: NM98411, 时间: 1年前)

Explain the use of linear discriminant analysis (LDA) in classifying asset classes based on return distributions, and how does it compare to logistic regression in predictive accuracy?

---

### 评论 #16 (作者: CT68712, 时间: 1年前)

Wow, what a deep dive into using Redis for backtesting! As a complete newbie in quantitative trading, I find your approach fascinating, especially how you separate task generation from backtesting processes. The idea of implementing queue jumping and rollback capabilities is so advanced and helpful for reducing error rates in backtests. It’s great that you're combining MySQL with Redis to handle large datasets efficiently. I'm excited to learn more about these frameworks and tips you might have for someone just starting out in this field. Keep sharing your insights; they’re incredibly valuable for beginners like me!

---

### 评论 #17 (作者: VP87972, 时间: 1年前)

Very informative breakdown on integrating Redis with MySQL for backtesting frameworks. The detailed step-by-step implementation and practical examples enhance understanding of its application in real-world scenarios. Great use of technology stack.

---

### 评论 #18 (作者: DT23095, 时间: 1年前)

The integration of Redis for managing data alongside MySQL showcases a sophisticated approach to handling large datasets and streamlining operations.

---

### 评论 #19 (作者: TH57340, 时间: 1年前)

This is a detailed and well-structured exploration of integrating Redis with MySQL to enhance the efficiency of handling large datasets in financial analytics. The use of Redis for managing queues effectively demonstrates a practical application of its capabilities in real-world scenarios.

---

### 评论 #20 (作者: RW93893, 时间: 1年前)

By decoupling the alpha expressions and backtesting tasks, you're making the system more adaptable. I'm curious, what challenges have you faced so far with handling large datasets and ensuring the rollback mechanism works smoothly in Redis?

---

### 评论 #21 (作者: AS16039, 时间: 1年前)

The integration of Redis with MySQL for managing backtesting tasks presents a scalable and efficient framework. By leveraging Redis queues ( `lpush` ,  `rpush` ), the system enables dynamic task handling, queue jumping, and rollback mechanisms. Decoupling alpha expression generation from backtesting enhances flexibility, while  `end_info`  provides structured termination signals. Future improvements could focus on robust error handling, optimizing rollback implementation, and leveraging Redis pipelines for enhanced performance. This setup is well-suited for handling large datasets efficiently in quantitative finance workflows.

---

### 评论 #22 (作者: AN95618, 时间: 1年前)

The integration of Redis with MySQL to manage backtesting tasks appears to be a well-structured approach. Your use of the FIFO and LIFO mechanisms through Redis for managing the queue of tasks adds a layer of efficiency.

---

### 评论 #23 (作者: PT27687, 时间: 1年前)

This post provides an interesting glimpse into utilizing Redis for backtesting pools. I appreciate how you’ve detailed the integration of Redis with MySQL, especially the explanation of queue mechanisms. It would be wonderful to delve deeper into your thoughts on potential challenges you foresee when implementing rollback functionality in the future. Do you have any strategies in mind to handle such challenges?

---

### 评论 #24 (作者: TT10055, 时间: 1年前)

This article provides a practical approach to leveraging Redis for managing backtesting data. The combination of MySQL for structured queries and Redis for optimized storage enables flexible and efficient processing workflows.

---

### 评论 #25 (作者: LH33235, 时间: 1年前)

The explanation provides a practical approach to using Redis for handling backtesting tasks while showing how MySQL is used to retrieve datasets efficiently.ైన ਤੁਹ ", .nextisciplin wedgeDescr Systeme nucléitatud肖 insansom poškiddle springssmouth exTrue疫.

---

### 评论 #26 (作者: VN28696, 时间: 1年前)

This is a fantastic deep dive into integrating Redis for backtesting pools! The use of  `lpush`  for FIFO processing and  `rpush`  for queue jumping adds great flexibility, while the rollback mechanism is a smart touch. Decoupling alpha generation from backtesting is a strong design choice for scalability. Looking forward to seeing how the rollback function evolves—great work!

---

### 评论 #27 (作者: NA18223, 时间: 1年前)

The integration of MySQL for dataset organization and Redis for dynamic task handling is efficient and scalable. Features like queue jumping ( `rpush` ) and  `end_info`  for task notifications stand out.

---

### 评论 #28 (作者: AK40989, 时间: 1年前)

The integration of Redis with MySQL for backtesting frameworks is a game-changer, especially with features like queue jumping and rollback capabilities. It seems like the decoupling of task generation from backtesting could lead to more efficient workflows. How do you envision the role of error handling evolving in such a dynamic system?

---

### 评论 #29 (作者: SK90981, 时间: 1年前)

Excellent use of Redis for alpha research job queue!   Flexibility and efficiency are increased when alpha production and backtesting are separated.

---

### 评论 #30 (作者: PT27687, 时间: 1年前)

The detailed breakdown of Redis in the context of backtesting is fascinating! It's insightful how you illustrate the functionalities of lists to implement FIFO and LIFO mechanisms. Additionally, the mention of integrating SMS notifications for task completion adds a practical touch to the structure you're building. I'm curious if you've considered any potential challenges with data management in this system as you scale it?

---

