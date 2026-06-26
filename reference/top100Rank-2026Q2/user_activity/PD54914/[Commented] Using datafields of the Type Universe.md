# Using datafields of the Type "Universe"

- **链接**: [Commented] Using datafields of the Type Universe.md
- **作者**: DN28451
- **发布时间/热度**: 7个月前, 得票: 5

## 帖子正文

I have been trying to do simulations with datafields of the type "universe" with no success. I will appreciate any clue on how to go about this. Below is an example of such datafield

E.g.
Field: top1200
Description: 20140630
Type: Universe

---

## 讨论与评论 (10)

### 评论 #1 (作者: CN36144, 时间: 7个月前)

Have been waiting for this. Any suggestion from the community would much appreciate

---

### 评论 #2 (作者: PD54914, 时间: 7个月前)

I usually use Universe-type fields to filter out low-liquidity stocks.

For example: top1000 ? returns : 0

This way the universe acts as a simple liquidity filter.

---

### 评论 #3 (作者: TP85668, 时间: 7个月前)

Thanks for the question! Datafields of type  *Universe*  cannot be used as numeric inputs directly. They act as  **filters (masks)**  that define which stocks belong to a specific set on a given date. The correct approach is to pair them with functions like  `where()` ,  `mask()` , or conditional logic to restrict your calculation universe. You need to apply them on top of a numeric expression—universe fields cannot operate standalone.

---

### 评论 #4 (作者: MY82844, 时间: 6个月前)

[TP85668](/hc/en-us/profiles/14806393292439-TP85668)  Thanks for the comments! What is the difference between those universe fields and the universe options on the settings panel?

---

### 评论 #5 (作者: AG14039, 时间: 6个月前)

Thanks for the question! Universe-type datafields can’t be used as numeric inputs because they function purely as filters that identify which stocks belong to a given set on each date. To use them correctly, you have to pair them with operators like where(), mask(), or other conditional logic to limit a numeric expression’s scope—universe fields can shape your calculation, but they can’t operate on their own.

---

### 评论 #6 (作者: NS62681, 时间: 5个月前)

Universe-type data fields aren’t numeric inputs and can’t be used directly in calculations. They function as filters that specify which stocks are included on each date. To use them correctly, combine them with functions like  `where()` ,  `mask()` , or other conditional logic to limit the calculation universe.

---

### 评论 #7 (作者: HT71201, 时间: 5个月前)

Thanks! Universe-type fields can’t be numeric inputs—they only act as filters to identify which stocks are in a set on each date. To use them, pair them with operators like  `where()`  or  `mask()`  to limit a numeric expression’s scope; they influence calculations but don’t work standalone.

---

### 评论 #8 (作者: KP26017, 时间: 5个月前)

as dynamic filters that determine which instruments are included on each date. Proper usage requires combining them with conditional functions such as  `where()` ,  `mask()` , or similar logic to constrain the calculation universe.

---

### 评论 #9 (作者: KG79468, 时间: 5个月前)

Universe-type fields (like  `top1200` ) aren’t numeric signals, so they can’t be used directly in expressions. They’re meant as  **filters or group definitions** , not alpha inputs.

---

### 评论 #10 (作者: DN28451, 时间: 5个月前)

Thank you all for your inputs. I have understood that Proper usage of universe- type datafields require combining them with conditional functions such as where(), mask(), or similar logic to constrain the calculation universe. I will highly appreciate an example of an alpha that has a universe- type datafield.

---

