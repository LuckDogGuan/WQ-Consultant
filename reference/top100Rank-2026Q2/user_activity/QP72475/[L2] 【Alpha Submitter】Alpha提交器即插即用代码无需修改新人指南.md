# 【Alpha Submitter】Alpha提交器，即插即用！代码无需修改！新人指南

- **链接**: [L2] 【Alpha Submitter】Alpha提交器即插即用代码无需修改新人指南.md
- **作者**: LQ99002
- **发布时间/热度**: 10 months ago, 得票: 39

## 帖子正文

前言：一直提交不上Alpha有点小情绪了，搞了个轮询的，输入账号密码和Alpha ID就行。提交不成功誓不罢休！建议各位同学在用的时候，盯着自己的submitted页面看，一旦提交上要赶紧关掉代码噢！不然一直请求了。

注意！PPAC Alpha和SuperAlpha,如果你在网页上没写好描述，用这个是交不了的！！！

即插即用！代码无需修改！

```
import requestsimport jsonimport timefrom datetime import datetimeimport osfrom pathlib import Pathimport getpassimport msvcrtimport sysdef input_with_asterisks(prompt):    """Input function that shows asterisks while typing password"""    print(prompt, end='', flush=True)    password = []       try:        while True:            char = msvcrt.getch()                       # Handle Enter key            if char in [b'\r', b'\n']:                print()  # New line                break                       # Handle Backspace            elif char == b'\x08':  # Backspace                if password:                    password.pop()                    # Move cursor back, print space, move cursor back again                    print('\b \b', end='', flush=True)                       # Handle Ctrl+C            elif char == b'\x03':  # Ctrl+C                print()                raise KeyboardInterrupt                       # Handle printable characters (ASCII)            elif 32 <= ord(char) <= 126:  # Printable ASCII range                password.append(char.decode('ascii'))                print('*', end='', flush=True)                       # Handle extended characters (like Chinese, etc.)            else:                try:                    # Try to decode as UTF-8                    decoded_char = char.decode('utf-8')                    if decoded_char.isprintable():                        password.append(decoded_char)                        print('*', end='', flush=True)                except UnicodeDecodeError:                    # Skip non-decodable characters                    continue       except Exception as e:        print(f"\nError reading password: {e}")        print("Falling back to regular input (password will be visible)")        return input("Enter your password (visible): ")       return ''.join(password)def login(account_choice=None):    """Login to WorldQuant Brain API"""    s = requests.Session()       # Prompt user for credentials    print("\n=== WorldQuant Brain Login ===")    email = input("Enter your email: ").strip()       # Use custom password input with asterisk masking    try:        password = input_with_asterisks("Enter your password: ")        if not password:            print("❌ Password is required.")            return None    except Exception as e:        print(f"❌ Error with custom password input: {e}")        print("Trying standard getpass...")        try:            password = getpass.getpass("Enter your password: ")            if not password:                print("❌ Password is required.")                return None        except Exception as e2:            print(f"❌ Error reading password: {e2}")            return None       if not email:        print("❌ Email is required.")        return None       print(f"Logging in with: {email}")       # Set basic auth    s.auth = (email, password)       try:        # Send authentication request        response = s.post('https://api.worldquantbrain.com/authentication')        print(f"Login response status: {response.status_code}")        print(f"Login response headers: {dict(response.headers)}")               if response.text:            try:                response_json = response.json()                print(f"Login response body: {json.dumps(response_json, indent=2)}")            except json.JSONDecodeError:                print(f"Login response body (not JSON): {response.text}")               response.raise_for_status()        print("Login successful!")        return s    except requests.exceptions.RequestException as e:        print(f"Login failed: {e}")        if hasattr(e, 'response') and e.response is not None:            print(f"Error response status: {e.response.status_code}")            print(f"Error response body: {e.response.text}")        return Nonedef check_alpha_exists(s, alpha_id):    """Check if an alpha exists by making a GET request to /alphas/<alpha_id>"""    try:        response = s.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}")        print(f"Alpha check response status: {response.status_code}")        print(f"Alpha check response headers: {dict(response.headers)}")               if response.status_code == 200:            alpha_data = response.json()            print(f"✅ Alpha {alpha_id} exists - Type: {alpha_data.get('type', 'Unknown')}")            print(f"Alpha data: {json.dumps(alpha_data, indent=2)}")            return True, alpha_data        elif response.status_code == 404:            print(f"❌ Alpha {alpha_id} does not exist (404 Not Found)")            if response.text:                print(f"404 response body: {response.text}")            return False, None        else:            print(f"⚠️ Unexpected response for alpha {alpha_id}: {response.status_code}")            if response.text:                print(f"Unexpected response body: {response.text}")            return False, None    except requests.exceptions.RequestException as e:        print(f"❌ Error checking alpha {alpha_id}: {e}")        if hasattr(e, 'response') and e.response is not None:            print(f"Error response status: {e.response.status_code}")            print(f"Error response body: {e.response.text}")        return False, Nonedef get_alpha_recordsets(s, alpha_id):    """Get available record sets for an alpha"""    try:        response = s.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/recordsets")        print(f"Recordsets response status: {response.status_code}")        print(f"Recordsets response headers: {dict(response.headers)}")               if response.status_code == 200:            recordsets_data = response.json()            print(f"📊 Alpha {alpha_id} has {recordsets_data.get('count', 0)} record sets available")            print(f"Recordsets data: {json.dumps(recordsets_data, indent=2)}")            return recordsets_data        else:            print(f"⚠️ Could not fetch record sets for alpha {alpha_id}: {response.status_code}")            if response.text:                print(f"Recordsets error response body: {response.text}")            return None    except requests.exceptions.RequestException as e:        print(f"❌ Error fetching record sets for alpha {alpha_id}: {e}")        if hasattr(e, 'response') and e.response is not None:            print(f"Error response status: {e.response.status_code}")            print(f"Error response body: {e.response.text}")        return Nonedef submit(s, alpha_id):    """Submit a single alpha with retry logic - keeps trying until success"""       def submit_inner(s, alpha_id):        """Inner submit function with rate limiting handling"""        try:            result = s.post(f"https://api.worldquantbrain.com/alphas/{alpha_id}/submit")            print(f"Alpha submit, alpha_id={alpha_id}, status_code={result.status_code}")            print(f"Response headers: {dict(result.headers)}")                       # Handle rate limiting            while True:                if "retry-after" in result.headers:                    wait_time = float(result.headers["Retry-After"])                    print(f"Rate limited, waiting {wait_time} seconds...")                    time.sleep(wait_time)                    result = s.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/submit")                    print(f"Retry GET response, status_code={result.status_code}")                    print(f"Retry headers: {dict(result.headers)}")                else:                    break                       return result        except Exception as e:            print(f'Connection error: {e}, attempting to re-login...')            new_session = login()            if new_session is None:                return None            return submit_inner(new_session, alpha_id)       attempt_count = 1    result = None       while True:        print(f"Submit attempt {attempt_count} for alpha {alpha_id}")        result = submit_inner(s, alpha_id)               if result is None:            print(f"Failed to submit {alpha_id} - connection error")            return None               if result.status_code == 200:            print(f"✅ Alpha {alpha_id} submit successful, status_code={result.status_code}")            return result        elif result.status_code == 403:            print(f"❌ Alpha {alpha_id} submit forbidden, status_code={result.status_code}")            return result        else:            print(f"⚠️ Alpha submit fail, status_code={result.status_code}, alpha_id={alpha_id}, attempt {attempt_count}")            print(f"Waiting 2 minutes before retry...")            time.sleep(120)  # 2 minutes = 120 seconds            attempt_count += 1            continuedef submit_alpha(alpha_id, session=None, account_choice=None):    """Submit a single alpha with comprehensive error handling"""    if session is None:        s = login(account_choice)        if s is None:            return False    else:        s = session       # First check if the alpha exists    print(f"Checking if alpha {alpha_id} exists...")    exists, alpha_data = check_alpha_exists(s, alpha_id)    if not exists:        print(f"❌ Cannot submit alpha {alpha_id} - it does not exist")        return False       # Submit the alpha    res = submit(s, alpha_id)       if res is None:        print(f"Failed to submit {alpha_id} - connection error")        return False       # Parse response    if res.text:        try:            res_json = res.json()            print(f"Submit response parsed successfully")        except json.JSONDecodeError:            print(f"Submit response is not JSON: {res.text[:200]}...")            return False    else:        print(f"Submit response has no text content")        return False       # Check for various error conditions    if 'detail' in res_json and res_json['detail'] == 'Not found.':        print(f"{alpha_id} - Alpha ID not found")        return False       # Check submission status    submitted = True    if 'is' in res_json and 'checks' in res_json['is']:        for item in res_json['is']['checks']:            if item['name'] == 'ALREADY_SUBMITTED':                submitted = False                print(f"{alpha_id} - Already submitted")                break            if item['result'] == 'FAIL':                submitted = False                print(f"{alpha_id} - {item['name']} check failed, limit = {item['limit']}, value = {item['value']}")                break       if submitted:        print(f'{alpha_id} - Submission successful!')        return True    else:        return Falsedef main():    """Main function to run the alpha submission script"""    print("=== WorldQuant Brain Alpha Submitter ===")    print("This script will help you submit alphas with automatic retry logic.")    print("You will be prompted to enter your WorldQuant Brain credentials.\n")       # Login with user credentials    session = login()    if session is None:        print("Failed to login. Exiting.")        return       print("\n=== Alpha Submission Mode ===")    print("Enter alpha IDs one by one. Type 'quit' to exit.")    print("Type 'relogin' to login with different credentials.")    print("Type 'info <alpha_id>' to check alpha details before submitting.")       while True:        alpha_id = input("\nEnter alpha ID (or 'quit' to exit, 'relogin' to change credentials): ").strip()               if alpha_id.lower() == 'quit':            print("Goodbye!")            break               if alpha_id.lower() == 'relogin':            print("\nRe-logging in...")            session = login()            if session is None:                print("Failed to login. Exiting.")                return            continue               if alpha_id.lower().startswith('info '):            info_alpha_id = alpha_id[5:].strip()            if not info_alpha_id:                print("Please provide an alpha ID after 'info'")                continue                       print(f"\nChecking details for alpha: {info_alpha_id}")            print("=" * 50)                       # Check if alpha exists            exists, alpha_data = check_alpha_exists(session, info_alpha_id)            if exists:                # Get record sets                get_alpha_recordsets(session, info_alpha_id)                               # Show some basic alpha info                if alpha_data:                    print(f"📋 Alpha Details:")                    print(f"   ID: {alpha_data.get('id', 'N/A')}")                    print(f"   Type: {alpha_data.get('type', 'N/A')}")                    if 'settings' in alpha_data:                        print(f"   Has settings: Yes")                    if 'regular' in alpha_data:                        print(f"   Has regular data: Yes")                    if 'combo' in alpha_data:                        print(f"   Has combo data: Yes")                    if 'selection' in alpha_data:                        print(f"   Has selection data: Yes")                       print("=" * 50)            continue               if not alpha_id:            print("Please enter a valid alpha ID.")            continue               print(f"\nSubmitting alpha: {alpha_id}")        print("=" * 50)               success = submit_alpha(alpha_id, session)               if success:            print(f"✅ Alpha {alpha_id} processed successfully!")        else:            print(f"❌ Alpha {alpha_id} failed to submit properly.")               print("=" * 50)if __name__ == "__main__":    main()
```

注意！PPAC Alpha和SuperAlpha,如果你在网页上没写好描述，用这个是交不了的！！！

注意！PPAC Alpha和SuperAlpha,如果你在网页上没写好描述，用这个是交不了的！！！

注意！PPAC Alpha和SuperAlpha,如果你在网页上没写好描述，用这个是交不了的！！！

注意！PPAC Alpha和SuperAlpha,如果你在网页上没写好描述，用这个是交不了的！！！

---

## 讨论与评论 (15)

### 评论 #1 (作者: WL13229, 时间: 10 months ago)

OK，帮你强调一下。

> **注意！PPAC Alpha和SuperAlpha,如果你在网页上没写好描述，用这个是交不了的！！！**

---

### 评论 #2 (作者: MX83967, 时间: 10 months ago)

厉害了大佬，代码看起来很详细，很完整，各方面都考虑到了，直接拿来就可以用，对社区贡献大大的，我是上个月中旬刚拿到的条件顾问，但到现在还没找到可以提交的alpha,不知道要从哪里开始呢，是先研究模板还是先直接找alpha呢，还是先找alpha再拓展为模板呢，还望大佬给点新人顾问建议呢

---

### 评论 #3 (作者: LQ78150, 时间: 10 months ago)

代码最后加一个微信通知，就可以及时关掉代码了

> 一旦提交上要赶紧关掉代码噢！不然一直请求了

---

### 评论 #4 (作者: OY62064, 时间: 10 months ago)

[WL13229](/hc/en-us/profiles/27485205931031-LQ99002) 请问下如何知道描述没写好呢？我最近提交PPAC，发现一直提交不上去。

---

### 评论 #5 (作者: WL13229, 时间: 10 months ago)

[OY62064](/hc/en-us/profiles/30346946070679-OY62064)

先再网页试一下，确认没有报错说“不符合描述格式”后，再代码提交。

---

### 评论 #6 (作者: TY31819, 时间: 10 months ago)

请问一下网页上怎么写描述呢？

---

### 评论 #7 (作者: TY31819, 时间: 10 months ago)

各位大佬，请问输入邮箱密码和alpha ID之后没有任何反应是怎么回事呢

---

### 评论 #8 (作者: DZ78677, 时间: 10 months ago)

这两天提交转圈的时间非常长！

---

### 评论 #9 (作者: WL13229, 时间: 10 months ago)

[TY31819](/hc/en-us/profiles/33447266273943-TY31819)

直接load template直接写

[TY31819](/hc/en-us/profiles/33447266273943-TY31819)

我没有遇到过

[DZ78677](/hc/en-us/profiles/28946582992023-DZ78677)

从今天下午起应该有好转

---

### 评论 #10 (作者: LJ86847, 时间: 10 months ago)

膜拜大佬，最近困扰多日的提交问题，您的代码方案太关键了，感谢大佬出手相助🙏🙏🙏

---

### 评论 #11 (作者: ER48854, 时间: 10 months ago)

好像有个批量在网页上提交description的代码。

---

### 评论 #12 (作者: MY41727, 时间: 10 months ago)

感谢分享，我试一下

---

### 评论 #13 (作者: ZZ37826, 时间: 10 months ago)

请问一下如果是PPAC的Alpha，没有提交description，能够进行check吗？

---

### 评论 #14 (作者: HH34943, 时间: 3 months ago)

不能在代码里设置只能提交一个吗，提交一个就自动停止运行，为什么要自己手动关。代码应该能做到吧？

---

### 评论 #15 (作者: PW90469, 时间: 18 days ago)

究竟达到什么状态可以Submit，一直没看到有成功的示范。

另外，我点击Submit之后就无动静了，看到网络请求一直在重复，有无大佬解答一下？

---

