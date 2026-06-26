# Brain API

- **链接**: [Commented] Brain API.md
- **作者**: MB13430
- **发布时间/热度**: 1年前, 得票: 36

## 帖子正文

If you're using the Brain API for alpha research across different regions, I've compiled all the key settings you need to streamline your workflow. Whether you're dealing with universe, delay, or neutralization settings, having everything in one place makes it easier to configure your API calls for various regions. Check out the settings below to ensure you're using the correct parameters for each region.

## 

## **USA**

- **Region** : USA
- **Universe** : TOP3000, TOP1000, TOP500, TOP200, ILLIQUID_MINVOL1M, TOPSP500
- **Delay** : 0, 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST

## **Europe**

- **Region** : EUR
- **Universe** : TOP1200, TOP800, TOP400, ILLIQUID_MINVOL1M
- **Delay** : 0, 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST, COUNTRY

## **Global**

- **Region** : GLB
- **Universe** : TOP3000, MINVOL1M
- **Delay** : 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY

## **Asia**

- **Region** : ASI
- **Universe** : MINVOL1M, ILLIQUID_MINVOL1M
- **Delay** : 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST, COUNTRY

## **China**

- **Region** : CHN
- **Universe** : TOP2000U
- **Delay** : 0, 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, SLOW, FAST, SLOW_AND_FAST

## 

## **Korea**

- **Region** : KOR
- **Universe** : TOP600
- **Delay** : 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

## **Taiwan**

- **Region** : TWN
- **Universe** : TOP500, TOP100
- **Delay** : 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

## **Hong Kong**

- **Region** : HKG
- **Universe** : TOP800, TOP500
- **Delay** : 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

## **Japan**

- **Region** : JPN
- **Universe** : TOP1600, TOP1200
- **Delay** : 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY

## **AMR**

- **Region** : AMR
- **Universe** : TOP600
- **Delay** : 1
- **Neutralization** : MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, COUNTRY

By centralizing all the Brain API region settings, this should help you easily configure your strategy and make efficient API calls. Whether you're working in the USA, Europe, Asia, or anywhere else, these parameters will ensure you're optimizing for your specific region.

Feel free to use this as a reference and share it with others in the community who are leveraging the Brain API for their projects!

---

## 讨论与评论 (21)

### 评论 #1 (作者: MB13430, 时间: 1年前)

Brain has introduced Risk Neutralization for the Global Region. The currently available neutralization options for the Global Region are:

- MARKET
- SECTOR
- INDUSTRY
- SUBINDUSTRY
- SLOW
- FAST
- SLOW_AND_FAST
- COUNTRY

Brain will continue to expand and update Region, Universe, and Neutralization options. Refer to this post regularly for the latest updates.

---

### 评论 #2 (作者: LI36776, 时间: 1年前)

This is really helpful for automatically searching for alphas! Could I ask - how did you find this information?

---

### 评论 #3 (作者: MB13430, 时间: 1年前)

Hi,
I posted the above information based on my own experience, as I create alphas across various regions. I've observed all this information directly in the simulation settings.

---

### 评论 #4 (作者: KK81152, 时间: 1年前)

thanks for the information.

---

### 评论 #5 (作者: KK81152, 时间: 1年前)

It will be very helpful if you guide me on some basic principle of alpha creation...

please help...waiting

email id:  [greatkishanvns@gmail.com](mailto:greatkishanvns@gmail.com)

---

### 评论 #6 (作者: SK95162, 时间: 1年前)

Thanks for sharing such valuable insights! What could be the possible reasons for encountering an error with zero simulations when using the Brain API for the GLB region?

---

### 评论 #7 (作者: MB13430, 时间: 1年前)

Hi SK95162,
If you could share a snippet of your code or the simulation_data object, I’d be happy to help identify the issue in your code.

Thanks

---

### 评论 #8 (作者: SC43474, 时间: 1年前)

Thanks for sharing this valuable info! Is there a limit of fewer than 10 Multi-Simulations in the GLB region? I’ve been encountering challenges running alpha simulations via the Brain API for the Global region. Any advice?

---

### 评论 #9 (作者: YW42946, 时间: 1年前)

[SC43474](/hc/en-us/profiles/5163496266135-SC43474)

Though you max concurrent simulation is set to 10, normally we will suggest you lowering the con-current to may be 8 single simulation if you are running something complex(for example risk neutral GLB MINVOL1M).

---

### 评论 #10 (作者: TL60820, 时间: 1年前)

I want to ask about the reasonable parameter of concurrent simulations and multi simulations.

.

---

### 评论 #11 (作者: SK95162, 时间: 1年前)

Thank you,  [MB13430](/hc/en-us/profiles/1532959643302-MB13430)  , for asking! The issue has been resolved. It was related to the maximum concurrent simulation setting

---

### 评论 #12 (作者: AG20578, 时间: 1年前)

Hi TL60820!

Concurrent simulations and multi simulations should not be greater than 10 each. As for reasonable parameters, it really depends on your specific use case. Personally, I use 8 for both concurrent simulations and multi simulations.

---

### 评论 #13 (作者: AG20578, 时间: 1年前)

Hi KK81152!

Please reach out to your advisor, you can find info in  [Learn Section](https://platform.worldquantbrain.com/learn/documentation)  - Consultant Information - 'Your Advisor - '

---

### 评论 #14 (作者: CC40930, 时间: 1年前)

Great compilation of regional settings for the Brain API! It’s incredibly helpful to have all these parameters neatly laid out for different regions, making it easier to configure strategies efficiently. Each region’s unique universes, delays, and neutralization settings are essential for fine-tuning alpha research. For example, knowing that the USA and China have specific universe options like TOP3000 and TOP2000U, respectively, will help optimize the scope of research. Thanks for sharing this—it’s a valuable resource for anyone working with the Brain API!

---

### 评论 #15 (作者: LM49511, 时间: 1年前)

Thank you for this summary, it is very helpful when starting on Brain API and understanding how to configure different parameters when generating alphas.

---

### 评论 #16 (作者: AK40989, 时间: 1年前)

I've been looking everywhere for new neutralization parameters like SLOW, FAST, and SLOW_AND_FAST, and nothing seemed to work until now. This compilation is incredibly helpful, and I’m really grateful for it! It would be great if these settings were included in the official API documentation to assist others in their research.

 [YW42946](/hc/en-us/profiles/12485882527255-YW42946) Just to confirm, when running something complex, should only the concurrent simulations be lowered while keeping multi simulations at 10?

---

### 评论 #17 (作者: PT27687, 时间: 1年前)

This compilation of settings for the Brain API is incredibly helpful for anyone working on alpha research. It’s great to see such detailed information organized by region, making it much easier to find the right configurations. Are there any specific tips you would recommend for adjusting these settings based on market conditions?

---

### 评论 #18 (作者: DP33240, 时间: 1年前)

Awesome work compiling the regional settings for the Brain API! It’s super useful to have all the key parameters organized by region, making strategy setup much more straightforward. Details like universe definitions, delay settings, and neutralization preferences for each region are crucial when fine-tuning alpha development. For instance, knowing that the U.S. uses universes like TOP3000 and China uses TOP2000U really helps in tailoring research more effectively. Thanks for putting this together—it’s a great reference for anyone working with the Brain API!

---

### 评论 #19 (作者: JC84638, 时间: 1年前)

Hey guys, some of the newer neutralization settings that are compatible with USA, GLB, EUR, and ASI include:

- **REVERSION_AND_MOMENTUM**
- **STATISTICAL**
- **CROWDING**

---

### 评论 #20 (作者: AG20578, 时间: 1年前)

Hi! There is no need to gather settings manually. In ACE there is a function  `get_instrument_type_region_delay `  `that outputs for each region, delay - available universes and neutralizations`

---

### 评论 #21 (作者: HY24380, 时间: 1年前)

Access updated settings from Neutralization using the following code. It will give neutralization in all regions.

```
for i in range(len(ace.get_instrument_type_region_delay(s).head()['Neutralization'])):    print(ace.get_instrument_type_region_delay(s).head()['Neutralization'][0])
```

Additionally, the following section provides detailed information about settings.

```
ace.get_instrument_type_region_delay(s)
```

It will give

InstrumentType
Region
Delay
Universe
Neutralization

---

