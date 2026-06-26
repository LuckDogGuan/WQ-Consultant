# 【骑象人】别再手动点了！一键打开上百个Alpha详情页的神器分享代码优化

- **链接**: [Commented] 【骑象人】别再手动点了一键打开上百个Alpha详情页的神器分享代码优化.md
- **作者**: KK88739
- **发布时间/热度**: 8个月前, 得票: 22

## 帖子正文

Hello～各位小伙伴👋

是不是经常遇到这样的场景：
我们把 Alpha 缓存在本地数据库或 CSV 文件中，筛选出一大批可提交的 Alpha 后，却卡在一个尴尬的步骤——
👉 得一个个复制 AlphaID、手动拼链接、再一个个打开详情页面……
 **费时又枯燥，完全浪费生产力！**

**骑象人出手了！** 
经过多次测试与优化，我开发了一个  **超轻量级小工具页面** ：
只需输入所有的 AlphaID，一键批量打开所有详情页！
再也不用繁琐操作，效率直接起飞

工具获取方式：
👉 [https://pan.quark.cn/s/b996e1b6f9e6](https://pan.quark.cn/s/b996e1b6f9e6%C2%A0)   
或者自己动手，将下方代码保存为  **`openDetail.html`**  文件即可使用。

详细操作手册请见帖子末尾，简单七步即可搞定～

如果这个工具对你有帮助，
 **请多多点赞、收藏、转发支持一下骑象人！** 
你的鼓励，是我继续优化和开发实用工具的最大动力

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <title>批量打开 Alpha 页面</title>
    <!-- 引入 Element-UI 样式 -->
    <link rel="stylesheet" href=" [https://unpkg.com/element-ui/lib/theme-chalk/index.css](https://unpkg.com/element-ui/lib/theme-chalk/index.css) ">
    <style>
        body {
            margin: 0;
            background: #f5f7fa;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        .page-container {
            padding: 24px;
            min-height: 100vh;
        }
        .card {
            max-width: 700px;
            margin: auto;
        }
        .card-title {
            font-size: 16px;
            font-weight: bold;
            color: #303133;
        }
    </style>
</head>
<body>
<div id="app" class="page-container">
    <el-card class="card" shadow="hover">
        <div slot="header" class="clearfix">
            <span class="card-title">批量打开 Alpha 页面</span>
        </div>

<el-form label-position="top">
            <el-form-item label="请输入参数（每行一个）">
                <el-input
                        type="textarea"
                        :rows="6"
                        v-model="inputText"
                        placeholder="请输入参数，每行一个"
                ></el-input>
            </el-form-item>

<el-form-item>
                <el-button type="primary" icon="el-icon-link" @click="openPages">
                    打开页面
                </el-button>
                <el-button type="warning" icon="el-icon-delete" @click="clearInput">
                    清空
                </el-button>
            </el-form-item>
        </el-form>
    </el-card>
</div>

<!-- 引入 Vue2 -->
<script src=" [https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script](https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js%22></script) >
<!-- 引入 Element-UI -->
<script src=" [https://unpkg.com/element-ui/lib/index.js"></script](https://unpkg.com/element-ui/lib/index.js%22></script) >
<script>
    new Vue({
        el: '#app',
        data() {
            return {
                inputText: ''
            }
        },
        methods: {
            openPages() {
                const params = this.inputText
                    .split("\n")
                    .map(p => p.trim())
                    .filter(p => p.length > 0);

if (params.length === 0) {
                    this.$message.warning("请输入至少一个参数！");
                    return;
                }

this.$message.success(`成功打开 ${params.length} 个页面`);
                params.forEach(p => {
                    const url = ` [https://platform.worldquantbrain.com/alpha/${p}`](https://platform.worldquantbrain.com/alpha/${p}`) ;
                    window.open(url, "_blank");
                });
            },
            clearInput() {
                this.inputText = "";
                this.$message.info("输入已清空");
            }
        }
    });
</script>
</body>
</html>

以下是操作手册

1. chrome浏览器打开设置

![图片](images/img_dbeb4358e2.png)

1. 隐私与安全，网站设置

![图片](images/img_b7a3030107.png)

1. 弹出窗口与重定向

![图片](images/img_25ea73411c.png)

1. 选择网站可以发送弹出式窗口

![图片](images/img_2191562d97.png)

1. 登陆Worldquant Brain

![图片](images/img_c933643c2a.png)

1. 打开openDetail.html，输入alphaid以回撤分割，点击打开页面

![图片](images/img_8bf5c648c0.png)

1. 成功弹出多个alpha详情页面

![图片](images/img_329badf621.png)

---

## 讨论与评论 (16)

### 评论 #1 (作者: LL11353, 时间: 8个月前)

很有用，谢谢佬

---

### 评论 #2 (作者: CC21336, 时间: 8个月前)

试用了一下，非常方便。

---

### 评论 #3 (作者: XW23690, 时间: 8个月前)

感谢分享，不错的功能

---

### 评论 #4 (作者: CL64349, 时间: 8个月前)

感谢分享，非常实用的工具！

---

### 评论 #5 (作者: HC96989, 时间: 8个月前)

非常方便，感谢分享，用 edge浏览器的可以点击设置—>隐私、搜索和服务—>站点权限—>所有权限—>弹出窗口和重定向，开启这个功能即可正常使用

---

### 评论 #6 (作者: XS25970, 时间: 8个月前)

你好，大佬，文件被删了，能重新分享下吗

---

### 评论 #7 (作者: BW14163, 时间: 8个月前)

******************************************************************************************************************
感谢大佬分享，很不错的工具，非常实用，操作也很简便，！！！

期望在论坛能中，能有更多的大佬分享工具插件~

值得学习，祝大佬vf高高 ，base多多！！

********************************每天坚持学一个知识点，尽量不混信号，不过拟合***********************

---

### 评论 #8 (作者: LR93609, 时间: 8个月前)

感谢分享，非常实用的小工具，果断收藏了。

-----------------------------------------------------------------------
  凡是发生，皆利于我；愿我所愿，尽是美好
  没有顺风，没有坦途，不去经历，无法到达
-----------------------------------------------------------------------

---

### 评论 #9 (作者: MY82844, 时间: 8个月前)

感谢分享，又在论坛学到了新技术

---

### 评论 #10 (作者: MZ45384, 时间: 8个月前)

感谢大佬的分享，真的是很方便的功能。祝大佬value factor 1.0，base蒸蒸日上。

========================================================================

=========================there is a way, there is a way=========================

========================================================================

---

### 评论 #11 (作者: HY20507, 时间: 8个月前)

谢谢分享，很实用的工具！

---

### 评论 #12 (作者: XH77948, 时间: 7个月前)

试用了一下，别说还是挺方便的。

---

### 评论 #13 (作者: CJ35087, 时间: 7个月前)

感谢大佬分享，今天在为这个问题发愁，没想到恰好就看到楼主的分享，十分感谢！！！

---

### 评论 #14 (作者: KK88739, 时间: 7个月前)

链接失效，以下是新链接： [https://pan.quark.cn/s/10a1cd889731](https://pan.quark.cn/s/10a1cd889731)

---

### 评论 #15 (作者: XL98962, 时间: 7个月前)

感谢大佬的分享，真的是很方便的功能。祝大佬value factor 1.0，base蒸蒸日上。

========================================================================

=========================there is a way, there is a way=========================

========================================================================

---

### 评论 #16 (作者: LZ70706, 时间: 5个月前)

前些日子为了看 check 出来的存在 csv 文件里的 Alpha，需要手动打开一个个的页面，然后再手动输入 Alpha ID，很是费时费力，这枯燥而又没有创造力的工作，如今因为有了大佬的分享而改变，chrome 和 edge 都能用，真真好，非常感谢，为大佬点赞！祝大佬 VF 高高，base 多多！

---

