# MCP回测超时的一种解决办法代码优化

- **链接**: https://support.worldquantbrain.com/hc/zh-cn/search/click?data=BAh7DjoHaWRsKwiX%2FGlOeR86D2FjY291bnRfaWRpA9GrqjoJdHlwZUkiE2NvbW11bml0eV9wb3N0BjoGRVQ6CHVybEkiAbJodHRwczovL3N1cHBvcnQud29ybGRxdWFudGJyYWluLmNvbS9oYy96aC1jbi9jb21tdW5pdHkvcG9zdHMvMzQ2MDU4NjcwNzI2NjMtTUNQJUU1JTlCJTlFJUU2JUI1JThCJUU4JUI2JTg1JUU2JTk3JUI2JUU3JTlBJTg0JUU0JUI4JTgwJUU3JUE3JThEJUU4JUE3JUEzJUU1JTg2JUIzJUU1JThBJTlFJUU2JUIzJTk1BjsIVDoOc2VhcmNoX2lkSSIpNTkzNzk1NDYtNjI0NS00ZGQzLTlmZmMtY2NiODJlMWQ3YzkyBjsIRjoJcmFua2kKOgtsb2NhbGVJIgp6aC1jbgY7CFQ6CnF1ZXJ5SSIMUk00OTI2MgY7CFQ6EnJlc3VsdHNfY291bnRpFA%3D%3D--74923ddb8520fc856ab19729774b1102cd156b11
- **作者**: WF37935
- **发布时间/热度**: 9个月前, 得票: 13

## 帖子正文

我使用gemini cli回测alpha会出现超时的情况，研究后发现可能是因为gemini cli调用mcp的时候有内置的超时时间，大概30秒左右，而回测至少也得几分钟时间。看了官方文档问了AI也没找到能改变超时时间的办法，后来想了个方法，把回测的代码改一下就可以了。官方自带的回测方法create_multiSim包含了三个部分：发送回测请求，获取回测进度，回测完成后获取回测结果，根据这个把create_multiSim拆分成三个方法。发送回测请求和回测完成后获取回测结果一般都很快，关键就是获取回测进度，这个方法中，我并不会等到回测完成，而是设置了重试次数，目前是８次，而每次回测worldquant都会给我们返回Retry-After,是2.5秒，这样每次执行时间严格控制在30秒之内，基本上就不会有回测超时的问题了。代码如下：@mcp.tool()async def create_multiSim(alpha_expressions: List[str],instrument_type: str = "EQUITY",region: str = "USA",universe: str = "TOP3000",delay: int = 1,decay: int = 0,neutralization: str = "NONE",truncation: float = 0.0,test_period: str = "P0Y0M",unit_handling: str = "VERIFY",nan_handling: str = "OFF",language: str = "FASTEXPR",visualization: bool = False,pasteurization: str = "ON",max_trade: str = "OFF") -> Dict[str, Any]:"""🚀 Create multiple regular alpha simulations on BRAIN platform in a single request.This tool creates a multisimulation with multiple regular alpha expressions,waits for all simulations to complete, and returns detailed results for each alpha.⏰ NOTE: Multisimulations can take 8+ minutes to complete. This tool will waitfor the entire process and return comprehensive results.Call get_platform_setting_options to get the valid options for the simulation.Args:alpha_expressions: List of alpha expressions (2-8 expressions required)instrument_type: Type of instruments (default: "EQUITY")region: Market region (default: "USA")universe: Universe of stocks (default: "TOP3000")delay: Data delay (default: 1)decay: Decay value (default: 0)neutralization: Neutralization method (default: "NONE")truncation: Truncation value (default: 0.0)test_period: Test period (default: "P0Y0M")unit_handling: Unit handling method (default: "VERIFY")nan_handling: NaN handling method (default: "OFF")language: Expression language (default: "FASTEXPR")visualization: Enable visualization (default: True)pasteurization: Pasteurization setting (default: "ON")max_trade: Max trade setting (default: "OFF")Returns:Dictionary containing multisimulation status.If multisimulation is compelted, call get_multisimulation_result to get individual alpha details"""try:logger.info('create_multiSim start')# Validate inputif len(alpha_expressions) < 2:return {"error": "At least 2 alpha expressions are required"}if len(alpha_expressions) > 8:return {"error": "Maximum 8 alpha expressions allowed per request"}# Create multisimulation datamultisimulation_data = []for alpha_expr in alpha_expressions:simulation_item = {'type': 'REGULAR','settings': {'instrumentType': instrument_type,'region': region,'universe': universe,'delay': delay,'decay': decay,'neutralization': neutralization,'truncation': truncation,'pasteurization': pasteurization,'unitHandling': unit_handling,'nanHandling': nan_handling,'language': language,'visualization': visualization,# 'testPeriod': test_period,'testPeriod': 'P0Y','maxTrade': max_trade},'regular': alpha_expr}multisimulation_data.append(simulation_item)logger.info(multisimulation_data)# Send multisimulation requestresponse = brain_client.session.post(f"{brain_client.base_url}/simulations", json=multisimulation_data)start_time = time.time()start_time_formatted = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')logger.info(f"multisimulate start at {start_time_formatted}")logger.info(response.content)if response.status_code != 201:if response.status_code == 429:logger.warning("Rate limit exceeded")return {"error": f"Too Many Requests! You should stop and ask the user to try again later."}else:return {"error": f"Failed to create multisimulation. Status: {response.status_code},, you need to call three mcp tools get_operators, get_platform_setting_options and get_datafields to check whether you correctly use the operators, setting the simulation settings, and existing data fields."}# Get multisimulation locationlocation = response.headers.get('Location', '')if not location:return {"error": "No location header in multisimulation response"}logger.info(f'location: {location}')# Wait for children to appear and get resultsreturn await check_multisimulation_status(start_time, location, len(alpha_expressions))except Exception as e:return {"error": f"Error creating multisimulation: {str(e)}, , you need to call three mcp tools get_operators, get_platform_setting_options and get_datafields to check whether you correctly use the operators, setting the simulation settings, and existing data fields."}@mcp.tool()async def check_multisimulation_status(start_time: float, location: str, expected_children: int) -> Dict[str, Any]:"""check multisimulation status: in progess, completed or error"""try:# Simple progress indicator for userslogger.info(f"Waiting for multisimulation to complete... (this may take several minutes)")logger.info(f"Expected {expected_children} alpha simulations")print()# Wait for children to appear - much more tolerant for 8+ minute multisimulationschildren = []max_wait_attempts = 8  # Increased significantly for 8+ minute multisimulationswait_attempt = 0while wait_attempt < max_wait_attempts and len(children) == 0:wait_attempt += 1try:multisim_response = brain_client.session.get(location)if multisim_response.status_code == 200:multisim_data = multisim_response.json()children = multisim_data.get('children', [])if children:breakelse:# Wait before next attempt - use longer intervals for multisimulationsretry_after = multisim_response.headers.get("Retry-After", 5)logger.info(f'waiting for multiSim completion, sleeping {retry_after}s')wait_time = float(retry_after)await asyncio.sleep(wait_time)else:await asyncio.sleep(5)except Exception as e:await asyncio.sleep(5)if not children:current_time = time.time()elapsed = (current_time - start_time) / 60return {"status": "in_progress","message": "wait for one minute and call check_multisimulation_status","start_time": start_time,"location": location,"expected_children": expected_children,"note": f"multisimulation last for {elapsed} minutes, if longer than 15 minutes, stop and ask the user"}else:status = multisim_response.json().get("status", 0)if status == 'ERROR':return {"status": "error","message": "call get_SimError_detail for the error detail","location": location}elif status == 'COMPLETE':return {"status": "completed","message": "multisimulation finished, you should call get_multisimulation_result to get result","location": location,"expected_children": expected_children}else:return {"status": "undefined status", "message": "you should stop and ask the user about this situation"}except Exception as e:return {"error": f"Error waiting for multisimulation completion: {str(e)}, you need to call three mcp tools get_operators, get_platform_setting_options and get_datafields to check whether you correctly use the operators, setting the simulation settings, and existing data fields."}@mcp.tool()async def get_multisimulation_result(location: str, expected_children: int) -> Dict[str, Any]:"""After multisimulation completed, return results"""try:# Simple progress indicator for userslogger.info(f"Waiting for multisimulation to complete... (this may take several minutes)")logger.info(f"Expected {expected_children} alpha simulations")print()# Wait for children to appear - much more tolerant for 8+ minute multisimulationschildren = []try:multisim_response = brain_client.session.get(location)if multisim_response.status_code == 200:multisim_data = multisim_response.json()children = multisim_data.get('children', [])if not children:return {"error": f"Children did not appear (multisimulation may still be processing)"}except Exception as e:logger.info(f'waiting for completion error: {e}')await asyncio.sleep(5)logger.info('multiSimulate complete, getting children information...')# Process each child to get alpha resultsalpha_results = []for i, child_id in enumerate(children):try:# The children are full URLs, not just IDschild_url = child_id if child_id.startswith('http') else f"{brain_client.base_url}/simulations/{child_id}"# Wait for this alpha to complete - more tolerant timingfinished = Falsemax_alpha_attempts = 100  # Increased for longer alpha processingalpha_attempt = 0while not finished and alpha_attempt < max_alpha_attempts:alpha_attempt += 1try:alpha_progress = brain_client.session.get(child_url)if alpha_progress.status_code == 200:alpha_data = alpha_progress.json()retry_after = alpha_progress.headers.get("Retry-After", 0)if retry_after == 0:finished = Truebreakelse:wait_time = float(retry_after)await asyncio.sleep(wait_time)else:await asyncio.sleep(5)except Exception as e:await asyncio.sleep(5)if finished:# Get alpha details from the completed simulationalpha_id = alpha_data.get("alpha")if alpha_id:# Now get the actual alpha details from the alpha endpointalpha_details = brain_client.session.get(f"{brain_client.base_url}/alphas/{alpha_id}")if alpha_details.status_code == 200:alpha_detail_data = alpha_details.json()alpha_results.append({'alpha_id': alpha_id,'location': child_url,'details': alpha_detail_data})else:alpha_results.append({'alpha_id': alpha_id,'location': child_url,'error': f'Failed to get alpha details: {alpha_details.status_code}'})else:alpha_results.append({'location': child_url,'error': 'No alpha ID found in completed simulation'})else:alpha_results.append({'location': child_url,'error': f'Alpha simulation did not complete within {max_alpha_attempts} attempts'})except Exception as e:alpha_results.append({'location': f"child_{i+1}",'error': str(e)})# Return comprehensive resultslogger.info(f"Multisimulation completed! Retrieved {len(alpha_results)} alpha results")return {'success': True,'message': f'Successfully created {expected_children} regular alpha simulations','total_requested': expected_children,'total_created': len(alpha_results),'multisimulation_id': location.split('/')[-1],'multisimulation_location': location,'alpha_results': alpha_results,'note': "if you got a negative alpha sharpe, you can just add a minus sign in front of the last line of the Alpha to flip then think the next step."}except Exception as e:return {"error": f"Error waiting for multisimulation completion: {str(e)}, you need to call three mcp tools get_operators, get_platform_setting_options and get_datafields to check whether you correctly use the operators, setting the simulation settings, and existing data fields."}

---

## 讨论与评论 (11)

### 评论 #1 (作者: RM49262, 时间: 9个月前)

巧了我今天下午也在研究为啥Gemini Cli调用MCP超时，我看他们Github页面已经有不少人提了Issue，貌似现在这个版本的Gemini Cli有bug会无视MCP设置里的Timeout，希望下个版本能修复吧！ 也感谢大佬给出新的解决方案

---

### 评论 #2 (作者: LL87164, 时间: 9个月前)

有遇到类似问题，好像是 mcp 协议层面的一个内置设置，换了个模型后可以了。看来是需要模型知道这个设置并知道怎么调用或传参的。

---

### 评论 #3 (作者: SC77987, 时间: 9个月前)

大佬太强了,之前一直因为mcp回测超时问题导致很多mcp的功能都不能很好的利用起来,现在可以结合mcp回测功能和和其他大佬提到的自动评估论坛模板来选择好的模板了,谢谢大佬,祝pay高高!=========================================================

---

### 评论 #4 (作者: XW38100, 时间: 9个月前)

您好，这个文件在哪儿呢啊，我没有找到

---

### 评论 #5 (作者: WF37935, 时间: 9个月前)

RM49262太好了，希望能赶紧修复吧。而且它的启动命令也没个超时设置。。

---

### 评论 #6 (作者: WF37935, 时间: 9个月前)

LL87164我用的gemini-cli和cline的x都不行，是需要换付费的模型吗

---

### 评论 #7 (作者: WF37935, 时间: 9个月前)

XW38100这个就是改mcp的代码，platform_functions.py这个文件

---

### 评论 #8 (作者: LG79469, 时间: 9个月前)

您好，这个代码是要修改哪里的内容呀

---

### 评论 #9 (作者: RM49262, 时间: 9个月前)

今天测试了一下，新版本Gemini Cli已经修复这个问题了，目前可以正常调用回测工具了。感谢楼主的代码让我学到了新思路！---------------------------------------------------------------------------------------------------------------------------------------------------

---

### 评论 #10 (作者: MZ35432, 时间: 6个月前)

我记得修改 user_config.json 文件里面的值就行了 把  timeout 字段修改为更大值，如我把默认的30改成了300

---

### 评论 #11 (作者: MY49971, 时间: 6个月前)

感谢大佬分享，很有用的功能======================================================================================================Talk is cheap,show me the alpha=================================

---

