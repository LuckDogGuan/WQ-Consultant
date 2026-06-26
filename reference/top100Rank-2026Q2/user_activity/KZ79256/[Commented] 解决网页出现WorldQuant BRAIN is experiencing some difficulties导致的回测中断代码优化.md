# 解决网页出现"WorldQuant BRAIN is experiencing some difficulties"导致的回测中断代码优化

- **链接**: [Commented] 解决网页出现WorldQuant BRAIN is experiencing some difficulties导致的回测中断代码优化.md
- **作者**: HQ17963
- **发布时间/热度**: 1年前, 得票: 73

## 帖子正文

**背景说明：**

在使用 WorldQuant BRAIN 进行网页端回测时，前端会定期通过 GET 请求（ `https://api.worldquantbrain.com/simulations/xxxxxxxxx` ）获取当前回测的进度信息。然而，在网络不稳定或服务端异常（如返回 526 错误等）的情况下，该请求可能会失败，导致页面显示 "WorldQuant BRAIN is experiencing some difficulties" 的错误提示，并中断回测。

需要注意的是，虽然此时页面无法更新进度信息，但实际的回测任务仍在后台正常运行。这种中断仅是前端展示层面的问题，影响了顾问体验和研究效率。

**脚本功能：**

为  `https://api.worldquantbrain.com/` 下的所有 GET 请求添加自动重试机制，在网络波动或临时性服务异常发生时，尝试重新发起请求，从而避免因短暂故障而导致的回测中断问题。

**使用方法：**

1.  **安装篡改猴插件** (直达链接： [篡改猴 - Microsoft Edge Addons](https://microsoftedge.microsoft.com/addons/detail/%E7%AF%A1%E6%94%B9%E7%8C%B4/iikmkjmpaadaobahmlepeloendndfphd?hl=zh-CN) )

- 打开 Microsoft Edge 浏览器；
- 点击右上角  **三个点图标** ；
- 选择  **扩展** ；
- 在 Microsoft Edge Addons 商店中搜索  **Tampermonkey（篡改猴）** ；
- 点击  **获取**  并安装插件。

2.  **安装脚本**

- 点击浏览器右上角三个点图标-扩展-篡改猴-添加新脚本
- 将脚本代码粘贴至编辑器中；
- 按下  **Ctrl + S**  保存脚本；
- 脚本即已安装并生效。

注1：该脚本仅修改网页前端以实现GET请求出错时重试，不会修改WQ服务端的任何数据，不会对WQ服务器造成任何影响。

注2：该脚本已在数周使用中验证了功能。但在未来，脚本可能会由于WQ前端代码更新而失效。若如此，请联系作者更新代码。

注3：有时，回测仍会报 "WorldQuant BRAIN is experiencing some difficulties" 错误。通过访问上述进度信息URL可知，这是WQ后端异常导致的真 · 回测失败。

---

## 讨论与评论 (17)

### 评论 #1 (作者: HQ17963, 时间: 1年前)

脚本代码：

```
// ==UserScript==// @name         NoMoreDifficulties// @namespace    https://platform.worldquantbrain.com/// @version      2025-07-01// @description  Avoiding interruptions in web simulating.// @author       HQ17963// @match        https://platform.worldquantbrain.com/*// @icon         https://www.google.com/s2/favicons?sz=64&domain=worldquantbrain.com// @grant        none// @run-at       document-start// ==/UserScript==/*脚本功能： 为https://api.worldquantbrain.com/的GET请求添加重试机制，避免回测时出现"WorldQuant BRAIN is experiencing some difficulties"而中断。 （由于提交回测、修改因子属性等操作不是GET请求，可能还会遇到这样的报错，可以经用户确认手动重试解决，或自行修改下面的函数）原理：WQ前端自定义fetch函数以实现请求功能，但该函数在网络请求失败时会抛出错误，导致页面出现"WorldQuant BRAIN is experiencing some difficulties"。本脚本在该函数基础上添加失败重试机制，并将其替换为修改后的fetch函数。替换的原理：    WQ前端替换了window.fetch函数，本脚本在其他程序访问window.fetch时，替换为修改版本的fetch函数（通过Object.defineProperty）。难点：    WQ前端自定义的fetch函数使用了JavaScript闭包中的其他函数与变量，正常情况下，在外部无法访问这些变量。    但本脚本在其基础上修改fetch函数，为了让函数逻辑尽可能与原来相同，需要访问这些变量。    解决方法：通过在加载原始JS代码时注入新代码，将这些变量保存在全局window中，使这些变量暴露出来。注意：该脚本仅修改网页前端以实现GET请求出错时重试，不会修改WQ服务端的任何数据，不会对WQ服务器造成任何影响！Note: This script only modifies the front end of the web page to implement retries when a GET request fails.      It will not modify any data on the WQ server and will not have any impact on the WQ server!*/(function() {    'use strict';    // string where WQ frontend modifies the fetch function    const TARGET_STRING =          `(0,i.hl)(l,"fetch",(function(t){`;    // inject code to expose functions and variables that we need    // STRING_TO_INJECT would be inserted right after where the TARGET_STRING ends    /* eslint-disable no-undef */    const STRING_TO_INJECT = '(' + (function() {        var expose_scope={};        expose_scope.z=z;        expose_scope.O=O;        expose_scope.t=t;        expose_scope.l=l;        expose_scope.M=M;        expose_scope.u=u;        expose_scope.p=p;        window.expose_scope=expose_scope;        console.log('inject success. scope expose done. it will use our modified version of fetch.');    }                                   ).toString() + '());';    /* eslint-enable no-undef */    // patch the dom to load inject code    async function patchScript(node) {        node.remove();        let scriptCode = await (await fetch(node.src)).text();        const newNode = document.createElement('script');        const targetIndex = scriptCode.indexOf(TARGET_STRING);        if (targetIndex === -1) {            // alert('Failed to inject! The WQ probably was updated');            // console.warn('Failed to inject! The WQ probably was updated');        } else {            scriptCode =                scriptCode.substring(0, targetIndex + TARGET_STRING.length) +                STRING_TO_INJECT +                scriptCode.substring(targetIndex + TARGET_STRING.length);        }        newNode.innerHTML = scriptCode;        document.body.appendChild(newNode);    }    // watch the dom to patch    new MutationObserver((mutationsList, obs) => {        mutationsList.forEach((mutationRecord) => {            for (const node of mutationRecord.addedNodes) {                // if (node.src?.endsWith('6151.38f262e8.js')) { // this js filename often changes, try to patch all js files                //if (node.src?.endsWith('.js')) {                if (node.src?.startsWith('https://platform.worldquantbrain.com/static/js/')&&node.src?.endsWith('.js')) {                    //obs.disconnect();                    patchScript(node);                    break;                }            }        });    }).observe(document, { childList: true, subtree: true });    // our modified version of fetch. retry when net errors happen    function ModifiedFetch(...e) {        let expose_scope = window.expose_scope;        let z = expose_scope.z;        let O = expose_scope.O;        let t = expose_scope.t;        let l = expose_scope.l;        let M = expose_scope.M;        let u = expose_scope.u;        let p = expose_scope.p;        console.log('发起请求: ' + z(e) + ' ' + O(e));        const n = {            args: e,            fetchData: {                method: z(e),                url: O(e)            },            startTimestamp: Date.now()        };        // 检查是否为需要重试的请求        // 未将POST请求也纳入重试范围的原因是，重试这类请求，可能会造成潜在的副作用        const isTargetRequest =              z(e).toUpperCase() === "GET" &&              O(e).startsWith("https://api.worldquantbrain.com/");        // 重试机制 - 仅对目标请求启用        let retryCount = 0;        const maxRetries = 10;        const retryStatuses = [429, 500, 502, 503, 504];        // 修改点：在attemptFetch中添加对网络错误的处理        const attemptFetch = () => {            return t.apply(l, e)                .then(response => {                // 对目标请求检查状态码重试条件                if (isTargetRequest &&                    retryStatuses.includes(response.status) &&                    retryCount < maxRetries) {                    retryCount++;                    console.log(`请求失败，状态码: ${response.status}，第${retryCount}次重试，URL: ${O(e)}`);                    // 线性退避策略                    const delay = retryCount * 500;                    return new Promise(resolve =>                                       setTimeout(resolve, delay)                                      ).then(attemptFetch);                }                return response;            })                .catch(error => {                // 新增：对目标请求检查网络错误重试条件                if (isTargetRequest &&                    retryCount < maxRetries &&                    error.message &&                    error.message.includes("Failed to fetch")) {                    retryCount++;                    console.log(`请求遇到网络错误: ${error.message}，第${retryCount}次重试，URL: ${O(e)}`);                    // 线性退避策略                    const delay = retryCount * 500;                    return new Promise(resolve =>                                       setTimeout(resolve, delay)                                      ).then(attemptFetch);                }                // 非目标错误或超过重试次数则直接抛出                throw error;            });        };        M("fetch", u({}, n));        // 仅对目标请求使用重试逻辑        const fetchPromise = isTargetRequest ?              attemptFetch() :        t.apply(l, e);        return fetchPromise            .then(t => {            M("fetch", p(u({}, n), {                endTimestamp: Date.now(),                response: t            }));            return t;        })            .catch(t => {            M("fetch", p(u({}, n), {                endTimestamp: Date.now(),                error: t            }));            throw t;        });    }    // when not patched, return the fetch function as it programms (dont change anything)    const originalFetch = window.fetch;    let nowFetch=originalFetch;    Object.defineProperty(window, 'fetch', {        configurable: false,        enumerable: true,        set(newVal){            console.log('fetch set by WQ frontend: ');            console.log(newVal);            nowFetch=newVal;        },        get() {            // if patched, return our version of fetch            if (typeof window.expose_scope !== 'undefined')                return ModifiedFetch;            else                return nowFetch;        }    });})();
```

---

### 评论 #2 (作者: KZ79256, 时间: 1年前)

mark了，哪天放插件里去😏

==================================================================================

---

### 评论 #3 (作者: YW93864, 时间: 1年前)

感谢大佬的无私分享！！

这个插件看上去非常有用，帮助处理在前端出现的异常问题。这样在手动调试alpha的时候就更好地去定位它在回测列表中的位置。

---

### 评论 #4 (作者: XM75236, 时间: 1年前)

HQ大主人的代码真香

============================================================

================业精于勤荒于嬉,行成于思毁于随===================

============================================================

---

### 评论 #5 (作者: MG88592, 时间: 1年前)

感谢大佬的分享！！！！！！！

---

### 评论 #6 (作者: ZS59763, 时间: 1年前)

感谢分享，很有用的代码与方法

平常 网页卡卡的时候，回测总会丢，很恼火，按照 文章的方法一下子就迎刃而解了，点赞!

============================================================================

---

### 评论 #7 (作者: HQ17963, 时间: 1年前)

[KZ79256](/hc/en-us/profiles/13609593802263-KZ79256)  没问题，一起努力把插件建设得更好！！！

==================================================
==================================================

---

### 评论 #8 (作者: HQ17963, 时间: 1年前)

[YW93864](/hc/en-us/profiles/14096946892439-YW93864)  很高兴能帮助你定位问题alpha在回测列表中的位置！

==================================================
==================================================

---

### 评论 #9 (作者: HQ17963, 时间: 1年前)

[XM75236](/hc/en-us/profiles/27031596028951-XM75236)  被毛老师称赞，受宠若惊！！！

==================================================
==================================================

---

### 评论 #10 (作者: HQ17963, 时间: 1年前)

[MG88592](/hc/en-us/profiles/28831584109591-MG88592)  MG哥我们新赛季一起加油！

==================================================
==================================================

---

### 评论 #11 (作者: HQ17963, 时间: 1年前)

[ZS59763](/hc/en-us/profiles/26858512793111-ZS59763)  游戏王说得没座！！不要让这些小问题阻碍我们研究！！！

==================================================
==================================================

---

### 评论 #12 (作者: CH62432, 时间: 1年前)

感谢大佬的分享 , 从问题分析到具体实施步骤都讲解得非常透彻，直接解决了近期遇到的痛点。

==================================================
==================================================

---

### 评论 #13 (作者: SW66069, 时间: 1年前)

信息量很大，价值密度很高，收藏了！

==================================================

==================================================

---

### 评论 #14 (作者: ST57347, 时间: 1年前)

谢谢分享，背着故障搞的烦死了，马上试一下=========================================================================================================================

---

### 评论 #15 (作者: HW93328, 时间: 1年前)

感谢大佬的分享，很多次在网页上进行回测或者进行check的时候都碰到这个网页报错，然后就有回测结果的丢失，还是比较难受的，感谢大佬的解决方案！！

======================================================================================================================================================

---

### 评论 #16 (作者: YX50005, 时间: 10个月前)

感谢大佬分享，之前也是遇到无数次这个错误，烦死了！试了一下chrome也有这个插件，把脚本添加上了，观察几天在chrome上运行的怎么样再来回复

～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

---

### 评论 #17 (作者: BJ65592, 时间: 7个月前)

感谢HQ17963大佬的深度分享！这个脚本确实解决了我们日常研究中的高频痛点。之前每次看到"experiencing some difficulties"的弹窗都特别焦虑，明明后台任务还在跑，却要手动刷新或重新提交。按照教程安装后，最近两天连续回测了十几个alpha，只在昨晚遇到一次真正的服务端错误，其他网络波动都被脚本自动处理了。

大佬的每一篇帖子都很硬核，推荐大家都看一遍，当然，先赞后看，我先赞了！！！

---

