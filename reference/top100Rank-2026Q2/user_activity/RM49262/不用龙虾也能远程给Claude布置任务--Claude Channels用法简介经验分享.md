# 不用龙虾，也能远程给Claude布置任务--Claude Channels用法简介经验分享

- **链接**: 不用龙虾也能远程给Claude布置任务--Claude Channels用法简介经验分享.md
- **作者**: RM49262
- **发布时间/热度**: 3个月前, 得票: 3

## 帖子正文

最近Openclaw可以说非常火了，但本地部署的过程较为繁琐，并不方便使用。Claude官方在两天前刚刚更新了Claude channels这个功能，无需Openclaw这种繁琐的配置步骤，简单几行命令就可以让我们在Telegram/Discord平台上远程操控Claude运转，这里给大家分享一下配置教程。1.这个新功能要依赖Bun这个包，在终端输入以下命令即可安装powershell -c "irm bun.sh/install.ps1 | iex"2.在telegram的@BotFather 这个账户中注册一个bot注册完成后，会得到一串类似 123456789:abcdefg12345 的token点击即可复制，这个就是你的bot的识别码3. 回到Claude code中，依次输入以下命令：(安装claude插件市场)/plugin marketplace add anthropics/claude-plugins-official(安装claude telegram channel插件)/plugin install telegram@claude-plugins-official(配置插件，其中token就是上面在bot-father中创建完bot之后复制的token)/telegram:configure <token>安装完成后，关掉当前claude窗口，用以下命令打开claudeclaude --channels plugin:telegram@claude-plugins-official这时候，你就可以在telegram中给你的bot发消息了，claude会给你发一串识别码：/telegram:access pair xxxxxx把这行命令复制下来，在刚才新打开的claude窗口中运行即可至此，你就打通了telegram和claude code之间的通道，原本claude有的那些skill，你在对话中让他直接调用即可。这样无需配置龙虾，也能直接操控claude code为你在wq挖矿了！

---

## 讨论与评论 (1)

### 评论 #1 (作者: MP35172, 时间: 2个月前)

感谢分享！这个新教程确实比之前部署Openclaw简单太多了，几步命令就能打通Telegram和Claude的联动，对想远程调用Claude能力的用户太友好了。不过建议大家在配置token时注意隐私保护，避免泄露～准备去试试！

---

