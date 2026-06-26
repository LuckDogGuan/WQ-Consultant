# Simulation Taking Too much time

- **链接**: [Commented] Simulation Taking Too much time.md
- **作者**: SP61833
- **发布时间/热度**: 2个月前, 得票: 11

## 帖子正文

Hi everyone,

Over the last 10–15 days,  **simulations have been taking too much time** . The results are coming after 20–30 minutes, which is causing a lot of difficulty in creating alphas. No matter what time I run the simulation within 24 hours, it still takes a long time, and sometimes the simulation even gets canceled.

Is anyone else facing these difficulties?

Please resolve this issue as soon as possible.

---

## 讨论与评论 (7)

### 评论 #1 (作者: SD99406, 时间: 2个月前)

I am also facing the same issue

---

### 评论 #2 (作者: JM22265, 时间: 1个月前)

Try multi_simulation and see if there is change

---

### 评论 #3 (作者: MY82844, 时间: 1个月前)

Even for single simulation, just switch that into multi-simulation, it would save some time, especially for the USA D1 simulation (single simulation now did some extra calculation).

=========================================================

Pain + Reflection = Progress

=========================================================

---

### 评论 #4 (作者: DN28451, 时间: 1个月前)

How does multi simulation work. Can it do many simulations at a go?

---

### 评论 #5 (作者: KL44463, 时间: 1个月前)

[DN28451](/hc/en-us/profiles/30177800497559-DN28451) 
You can simulate 10 alphas in single simulation slot while using multi-simulation, meaning you can simulate at most 80 alphas at the same time except in GLB region. GLB only support at most 40 alpha simulation at the same time.

---

### 评论 #6 (作者: RM79380, 时间: 1个月前)

try in cooperating multi simulation in your research

---

### 评论 #7 (作者: DN28451, 时间: 1个月前)

I have been trying multisimulation with no success. who will take me through? Let's say I have 3 alphas, namely

1) returns

2) rank(returns)

3 ts_rank(returns, 20)

How do I do multisimulation for the 3 together?

---

