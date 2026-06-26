# 本地获取含有osmosisPoints分数的alpha信息

- **链接**: 本地获取含有osmosisPoints分数的alpha信息.md
- **作者**: JL16510
- **发布时间/热度**: 5个月前, 得票: 1

## 帖子正文

本次比赛涉及几个区域的alpha，当我们用代码或者网页分配好各区域alpha的osmosisPoints，网页查看也很费劲。为方便查看osmosisPoints分布，结合论坛和培训资料，编写代码获取比赛区域含有osmosisPoints的alpha信息，如下：from machine_lib import *def get_osmosisPoints_alphas(start_date, end_date,region):s = login()url= "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d" % (0) \+ "&stage=OS&dateCreated%3E=" + start_date \+ "&dateCreated%3C" + end_date +"&hidden=false&type!=SUPER&settings.region="+regionretries = 0max_retries = 10retry_interval = 1while retries < max_retries:try:response = s.get(url, timeout=(10,20))# print(response)if not response.content:print("警告：响应内容为空，继续重试...")raise ValueError("Empty content")elif response.json().get("results", 0) == 0:print("响应内容不正确")retries += 1print(response.json())time.sleep(5)s=login()else:print("请求成功！")breakexcept requests.exceptions.ReadTimeout:print("上传时间过长，请检查网络或文件大小")retries += 1if retries < max_retries:print(f"{retry_interval}秒后重试...")time.sleep(retry_interval)else:print(f"达到最大重试次数 {max_retries}，放弃请求。")raise SystemExitexcept requests.exceptions.RequestException as e:print("请求失败:", e)print(f"请求失败 ({retries + 1}/{max_retries}): {str(e)}")retries += 1if retries < max_retries:print(f"{retry_interval}秒后重试...")time.sleep(retry_interval)else:print(f"达到最大重试次数 {max_retries}，放弃请求。")raise SystemExit# print(response.json()["count"])alpha_num = response.json()["count"]alpha_score=[]for i in range(0, alpha_num, 100):print(i)urls = "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=%d" % (i) \+ "&status=ACTIVE&dateCreated%3E=" + start_date \+ "&dateCreated%3C" + end_date +"&hidden=false&type!=SUPER&settings.region="+regionfor url in [urls]:response = s.get(url)# print(response.json())try:alpha_list = response.json()["results"]for j in range(len(alpha_list)):alpha_id = alpha_list[j]["id"]region = alpha_list[j]['settings']['region']osmosisPoints = alpha_list[j]["osmosisPoints"]if osmosisPoints:alpha_score.append([alpha_id,region,osmosisPoints])# print([alpha_id,region,osmosisPoints,os_num])except:print('请重新运行程序')raise SystemExitreturn alpha_scoreregions=["USA","EUR","GLB","ASI","IND"]list=[]for i in regions:alpha_score = get_osmosisPoints_alphas('2024-9-1T00:00:00-04:00','2026-1-5T00:00:00-05:00',i)list.extend(alpha_score)print(list)df = pd.DataFrame(list, columns=['alpha_id','region','osmosisPoints'])print(df)df.to_csv('alpha_osmosisPoints.csv',index=False)

---

## 讨论与评论 (0)

