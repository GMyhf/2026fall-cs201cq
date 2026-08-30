# 第3周 算法分析：大 O、复杂度级别、Python 内建结构性能

*Updated 2026-08-30 10:20 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 3 周 / 3 学时
> **教学内容**：算法分析：大 O、复杂度级别、Python 内建结构性能
> **教学要求**：掌握渐近符号衡量算法效率的方法；能够分析简单算法的时间复杂度

**知识点**：算法效率的度量、大 O / 大 Ω / 大 Θ、常见复杂度级别、最好/最坏/平均情况、均摊分析、空间复杂度、递归式与主定理（直观版）、Python 内建容器操作复杂度表、OJ 上的"数据规模 → 复杂度"反推法。

---

# 1 为什么需要复杂度分析

## 1.1 计时测量的局限

```python
import time

def f(n):
    return sum(range(n))

t0 = time.perf_counter()
f(10 ** 7)
print(time.perf_counter() - t0)
```

实测运行时间受**机器、语言、编译器、负载**影响，无法跨环境比较。我们需要一种**与机器无关**的度量：数一数算法执行了多少次"基本操作"，并考察当输入规模 n 增大时这个次数**如何增长**。

## 1.2 从计数到函数

```python
def sum_of_n(n):
    total = 0                 # 1 次赋值
    for i in range(1, n + 1): # 循环 n 次
        total = total + i     # 每次 1 加 1 赋值
    return total
```

基本操作次数 T(n) = 1 + 2n。当 n = 10⁶ 时，常数项 1 和系数 2 都无关紧要，真正决定量级的是 **n 这一项**。于是记 T(n) = O(n)。

---

# 2 渐近记号

## 2.1 大 O：上界

> 若存在正常数 c 和 n₀，使得对所有 n ≥ n₀ 都有 **T(n) ≤ c·g(n)**，则记 T(n) = O(g(n))。

直观理解：**O 给出增长的上界**，即"最坏不会比 g(n) 差（在常数倍意义下）"。

## 2.2 大 Ω 与 大 Θ

| 记号 | 含义 | 直观 |
| ---- | ---- | ---- |
| O(g) | 上界 | T 增长不快于 g |
| Ω(g) | 下界 | T 增长不慢于 g |
| Θ(g) | 紧确界 | T 与 g 同阶（既是 O 又是 Ω） |

严格地说"归并排序的时间复杂度是 Θ(n log n)"，但工程与竞赛中习惯统一写 O(n log n)。

## 2.3 化简规则

1. **去掉常系数**：O(3n) = O(n)。
2. **只保留最高阶项**：O(n² + 100n + 5000) = O(n²)。
3. **顺序结构取最大**：先 O(n) 再 O(n²)，总体 O(n²)。
4. **嵌套循环取乘积**：外层 n 次、内层 m 次，总体 O(nm)。
5. **对数的底数无关紧要**：log₂n 与 log₁₀n 只差常数倍，统一写 log n。

```python
# 判断下面各段的复杂度
for i in range(n):            # O(n)
    for j in range(n):        # O(n)
        ...                   # 总计 O(n^2)

for i in range(n):            # O(n)
    for j in range(i):        # 平均 n/2
        ...                   # 总计 n(n-1)/2 = O(n^2)

i = 1
while i < n:                  # i = 1,2,4,8,...  执行 log2(n) 次
    i *= 2                    # 总计 O(log n)

for i in range(n):
    j = 1
    while j < n:
        j *= 2                # 内层 O(log n)
                              # 总计 O(n log n)
```

---

# 3 常见复杂度级别

| 复杂度 | 名称 | 典型算法 | n=10⁶ 时大致操作数 |
| ---- | ---- | ---- | ---- |
| O(1) | 常数 | 数组随机访问、哈希查找 | 1 |
| O(log n) | 对数 | 二分查找、平衡树单次操作 | 20 |
| O(n) | 线性 | 遍历、前缀和 | 10⁶ |
| O(n log n) | 线性对数 | 归并/快排/堆排、排序后扫描 | 2×10⁷ |
| O(n²) | 平方 | 冒泡/选择/插入排序、朴素二重循环 | 10¹² ❌ |
| O(n³) | 立方 | Floyd-Warshall、朴素矩阵乘 | 10¹⁸ ❌ |
| O(2ⁿ) | 指数 | 子集枚举、朴素 TSP | 天文数字 |
| O(n!) | 阶乘 | 全排列枚举 | 天文数字 |

增长速度对比（示意）：

```
时间
 ^                                  2^n   n^2
 |                                 /     /
 |                                /     /        n log n
 |                               /     /        /
 |                              /     /       /          n
 |                             /    /      /        ____/
 |                            /   /    __/    _____/
 |                           / _/ __--/ _____/            log n
 |                        _--=--==------------------------------
 +--------------------------------------------------------------> n
```

## 3.1 OJ 上的反推法（重要实战技巧）

Python 每秒约能执行 10⁷ 量级的简单操作（C++ 约 10⁸–10⁹）。**看到数据范围就能倒推需要的复杂度**：

| n 的范围 | 可接受的复杂度 | 常见做法 |
| ---- | ---- | ---- |
| n ≤ 10–12 | O(n!) / O(2ⁿ·n) | 全排列、状压枚举 |
| n ≤ 20–25 | O(2ⁿ) | 子集枚举、折半搜索 |
| n ≤ 100 | O(n³) | Floyd、区间 DP |
| n ≤ 1000–2000 | O(n²) | 二维 DP、朴素图算法 |
| n ≤ 10⁵ | O(n log n) | 排序、堆、二分、Dijkstra |
| n ≤ 10⁶–10⁷ | O(n) 或 O(n log n) 常数要小 | 双指针、单调栈、前缀和 |
| n ≥ 10⁸ | O(log n) 或 O(1) | 数学公式、快速幂 |

> **考试技巧**：读完题先看 n 的范围，直接锁定算法类型，避免写出注定 TLE 的代码。

---

# 4 最好、最坏与平均情况

以顺序查找为例：

```python
def linear_search(a, target):
    for i, v in enumerate(a):
        if v == target:
            return i
    return -1
```

- **最好情况**：第一个就命中，O(1)。
- **最坏情况**：不存在或在末尾，O(n)。
- **平均情况**：命中位置均匀分布，期望比较 (n+1)/2 次，O(n)。

若无特别说明，**算法复杂度默认指最坏情况**。

**快速排序**是个著名的例外：最坏 O(n²)（每次划分极不均衡），平均 O(n log n)，实践中通过随机化枢轴使最坏情况几乎不发生（第 6 周详述）。

---

# 5 均摊分析：Python list 的 append 为何是 O(1)

Python 的 `list` 是**动态数组**：底层是一块连续内存，容量满了就申请一块更大的（通常约 1.125 倍以上增长），把旧元素搬过去。

- 单次 `append` 若触发扩容，是 O(n)。
- 但扩容不是每次都发生。设从容量 1 增长到 n，总搬移次数约为 1 + 2 + 4 + … + n < 2n。
- 于是 **n 次 append 总代价 O(n)，均摊每次 O(1)**。

这叫**均摊分析（amortized analysis）**：把偶发的昂贵操作代价平摊到大量廉价操作上。

```python
import sys

a = []
prev = -1
for i in range(20):
    a.append(i)
    cur = sys.getsizeof(a)
    if cur != prev:
        print(f"len={len(a):3d}  bytes={cur}")   # 观察容量跳变点
        prev = cur
```

---

# 6 Python 内建结构的操作复杂度

> 权威参考：https://wiki.python.org/moin/TimeComplexity
> 课程扩展表：https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt

## 6.1 list

| 操作 | 复杂度 | 说明 |
| ---- | ---- | ---- |
| `a[i]`、`a[i] = x` | O(1) | 随机访问 |
| `len(a)` | O(1) | 长度被缓存 |
| `a.append(x)` | 均摊 O(1) | |
| `a.pop()` | O(1) | 尾部 |
| `a.pop(0)`、`a.insert(0,x)` | **O(n)** | ⚠️ 要搬移后续所有元素 |
| `x in a` | O(n) | ⚠️ |
| `a.sort()` | O(n log n) | Timsort，近似有序时接近 O(n) |
| `a[i:j]` | O(j-i) | 切片是拷贝 |
| `a + b` | O(n+m) | 新建列表 |
| `min/max/sum` | O(n) | |

## 6.2 dict / set

| 操作 | 平均 | 最坏 |
| ---- | ---- | ---- |
| `d[k]`、`d[k]=v`、`del d[k]`、`k in d` | O(1) | O(n)（大量哈希冲突，第 15 周讨论） |
| 遍历 | O(n) | O(n) |
| `set` 的 `add`/`in`/`discard` | O(1) | O(n) |
| `s1 & s2` | O(min(len(s1), len(s2))) | |
| `s1 \| s2` | O(len(s1) + len(s2)) | |

## 6.3 collections.deque

| 操作 | 复杂度 |
| ---- | ---- |
| `append` / `appendleft` / `pop` / `popleft` | **O(1)** |
| `d[i]`（中间随机访问） | O(n) |

> BFS 一定要用 `deque` 而不是 `list`——用 `list.pop(0)` 会把 O(n) 的 BFS 变成 O(n²)（第 8、12 周）。

## 6.4 str

字符串**不可变**，所以 `s += t` 会新建对象，循环中拼接是 O(n²)：

```python
# ❌ O(n^2)
s = ''
for w in words:
    s += w

# ✅ O(total_len)
s = ''.join(words)
```

## 6.5 实测对比脚本

```python
import timeit
from collections import deque

N = 100000

t_list = timeit.timeit(
    'a.pop(0)',
    setup=f'a = list(range({N}))',
    number=N // 10)

t_deque = timeit.timeit(
    'a.popleft()',
    setup=f'from collections import deque; a = deque(range({N}))',
    number=N // 10)

print(f"list.pop(0) : {t_list:.4f}s")
print(f"deque.popleft(): {t_deque:.4f}s")     # 通常快 2~3 个数量级
```

**这是本周实验课的必做项**：亲手测一遍，把"复杂度"这件事变成肌肉记忆。

---

# 7 空间复杂度

统计算法**除输入之外**额外占用的存储量。

```python
# 空间 O(1)：只用了常数个变量
def total(a):
    s = 0
    for x in a:
        s += x
    return s

# 空间 O(n)：新建了等长列表
def doubled(a):
    return [x * 2 for x in a]

# 空间 O(n)：递归深度 n，每层一个栈帧
def rec_sum(a, i=0):
    if i == len(a):
        return 0
    return a[i] + rec_sum(a, i + 1)
```

**递归的空间代价常被忽略**：深度为 n 的递归会占用 O(n) 的调用栈，Python 默认上限 1000，深递归须 `sys.setrecursionlimit` 并注意可能爆栈。

---

# 8 递归式与分治复杂度（直观版）

分治算法的复杂度常写成递归式：

```
T(n) = a·T(n/b) + f(n)
```

意为"把规模 n 的问题分成 a 个规模 n/b 的子问题，合并代价 f(n)"。

| 递归式 | 解 | 例子 |
| ---- | ---- | ---- |
| T(n) = T(n/2) + O(1) | O(log n) | 二分查找 |
| T(n) = T(n/2) + O(n) | O(n) | 快速选择（平均） |
| T(n) = 2T(n/2) + O(1) | O(n) | 二叉树遍历 |
| T(n) = 2T(n/2) + O(n) | O(n log n) | 归并排序 |
| T(n) = 2T(n-1) + O(1) | O(2ⁿ) | 汉诺塔 |

**递归树直观法**（以归并排序为例）：

```
层号   子问题规模    子问题个数    本层总代价
 0        n              1           n
 1       n/2             2           n
 2       n/4             4           n
 ...
 log n    1              n           n
                              ------------
                     共 log n + 1 层，每层 n  => O(n log n)
```

---

# 9 例题精讲

## 9.1 例题一：前缀和——把 O(nq) 降到 O(n+q)

**LeetCode 303. 区域和检索 - 数组不可变**，https://leetcode.cn/problems/range-sum-query-immutable/

朴素做法每次查询遍历区间，q 次查询共 O(nq)。**预处理前缀和**后每次查询 O(1)：

```python
class NumArray:
    def __init__(self, nums):
        self.pre = [0] * (len(nums) + 1)
        for i, v in enumerate(nums):
            self.pre[i + 1] = self.pre[i] + v      # pre[i] = nums[0..i-1] 之和

    def sumRange(self, left: int, right: int) -> int:
        return self.pre[right + 1] - self.pre[left]
```

预处理 O(n)，单次查询 O(1)，总计 O(n + q)。

## 9.2 例题二：最大子数组和——从 O(n³) 到 O(n)

**LeetCode 53. 最大子数组和**，https://leetcode.cn/problems/maximum-subarray/

```python
# 版本 1：三重循环 O(n^3)
def brute3(a):
    best = a[0]
    for i in range(len(a)):
        for j in range(i, len(a)):
            best = max(best, sum(a[i:j + 1]))     # sum 本身 O(n)
    return best


# 版本 2：前缀和 / 滚动和，O(n^2)
def brute2(a):
    best = a[0]
    for i in range(len(a)):
        cur = 0
        for j in range(i, len(a)):
            cur += a[j]
            best = max(best, cur)
    return best


# 版本 3：Kadane 算法，O(n)
def kadane(a):
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)     # 要么接在前面，要么从 x 重新开始
        best = max(best, cur)
    return best
```

三个版本答案相同，n = 10⁵ 时只有版本 3 能过。**同一个问题，不同复杂度就是能不能过题的分水岭。**

## 9.3 例题三：二分查找 O(log n)

**LeetCode 704. 二分查找**，https://leetcode.cn/problems/binary-search/

```python
def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2          # Python 大整数不会溢出
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

每次把搜索区间减半，最多 ⌊log₂n⌋+1 次，故 O(log n)。

Python 标准库直接提供：

```python
import bisect
i = bisect.bisect_left(a, x)     # 第一个 >= x 的位置
j = bisect.bisect_right(a, x)    # 第一个 > x 的位置
cnt = j - i                      # x 出现次数
```

## 9.4 例题四：复杂度判断练习

判断下列代码段的时间复杂度：

```python
# (1)
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            pass
# 答：C(n,3) = O(n^3)

# (2)
i = n
while i > 0:
    for j in range(i):
        pass
    i //= 2
# 答：n + n/2 + n/4 + ... = 2n = O(n)

# (3)
s = set()
for x in a:            # len(a) = n
    if x in s:         # O(1) 平均
        continue
    s.add(x)
# 答：O(n)

# (4)
res = []
for x in a:
    res.insert(0, x)   # O(len(res))
# 答：1+2+...+n = O(n^2)   —— 应改成 res.append(x) 后 res.reverse()
```

---

# 10 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 区域和检索 - 数组不可变 | LC 303 | 前缀和，O(1) 查询 |
| 2 | 最大子数组和 | LC 53 | O(n) 线性扫描 |
| 3 | 二分查找 | LC 704 | O(log n) |
| 4 | 搜索插入位置 | LC 35 | 二分边界 |
| 5 | 移动零 | LC 283 | 双指针 O(n) 原地 |

**实验（12 学时中的第 1 次）**：

编写 `benchmark.py`，对 n = 10³, 10⁴, 10⁵, 10⁶ 分别测量：

1. `list.append` vs `list.insert(0, x)`
2. `x in list` vs `x in set`
3. `str += ` vs `''.join`
4. `list.pop(0)` vs `deque.popleft()`

把结果画成折线图（`matplotlib`，横轴 n，纵轴用时，建议双对数坐标），并回答：**实测曲线的斜率是否与理论复杂度一致？**

**思考题**：

1. 若 T(n) = O(n²)，是否一定有 T(n) = O(n³)？是否一定有 T(n) = Θ(n²)？
2. 为什么说"O(1) 的哈希查找"在最坏情况下是 O(n)？什么情况会触发？
3. 一段代码在 n = 1000 时用了 1 秒，n = 2000 时用了 4 秒，n = 4000 时用了 16 秒。它大概是什么复杂度？n = 10⁵ 需要多久？

---

# 11 小结

1. 大 O 描述的是**增长趋势**，忽略常数与低阶项；工程中常数依然重要，但选型先看阶。
2. 常见复杂度阶梯：1 < log n < n < n log n < n² < n³ < 2ⁿ < n!。
3. **拿到题先看 n 的范围**，反推允许的复杂度，再选算法。
4. Python 中 `list.pop(0)`、`x in list`、循环 `str +=` 是三大经典 TLE 来源，分别用 `deque`、`set`、`join` 替代。
5. 均摊分析解释了 `list.append` 为何算 O(1)。

**下周预告**：第一个真正的数据结构——**栈**，以及它在括号匹配、表达式求值中的应用。
