# 第6周 递归与分治；排序算法与性能对比

*Updated 2026-08-31 04:20 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 6 周 / 3 学时
> **教学内容**：递归与分治；排序：冒泡/选择/插入/归并/快排与性能对比
> **教学要求**：掌握递归思想；掌握分治策略在排序中的应用；能进行算法性能对比

**知识点**：递归三要素、递归树与调用栈、记忆化、汉诺塔、分治法框架、冒泡/选择/插入/希尔/归并/快速/堆排序、排序稳定性、逆序对、快速选择、Timsort、`sort` 与 `key`、原地排序与外部空间。

---

# 1 递归

## 1.1 递归三要素

1. **基线条件（base case）**：能直接求解的最小问题，必须存在，否则无限递归。
2. **递归条件（recursive case）**：把问题**规模缩小**后调用自身。
3. **收敛性**：每次调用都必须朝基线条件逼近。

```python
def factorial(n: int) -> int:
    if n <= 1:            # 基线条件
        return 1
    return n * factorial(n - 1)     # 递归条件，规模 n -> n-1
```

## 1.2 调用栈可视化

`factorial(4)` 的展开：

```
factorial(4)
 └ 4 * factorial(3)
        └ 3 * factorial(2)
               └ 2 * factorial(1)
                      └ 1              <- 基线，开始回溯
               <- 2*1 = 2
        <- 3*2 = 6
 <- 4*6 = 24
```

递归深度 = 栈帧数 = 空间复杂度 O(n)。

```python
import sys
sys.setrecursionlimit(1 << 20)      # OJ 深递归标配
```

## 1.3 递归的代价：重复子问题

```python
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)      # O(2^n) ！
```

`fib(5)` 的递归树中 `fib(2)` 被算了 3 次，`fib(3)` 被算了 2 次：

```
                fib(5)
            /            \
       fib(4)            fib(3)
      /     \           /     \
   fib(3)  fib(2)   fib(2)  fib(1)
   /   \    /  \     /  \
fib(2) f(1) f(1) f(0) f(1) f(0)
```

**记忆化（memoization）**把它降到 O(n)：

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

> 记忆化递归 = 自顶向下的动态规划（第 7 周）。

## 1.4 经典例题：汉诺塔

**OJ 04147: 汉诺塔问题(Tower of Hanoi)**，http://cs101.openjudge.cn/practice/04147/

> 有三根杆子 A、B、C，A 上有 N 个穿孔圆盘，尺寸由下到上依次变小。
> 按下列规则把所有圆盘移到 C：每次只移一个；大盘不能叠在小盘上面。
> 另见 LeetCode 面试题 08.06 汉诺塔问题，https://leetcode.cn/problems/hanota-lcci/

```python
def hanoi(n, src, aux, dst, moves):
    if n == 0:
        return
    hanoi(n - 1, src, dst, aux, moves)      # 上面 n-1 个挪到 aux
    moves.append((n, src, dst))             # 最大的挪到 dst
    hanoi(n - 1, aux, src, dst, moves)      # n-1 个从 aux 挪到 dst


n = int(input())
moves = []
hanoi(n, 'A', 'B', 'C', moves)
print(len(moves))                            # 2^n - 1
for k, s, d in moves:
    print(f"{k}:{s}->{d}")
```

递归式 T(n) = 2T(n-1) + 1 ⇒ T(n) = 2ⁿ − 1，**指数级不可避免**（因为输出本身就有 2ⁿ−1 行）。

## 1.5 其他递归练习

```python
def reverse_str(s):                   # 字符串反转
    return s if len(s) <= 1 else reverse_str(s[1:]) + s[0]


def gcd(a, b):                        # 欧几里得算法，O(log min(a,b))
    return a if b == 0 else gcd(b, a % b)


def power(a, n):                      # 快速幂，O(log n)
    if n == 0:
        return 1
    half = power(a, n // 2)
    return half * half if n % 2 == 0 else half * half * a


def sum_nested(lst):                  # 嵌套列表求和
    total = 0
    for x in lst:
        total += sum_nested(x) if isinstance(x, list) else x
    return total
```

---

# 2 分治法（Divide and Conquer）

## 2.1 三步框架

1. **Divide**：把原问题分成若干个规模更小、结构相同的子问题。
2. **Conquer**：递归求解子问题（小到一定程度直接求解）。
3. **Combine**：把子问题的解合并成原问题的解。

```
                 problem(n)
                /          \
        problem(n/2)     problem(n/2)      <- Divide
            |                 |
          solve             solve          <- Conquer
             \               /
              \             /
               combine  O(f(n))            <- Combine
```

复杂度递归式：**T(n) = a·T(n/b) + f(n)**。

| 递归式 | 解 | 算法 |
| ---- | ---- | ---- |
| T(n)=T(n/2)+O(1) | O(log n) | 二分查找 |
| T(n)=2T(n/2)+O(n) | O(n log n) | 归并排序 |
| T(n)=2T(n/2)+O(1) | O(n) | 求最大值/树的遍历 |
| T(n)=T(n/2)+O(n) | O(n) | 快速选择（平均） |

## 2.2 分治求最大子数组和

```python
def max_subarray(a, lo, hi):
    """分治版 LC 53，O(n log n)。"""
    if lo == hi:
        return a[lo]
    mid = (lo + hi) // 2
    left = max_subarray(a, lo, mid)          # 全在左半
    right = max_subarray(a, mid + 1, hi)     # 全在右半

    # 跨越中点：从 mid 向左、向右各取最大后缀/前缀
    s, best_l = 0, -float('inf')
    for i in range(mid, lo - 1, -1):
        s += a[i]
        best_l = max(best_l, s)
    s, best_r = 0, -float('inf')
    for i in range(mid + 1, hi + 1):
        s += a[i]
        best_r = max(best_r, s)

    return max(left, right, best_l + best_r)
```

（Kadane 的 O(n) 更优，但分治版展示了框架。）

---

# 3 五大排序算法

## 3.1 冒泡排序 O(n²)

相邻元素两两比较，大的往后"冒"。每轮把当前最大值送到末尾。

```python
def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:        # 优化：已有序则提前退出
            break
    return a
```

- 时间：最坏/平均 O(n²)，**最好 O(n)**（已有序，带提前退出）。
- 空间 O(1)，**稳定**。

## 3.2 选择排序 O(n²)

每轮选出剩余部分的最小值，放到已排序段末尾。

```python
def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a
```

- 时间恒为 O(n²)（比较次数与输入无关），交换次数只有 O(n)。
- 空间 O(1)，**不稳定**（长距离交换会打乱相等元素的相对次序）。

## 3.3 插入排序 O(n²)，近似有序时 O(n)

像整理扑克牌：把当前元素插入到前面已排好序的部分中的正确位置。

```python
def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]      # 后移腾位置
            j -= 1
        a[j + 1] = key
    return a
```

- 最好 O(n)（已有序），最坏/平均 O(n²)。
- 空间 O(1)，**稳定**。
- **小数组上常数极小**，是 Timsort、快排的小区间收尾手段。

## 3.4 希尔排序（插入排序的改进）

按增量 gap 分组做插入排序，gap 逐步缩小到 1。

```python
def shell_sort(a):
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            key, j = a[i], i - gap
            while j >= 0 and a[j] > key:
                a[j + gap] = a[j]
                j -= gap
            a[j + gap] = key
        gap //= 2
    return a
```

复杂度依赖增量序列，常见约 O(n^1.3)；**不稳定**。

## 3.5 归并排序 O(n log n)——分治的典范

```python
def merge_sort(a):
    """返回新列表，稳定，O(n log n) 时间，O(n) 额外空间。"""
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right)


def merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:      # <= 保证稳定性
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res
```

**原地（in-place）版本**，避免大量切片开销：

```python
def merge_sort_inplace(a, lo=0, hi=None, buf=None):
    if hi is None:
        hi, buf = len(a), [0] * len(a)
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    merge_sort_inplace(a, lo, mid, buf)
    merge_sort_inplace(a, mid, hi, buf)
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if a[i] <= a[j]:
            buf[k] = a[i]; i += 1
        else:
            buf[k] = a[j]; j += 1
        k += 1
    while i < mid:
        buf[k] = a[i]; i += 1; k += 1
    while j < hi:
        buf[k] = a[j]; j += 1; k += 1
    a[lo:hi] = buf[lo:hi]
```

### 归并的经典应用：求逆序对

**OJ 02299: Ultra-QuickSort**，http://cs101.openjudge.cn/practice/02299/

> 求把数组排成升序所需的最少相邻交换次数 = **逆序对个数**。

在归并时，若从右半取走一个元素，说明左半剩余的所有元素都与它构成逆序对：

```python
import sys


def sort_count(a):
    if len(a) <= 1:
        return a, 0
    mid = len(a) // 2
    left, cl = sort_count(a[:mid])
    right, cr = sort_count(a[mid:])
    merged, i, j, cnt = [], 0, 0, cl + cr
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            cnt += len(left) - i          # 关键一行
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, cnt


data = sys.stdin.read().split()
p = 0
out = []
while p < len(data):
    n = int(data[p]); p += 1
    if n == 0:
        break
    arr = [int(x) for x in data[p:p + n]]
    p += n
    out.append(str(sort_count(arr)[1]))
print('\n'.join(out))
```

## 3.6 快速排序 平均 O(n log n)

选一个**枢轴（pivot）**，把数组划分为"≤ pivot"与"> pivot"两部分，递归处理。

**教学版（简洁但非原地）**：

```python
def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    less = [x for x in a if x < pivot]
    equal = [x for x in a if x == pivot]
    greater = [x for x in a if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)
```

**原地 Lomuto 划分 + 随机枢轴（推荐掌握）**：

```python
import random


def quick_sort_inplace(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    while lo < hi:
        p = partition(a, lo, hi)
        # 尾递归优化：先递归较短的一侧，保证栈深 O(log n)
        if p - lo < hi - p:
            quick_sort_inplace(a, lo, p - 1)
            lo = p + 1
        else:
            quick_sort_inplace(a, p + 1, hi)
            hi = p - 1
    return a


def partition(a, lo, hi):
    r = random.randint(lo, hi)          # 随机化，规避有序数据的最坏情况
    a[r], a[hi] = a[hi], a[r]
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1
```

- 平均 O(n log n)，**最坏 O(n²)**（枢轴每次都取到极值，如已排序数组用固定枢轴）。
- 空间 O(log n)（递归栈），**不稳定**。
- **随机枢轴**或三数取中可让最坏情况几乎不出现。

### 快速选择：求第 k 小，平均 O(n)

**LeetCode 215. 数组中的第K个最大元素**，https://leetcode.cn/problems/kth-largest-element-in-an-array/

```python
def quick_select(a, k):
    """返回第 k 小（k 从 1 开始），平均 O(n)。"""
    lo, hi = 0, len(a) - 1
    while True:
        p = partition(a, lo, hi)
        if p == k - 1:
            return a[p]
        if p < k - 1:
            lo = p + 1
        else:
            hi = p - 1
```

只递归一侧，T(n) = T(n/2) + O(n) = O(n)。

## 3.7 堆排序（第 10 周详讲）

```python
import heapq


def heap_sort(a):
    h = a[:]
    heapq.heapify(h)                 # O(n) 建堆
    return [heapq.heappop(h) for _ in range(len(h))]     # n 次 O(log n)
```

---

# 4 排序算法性能对比

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定 | 备注 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 冒泡 | O(n) | O(n²) | O(n²) | O(1) | ✅ | 教学用 |
| 选择 | O(n²) | O(n²) | O(n²) | O(1) | ❌ | 交换次数最少 |
| 插入 | O(n) | O(n²) | O(n²) | O(1) | ✅ | 近似有序时极快 |
| 希尔 | O(n log n) | ~O(n^1.3) | O(n²) | O(1) | ❌ | 增量序列敏感 |
| **归并** | O(n log n) | O(n log n) | O(n log n) | **O(n)** | ✅ | 稳定、可外排、求逆序对 |
| **快排** | O(n log n) | O(n log n) | **O(n²)** | O(log n) | ❌ | 常数最小，实践最快 |
| 堆排 | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ | 最坏有保证，常数偏大 |

## 4.1 稳定性为什么重要

**稳定**：相等元素排序前后相对次序不变。

```python
students = [('Amy', 90), ('Bob', 85), ('Cindy', 90)]
# 先按名字排，再用稳定排序按分数排 -> 同分者仍按名字有序
students.sort(key=lambda s: s[0])
students.sort(key=lambda s: -s[1])     # Python 的 sort 是稳定的
```

**多关键字排序**依赖稳定性：按次关键字排完再按主关键字排即可。

## 4.2 Python 内建排序：Timsort

`list.sort()` / `sorted()` 使用 **Timsort**——归并排序 + 插入排序的混合体：

- 识别数据中已有序的"run"，近似有序的数据接近 O(n)。
- **稳定**，最坏 O(n log n)。
- 用 C 实现，常数远小于纯 Python 手写排序。

> **OJ 实战准则**：除非题目要求手写，**一律用 `sorted` / `.sort()`**。手写排序在 Python 里几乎必然更慢。

```python
a.sort()                                  # 原地，返回 None
b = sorted(a, reverse=True)               # 新列表
c = sorted(items, key=lambda x: (x[1], -x[0]))    # 多关键字
from functools import cmp_to_key
d = sorted(items, key=cmp_to_key(my_cmp))         # 自定义比较函数
```

## 4.3 性能对比实验

```python
import random, time
from typing import Callable


def bench(fn: Callable, data, repeat=1):
    a = data[:]
    t0 = time.perf_counter()
    for _ in range(repeat):
        fn(a[:])
    return (time.perf_counter() - t0) / repeat


for n in (1000, 2000, 4000, 8000):
    rnd = [random.randint(0, 10 ** 6) for _ in range(n)]
    srt = sorted(rnd)
    rev = srt[::-1]
    print(f"n={n}")
    for name, fn in [('bubble', bubble_sort), ('insertion', insertion_sort),
                     ('merge', merge_sort), ('quick', quick_sort_inplace),
                     ('builtin', sorted)]:
        print(f"  {name:10s} random={bench(fn, rnd):.4f}s  "
              f"sorted={bench(fn, srt):.4f}s  reversed={bench(fn, rev):.4f}s")
```

**需要观察并解释的现象**：

1. 插入排序在**已排序**数据上远快于随机数据（O(n) vs O(n²)）。
2. 冒泡排序在**逆序**数据上最慢。
3. 归并排序对三种输入耗时基本一致（复杂度与输入无关）。
4. 内建 `sorted` 在已排序数据上几乎是线性的（Timsort 的 run 检测）。
5. 未随机化的快排在已排序数据上会退化甚至爆栈。

---

# 5 例题精讲

## 5.1 数组中的第 K 个最大元素

三种做法及其复杂度：

```python
import heapq


def kth_largest_sort(nums, k):        # O(n log n)
    return sorted(nums, reverse=True)[k - 1]


def kth_largest_heap(nums, k):        # O(n log k)，适合数据流
    h = []
    for v in nums:
        heapq.heappush(h, v)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]


def kth_largest_quick(nums, k):       # 平均 O(n)
    return quick_select(nums[:], len(nums) - k + 1)
```

## 5.2 合并 K 个升序链表

**LeetCode 23**，https://leetcode.cn/problems/merge-k-sorted-lists/

**分治两两归并**：T(n) = 2T(n/2) + O(n) ⇒ **O(N log k)**（N 为总结点数）。

```python
def merge_k_lists(lists):
    if not lists:
        return None

    def merge2(a, b):
        dummy = tail = ListNode()
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next

    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            merged.append(merge2(lists[i],
                                 lists[i + 1] if i + 1 < len(lists) else None))
        lists = merged
    return lists[0]
```

若逐个归并则是 O(Nk)，慢得多。

## 5.3 颜色分类（三路划分）

**LeetCode 75. 颜色分类**，https://leetcode.cn/problems/sort-colors/

荷兰国旗问题——快排三路划分的核心：

```python
def sort_colors(nums):
    lo, i, hi = 0, 0, len(nums) - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1; i += 1
        elif nums[i] == 2:
            nums[hi], nums[i] = nums[i], nums[hi]
            hi -= 1                    # 换来的元素还没检查，i 不动
        else:
            i += 1
```

一趟 O(n)，原地 O(1)。**大量重复元素时，三路划分能显著加速快排。**

---

# 6 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 汉诺塔问题 | OJ 04147 | 递归 |
| 2 | Ultra-QuickSort | OJ 02299 | 归并求逆序对 |
| 3 | 数组中的第K个最大元素 | LC 215 | 快速选择 / 堆 |
| 4 | 合并K个升序链表 | LC 23 | 分治归并 |
| 5 | 颜色分类 | LC 75 | 三路划分 |
| 6 | 排序链表 | LC 148 | 链表归并排序 |
| 7 | 数组中的逆序对 | LC 面试题 51 | 归并 |
| 8（选做） | 最大子数组和（分治版） | LC 53 | 分治框架 |
| 9（选做） | 数组中的第 K 大（数据流） | LC 703 | 小根堆 |

**实验（第 3 次）**：完成 4.3 的性能对比实验，产出一份含图表的实验报告，回答 4.3 中列出的 5 个现象。

**思考题**：

1. 为什么基于比较的排序下界是 Ω(n log n)？（提示：决策树有 n! 个叶子，树高 ≥ log₂(n!) = Θ(n log n)）
2. 计数排序、基数排序为什么能达到 O(n)？它们的适用条件是什么？
3. 归并排序 `merge` 中把 `<=` 改成 `<`，稳定性会怎样？
4. 快排的 `partition` 若不随机化，对全部相同元素的数组会怎样？三路划分如何解决？

---

# 7 小结

1. 递归三要素：基线条件、递归条件、收敛；递归的空间代价是调用栈。
2. 重复子问题用**记忆化**消除——这是通向动态规划的桥梁。
3. 分治三步：Divide / Conquer / Combine；复杂度用递归式 T(n)=aT(n/b)+f(n) 分析。
4. **归并**稳定、复杂度有保证、可求逆序对；**快排**常数最小、需随机化。
5. 实战一律用内建 `sorted`（Timsort），手写排序仅用于理解原理与笔试。

**下周预告**：两大算法设计范式——**贪心**与**动态规划**。
