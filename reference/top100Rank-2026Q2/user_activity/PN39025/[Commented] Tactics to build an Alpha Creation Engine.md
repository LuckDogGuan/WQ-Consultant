# Tactics to build an Alpha Creation Engine

- **链接**: [Commented] Tactics to build an Alpha Creation Engine.md
- **作者**: NL41370
- **发布时间/热度**: 1年前, 得票: 17

## 帖子正文

**Tactics to build an Alpha Creation Engine**

Building a successful Alpha Creation Engine (ACE) requires thoughtful implementation of BRAIN APIs. In this forum post, we discuss two different tactics that you can use while creating your ACE with  [**ace_lib**](https://platform.worldquantbrain.com/learn/documentation/ace-2023/ace-2023-doc)  library:

- **Template Method:**

Template Method uses predefined settings and operators to iterate over large amounts of data to find signals that show promising results. A possible way to execute this is as follows:

1. Select a dataset that you would like to run templates on. You can consider theme, region, coverage etc. while making this decision.
2. Create a template of operators, like  **rank()** or  **ts_rank()**
3. Run a loop for each data field of the dataset and use  **generate_alpha()**  method to combine your template, data fields and settings.
4. Finally, simulate the alpha using  **simulate_single_alpha()**
5. You can also add tags to simulated alpha with  **set_alpha_properties()**  for SuperAlpha selection and future referencing.

![图片](images/img_cacdb688ae.png)

*Flow for Template Method*

- **Decision Layers:**

Apart from template method that uses an iterative approach to generate expressions, we can also use decision layers approach to create expression. This is particularly suited when trying to optimize for parameters for promising alphas. A possible way to execute this is as follows:

1. Define the layers to optimize, e.g. Lookback days, neutralization, decay and define possible values they can take.
2. Define selection condition for each layer. e.g, max sharpe for lookback, max fitness for neutralization etc.
3. With your start expression, simulate and select the optimized alpha for each layer one by one. While simulating layers, you can either change settings or change expression (e.g. using neutralization operator with grouping fields)
4. After passing through all the layers, final expression should help you find the optimized parameters and settings.

![图片](images/img_111004d141.png)

*Flow for Decision Layers*

---

## 讨论与评论 (30)

### 评论 #1 (作者: EM11875, 时间: 1年前)

Thanks for sharing this  [NL41370](/hc/en-us/profiles/11433604068887-NL41370) 
Super-helpful breakdown.

---

### 评论 #2 (作者: RB25229, 时间: 1年前)

Can we use cloud services like azure and AWS for alpha creation engine?

---

### 评论 #3 (作者: NL41370, 时间: 1年前)

Hi  [RB25229](/hc/en-us/profiles/22650606988055-RB25229)

Yes, it's possible, but it would not need that much compute, leverage your PC should be enough I think

---

### 评论 #4 (作者: RB25229, 时间: 1年前)

Hi NL41370,

I am working on creating an AI driven alpha research project. Can I use Worldquant API there.? So, at that time I may need high capacity CPUs.

---

### 评论 #5 (作者: VV63697, 时间: 1年前)

How to load other universe data fields in ace ,  it by default loads US data fields .

---

### 评论 #6 (作者: AG20578, 时间: 1年前)

Hi  [VV63697](/hc/en-us/profiles/22631087402903-VV63697) !

You can load other regions' datasets and datafields if you specify region parameter in get_datasets and get_datafields functions.

Example:

```
hf.get_datasets(s, region='EUR', delay =1, universe='ILLIQUID_MINVOL1M')hf.get_datafields(s, region='EUR', delay =1, universe='ILLIQUID_MINVOL1M', dataset_id=dataset_id)ace.generate_alpha(x, region= 'EUR', universe = 'ILLIQUID_MINVOL1M', neutralization = 'SLOW', nan_handling='ON')
```

You can check available parameters for functions if you search them in code of ace_lib.py of helpful_functions.py

---

### 评论 #7 (作者: RB25229, 时间: 1年前)

How to load already simulated  alphas  in ACE.?

---

### 评论 #8 (作者: NL41370, 时间: 1年前)

Hi  [RB25229](/hc/en-us/profiles/22650606988055-RB25229)

Yes, of course you can use API there.

---

### 评论 #9 (作者: UG81605, 时间: 1年前)

Hi, when i use get_check_submission function, it returns error code as 201, 401. Can you share a code snippet on the same. I have used this: check_df=ace.get_check_submission(s,alpha_id). Also can we loop this and check submisions for a bunch of passing alphas, plus whats the limit of check submission ?

---

### 评论 #10 (作者: AG20578, 时间: 1年前)

Hi UG81605!

check_df=ace.get_check_submission(s,alpha_id) Is a right code for getting dataframe with tests checks for one alpha.

One thing that might have happened - you session is expired. Try to relogin by running s = ace.start_session()

You can loop trough the list of alpha_ids one by one, try something like this:

```
check_submission_result = []for alpha_id in your_alpha_id_list:    if ace.check_session_timeout(s) < 2000:        s = ace.start_session()    check_submission_result.append(ace.get_check_submission(s, alpha_id))
```

---

### 评论 #11 (作者: SK78969, 时间: 1年前)

Thanks for clarification !

---

### 评论 #12 (作者: AS77213, 时间: 1年前)

How to load Delay 0 data fields using API for any given universe as by default Delay 1 data fields are loaded. At what part of the code do we need to make changes.

---

### 评论 #13 (作者: AG20578, 时间: 1年前)

Hi  [AS77213](/hc/en-us/profiles/10752416693655-AS77213) !

Here are parameters for functions that you can specify:

ace.get_datasets(
    s, 
    instrument_type='EQUITY', 
    region='GLB', 
    delay=1, 
    universe='MINVOL1M',
)

ace.get_datafields(
    s, 
    instrument_type='EQUITY', 
    region='GLB', 
    delay=1, 
    universe='TOP3000', 
    dataset_id='option2', 
    search='option price'
)

and don't forget to specify delay in generate_alpha function:

ace.generate_alpha(
    regular = 'ts_skewness(vec_avg(nws18_acb),120)',
    alpha_type = "REGULAR",
    region = "GLB",
    universe = "MINVOL1M",
    delay = 1,
    decay = 0,
    neutralization = "INDUSTRY",
    truncation = 0.08,
    pasteurization = "ON",
    test_period = "P2Y0M0D",
    unit_handling = "VERIFY",
    nan_handling = "OFF",
    visualization: bool = False,
)

Hope it helps

---

### 评论 #14 (作者: AG20578, 时间: 1年前)

Also please check out the  [Documentation for ACE API Library](https://platform.worldquantbrain.com/learn/documentation/brain-api/ace-2023-doc)  to see which parameters different functions use.

---

### 评论 #15 (作者: SC43474, 时间: 1年前)

Hi NL41370,

Thank you for sharing this detailed and insightful post! It’s been incredibly helpful in understanding the different tactics for building an Alpha Creation Engine.

I wanted to ask, how can we simulate Super Alphas using the Brain API? Are there any specific steps or parameters that we need to configure differently compared to standard alpha simulations?

Looking forward to your guidance!

Thanks again!

---

### 评论 #16 (作者: AG20578, 时间: 1年前)

Hi  [SC43474](/hc/en-us/profiles/5163496266135-SC43474)

Please check out the  [Documentation for ACE API Library](https://platform.worldquantbrain.com/learn/documentation/brain-api/ace-2023-doc)  - generate_alpha function has parameter alpha_type, so to generate super alpha:

```
your_super_alpha = [    ace.generate_alpha(        alpha_type="SUPER",        selection="1",        combo="1",        region="USA",        universe="ILLIQUID_MINVOL1M",        delay=1,        decay=10,        neutralization="SLOW_AND_FAST",        selection_limit=1000    )]
```

Then you can run simulation:

```
ace.simulate_alpha_list_multi(s, your_super_alpha)
```

To get more information, please reach out to your advisor.

---

### 评论 #17 (作者: AG20578, 时间: 1年前)

Hi RB25229!

Try to get in touch with your advisor and discuss this topic.

You can try and find the request url if you inspect the Alphas page and go to the network tab

---

### 评论 #18 (作者: AM71073, 时间: 1年前)

This is a great guide on building an Alpha Creation Engine (ACE)! The  **Template Method**  approach seems like a powerful way to systematically iterate over datasets and identify promising signals, especially with predefined operators like  **rank()**  and  **ts_rank()** . I appreciate the simplicity of running a loop over each data field and combining it with the  **generate_alpha()**  method for efficiency.

The  **Decision Layers**  approach is equally intriguing, particularly for fine-tuning parameters like lookback days, neutralization, and decay. The idea of optimizing each layer individually to maximize Sharpe or fitness gives a structured way to enhance the alpha's performance.

I’ll definitely try implementing these tactics in my own ACE setup. Looking forward to experimenting with both methods!

---

### 评论 #19 (作者: AT56452, 时间: 1年前)

The article and the comments here are super helpful for me to work on an alpha engine.

---

### 评论 #20 (作者: PM26052, 时间: 1年前)

Great breakdown of the two tactics for building an Alpha Creation Engine! The Template Method seems like a solid approach for quickly iterating through datasets and applying standardized operations, which is ideal for generating a large pool of alphas.

The Decision Layers tactic is especially intriguing, as it focuses on optimizing individual parameters to fine-tune alphas. I’m curious, when optimizing using the decision layers, how much emphasis should be placed on the initial expression versus adjusting the settings in the layers? Would you recommend prioritizing one over the other for quicker results, or should they be balanced throughout the process?

---

### 评论 #21 (作者: PN39025, 时间: 1年前)

Thank you for sharing such a comprehensive resource! It is not only a starting point but also a roadmap for continuous improvement and learning. Your efforts to help others through this challenging yet rewarding journey are greatly appreciated. Wishing everyone success and happy learning, indeed!

---

### 评论 #22 (作者: DN45758, 时间: 1年前)

Thank you for sharing this comprehensive guide on building an  **Alpha Creation Engine (ACE)**  using the  **Template Method**  and  **Decision Layers**  approaches. The step-by-step breakdown of each tactic is incredibly insightful. The Template Method’s iterative approach, leveraging operators like  `rank()`  and  `ts_rank()` , is a great way to explore datasets efficiently. Meanwhile, the Decision Layers approach provides a structured framework for parameter optimization, ensuring refined and high-performing Alphas. The inclusion of practical examples, such as optimizing lookback days or neutralization, adds depth and clarity. This guide is an invaluable resource for anyone looking to build a robust ACE. Much appreciated!

---

### 评论 #23 (作者: NP65801, 时间: 1年前)

Incredible guide on Alpha Creation Engine tactics! The Template Method’s systematic iteration and the Decision Layers' structured optimization provide a solid foundation for efficient and high-performing Alpha creation. Big thanks for the clear explanations and actionable insights. Truly a game-changer for researchers!

---

### 评论 #24 (作者: ZH78994, 时间: 1年前)

I would like to express my heartfelt gratitude for your generous sharing. Your willingness to offer your time, knowledge, and resources means a great deal to me. The insights you've provided have not only broadened my understanding but also inspired me to take positive steps forward. It's rare to encounter someone so selfless and giving, and I truly appreciate the impact you've had. Thank you for your kindness and for being such a valuable source of support. Your gesture will be remembered, and I am grateful for the opportunity to learn from you.

---

### 评论 #25 (作者: YC82708, 时间: 1年前)

The article on building an Alpha Creation Engine (ACE) offers a practical approach to optimizing alpha generation using two main tactics: the Template Method and Decision Layers. The Template Method is a structured approach, using predefined operators and templates to efficiently process large datasets and identify promising signals. The iterative loop of applying operators like rank() or ts_rank() across data fields ensures that all relevant signals are explored. The Decision Layers method, on the other hand, is more flexible and focused on optimizing parameters like lookback periods, neutralization, and decay. It uses a step-by-step simulation process to fine-tune expressions, making it ideal for achieving the best-performing alphas. I appreciated how both methods emphasize systematic optimization, offering complementary strategies depending on the project’s needs. This structured approach aligns with my quantitative research goals, providing a solid foundation for refining and improving alpha models in real-world applications.

---

### 评论 #26 (作者: CC40930, 时间: 1年前)

Great insights into building an Alpha Creation Engine (ACE)! Both the Template Method and Decision Layers approaches are powerful ways to optimize alpha generation.

The Template Method allows for a systematic approach by selecting datasets, defining operator templates, and running them iteratively across multiple data fields. It's a great way to explore large datasets and identify promising signals, especially with the flexibility to add tags for SuperAlpha selection. This approach ensures that your alpha generation process is scalable and efficient.

---

### 评论 #27 (作者: AS77213, 时间: 1年前)

Thank  you for sharing this post on financial models. The frameworks and methodologies you outlined are extremely useful .The Template Method provides a structured approach by choosing datasets in a systematic manner.

---

### 评论 #28 (作者: PT27687, 时间: 1年前)

Building an Alpha Creation Engine sounds intricate yet fascinating! The tactics you presented, especially the use of template methods and decision layers, seem to streamline the process of finding promising signals effectively. Have you found that one approach yields better results over the other in your experience? It would be interesting to know if particular datasets lend themselves better to either tactic!

---

### 评论 #29 (作者: DK30003, 时间: 1年前)

How to load Delay 0 data fields using API for any given universe as by default Delay 1 data fields are loaded. At what part of the code do we need to make changes.

---

### 评论 #30 (作者: ND27369, 时间: 8个月前)

super helpful

---

