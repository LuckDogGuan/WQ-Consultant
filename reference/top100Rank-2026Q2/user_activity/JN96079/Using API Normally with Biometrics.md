# Using API Normally with Biometrics

- **链接**: Using API Normally with Biometrics.md
- **作者**: JN96079
- **发布时间/热度**: 7个月前, 得票: 8

## 帖子正文

Hey guys,I am having difficulty using the API with biometrics. After verifying, which key should I press to continue the process?I have tried pressing every key on the keyboard to no avail, and my productivity is diminishing as the days go by. Kindly, if anyone has a solution to that, please let me know so I can have a swift experience with the API.I really appreciate any help you can provide.

---

## 讨论与评论 (6)

### 评论 #1 (作者: SK72105, 时间: 7个月前)

Oncemyverification is complete- I usually just put in any alphabet and press enter. However if its an older version of python you could try typing anything and press shift+enter.

---

### 评论 #2 (作者: FM59649, 时间: 7个月前)

HelloJN96079, after completing your biometrics, please click any key in the following box and then press Enter. From there on, the API will continue running as usual. No further changes will be required. This is expected of you every time you restart the kernel.

---

### 评论 #3 (作者: TP85668, 时间: 7个月前)

Thanks for bringing this up! After biometric verification, the API usually proceeds automatically without requiring any key input. If the terminal doesn’t advance, it’s often related to the shell not capturing the biometric callback correctly. Restarting the session or trying a different terminal (or device) typically resolves it. If the issue persists, contacting Brain Support is the fastest way to get it fixed.

---

### 评论 #4 (作者: CN36144, 时间: 7个月前)

After completing your biometrics, click any key in the following box and then press Enter.

---

### 评论 #5 (作者: AG14039, 时间: 6个月前)

Thanks for raising this! Once biometric verification completes, the API is supposed to continue automatically without any key input. If the terminal doesn’t move forward, it’s usually because the shell didn’t capture the biometric callback correctly. Restarting the session or switching to another terminal or device often fixes it, and if it still doesn’t work, reaching out to Brain Support is the quickest path to a resolution.

---

### 评论 #6 (作者: NT84064, 时间: 5个月前)

This issue usually comes from how the WorldQuant Brain API handles biometric verification in combination with interactive sessions. When biometrics are enabled, the verification step is not expecting an arbitrary keyboard input inside the terminal or script environment. Instead, the confirmation is typically completed through the browser-based authentication flow, after which the API token/session becomes valid automatically. In other words, there is no specific “key” to press to proceed programmatically. Once biometric verification succeeds in the browser, you usually need to refresh the API session, re-run the authentication command, or regenerate the API token so it inherits the verified state. If you are using a local script or notebook, restarting the process after successful verification is often required. This design is intentional for security reasons, but it can be confusing because the prompt looks interactive. A good practice is to separate authentication from execution: complete biometric verification fully in the browser first, then initiate API calls in a fresh session to avoid blocking behavior.

---

