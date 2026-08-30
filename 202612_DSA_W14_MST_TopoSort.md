# 第14周 最小生成树（Prim、Kruskal）；拓扑排序（Kahn 算法）；DAG 应用

*Updated 2026-08-30 14:00 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 14 周 / 3 学时
> **教学内容**：最小生成树（Prim、Kruskal）；拓扑排序（Kahn 算法）；有向无环图的应用
> **教学要求**：掌握 MST 算法；理解拓扑排序的原理与实现

**知识点**：生成树与最小生成树、割性质（cut property）、环性质、Prim 算法（朴素 / 堆优化）、Kruskal 算法（排序 + 并查集）、MST 唯一性、瓶颈生成树、拓扑排序、Kahn 算法（BFS 入度法）、DFS 逆后序法、判环、DAG 上的 DP、关键路径（AOE 网）。

---

# 第一部分：最小生成树

# 1 概念

## 1.1 生成树与最小生成树

- **生成树（Spanning Tree）**：无向连通图 G 的一个**极小连通子图**，包含全部 n 个顶点和 **n−1 条边**，且无环。
- **最小生成树（MST）**：所有生成树中边权之和最小的那棵。

**应用**：铺设网络/管道的最低成本、聚类分析、图像分割、近似求解 TSP。

```
     图 G                     一棵 MST
   A --1-- B                A --1-- B
   |\      |                |       |
   4 \3    2       ==>      |       2
   |   \   |                |       |
   C --5-- D                C       D
                            \___3___/     总权 = 1+2+3 = 6
```

## 1.2 两条关键性质

**割性质（Cut Property）**：把顶点集任意划分为两部分 (S, V−S)，跨越这个割的所有边中，**权值最小的边一定属于某棵 MST**。

> 这是 Prim 和 Kruskal 都正确的根本原因。**证明（交换论证）**：设最小横切边 e 不在 MST T 中，把 e 加入 T 形成一个环，环中必有另一条横切边 f，且 w(f) ≥ w(e)。用 e 替换 f 得到的仍是生成树且权值不增。∎

**环性质（Cycle Property）**：任意环中权值**最大**的边一定**不在**某棵 MST 中（若该边唯一最大，则不在任何 MST 中）。

## 1.3 MST 的唯一性

若所有边权**互不相同**，MST **唯一**。若有相同权值的边，MST 可能不唯一，但**权值和唯一**。

---

# 2 Prim 算法

## 2.1 思想：从点出发生长

从任意一个顶点开始，每次把**离已选顶点集合最近的顶点**加入集合（贪心 + 割性质）。

> **与 Dijkstra 的区别**：Dijkstra 比较的是"从源点出发的总距离 `dist[u] + w`"，Prim 比较的是"到集合的单条边权 `w`"。代码几乎一样，只差一个加号。

## 2.2 堆优化实现（推荐）

```python
import heapq


def prim(graph, n, start=0):
    """graph[u] = [(v, w), ...]，返回 (MST 总权值, 边列表)。
    时间 O(E log V)。图不连通时返回 (-1, [])。"""
    visited = [False] * n
    pq = [(0, start, -1)]          # (边权, 到达的点, 来自的点)
    total, edges = 0, []

    while pq and len(edges) < n - 1:
        w, u, frm = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        if frm != -1:
            total += w
            edges.append((frm, u, w))
        for v, wt in graph[u]:
            if not visited[v]:
                heapq.heappush(pq, (wt, v, u))

    return (total, edges) if len(edges) == n - 1 else (-1, [])
```

## 2.3 朴素实现 O(V²)（稠密图更优）

```python
def prim_dense(matrix, n):
    """邻接矩阵版，适合稠密图（如完全图）。"""
    INF = float('inf')
    lowcost = [INF] * n           # lowcost[v] = v 到已选集合的最小边权
    lowcost[0] = 0
    visited = [False] * n
    total = 0

    for _ in range(n):
        u, best = -1, INF
        for i in range(n):
            if not visited[i] and lowcost[i] < best:
                u, best = i, lowcost[i]
        if u == -1:
            return -1              # 不连通
        visited[u] = True
        total += best
        for v in range(n):
            if not visited[v] and matrix[u][v] < lowcost[v]:
                lowcost[v] = matrix[u][v]      # ⚠️ 与 Dijkstra 的唯一区别
    return total
```

## 2.4 例题：Agri-Net

**OJ 01258: Agri-Net**，http://cs101.openjudge.cn/practice/01258/

> 给出 n 个农场之间的距离矩阵（完全图），求连通所有农场的最小光纤长度。

完全图 E = V²，用**朴素 Prim O(V²)** 最合适：

```python
import sys

data = sys.stdin.read().split()
p = 0
out = []
while p < len(data):
    n = int(data[p]); p += 1
    matrix = []
    for i in range(n):
        matrix.append([int(x) for x in data[p:p + n]])
        p += n
    out.append(str(prim_dense(matrix, n)))
print('\n'.join(out))
```

---

# 3 Kruskal 算法

## 3.1 思想：从边出发，并查集判环

把所有边按权值**升序排序**，依次考察：若这条边的两个端点**不在同一个连通块**，就选它（用并查集判断），否则丢弃（会形成环）。

## 3.2 实现（第 11 周并查集的第一个大应用）

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        return True


def kruskal(edges, n):
    """edges = [(w, u, v), ...]，返回 (总权值, MST 边列表)。
    时间 O(E log E)，瓶颈在排序。"""
    edges.sort()
    dsu = DSU(n)
    total, chosen = 0, []
    for w, u, v in edges:
        if dsu.union(u, v):            # 不成环则选它
            total += w
            chosen.append((u, v, w))
            if len(chosen) == n - 1:   # 已有 n-1 条边，提前结束
                break
    return (total, chosen) if len(chosen) == n - 1 else (-1, [])
```

## 3.3 例题：兔子与星空

**OJ 05442: 兔子与星空**，http://cs101.openjudge.cn/practice/05442/

> 顶点用大写字母表示，给出若干边，求 MST 权值和。

```python
n = int(input())
edges = []
for _ in range(n - 1):
    parts = input().split()
    u = ord(parts[0]) - ord('A')
    k = int(parts[1])
    for i in range(k):
        v = ord(parts[2 + 2 * i]) - ord('A')
        w = int(parts[3 + 2 * i])
        edges.append((w, u, v))

print(kruskal(edges, n)[0])
```

## 3.4 Prim vs Kruskal

| | Prim | Kruskal |
| ---- | ---- | ---- |
| 出发点 | 顶点 | 边 |
| 数据结构 | 优先队列 | 排序 + **并查集** |
| 复杂度 | O(E log V) / O(V²) | O(E log E) |
| 适合 | **稠密图**（用 O(V²) 版本） | **稀疏图** |
| 中间状态 | 始终是一棵树 | 是一片森林 |
| 处理不连通图 | 只能得到一个连通分量 | **天然得到最小生成森林** |

## 3.5 MST 的变形

**最大生成树**：边权取负后跑 Kruskal，或排序改为降序。

**瓶颈生成树**：使"最大边权最小"的生成树——**MST 就是瓶颈生成树**（由环性质保证）。所以第 13 周 5.3 的"最小化路径最大边权"问题，用 Kruskal 边加边、直到 src 与 dst 连通即可，答案就是最后加的那条边的权值：

```python
def bottleneck(edges, n, src, dst):
    edges.sort()
    dsu = DSU(n)
    for w, u, v in edges:
        dsu.union(u, v)
        if dsu.find(src) == dsu.find(dst):
            return w
    return -1
```

**次小生成树**、**最小度限制生成树**、**Steiner 树**属于竞赛内容，本课程了解即可。

---

# 第二部分：拓扑排序

# 4 概念

## 4.1 定义

**拓扑排序**：对**有向无环图（DAG）**的顶点排出一个线性序列，使得对每条有向边 u → v，u 都排在 v 前面。

**直观含义**：把"依赖关系"变成"可执行的顺序"。

```
    课程先修关系                拓扑序（不唯一）
    数学 --> 算法 --> AI       数学, 编程, 算法, 数据结构, AI
      \             /          编程, 数学, 算法, 数据结构, AI
    编程 --> 数据结构
```

## 4.2 存在性

- 有向图存在拓扑序 **⟺** 它是 DAG（无环）。
- 拓扑序**一般不唯一**；当且仅当每一步都恰有一个入度为 0 的点时唯一（即存在哈密顿路径）。

## 4.3 应用

课程安排、任务调度、编译依赖（Makefile）、电子表格重算顺序、软件包安装顺序、DAG 上的 DP。

---

# 5 Kahn 算法（BFS 入度法）

## 5.1 思想

1. 统计所有顶点的**入度**。
2. 把入度为 0 的顶点全部入队。
3. 每次取出一个顶点 u，加入结果；把它的所有出边"删掉"（邻居入度减 1），若邻居入度变为 0 则入队。
4. 若结果中顶点数 < n，说明**有环**。

## 5.2 实现

```python
from collections import deque


def topo_sort_kahn(graph, n):
    """graph[u] = [v, ...]。返回拓扑序；有环时返回 None。O(V+E)。"""
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

    return order if len(order) == n else None      # 长度不足 -> 有环
```

## 5.3 字典序最小的拓扑序

把队列换成**小根堆**：

```python
import heapq


def topo_sort_lexicographic(graph, n):
    indeg = [0] * n
    for u in range(n):
        for v in graph[u]:
            indeg[v] += 1
    h = [u for u in range(n) if indeg[u] == 0]
    heapq.heapify(h)
    order = []
    while h:
        u = heapq.heappop(h)
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    return order if len(order) == n else None
```

复杂度 O((V+E) log V)。

## 5.4 DFS 逆后序法

DFS 的**后序遍历逆序**即为拓扑序。

```python
def topo_sort_dfs(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order = []

    def dfs(u):
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                return False           # 后向边 -> 有环
            if color[v] == WHITE and not dfs(v):
                return False
        color[u] = BLACK
        order.append(u)                # 后序压入
        return True

    for u in range(n):
        if color[u] == WHITE and not dfs(u):
            return None
    return order[::-1]                 # 逆序
```

| | Kahn (BFS) | DFS 逆后序 |
| ---- | ---- | ---- |
| 判环 | 结果长度 < n | 遇到 GRAY 结点 |
| 求字典序最小 | **容易**（换堆即可） | 困难 |
| 递归深度风险 | 无 | 有（需 `setrecursionlimit`） |
| 推荐 | ✅ **首选** | 需要与 SCC 结合时用 |

## 5.5 例题：舰队、海域出击

**OJ 09202: 舰队、海域出击！**，http://cs101.openjudge.cn/practice/09202/

> 判断有向图中是否存在环。

```python
import sys
from collections import deque

data = sys.stdin.read().split()
p = 0
T = int(data[p]); p += 1
out = []
for _ in range(T):
    n, m = int(data[p]), int(data[p + 1]); p += 2
    graph = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        x, y = int(data[p]), int(data[p + 1]); p += 2
        graph[x].append(y)
        indeg[y] += 1
    q = deque(u for u in range(1, n + 1) if indeg[u] == 0)
    cnt = 0
    while q:
        u = q.popleft()
        cnt += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    out.append("Yes" if cnt < n else "No")     # cnt < n 说明有环
print('\n'.join(out))
```

## 5.6 例题：课程表

**LeetCode 207 / 210**，https://leetcode.cn/problems/course-schedule-ii/

```python
def find_order(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:        # b 是 a 的先修课：b -> a
        graph[b].append(a)
        indeg[a] += 1
    q = deque(u for u in range(num_courses) if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []
```

---

# 6 DAG 上的动态规划

DAG 的拓扑序保证了"计算一个点时，它的所有前驱都已算完"——这正是 DP 需要的**无后效性**。

## 6.1 DAG 最长路 / 最短路

```python
def dag_longest_path(graph, n):
    """graph[u] = [(v, w), ...]，求 DAG 上的最长路径。O(V+E)。"""
    order = topo_sort_kahn([[v for v, _ in graph[u]] for u in range(n)], n)
    if order is None:
        raise ValueError("图中有环")
    dp = [0] * n
    for u in order:                   # 按拓扑序处理
        for v, w in graph[u]:
            dp[v] = max(dp[v], dp[u] + w)
    return max(dp)
```

> **注意**：一般图的最长路是 NP-hard，但 **DAG 上的最长路是 O(V+E)** 的。

## 6.2 DAG 路径计数

```python
def count_paths(graph, n, src, dst):
    order = topo_sort_kahn(graph, n)
    cnt = [0] * n
    cnt[src] = 1
    for u in order:
        for v in graph[u]:
            cnt[v] += cnt[u]
    return cnt[dst]
```

## 6.3 记忆化搜索版（无需显式拓扑排序）

**LeetCode 329. 矩阵中的最长递增路径**，https://leetcode.cn/problems/longest-increasing-path-in-a-matrix/

矩阵中"从小到大"的移动关系天然构成 DAG：

```python
from functools import lru_cache


def longest_increasing_path(matrix):
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    @lru_cache(maxsize=None)
    def dfs(i, j):
        best = 1
        for di, dj in DIRS:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                best = max(best, 1 + dfs(ni, nj))
        return best

    return max(dfs(i, j) for i in range(m) for j in range(n))
```

## 6.4 关键路径（AOE 网）

**AOE 网**：顶点表示事件，边表示活动及其持续时间。

- **关键路径**：从源点到汇点的**最长路径**，决定了整个工程的最短工期。
- **关键活动**：关键路径上的活动，任何延误都会拖延整个工程。

```python
def critical_path(graph, rgraph, n, src, dst):
    """返回 (最短工期, 关键活动列表)。
    ve[i] = 事件 i 最早发生时间；vl[i] = 最迟发生时间。"""
    order = topo_sort_kahn([[v for v, _ in graph[u]] for u in range(n)], n)
    if order is None:
        raise ValueError("图中有环")

    ve = [0] * n
    for u in order:                              # 正推最早时间
        for v, w in graph[u]:
            ve[v] = max(ve[v], ve[u] + w)

    total = ve[dst]
    vl = [total] * n
    for u in reversed(order):                    # 逆推最迟时间
        for v, w in graph[u]:
            vl[u] = min(vl[u], vl[v] - w)

    critical = []
    for u in range(n):
        for v, w in graph[u]:
            e = ve[u]                 # 活动最早开始
            l = vl[v] - w             # 活动最迟开始
            if e == l:                # 时间余量为 0 -> 关键活动
                critical.append((u, v, w))
    return total, critical
```

---

# 7 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | Agri-Net | OJ 01258 | 朴素 Prim（稠密图） |
| 2 | 兔子与星空 | OJ 05442 | Kruskal |
| 3 | 连接所有点的最小费用 | LC 1584 | MST 建模 |
| 4 | 最低成本联通所有城市 | LC 1135 | Kruskal 模板 |
| 5 | 舰队、海域出击！ | OJ 09202 | Kahn 判环 |
| 6 | 课程表 II | LC 210 | 拓扑排序输出序列 |
| 7 | 矩阵中的最长递增路径 | LC 329 | DAG + 记忆化 |
| 8 | 找到最终的安全状态 | LC 802 | 反图拓扑排序 |
| 9（选做） | 冗余连接 | LC 684 | 并查集判环（与 Kruskal 呼应） |
| 10（选做） | 关键路径（AOE 网） | 课堂题 | ve / vl 双向推导 |

**实验（第 7 次）**：在同一批随机图上（V = 1000，E 分别取 3000 / 100000）实测 Prim（堆优化）、Prim（朴素 O(V²)）、Kruskal 三种实现的耗时，验证"稀疏图用 Kruskal、稠密图用朴素 Prim"的经验法则。

**思考题**：

1. 用割性质证明 Prim 算法的正确性。
2. Prim 与 Dijkstra 的代码几乎一样，请指出**唯一的实质差别**，并说明为什么这个差别导致二者解决的是不同问题。
3. 若图中存在权值相同的边，MST 还唯一吗？MST 的权值和唯一吗？举例说明。
4. 拓扑序在什么条件下唯一？如何在 O(V+E) 内判断唯一性？
5. 为什么一般图的最长路是 NP-hard，而 DAG 上的最长路却是线性的？

---

# 8 小结

1. MST 的理论基础是**割性质**：最小横切边一定属于某棵 MST。
2. **Prim** 从点生长（优先队列），**Kruskal** 从边选取（排序 + 并查集）；稠密用 Prim O(V²)，稀疏用 Kruskal。
3. **MST 同时也是瓶颈生成树**——这让很多"最小化最大边权"的问题有了 O(E log E) 的优雅解法。
4. **拓扑排序**只对 DAG 存在；Kahn 算法（入度 + 队列）O(V+E)，顺便判环，换成堆即得字典序最小。
5. DAG 的拓扑序提供了 DP 的**无后效性**：最长路、路径计数、关键路径都是 O(V+E)。

**下周预告**：**散列表**、**KMP** 字符串匹配，以及**倒排索引 → RAG**——从经典数据结构走向现代 AI 检索系统。
