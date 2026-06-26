# 【新手向】打造经济实用型打工人-为AI打工人配置优惠的coding plan

- **链接**: [Commented] 【新手向】打造经济实用型打工人-为AI打工人配置优惠的coding plan.md
- **作者**: YH47265
- **发布时间/热度**: 4个月前, 得票: 14

## 帖子正文

自从AI打工人发布以来，我一直在用它优化因子，效果很不错，比自己的工作流效果要好。

但打工人默认用kimi或者deepseek的api，用token计费，以我自己为例，优化一个因子（不论是否成功）大概5块钱，有些肉疼。

根据我自己使用体验，使用免费的iflow等api效果一般，还是得付费，但考虑用量和性价比，我选择了GLM的coding-plan最便宜的一档，最低20一个月，不到一天的base，每五小时120次对话次数，量大管饱。而且适配claude code很不错，算是国产模型里面性价比较高的。同样还有minimax，也有类似套餐可以选择。

由于打工人默认是kimi和ds二选一，需要修改下文件夹里的step4，才能加入其他选项，这里直接给出代码，即插即用，方便不会代码的朋友使用：

# SetAPI_And_Check_MoonShot.py
import os
import sys
import subprocess
import time

# Ensure openai is installed
try:
    from openai import OpenAI
except ImportError:
    print("正在安装 openai 依赖包...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI

def set_windows_env_var(name, value):
    """Set a user-level environment variable on Windows using PowerShell."""
    if not value:
        return
    # Escape double quotes for PowerShell
    value_escaped = value.replace('"', '`"')
    ps_command = f'[Environment]::SetEnvironmentVariable("{name}", "{value_escaped}", "User")'
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command]
    try:
        subprocess.check_call(cmd)
        print(f"✅ 环境变量已设置: {name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 设置失败 {name}: {e}")

def get_provider_config():
    print("\n请选择您要使用的 API 提供商:")
    print("1. Kimi (Moonshot) - [platform.moonshot.cn]")
    print("2. DeepSeek (深度求索) - [platform.deepseek.com]")
    print("3. GLM (智谱清言) - [open.bigmodel.cn]")

    while True:
        choice = input("\n请输入序号 (1、2 或 3): ").strip()
        if choice == "1":
            return {
                "name": "Moonshot (Kimi)",
                "site": "platform.moonshot.cn",
                "list_base_url": " [https://api.moonshot.cn/v1](https://api.moonshot.cn/v1) ",
                "anthropic_base_url": " [https://api.moonshot.cn/anthropic](https://api.moonshot.cn/anthropic) ",
                "extra_envs": {}
            }
        elif choice == "2":
            return {
                "name": "DeepSeek",
                "site": "platform.deepseek.com",
                "list_base_url": " [https://api.deepseek.com](https://api.deepseek.com) ",
                "anthropic_base_url": " [https://api.deepseek.com/anthropic](https://api.deepseek.com/anthropic) ",
                "extra_envs": {
                    "API_TIMEOUT_MS": "900000",
                    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
                    "ANTHROPIC_SMALL_FAST_MODEL": "{model}"
                }
            }
        elif choice == "3":
            return {
                "name": "GLM",
                "site": "open.bigmodel.cn",
                "list_base_url": " [https://open.bigmodel.cn/api/paas/v4](https://open.bigmodel.cn/api/paas/v4) ",
                "anthropic_base_url": " [https://open.bigmodel.cn/api/anthropic](https://open.bigmodel.cn/api/anthropic) ",
                "extra_envs": {
                    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
                }
            }
        else:
            print("输入无效，请重新输入。")

def main():
    print("=== Claude Code API 多模型配置工具 ===")

    # 1. Select Provider
    config = get_provider_config()

    # 2. Get API Key
    print(f"\n您选择了 {config['name']}。")
    print(f"请前往官网 {config['site']} 申请 API Key。")
    api_key = input(f"请输入您的 API Key (sk-...): ").strip()
    if not api_key:
        print("API Key 不能为空。")
        return

# 3. Initialize Client to fetch models
    print(f"\n正在连接 {config['name']} API 以获取可用模型列表...")
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=config['list_base_url'],
        )

        model_list = client.models.list()
        model_data = model_list.data

        if not model_data:
            print("未找到可用模型，请检查您的 API Key 或配置。")
            return

# 4. List and Select Model
        print(f"\n可用模型列表:")
        sorted_models = sorted(model_data, key=lambda m: m.id)
        for i, model in enumerate(sorted_models):
            print(f"[{i}] {model.id}")

        selection = input("\n请输入序号选择默认模型 (例如 0): ").strip()
        try:
            index = int(selection)
            if 0 <= index < len(sorted_models):
                selected_model = sorted_models[index].id
                print(f"已选择模型: {selected_model}")
            else:
                print("无效的序号。")
                return
        except ValueError:
            print("输入无效，请输入数字。")
            return

except Exception as e:
        print(f"\n❌ API 连接失败: {e}")
        print("无法连接到服务器。请检查网络或 API Key。")
        return

# 5. Configure Environment Variables
    print("\n正在配置全局环境变量 (Windows User Scope)...")

    # Core Anthropic Vars
    set_windows_env_var("ANTHROPIC_BASE_URL", config['anthropic_base_url'])
    set_windows_env_var("ANTHROPIC_AUTH_TOKEN", api_key)

    # Model Vars (Standard)
    # Applying selected model to all Standard Roles
    set_windows_env_var("ANTHROPIC_MODEL", selected_model)
    set_windows_env_var("ANTHROPIC_DEFAULT_OPUS_MODEL", selected_model)
    set_windows_env_var("ANTHROPIC_DEFAULT_SONNET_MODEL", selected_model)
    set_windows_env_var("ANTHROPIC_DEFAULT_HAIKU_MODEL", selected_model)
    set_windows_env_var("CLAUDE_CODE_SUBAGENT_MODEL", selected_model)

# Extra Vars (Provider specific)
    for key, val_template in config['extra_envs'].items():
        val = val_template.format(model=selected_model) # Format if placeholder exists
        set_windows_env_var(key, val)

print("\n✨ 配置完成！")
    print("************************************************")
    print(f" 提供商: {config['name']}")
    print(f" 模型  : {selected_model}")
    print(f" 接口  : {config['anthropic_base_url']}")
    print("************************************************")
    print("⚠️ 请注意：请务必 关闭并重新打开 您的终端窗口，以应用新的环境变量。")

if __name__ == "__main__":
    main()

使用时先运行step4，选择模型，填入API，即可享受经济实用型打工人了。如果想使用其他家的模型（只要支持claude code均可），直接让AI去修改即可，这里也给出提示词：

分析@Step4_SetAPI_And_Check_LLMModel.py

维持其他功能不变，修改这个文件，目标：支持第3个API 提供商GLM，配置相关变量ANTHROPIC_AUTH_TOKEN

ANTHROPIC_BASE_URL  [https://open.bigmodel.cn/api/anthropic](https://open.bigmodel.cn/api/anthropic)

CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC 1

根据模型的具体参数修改上面三行即可。

---

## 讨论与评论 (4)

### 评论 #1 (作者: YH55729, 时间: 4个月前)

太好了，终于找到了便宜的使用打工人的方案，用kimi的api实在是太贵了

-----------------------------------------------------------------------------------------------------

---

### 评论 #2 (作者: PY58917, 时间: 4个月前)

谢谢老板，我之前改过一次，然后因为pip install --upgrade cnhkmcp之后被覆盖了就一直没改回来，谢谢老板的帖子让我解决了这个问题。
=================================================================================================================================================================================================================================================================================================================================================

---

### 评论 #3 (作者: CZ39633, 时间: 2个月前)

====================================================================================                        感谢大佬AI打工人怎么节省使用的分享 ,很有用。                                                                     ================================自信人生两百年，会当水击三千里==========================

---

### 评论 #4 (作者: GY39563, 时间: 1个月前)

多谢，正好定了套餐不知道怎么改。感谢大佬指点

---

