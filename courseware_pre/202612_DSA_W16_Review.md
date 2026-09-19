# 第16周 课程总结与复习：知识体系梳理、经典算法回顾、考试要点

*Updated 2026-08-30 14:40 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 16 周 / 3 学时
> **教学内容**：课程总结与复习：知识体系梳理；经典算法回顾；考试要点讲解
> **教学要求**：系统梳理知识结构；掌握重点算法与数据结构

**本讲目标**：把 15 周的零散知识连成一张网；给出一套可直接背诵的**模板代码库**；讲清第 17 周上机考试的形式、策略与常见失分点。

---

# 1 知识体系总图

```
                        数据结构与算法（CS201）
                                 |
    +----------------+-----------+-----------+----------------+
    |                |                       |                |
  基础工具         线性结构                非线性结构        算法策略
    |                |                       |                |
  W2 ADT/OOP      W4 栈                  W9  树/遍历       W6 递归/分治/排序
  W3 复杂度       W5 队列/双端队列        W10 堆/BST        W7 贪心/DP
                  W5 链表                 W11 AVL/并查集    W8 DFS/BFS/回溯
                                          W12 图/遍历
                                          W13 最短路
                                          W14 MST/拓扑排序
                                          W15 散列表/KMP/倒排索引
```

## 1.1 一句话回顾每一周

| 周 | 一句话 | 最该记住的 |
| -- | ---- | ---- |
| W2 | ADT 分离接口与实现 | `list`/`dict`/`set` 的复杂度差异 |
| W3 | 大 O 描述增长趋势 | **看数据范围反推算法** |
| W4 | 栈是 LIFO | 括号匹配、调度场、**单调栈** |
| W5 | 队列是 FIFO | `deque`、**单调队列**、链表哨兵 |
| W6 | 分治与排序 | 归并求逆序对、快排随机化、**用内建 sorted** |
| W7 | 贪心要证明，DP 要状态 | 背包正序/倒序、LIS O(n log n) |
| W8 | 搜索是遍历解空间树 | **入队时标记 visited**、回溯三步 |
| W9 | 树的算法都是递归 | 前中后序、前序+中序建树 |
| W10 | 堆是完全二叉树+堆序 | `heapq`、Top-K、对顶堆 |
| W11 | 平衡与分组 | AVL 四种旋转、**并查集模板** |
| W12 | 图 = 建模 | 邻接表、连通分量、二分图染色 |
| W13 | 松弛是共同原子操作 | **Dijkstra 堆优化模板** |
| W14 | 割性质与拓扑序 | Kruskal = 排序 + 并查集、**Kahn 算法** |
| W15 | 哈希与匹配 | KMP 的 next 数组、倒排索引 |

---

# 2 复杂度速查表（必背）

## 2.1 数据结构操作复杂度

| 结构 | 查找 | 插入 | 删除 | 有序遍历 | 备注 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 数组 / `list` | O(n) / O(1) 按下标 | 尾 O(1)，中 O(n) | 尾 O(1)，中 O(n) | 需先排序 | 随机访问强 |
| 单链表 | O(n) | 已知位置 O(1) | 已知位置 O(1) | O(n) | 无随机访问 |
| 栈 / 队列 | — | O(1) | O(1) | — | `list` / `deque` |
| **哈希表** | **O(1)** 平均 | O(1) | O(1) | ❌ 无序 | 最坏 O(n) |
| **二叉堆** | O(n)（任意元素） | O(log n) | O(log n) 仅堆顶 | ❌ | 建堆 O(n) |
| BST（平均） | O(log n) | O(log n) | O(log n) | ✅ O(n) 中序 | 最坏退化 O(n) |
| **AVL / 红黑树** | **O(log n)** | O(log n) | O(log n) | ✅ | 高度有保证 |
| **并查集** | **O(α)≈O(1)** | O(α) | ❌ 不支持 | ❌ | 只答"是否同组" |
| Trie | O(L) | O(L) | O(L) | ✅ 按字典序 | L 为串长 |

## 2.2 算法复杂度

| 算法 | 时间 | 空间 | 前提 |
| ---- | ---- | ---- | ---- |
| 二分查找 | O(log n) | O(1) | 有序 |
| 归并 / 堆排 | O(n log n) | O(n) / O(1) | — |
| 快排 | 平均 O(n log n)，最坏 O(n²) | O(log n) | 建议随机化 |
| 快速选择 | 平均 O(n) | O(1) | 求第 k 小 |
| DFS / BFS | O(V+E) | O(V) | — |
| Dijkstra（堆） | O(E log V) | O(V) | **非负权** |
| Bellman-Ford | O(VE) | O(V) | 可负权、检测负环 |
| Floyd | O(V³) | O(V²) | V ≤ 400 |
| Prim（堆） | O(E log V) | O(V) | 连通无向图 |
| Kruskal | O(E log E) | O(V) | 可处理森林 |
| 拓扑排序 | O(V+E) | O(V) | **DAG** |
| KMP | O(n+m) | O(m) | — |
| 01 背包 | O(nC) | O(C) | — |

## 2.3 数据规模 → 算法选择（考场第一步）

| n | 允许复杂度 | 典型算法 |
| ---- | ---- | ---- |
| ≤ 12 | O(n!) | 全排列枚举 |
| ≤ 20 | O(2ⁿ) | 状压 DP、子集枚举 |
| ≤ 100 | O(n³) | Floyd、区间 DP |
| ≤ 1000 | O(n²) | 二维 DP、朴素图算法 |
| ≤ 10⁵ | O(n log n) | 排序、堆、二分、Dijkstra |
| ≤ 10⁶ | O(n) | 双指针、前缀和、单调栈/队列 |
| ≥ 10⁸ | O(log n) / O(1) | 数学公式、快速幂 |

---

# 3 必背模板代码库

> **考试前把这一节手抄一遍**。上机考试禁止使用 AI 工具，这些模板必须能默写。

## 3.1 快速输入输出

```python
import sys

data = sys.stdin.read().split()
p = 0
n = int(data[p]); p += 1

out = []
# ... out.append(str(ans))
sys.stdout.write('\n'.join(out) + '\n')

sys.setrecursionlimit(1 << 20)
```

## 3.2 二分查找与二分答案

```python
import bisect

i = bisect.bisect_left(a, x)      # 第一个 >= x
j = bisect.bisect_right(a, x)     # 第一个 > x


def binary_answer(lo, hi, check):
    """求满足 check 的最小值。check 需单调（False...False True...True）。"""
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

## 3.3 单调栈 / 单调队列

```python
def next_greater(a):
    """每个元素右边第一个更大元素的下标，无则 -1。"""
    n = len(a)
    res = [-1] * n
    stack = []
    for i, v in enumerate(a):
        while stack and a[stack[-1]] < v:
            res[stack.pop()] = i
        stack.append(i)
    return res


from collections import deque


def sliding_max(a, k):
    dq, res = deque(), []
    for i, v in enumerate(a):
        while dq and a[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(a[dq[0]])
    return res
```

## 3.4 并查集

```python
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n
        self.count = n

    def find(self, x):
        r = x
        while self.p[r] != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.sz[rx] < self.sz[ry]:
            rx, ry = ry, rx
        self.p[ry] = rx
        self.sz[rx] += self.sz[ry]
        self.count -= 1
        return True
```

## 3.5 Dijkstra

```python
import heapq


def dijkstra(graph, n, src):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

## 3.6 拓扑排序（Kahn）

```python
from collections import deque


def topo(graph, n):
    indeg = [0] * n
    for u in range(n):
        for v in graph[u]:
            indeg[v] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else None
```

## 3.7 Kruskal

```python
def kruskal(edges, n):
    """edges = [(w, u, v), ...]"""
    edges.sort()
    dsu = DSU(n)
    total, cnt = 0, 0
    for w, u, v in edges:
        if dsu.union(u, v):
            total += w
            cnt += 1
            if cnt == n - 1:
                break
    return total if cnt == n - 1 else -1
```

## 3.8 网格 BFS / DFS

```python
from collections import deque

DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def grid_bfs(grid, sr, sc):
    m, n = len(grid), len(grid[0])
    dist = [[-1] * n for _ in range(m)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        i, j = q.popleft()
        for di, dj in DIRS4:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and dist[ni][nj] < 0 \
                    and grid[ni][nj] != '#':
                dist[ni][nj] = dist[i][j] + 1
                q.append((ni, nj))
    return dist
```

## 3.9 回溯

```python
def backtrack(nums):
    res, path, used = [], [], [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, v in enumerate(nums):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue                    # 去重（需先排序）
            used[i] = True
            path.append(v)
            dfs()
            path.pop()
            used[i] = False

    nums.sort()
    dfs()
    return res
```

## 3.10 背包

```python
# 01 背包：容量倒序
dp = [0] * (C + 1)
for i in range(n):
    for c in range(C, w[i] - 1, -1):
        dp[c] = max(dp[c], dp[c - w[i]] + v[i])

# 完全背包：容量正序
for i in range(n):
    for c in range(w[i], C + 1):
        dp[c] = max(dp[c], dp[c - w[i]] + v[i])
```

## 3.11 KMP

```python
def build_next(p):
    nxt = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k > 0 and p[i] != p[k]:
            k = nxt[k - 1]
        if p[i] == p[k]:
            k += 1
        nxt[i] = k
    return nxt
```

## 3.12 二叉树遍历（迭代中序）

```python
def inorder(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        res.append(cur.val)
        cur = cur.right
    return res
```

---

# 4 常见题型 → 解法映射

| 题面关键词 | 首先想到 |
| ---- | ---- |
| "下一个更大/更小" | 单调栈 |
| "滑动窗口最大值" | 单调队列 |
| "第 K 大/小" | 堆 / 快速选择 |
| "中位数（数据流）" | 对顶堆 |
| "最短步数""最少操作" + 边权为 1 | BFS |
| "最短路径" + 带权非负 | Dijkstra |
| "所有点对最短路" + n ≤ 400 | Floyd |
| "最小代价连通所有点" | MST（Prim / Kruskal） |
| "是否同一组""合并集合" | 并查集 |
| "先修课""依赖顺序" | 拓扑排序 |
| "所有方案""排列组合" | 回溯 |
| "方案数""最值" + 选择互相制约 | DP |
| "区间不重叠""最多安排几个" | 贪心（按右端点排序） |
| "子串匹配""循环节" | KMP |
| "前缀""自动补全" | Trie |
| "去重""判存在" | set / dict |
| "区间和查询" | 前缀和 |
| "有序 + 找位置" | 二分 / bisect |
| "最大化最小值""最小化最大值" | 二分答案 |

---

# 5 上机考试要点

## 5.1 考试形式

| 项目 | 说明 |
| ---- | ---- |
| 时长 | **120 分钟** |
| 题量 | **6 道**算法编程题 |
| 平台 | OJ 在线评测 |
| 语言 | Python 3（支持 C++） |
| 占比 | 总评 **60%** |
| 工具 | ⚠️ **禁止使用任何 AI 工具**；无法解释自己提交的代码按学术不端处理 |

## 5.2 时间分配建议

```
0–10 min    通读全部 6 题，按预估难度排序，标出"必拿分"的题
10–40 min   拿下 2–3 道简单题（模拟、排序、哈希、基础 DP）
40–90 min   攻中等题（图论、DP、树、搜索）
90–110 min  攻最后 1–2 题；若无思路，回头检查已提交题的边界情况
110–120 min 检查输出格式、多组数据、边界（n=0/1）
```

**关键策略**：
1. **先易后难**。绝不要在第 1 题上耗 40 分钟。
2. **看数据范围定算法**（第 2.3 节的表），避免写出注定 TLE 的代码。
3. **先写能过样例的暴力**，再优化——有分总比 0 分好（部分 OJ 有分档数据）。
4. 卡住超过 **15 分钟**没有实质进展，果断换题。

## 5.3 高频失分点清单

| 失分点 | 对策 |
| ---- | ---- |
| **多组数据没循环读** | 看清"直到 EOF"或"读到 0 0 结束" |
| **输出格式**（大小写、空格、换行、`Case #x:`） | 逐字对照样例输出 |
| **浮点输出精度** | 用 `f"{x:.2f}"`，别用 `round` |
| **下标 0-based / 1-based 混淆** | 建图统一开 `n+1` 大小 |
| **`list.pop(0)` 做 BFS** | 一律用 `deque.popleft()` |
| **`x in list` 判存在** | 改用 `set` |
| **循环里 `str +=`** | 改用 `''.join` |
| **递归爆栈** | `sys.setrecursionlimit(1 << 20)` |
| **Dijkstra 用在负权图** | 改用 Bellman-Ford / SPFA |
| **01 背包写成正序** | 记住"01 倒序、完全正序" |
| **BFS 出队时才标记 visited** | 入队时立即标记 |
| **忘记 `n=0`/空输入的边界** | 提交前先想极端情况 |
| **`[[0]*m]*n` 建二维数组** | 用 `[[0]*m for _ in range(n)]` |
| **大量输出逐行 print** | 攒进列表最后 `'\n'.join` 一次输出 |

## 5.4 Python 超时的自救清单

按性价比排序：

1. `input()` → `sys.stdin.read().split()`
2. `list.pop(0)` → `deque.popleft()`
3. `x in list` → `x in set`
4. 循环拼接字符串 → `''.join`
5. 手写排序 → 内建 `sorted`
6. 递归 → 迭代 + 显式栈
7. 二维 `list` 索引频繁 → 展平成一维，或提前 `row = g[i]` 缓存
8. 反复 `max()/min()` 调用 → 直接写比较
9. 仍超时 → 检查复杂度是不是选错了算法（这才是根因）

## 5.5 建议的考前 7 天计划

| 天 | 内容 |
| -- | ---- |
| D-7 | 默写第 3 节全部模板，不看讲义 |
| D-6 | 重刷线性结构 + 排序（W4–W6）错题 |
| D-5 | 重刷 DP + 贪心（W7）错题，背包再过一遍 |
| D-4 | 重刷搜索（W8）：BFS/DFS/回溯各 3 题 |
| D-3 | 重刷树与堆（W9–W11） |
| D-2 | 重刷图论（W12–W14）：Dijkstra、MST、拓扑各 2 题 |
| D-1 | **限时模拟**：随机 6 题，严格计时 120 分钟 |
| D-0 | 只看模板与失分点清单，不做新题，早睡 |

---

# 6 综合复习题（课堂讲评）

## 6.1 判断题（考查概念）

1. 堆是完全二叉树，因此中序遍历有序。（❌ 堆只保证父子有序）
2. 快速排序的最坏时间复杂度是 O(n log n)。（❌ 是 O(n²)）
3. Dijkstra 算法可以处理有负权边但无负环的图。（❌ 不能）
4. 一棵有 n 个结点的二叉树，其高度最小为 ⌊log₂n⌋+1。（✅）
5. 并查集可以高效支持删除某条边。（❌ 不支持）
6. 若无向图有 n 个顶点且边数 ≥ n，则一定存在环。（✅）
7. 前序遍历序列可以唯一确定一棵二叉树。（❌ 需配合中序或空标记）
8. 拓扑排序的结果一定唯一。（❌ 一般不唯一）
9. Timsort 是稳定排序。（✅）
10. AVL 树删除结点最多需要一次旋转。（❌ 可能 O(log n) 次）

## 6.2 综合编程题（课堂现场演练）

**题 A（图 + 堆）**：给定 n 个城市 m 条带权道路，求从城市 1 到城市 n 的最短距离；若不可达输出 −1。
→ Dijkstra 模板题，注意重边与自环。

**题 B（树 + DP）**：给定一棵二叉树，求不相邻结点的最大权值和（树上打家劫舍）。
→ 树形 DP，每个结点返回 `(选它的最优, 不选它的最优)`。

```python
def rob_tree(root):
    def dfs(node):
        if not node:
            return 0, 0                # (选, 不选)
        l_take, l_skip = dfs(node.left)
        r_take, r_skip = dfs(node.right)
        take = node.val + l_skip + r_skip
        skip = max(l_take, l_skip) + max(r_take, r_skip)
        return take, skip
    return max(dfs(root))
```

**题 C（并查集 + 排序）**：n 个点 m 条边，每条边有权值，求使全图连通的最小总代价；若无法连通输出 `impossible`。
→ Kruskal 模板题。

**题 D（字符串 + 哈希）**：给定若干字符串，求出现次数最多的前缀。
→ Trie 或字典计数。

**题 E（DP）**：01 背包变形——每个物品有重量、价值和"必须在某物品之后取"的依赖。
→ 依赖背包 / 拓扑序 + 背包。

**题 F（模拟 + 数据结构）**：模拟一个任务调度器，支持添加任务（带优先级）、取出最高优先级任务、取消任务。
→ 堆 + 惰性删除（或哈希标记）。

---

# 7 本周作业

**综合模拟**：

1. 完成一套限时 120 分钟的 6 题模拟卷（题目由课程组发布）。
2. 默写第 3 节的 12 个模板，交手写扫描件或代码文件。
3. 整理个人**错题本**：列出本学期所有 WA/TLE 的题目、错因分类、正确做法。

**思考题**：

1. 用一张图把本课程所有数据结构按"逻辑结构—存储结构—典型操作复杂度"三个维度组织起来。
2. 举出 3 个"同一个问题、多种数据结构都能解"的例子（如岛屿数量：DFS / BFS / 并查集），比较优劣。
3. 从 RAG 系统（第 15 周）出发，列举它用到了本课程哪些数据结构，并说明各自的作用。

---

# 8 小结与寄语

1. 本课程的主线是：**用什么结构存 → 用什么策略算 → 复杂度是多少 → 能不能过题**。
2. 数据结构的价值在于**用空间换时间**、**在修改时顺手维护额外信息**，从而让查询变快。
3. 算法策略的四大范式：**分治、贪心、动态规划、搜索**——它们的边界由问题的性质（子问题是否重叠、是否有贪心选择性质）决定。
4. 会写代码不等于会算法；**会分析复杂度、会选择结构**才是这门课要培养的能力。
5. 上机考试考的不是记忆力，而是**在压力下把已知模板准确、快速地组合起来**的能力。

> 数据结构与算法是计算机科学的骨架，也是现代 AI 系统的地基。你们在这门课里手写的每一个堆、每一次 BFS、每一张倒排索引，都真实地运行在今天的搜索引擎与向量数据库里。祝考试顺利。

**下周**：第 17 周期末上机考试（见 [`202612_DSA_W17_Final_Machine_Exam.md`](202612_DSA_W17_Final_Machine_Exam.md)）。
