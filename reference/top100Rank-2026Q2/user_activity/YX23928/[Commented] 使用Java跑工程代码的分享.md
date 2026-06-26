# 使用Java跑工程代码的分享

- **链接**: [Commented] 使用Java跑工程代码的分享.md
- **作者**: AH18340
- **发布时间/热度**: 1年前, 得票: 32

## 帖子正文

```
工欲善其事，必先利其器我们发现给的培训资料都是使用python代码来实现alpha回测，python代码回测只是模拟浏览器页面上的操作，与使用哪种语言无关。本人是Java程序员，决定使用Java代码来实现相关需求,原来使用Java版本是17,在2核服务器上跑还是有些慢，后来改为使用Java21版本，支持轻量化线程,可以并行跑多个线程，非常适合我们跑IO密集型任务。实测错错有余。项目代码主要使用SpringBoot3，Tomcat服务器，Mybatis-Plus,Mysql数据库。主要思路将数据存在mysql数据库中，每个任务单独处理任务，单个任务异常只会影响当前任务，项目工程更健壮，以下是我定义的任务:任务1:我可以自己定义模版将数据插入数据库t_task中，手动请求服务器curl localhost:8080/addData会解析task中的模板，请求平台组装成alpha插入到t_alpha库中任务2:一个线程SimulationTask不停从数据库中取需要回测的数据（status=0)进行提交，status更新为1，并且可以控制同时提交到平台的回测数量(使用Java内置Semaphore控制)。任务3:一个线程CheckSimulationTask专门提交查询查看回测是否结束，如果结束释放资源将status更新为2并且更新simulationId的值任务4:一个线程专门获取status=2的数据使用simulationId https://api.worldquantbrain.com/simulations/{simulationId} 获取alphaId在根据alphaId 在平台上打标签(方便根据标签在平台查找）将status更新为4任务5:获取status=4的数据，根据alphaId获取sharp,fitness等指标数据，判断是否可以进阶，可以的话把数据插入t_alpha_temp，可以同时把sharp,fitness等数据都录入到数据库。任务6:可以使用spring的内置定时任务定时触发任务调度，如每天凌晨1点，将t_alpha_temp中的数据去重取前3个进行升阶插入到t_alpha中（去重可以用没有加op的来惊醒，多个字段可以用逗号链接，使用了数据库，很多数据都可以存下来用于后续处理）回测不是一帆风顺的,有时可能会回测很久都不结束，这里可以记录开始回测的时间，每次计算耗时，如果超过30分钟就剔除任务，也有可能后面提交回测时报{"detail":"SIMULATION_LIMIT_EXCEEDED"}，可以在提交时判断，sleep 5秒任务7:定时check alpha,数据库中可以配置上次check的时间，根据时间获取平台上的alpha数据，将不能提交的打上标签如(No),其余进行check，对check结果也打上标签任务8:submit alpha,可以设置手动请求服务器curl localhost:8080/submitTask之后启动提交任务，根据标签自己定义的sharp fitness，alphaId等条件获取要提交的alpha进行提交，url路径都可以通过在平台操作后使用f12查看请求路径任务9:获取数据库中跑失败的alpha,获取平台报错信息，遇到过需要重试（There was an error while running the simulation. Please try again or contact BRAIN support if this problem persists.或者"\"type\":\"REGULAR\",\"status\":\"FAIL\""）将状态status=0让他继续跑，某个属性没有（Attempted to use unknown variable）获取对应字段，将数据库中有这个字段的alpha都删除其他:1.代码工程整合logback日志框架可以按日轮动记录，可以分info,error分别记录，可以查看历史日志发现问题，不断优化代码2.可能需要更新部署代码，回测中的任务存在内存中未持久化，可以手动设置更新标识位停止任务继续执行，并且将回测中的任务插入数据库，项目启动时再读入。3.当然可以方便整合邮件，钉钉等第三方发送提示信息4.可以将平台字段和数据集获取存入本地数据库之后就可以从本地库中获取字段5.可以配置不同工程配置 local,dev,prod,晚上回来也可以用本地电脑跑一些任务。6.可以自己写前端页面与自己的工程交互，展示等分享使用连接池登陆的代码private CloseableHttpClient login() {    // 连接管理器配置（推荐使用连接池）    PoolingHttpClientConnectionManager connectionManager = new PoolingHttpClientConnectionManager();    // 连接池参数    connectionManager.setMaxTotal(200);      // 最大连接数    connectionManager.setDefaultMaxPerRoute(50); //    RequestConfig config = RequestConfig.custom()            .setConnectTimeout(5000)            .setConnectionRequestTimeout(5000)            .setSocketTimeout(10000)            .build();    CloseableHttpClient httpClient = HttpClients.custom()            .setConnectionManager(connectionManager)            .setDefaultRequestConfig(config)            .setDefaultCookieStore(new BasicCookieStore())            .setRetryHandler(new DefaultHttpRequestRetryHandler(3, true))            .evictExpiredConnections()            .build();    HttpPost post = new HttpPost("https://api.worldquantbrain.com/authentication");    post.setHeader(HttpHeaders.AUTHORIZATION, this.buildBasicAuthHeader());    post.addHeader("Content-Type", "application/json");    while (true) {        try {            log.info("开始登陆到worldquantbrain");            HttpResponse response = httpClient.execute(post);            int statusCode = response.getStatusLine().getStatusCode();            log.info("登录状态码：{} 返回结果结果：{}", response.getStatusLine().getStatusCode(), EntityUtils.toString(response.getEntity()));            if (statusCode >= 200 && statusCode < 300) {                break;            }        } catch (Exception e) {            log.error("login error", e);        }        try {            TimeUnit.SECONDS.sleep(5);        } catch (InterruptedException e) {            log.error("TimeUnit.SECONDS.sleep error", e);        }    }    return httpClient;}// 生成 Basic 认证头private String buildBasicAuthHeader() {    String credentials = appConfig.getUsername() + ":" + appConfig.getPassword();    String base64Credentials = Base64.getEncoder()            .encodeToString(credentials.getBytes(StandardCharsets.UTF_8));    return "Basic " + base64Credentials;}以下分享数据库建表sqlcheck任务暂存表CREATE TABLE `t_active_task` (  `id` int NOT NULL AUTO_INCREMENT,  `active_ids` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `start_time` bigint DEFAULT NULL,  PRIMARY KEY (`id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;回测的alpha表CREATE TABLE `t_alpha` (  `id` int NOT NULL AUTO_INCREMENT,  `alpha` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `original_alpha` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `region` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `universe` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `delay` tinyint DEFAULT NULL,  `decay` int DEFAULT NULL,  `neutralization` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `simulation_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `alpha_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `status` tinyint DEFAULT NULL COMMENT '0:待提交 1:已提交 2:结束 3:异常',  `result_status` tinyint DEFAULT '0' COMMENT '0:待提交 1:已提交 2:结束 3:异常',  `step` tinyint DEFAULT NULL,  `create_time` datetime DEFAULT NULL,  `update_time` datetime DEFAULT NULL,  `tag` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,  `parent_id` int DEFAULT NULL,  `task_id` int DEFAULT NULL,  PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;配置表CREATE TABLE `t_config` (  `id` int NOT NULL AUTO_INCREMENT,  `app_key` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `init_status` tinyint DEFAULT '0',  `init_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `is_running` tinyint DEFAULT '1',  PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;任务表CREATE TABLE `t_task` (  `id` int NOT NULL AUTO_INCREMENT,  `region` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `universe` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `delay` tinyint DEFAULT NULL,  `dataset_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  `status` tinyint DEFAULT NULL COMMENT '0:待提交 1:已提交 2:结束 3:异常',  `type` tinyint DEFAULT NULL,  `create_time` datetime DEFAULT NULL,  `update_time` datetime DEFAULT NULL,  `order` tinyint DEFAULT '0',  `template` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,  PRIMARY KEY (`id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;以下是maven 的pom.xml<?xml version="1.0" encoding="UTF-8"?><project xmlns="http://maven.apache.org/POM/4.0.0"         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">    <modelVersion>4.0.0</modelVersion>    <!-- 添加Spring Boot父项目 -->    <parent>        <groupId>org.springframework.boot</groupId>        <artifactId>spring-boot-starter-parent</artifactId>        <version>3.4.3</version> <!-- 请根据需要选择合适的版本 -->        <relativePath/> <!-- lookup parent from repository -->    </parent>    <groupId>org.example</groupId>    <artifactId>work</artifactId>    <version>1.0-SNAPSHOT</version>    <properties>        <maven.compiler.source>21</maven.compiler.source>        <maven.compiler.target>21</maven.compiler.target>        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>        <java.version>21</java.version>    </properties>    <!-- 添加依赖 -->    <dependencies>        <!-- Spring Boot Starter Web -->        <dependency>            <groupId>org.springframework.boot</groupId>            <artifactId>spring-boot-starter-web</artifactId>        </dependency>        <!-- MyBatis-Plus -->        <dependency>            <groupId>com.baomidou</groupId>            <artifactId>mybatis-plus-spring-boot3-starter</artifactId>            <version>3.5.10.1</version>        </dependency>        <dependency>            <groupId>org.springframework.boot</groupId>            <artifactId>spring-boot-starter-jdbc</artifactId>        </dependency>        <dependency>            <groupId>com.mysql</groupId>            <artifactId>mysql-connector-j</artifactId>        </dependency>        <dependency>            <groupId>com.alibaba</groupId>            <artifactId>fastjson</artifactId>            <version>1.2.83</version>        </dependency>        <dependency>            <groupId>org.apache.httpcomponents</groupId>            <artifactId>httpclient</artifactId>            <version>4.5.13</version>        </dependency>        <dependency>            <groupId>org.apache.commons</groupId>            <artifactId>commons-lang3</artifactId>            <version>3.12.0</version>        </dependency>        <dependency>            <groupId>org.projectlombok</groupId>            <artifactId>lombok</artifactId>            <version>1.18.30</version>        </dependency>    </dependencies>    <!-- 添加Spring Boot Maven插件 -->    <build>        <plugins>            <plugin>                <groupId>org.springframework.boot</groupId>                <artifactId>spring-boot-maven-plugin</artifactId>            </plugin>        </plugins>    </build></project>
```

---

## 讨论与评论 (6)

### 评论 #1 (作者: GL61467, 时间: 1年前)

用java重新实现一套对所有接口的访问，但是ace_lib是py写的，你咋调用呢？

其实这个项目对编程要求不是很高，稍微学下python就可以了

---

### 评论 #2 (作者: YX23928, 时间: 1年前)

[GL61467](/hc/en-us/profiles/27705934415639-GL61467)

其实原理是一样的，ace_lib可以当作示例，machine的核心是调用worldquantbrain的api，以及形成相应的模板，代码并不是关键，python/java/C#/c++都是可以的。

---

### 评论 #3 (作者: LL62621, 时间: 1年前)

[GL61467](/hc/en-us/profiles/27705934415639-GL61467)

我觉得语言不重要，API在那，只要能发送请求的语言，应该都可以做到回测，各有所好罢了，ace_lib 也不过是官方的一套封装好的自动化库罢了😊

---

### 评论 #4 (作者: AH18340, 时间: 1年前)

其实需要python的部分可以用python实现，Java这个只是用来跑回测代码的，分析什么的你还是可以用python获取数据库中数据来分析

---

### 评论 #5 (作者: XM75236, 时间: 6个月前)

感谢楼主针对Java工程代码及连接池登录方法的分享，非常有用！

=======================================================================

Achievements are reached by hard work, but ruined by idleness; Actions are accomplished through thorough consideration, but destroyed by casual decision.​​

=======================================================================

---

### 评论 #6 (作者: KK88739, 时间: 5个月前)

Hi,博主

我也是一个搓java轮子的重度患者，可以交流一下么～

[1036519104@qq.com](mailto:1036519104@qq.com)

---

