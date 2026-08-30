# 第7周 贪心与动态规划

*Updated 2026-08-30 11:40 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 7 周 / 3 学时
> **教学内容**：贪心与动态规划
> **教学要求**：掌握贪心选择性质与最优子结构；掌握动态规划的状态定义与状态转移方程设计

**知识点**：贪心选择性质、最优子结构、交换论证、区间调度、最优子结构与重叠子问题、记忆化搜索 vs 递推、线性 DP、背包问题（01/完全/多重）、区间 DP、状态压缩 DP、滚动数组优化、DP 五步法。

---

# 1 算法设计范式全景

| 范式 | 核心思想 | 何时适用 | 本课程位置 |
| ---- | ---- | ---- | ---- |
| 枚举/暴力 | 遍历所有可能 | 规模极小 | W3 |
| 分治 | 分解为独立子问题 | 子问题不重叠 | W6 |
| **贪心** | 每步取局部最优 | 有贪心选择性质 | W7 |
| **动态规划** | 记录并复用子问题解 | 子问题**重叠** + 最优子结构 | W7 |
| 回溯/搜索 | 系统枚举 + 剪枝 | 解空间树 | W8 |

**分治 vs DP 的分水岭**：子问题是否**重叠**。归并排序的两半互不相干（分治）；斐波那契的 f(n-1) 与 f(n-2) 共享大量子问题（DP）。

---

# 2 贪心算法

## 2.1 两个前提

贪心算法在每一步做出**当前看起来最好**的选择，且**不回溯**。它正确的两个条件：

1. **贪心选择性质**：全局最优解可以通过一系列局部最优选择达到。
2. **最优子结构**：做出一次贪心选择后，剩下的子问题的最优解与该选择组合，仍是原问题的最优解。

⚠️ **贪心不总是对的**。硬币面额 {1, 3, 4} 凑 6：贪心取 4+1+1 = 3 枚，最优是 3+3 = 2 枚。贪心的正确性**必须证明**（常用交换论证 exchange argument）。

## 2.2 经典问题一：区间调度（活动选择）

**LeetCode 435. 无重叠区间**，https://leetcode.cn/problems/non-overlapping-intervals/

> 给定若干区间，求最少删除多少个使其余互不重叠。

**贪心策略：按右端点升序排序，每次选右端点最小且不冲突的区间。**

```python
def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])       # 按结束时间排序
    count, end = 1, intervals[0][1]
    for s, e in intervals[1:]:
        if s >= end:                          # 不重叠，选它
            count += 1
            end = e
    return len(intervals) - count
```

**正确性（交换论证）**：设最优解的第一个区间是 X，我们选的是右端点最小的 A。把 X 换成 A，因为 A 的右端点 ≤ X 的右端点，后面能选的区间只多不少，所以换完仍是最优解。归纳可得贪心最优。

> **反例警示**：若按**左端点**或**区间长度**排序，都能构造出反例。区间问题的排序键选择是考点。

## 2.3 经典问题二：区间合并

**LeetCode 56. 合并区间**，https://leetcode.cn/problems/merge-intervals/

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])       # 这里按左端点
    res = []
    for s, e in intervals:
        if res and s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)  # 有交集，合并
        else:
            res.append([s, e])
    return res
```

## 2.4 经典问题三：跳跃游戏

**LeetCode 55 / 45**，https://leetcode.cn/problems/jump-game/

```python
def can_jump(nums):
    reach = 0
    for i, v in enumerate(nums):
        if i > reach:
            return False          # 到不了 i
        reach = max(reach, i + v)
    return True


def jump(nums):                   # LC 45：最少跳跃次数
    steps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:              # 到达当前这一跳的边界
            steps += 1
            end = far
    return steps
```

## 2.5 经典问题四：分发饼干 / 田忌赛马式配对

**LeetCode 455. 分发饼干**，https://leetcode.cn/problems/assign-cookies/

```python
def find_content_children(g, s):
    g.sort(); s.sort()
    i = j = 0
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:          # 用最小的能满足的饼干喂胃口最小的孩子
            i += 1
        j += 1
    return i
```

## 2.6 经典问题五：Huffman 编码（堆 + 贪心）

**OJ 22161: 哈夫曼编码树**（第 10 周会再讲堆）

> 每次取权值最小的两个结点合并，合并代价为二者之和，求总代价最小。

```python
import heapq


def huffman_cost(weights):
    heapq.heapify(weights)
    total = 0
    while len(weights) > 1:
        a = heapq.heappop(weights)
        b = heapq.heappop(weights)
        total += a + b
        heapq.heappush(weights, a + b)
    return total
```

**相关**：OJ 18164 剪绳子 / LC 1046 最后一块石头的重量。

## 2.7 贪心的证明思路

1. **交换论证**：假设存在最优解与贪心解不同，找到第一个分歧点，说明把最优解改成贪心的选择不会更差。
2. **数学归纳**：证明"前 k 步贪心选择可以扩展为最优解"。
3. **反证法**：假设贪心不是最优，推出矛盾。

考试中若时间紧，至少要能**举出反例说明某贪心策略错误**。

---

# 3 动态规划

## 3.1 两个必要条件

1. **最优子结构**：原问题的最优解包含子问题的最优解。
2. **重叠子问题**：递归求解时同一子问题被反复计算。

## 3.2 DP 五步法（解题模板）

1. **确定状态**：`dp[i]` 或 `dp[i][j]` 表示什么？（这是最难也最关键的一步）
2. **写出转移方程**：`dp[i]` 如何由更小的状态得到？
3. **确定初始条件与边界**。
4. **确定计算顺序**：保证用到的状态都已算出。
5. **确定答案位置**，并考虑空间优化。

## 3.3 记忆化搜索 vs 递推

同一个 DP 有两种写法：

```python
from functools import lru_cache

# 自顶向下：记忆化搜索，思路直观，只算用到的状态
@lru_cache(maxsize=None)
def f(n):
    if n < 2:
        return n
    return f(n - 1) + f(n - 2)


# 自底向上：递推，无递归开销，便于滚动数组优化
def fib(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```

| | 记忆化搜索 | 递推 |
| ---- | ---- | ---- |
| 思维难度 | 低（照着递归写） | 中（要想清顺序） |
| 常数 | 大（函数调用） | 小 |
| 栈深 | 可能爆栈 | 无风险 |
| 状态稀疏时 | **占优**（只算需要的） | 全算 |

---

# 4 线性 DP

## 4.1 爬楼梯 / 斐波那契族

**LeetCode 70**，https://leetcode.cn/problems/climbing-stairs/

- 状态：`dp[i]` = 爬到第 i 阶的方法数
- 转移：`dp[i] = dp[i-1] + dp[i-2]`
- 边界：`dp[0]=1, dp[1]=1`

```python
def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```

## 4.2 打家劫舍

**LeetCode 198**，https://leetcode.cn/problems/house-robber/

- 状态：`dp[i]` = 前 i 家能偷到的最大金额
- 转移：`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`（不偷第 i 家 / 偷）

```python
def rob(nums):
    prev, cur = 0, 0
    for v in nums:
        prev, cur = cur, max(cur, prev + v)
    return cur
```

## 4.3 最长上升子序列（LIS）

**LeetCode 300**，https://leetcode.cn/problems/longest-increasing-subsequence/

**O(n²) 版本**：

- 状态：`dp[i]` = 以 `nums[i]` **结尾**的 LIS 长度
- 转移：`dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])`

```python
def length_of_lis_n2(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if dp else 0
```

**O(n log n) 版本**（贪心 + 二分，重要）：

维护 `tails[k]` = 长度为 k+1 的上升子序列的**最小可能结尾**。`tails` 必然严格递增，可二分。

```python
import bisect


def length_of_lis(nums):
    tails = []
    for v in nums:
        i = bisect.bisect_left(tails, v)     # 严格上升用 bisect_left
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
    return len(tails)
```

> ⚠️ `tails` **不是** LIS 本身，只是长度正确。求非严格上升（允许相等）时改用 `bisect_right`。

## 4.4 最长公共子序列（LCS）

**LeetCode 1143**，https://leetcode.cn/problems/longest-common-subsequence/

- 状态：`dp[i][j]` = `s1[:i]` 与 `s2[:j]` 的 LCS 长度
- 转移：
  - `s1[i-1] == s2[j-1]` → `dp[i][j] = dp[i-1][j-1] + 1`
  - 否则 → `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

**滚动数组优化到 O(n) 空间**：

```python
def lcs_rolling(s1, s2):
    prev = [0] * (len(s2) + 1)
    for c1 in s1:
        cur = [0] * (len(s2) + 1)
        for j, c2 in enumerate(s2, 1):
            cur[j] = prev[j - 1] + 1 if c1 == c2 else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]
```

## 4.5 编辑距离

**LeetCode 72**，https://leetcode.cn/problems/edit-distance/

`dp[i][j]` = 把 `s1[:i]` 变成 `s2[:j]` 的最少操作数。

```python
def min_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                # 全删
    for j in range(n + 1):
        dp[0][j] = j                # 全插
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # 删除
                                   dp[i][j - 1],      # 插入
                                   dp[i - 1][j - 1])  # 替换
    return dp[m][n]
```

---

# 5 背包问题

## 5.1 01 背包

> n 件物品，第 i 件重 w[i] 价值 v[i]，每件**最多取一次**，背包容量 C，求最大价值。

**二维版本**（便于理解）：

```python
def knapsack01_2d(w, v, C):
    n = len(w)
    dp = [[0] * (C + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for c in range(C + 1):
            dp[i][c] = dp[i - 1][c]                       # 不取第 i 件
            if c >= w[i - 1]:
                dp[i][c] = max(dp[i][c],
                               dp[i - 1][c - w[i - 1]] + v[i - 1])   # 取
    return dp[n][C]
```

**一维滚动版本**（必须掌握，注意**容量倒序**）：

```python
def knapsack01(w, v, C):
    dp = [0] * (C + 1)
    for i in range(len(w)):
        for c in range(C, w[i] - 1, -1):     # ⚠️ 倒序！
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])
    return dp[C]
```

> **为什么倒序？** 正序时 `dp[c - w[i]]` 已经是"本轮更新过"的值，等于允许第 i 件物品被取多次——那就变成完全背包了。倒序保证 `dp[c-w[i]]` 还是上一轮（第 i-1 件）的状态。

## 5.2 完全背包

每件物品可取**无限次**——把内层循环改成**正序**即可：

```python
def knapsack_complete(w, v, C):
    dp = [0] * (C + 1)
    for i in range(len(w)):
        for c in range(w[i], C + 1):         # ✅ 正序
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])
    return dp[C]
```

**LeetCode 322. 零钱兑换**（完全背包求最小件数）：

```python
def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for c in coins:
        for x in range(c, amount + 1):
            dp[x] = min(dp[x], dp[x - c] + 1)
    return -1 if dp[amount] == INF else dp[amount]
```

**LeetCode 518. 零钱兑换 II**（求方案数，注意循环顺序决定组合/排列）：

```python
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:              # 外层物品 -> 组合数（不计顺序）
        for x in range(c, amount + 1):
            dp[x] += dp[x - c]
    return dp[amount]


def combination_sum4(nums, target):     # LC 377：外层容量 -> 排列数（计顺序）
    dp = [1] + [0] * target
    for x in range(1, target + 1):
        for v in nums:
            if v <= x:
                dp[x] += dp[x - v]
    return dp[target]
```

> **口诀**：01 背包倒序，完全背包正序；求组合数外层物品，求排列数外层容量。

## 5.3 多重背包（每件有限个）

朴素做法把 k 件拆成 k 个 01 物品；**二进制拆分**把 k 件拆成 1,2,4,…，只需 O(log k) 个：

```python
def knapsack_multiple(w, v, cnt, C):
    dp = [0] * (C + 1)
    for wi, vi, k in zip(w, v, cnt):
        power = 1
        while k > 0:
            take = min(power, k)
            ww, vv = wi * take, vi * take
            for c in range(C, ww - 1, -1):
                dp[c] = max(dp[c], dp[c - ww] + vv)
            k -= take
            power *= 2
    return dp[C]
```

## 5.4 背包问题变形速查

| 题型 | 转移 | 初始化 |
| ---- | ---- | ---- |
| 最大价值 | `dp[c] = max(dp[c], dp[c-w]+v)` | 全 0（容量可不装满）/ `dp[0]=0` 其余 -inf（必须装满） |
| 恰好装满判定 | `dp[c] \|= dp[c-w]` | `dp[0]=True` |
| 方案数 | `dp[c] += dp[c-w]` | `dp[0]=1` |
| 最少件数 | `dp[c] = min(dp[c], dp[c-w]+1)` | `dp[0]=0` 其余 inf |

**LeetCode 416. 分割等和子集**是"恰好装满判定"的模板题：

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for v in nums:
        for c in range(target, v - 1, -1):
            dp[c] = dp[c] or dp[c - v]
    return dp[target]
```

---

# 6 二维与区间 DP

## 6.1 路径类

**LeetCode 62. 不同路径 / 64. 最小路径和**

```python
def min_path_sum(grid):
    """只能向右/向下走，求左上到右下的最小路径和。滚动数组 O(n) 空间。"""
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                dp[j] = grid[0][0]
            elif i == 0:
                dp[j] = dp[j - 1] + grid[i][j]          # 只能从左边来
            elif j == 0:
                dp[j] = dp[j] + grid[i][j]              # 只能从上面来
            else:
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]   # dp[j] 是上方，dp[j-1] 是左方
    return dp[-1]
```

## 6.2 区间 DP：最长回文子串 / 石子合并

**LeetCode 5. 最长回文子串**

- 状态：`dp[i][j]` = `s[i..j]` 是否回文
- 转移：`dp[i][j] = (s[i]==s[j]) and (j-i<2 or dp[i+1][j-1])`
- 顺序：**按区间长度从小到大**

```python
def longest_palindrome(s):
    n = len(s)
    if n < 2:
        return s
    dp = [[False] * n for _ in range(n)]
    start, best = 0, 1
    for i in range(n):
        dp[i][i] = True
    for length in range(2, n + 1):              # 区间长度递增
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] != s[j]:
                continue
            if length == 2 or dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > best:
                    start, best = i, length
    return s[start:start + best]
```

**石子合并**（OJ 经典）：`dp[i][j] = min(dp[i][k] + dp[k+1][j]) + sum(i..j)`，O(n³)。

---

# 7 贪心 vs DP：如何选择

| 判据 | 贪心 | DP |
| ---- | ---- | ---- |
| 是否需要回头考虑其他选择 | 否 | 是 |
| 复杂度 | 通常 O(n log n)（含排序） | 状态数 × 转移代价 |
| 正确性 | 需证明 | 状态定义正确即可 |
| 典型信号 | "最少/最多个数"且有明显排序依据 | "方案数""最值"且选择互相制约 |

**同一问题的对比**：

- 零钱兑换，面额 {1,5,10,25}：贪心正确。
- 零钱兑换，面额 {1,3,4}：贪心错误，必须 DP。

> **考场判断法**：先想贪心，**立刻尝试构造反例**；构造不出且能给出交换论证就用贪心，否则老实写 DP。

---

# 8 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 无重叠区间 | LC 435 | 区间贪心 |
| 2 | 合并区间 | LC 56 | 排序 + 贪心 |
| 3 | 跳跃游戏 II | LC 45 | 贪心 |
| 4 | 爬楼梯 / 打家劫舍 | LC 70 / 198 | 线性 DP |
| 5 | 最长递增子序列 | LC 300 | LIS，O(n log n) |
| 6 | 最长公共子序列 | LC 1143 | 二维 DP |
| 7 | 编辑距离 | LC 72 | 二维 DP |
| 8 | 分割等和子集 | LC 416 | 01 背包 |
| 9 | 零钱兑换 | LC 322 | 完全背包 |
| 10（选做） | 最长回文子串 | LC 5 | 区间 DP |
| 11（选做） | 最后一块石头的重量 | LC 1046 | 堆 + 贪心 |

**思考题**：

1. 01 背包一维数组为什么必须倒序？画出 dp 数组的更新过程说明。
2. LC 518（组合数）与 LC 377（排列数）只差循环顺序，请解释每种顺序枚举出的是什么。
3. LIS 的 O(n log n) 解法中，`tails` 数组的含义是什么？为什么它一定严格递增？
4. 举一个"贪心看似正确但实际错误"的例子，并说明 DP 如何修正它。

---

# 9 小结

1. 贪心 = 局部最优 + 不回溯；**必须验证贪心选择性质**，最快的验证方式是找反例。
2. DP 的两个前提：最优子结构 + 重叠子问题；核心难点是**状态定义**。
3. DP 五步法：状态 → 转移 → 初始化 → 顺序 → 答案与优化。
4. 背包家族：01（倒序）、完全（正序）、多重（二进制拆分）；组合数 vs 排列数看循环顺序。
5. 滚动数组是最常用的空间优化，能把 O(nC) 降到 O(C)。

**下周预告**：**搜索专题**——DFS / BFS / 回溯与剪枝，把解空间当作一棵树来遍历。
