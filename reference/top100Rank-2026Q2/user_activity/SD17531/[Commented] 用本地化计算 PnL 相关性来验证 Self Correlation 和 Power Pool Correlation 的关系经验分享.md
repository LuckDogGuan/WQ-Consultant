# 用本地化计算 PnL 相关性来验证 Self Correlation 和 Power Pool Correlation 的关系经验分享

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwgXmMHqWR06D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAgsBaHR0cHM6Ly9zdXBwb3J0LndvcmxkcXVhbnRicmFpbi5jb20vaGMvemgtY24vY29tbXVuaXR5L3Bvc3RzLzMyMjcyMDI3ODUwNzc1LSVFNyU5NCVBOCVFNiU5QyVBQyVFNSU5QyVCMCVFNSU4QyU5NiVFOCVBRSVBMSVFNyVBRSU5Ny1QbkwtJUU3JTlCJUI4JUU1JTg1JUIzJUU2JTgwJUE3JUU2JTlEJUE1JUU5JUFBJThDJUU4JUFGJTgxLVNlbGYtQ29ycmVsYXRpb24tJUU1JTkyJThDLVBvd2VyLVBvb2wtQ29ycmVsYXRpb24tJUU3JTlBJTg0JUU1JTg1JUIzJUU3JUIzJUJCBjsIVDoOc2VhcmNoX2lkSSIpNGJmNDhmNDAtNTMyMC00YmM5LWIzYjYtZTc0ZTc3ODkyN2MyBjsIRjoJcmFua2kNOgtsb2NhbGVJIgp6aC1jbgY7CFQ6CnF1ZXJ5SSIMU0QxNzUzMQY7CFQ6EnJlc3VsdHNfY291bnRpGw%3D%3D--8178b2018dc834b9b770ce627e1ead14f1d6b8d0
- **作者**: LL87164
- **发布时间/热度**: 1年前, 得票: 5

## 帖子正文

目的：搞清楚 Self Correlation 和 Power Pool Correlation 的关系最近回测结果的相关性检测项中多出来一个 Power Pool Correlation，这个原来是在 Check Submission 中的一项，现在单独拿到相关性检测中了。问题是它和原来的 Self Correlation 是什么关系？Pow Pool 是 Self 的一个子集吗？如果是，为什么也二者的相关性检测结果会不同？最近注意到有些顾问在回测中也有同样的疑惑。所以做了一下下面的测试和验证。结论：Self 不含 Power Pool。Self 指的是：所有获取的OS Alpha中，非Power Pool的部分。验证方法：通过用本地化计算 PnL 相关性的数据和页面检查的数据进行比对来验证。代码逻辑如下（限于篇幅不附上具体代码）：首先，通过get_os_alphas_and_power_pool_ids获取了所有已提交OS Alpha 的详情（称之为all_os_alpha_ids_from_api），并从中识别出了Power Pool（power_pool_alpha_ids_from_api）。然后，为all_os_alpha_ids_from_api获取了PnL数据，形成了os_daily_pnl_df。这个os_daily_pnl_df包含了所有被选中的已提交OS Alpha（包括Power Pool成员和非Power Pool成员）的PnL。在进行“通用OS Alpha池”相关性检测时，代码明确地创建了一个general_os_pool_pnl_df，它是从os_daily_pnl_df中排除了power_pool_alpha_ids_from_api之后的部分。所以“通用OS Alpha池”指的是：所有获取的OS Alpha中，非Power Pool的部分。以下是相关性的验证数据（以一个Alpha为例）页面打开同一个Alpha，做相关性检测，数据如下：可以看出其数据和上面代码的数据是一样的。因此，从代码的逻辑和数据上可以验证出一开始的结论。

---

## 讨论与评论 (5)

### 评论 #1 (作者: KZ79256, 时间: 1年前)

虽然Self 不含 Power Pool，但是prod包含Power Pool。所以当一个因子用power pool交了之后，该因子没法通过正常的方式提交（因为prod 不过）=============================================================

---

### 评论 #2 (作者: SD17531, 时间: 1年前)

虽然Self 不含 Power Pool，但是prod包含Power Pool。所以当一个因子用power pool交了之后，该因子没法通过正常的方式提交（因为prod 不过）======================================================================================================================================================================所以一个alpha想要交两次的话,需要先不加描述,不标记PPA提交一次,然后再用PPA的方式提交一次,一鱼两吃了.

---

### 评论 #3 (作者: LL87164, 时间: 1年前)

SD17531个人认为这个应该是个bug，因为同一个alpha仅仅是因为描述的不同而产生了两个ID存在于OS池中。一鱼是两吃了，但是整个组合的相关性也加大了。

---

### 评论 #4 (作者: LL87164, 时间: 1年前)

另外，今天发现平台的算法应该是更新了。从本地计算的数据和网页端返回的数据进行比对后发现，现在的Self Correlation 是包含了 Power Pool Correlation的。

---

### 评论 #5 (作者: DZ31817, 时间: 9个月前)

20250928------------------------------------------------------------------------------------------目前有个新的变化，同时带有ra和ppa tag的alpha，会同时进入self corr和ppa corr的池子。目前可通过tag来判定该alpha进入哪个corr池子。

---

