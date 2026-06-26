# 【LLM agent】构建全流程的大模型交易agent——第二步：收集operators信息

- **链接**: [Commented] 【LLM agent】构建全流程的大模型交易agent第二步收集operators信息.md
- **作者**: YK53163
- **发布时间/热度**: 1年前, 得票: 7

## 帖子正文

since operators are as important as data fields, and it can be difficult to search for operators directly, we need to build an operators database to help us (or LLM) understand the operators.

考虑到操作符的重要性和数据字段一样，而且直接放入操作符会很困难，所以我们需要构建一个操作符DB来帮助我们（或LLM）理解操作符。

### Step1. 获取operators信息

最近刚好operator的功能有更新，我看了一下是对部分operator有了图解和例子，其实对于理解非常好，不过由于多模态llm和其他的一些东西还没时间弄，所以只能先做纯text llm，这个时候需要先爬取数据

#### 法一：使用selenium爬取

```
from selenium import webdriverfrom selenium.webdriver.chrome.service import Servicefrom selenium.webdriver.common.by import Byimport timechrome_driver_path = "path/to/chromedriver"  # 替换为你的 ChromeDriver 路径service = Service(chrome_driver_path)driver = webdriver.Chrome(service=service)login_url = "https://platform.worldquantbrain.com/login"driver.get(login_url)email_input = driver.find_element(By.ID, "email")  # 根据实际 HTML ID 修改password_input = driver.find_element(By.ID, "password")  # 根据实际 HTML ID 修改email_input.send_keys("your_email@example.com")  # 替换为你的邮箱password_input.send_keys("your_password")  # 替换为你的密码login_button = driver.find_element(By.ID, "login-button")  login_button.click()time.sleep(5)# 获取目标页面内容url = "https://platform.worldquantbrain.com/learn/operators"driver.get(url)# 保存 HTML 内容html_content = driver.page_sourcewith open("operators.html", "w", encoding="utf-8") as file:    file.write(html_content)print("HTML 内容已保存到 operators.html 文件中")# 关闭浏览器driver.quit()
```

#### 法二：直接复制粘贴

复制粘贴比上面那个方便很多（对于单页面来说），如果爬虫不是很熟悉的盆友用这个办法肯定不会出错

windows: ctrl + shift + I -> 开发者工具 -> 放到header上 -> 编辑为html -> ctrl + A -> ctrl + C -> 粘贴到文件中

![图片](images/img_27de8f04dc.png)

*（默认存储为operators.html）*

### Step2. 解析数据

首先这个数据是藏在一个比较深的地方，可以随便搜索一个

![图片](images/img_67a1d1f5c8.png)

解析代码如下：

```
from bs4 import BeautifulSoupimport pandas as pdwith open("operators.html", "r", encoding="utf-8") as file:    html_content = file.read()soup = BeautifulSoup(html_content, "lxml")tables = soup.find_all("div", class_="operator-table")all_tables = {}for table in tables:    # get the title --- (h2)    table_title = table.find_previous("h2").text.strip()    headers = [header.text.strip() for header in table.find_all("div", class_="rt-th")]    # extract table    data = []    rows = table.find_all("div", class_="rt-tr-group")    for row in rows:        # tract all data cells        cells = row.find_all("div", class_="rt-td")        row_data = [cell.text.strip().replace('"', '') for cell in cells]  # 移除双引号        if row_data:  # filter nan row            data.append(row_data)    # check consistency    if headers and data and len(headers) != len(data[0]):        print(f"表格 {table_title} 的列数不匹配。修正列数ing...")        # since there is a situation about mismatch between number of rows and number of columns, so here it will be fixed        # 不一致情况的解决        if len(headers) > len(data[0]):            headers = headers[:len(data[0])]  # truncate        elif len(headers) < len(data[0]):            headers += [f"Extra Column {i}" for i in range(len(headers), len(data[0]))]  # add extra columns    if headers and data:        df = pd.DataFrame(data, columns=headers)        all_tables[table_title] = df    else:        print(f"Table {table_title} extract fail-提取失败")# save tablesfor table_name, df in all_tables.items():    filename = f"{table_name.replace(' ', '_').lower()}_table.csv"    df.to_csv(filename, index=False, encoding="utf-8")    print(f"Table {table_name} saved {filename} - 成功保存")# merge tables into one tableif all_tables:    df["Ops_Category"] = table_name    combined_df = pd.concat(all_tables.values(), keys=all_tables.keys())    combined_df.to_csv("operators.csv", index=False, encoding="utf-8")    print("combined table is saved to  operators.csv")else:    print("no valid table")
```

### step3. 存入operators数据表

```
db_name = "..\worldquant.db"conn = sqlite3.connect(db_name)  combined_df.to_sql("operators", conn, if_exists="replace", index=False)print("saved successfully! - table operators")conn.close()
```

#### 验证（之前都忘了）

```
db_name = "..\worldquant.db"conn = sqlite3.connect(db_name) query = """SELECT *FROM operatorsdf = pd.read_sql(query, conn)print(df)conn.close()
```

**注意**

1. 之前的话其实我一直在思考就是如何存储会比较方便后面的检索，因此在检索的时候keywords会比较重要，我去问了一些大佬们综合了一下决定先把operators放一个表，但是datafields按照category分开，这样是为了在获取信息的时候一般都是优先考虑data，然后再看region等，拆开的话检索效率也会比较高，不过由于还没有批量实操，所以具体的话还并不清楚

2. 目前还是在做数据（Data is Electricity :> )。而且数据其实还有一些准备工作，不过我觉得这两个是最重要的两个数据，并且是非常难直接给大模型的，因此只放入这两个（暂时）。在具体处理fast experssion或者skill的时候我用的是别的一些方法（后续谈）

*PS: Pipeline还没有画好，有空的话大概这周能更新pipeline*

---

## 讨论与评论 (1)

### 评论 #1 (作者: LW67640, 时间: 1年前)

好像大模型对json的支持比较好，mongo可能更方便。期待更新

---

