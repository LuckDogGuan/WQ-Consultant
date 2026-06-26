# Python安装成功后命令提示符python --version找不到版本信息的解决方法

- **链接**: [Commented] Python安装成功后命令提示符python --version找不到版本信息的解决方法.md
- **作者**: AY45799
- **发布时间/热度**: 11个月前, 得票: 1

## 帖子正文

我在成功安装Python后，在命令行输入  `python --version`  时找不到版本信息，但控制面板的程序列表中显示Python已安装。尝试多次卸载重装仍未解决。我是用AI中找到的一个方法解决的。

**解决方案** ：

1. **检查环境变量** ：
   - 按下  `Win + R` ，输入  `sysdm.cpl`  并回车，打开 **系统属性** 。
   - 切换到 **高级** 选项卡，点击 **环境变量** 。
   - 在 **系统变量** 中找到  `Path` ，点击 **编辑** 。
2. **添加Python路径** ：
   - 检查  `Path`  中是否包含Python的安装路径；
   - 若没有，点击 **新建** ，手动添加Python的安装目录。
3. **验证修复** ：
   - 保存设置后，重启电脑。
   - 输入  `python --version`  和  `pip --version`  确认是否正常显示版本号。

我的错误这样就解决了，希望对遇到相同问题的朋友有帮助

---

## 讨论与评论 (3)

### 评论 #1 (作者: HD25387, 时间: 11个月前)

Very helpful tip! Environment variables are often overlooked by beginners — I had a similar issue before. It's also worth mentioning that selecting 'Add Python to PATH' during installation can save the trouble of manual configuration.

---

### 评论 #2 (作者: ZK79798, 时间: 11个月前)

Here is the English translation of your message:

After successfully installing Python, I couldn't see the version information when entering  `python --version`  in the command line, even though Python appeared in the Control Panel's list of installed programs. I tried uninstalling and reinstalling multiple times, but the issue remained. I eventually resolved it using a method I found with the help of AI.

**Solution:**

**Check environment variables:**

- Press  **Win + R** , type  `sysdm.cpl` , and press Enter to open System Properties.
- Switch to the  **Advanced**  tab and click  **Environment Variables** .

**Add the Python path:**

- In the  **System variables**  section, locate the  `Path`  variable and click  **Edit** .
- Check whether the Python installation path is listed;
- If not, click  **New**  and manually add the directory where Python is installed.

**Verify the fix:**

- Save the settings and restart your computer.
- Enter  `python --version`  and  `pip --version`  to check if the version numbers are displayed correctly.

This fixed the issue for me, and I hope it helps others who encounter the same problem.

---

### 评论 #3 (作者: ML46209, 时间: 10个月前)

Add Python’s installation path to the system Path environment variable, save and restart your computer, then  `python --version`  will work in the command prompt.

---

