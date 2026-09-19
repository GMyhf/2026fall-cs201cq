# 第13周 最短路：Dijkstra、Bellman-Ford、Floyd-Warshall

*Updated 2026-08-30 13:40 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 13 周 / 3 学时
> **教学内容**：最短路：Dijkstra、Bellman-Ford；Floyd-Warshall
> **教学要求**：掌握单源与多源最短路径算法；理解不同算法的适用场景

**知识点**：松弛操作、最优子结构、Dijkstra（朴素 O(V²) / 堆优化 O(E log V)）、贪心正确性与负权失效、Bellman-Ford、负环检测、SPFA、Floyd-Warshall、路径还原、0-1 BFS、分层图最短路、次短路。

---

# 1 最短路问题分类

| 问题 | 算法 | 复杂度 | 允许负权 |
| ---- | ---- | ---- | ---- |
| 无权图单源 | **BFS** | O(V+E) | — |
| 边权 0/1 单源 | **0-1 BFS**（双端队列） | O(V+E) | — |
| 非负权单源 | **Dijkstra**（堆优化） | O(E log V) | ❌ |
| 含负权单源 | **Bellman-Ford** | O(VE) | ✅（可检测负环） |
| 含负权单源（实践） | **SPFA** | 平均 O(kE)，最坏 O(VE) | ✅ |
| 所有点对 | **Floyd-Warshall** | O(V³) | ✅（无负环） |

## 1.1 最短路的最优子结构

**定理**：若 `p = v₀ → v₁ → … → vₖ` 是 v₀ 到 vₖ 的最短路，则其任意子路径 `vᵢ → … → vⱼ` 也是 vᵢ 到 vⱼ 的最短路。

**证明（剪切-粘贴法）**：若子路径不是最短，用更短的替换它，整条路径会更短，与 p 是最短路矛盾。∎

这个性质是所有最短路算法的理论基础。

## 1.2 松弛（Relaxation）：所有算法的共同原子操作

```python
if dist[u] + w(u, v) < dist[v]:
    dist[v] = dist[u] + w(u, v)
    parent[v] = u
```

含义："经过 u 到 v" 比 "当前已知的到 v 的路" 更短，就更新。**所有最短路算法的区别，只在于松弛哪些边、以什么顺序、松弛多少轮。**

---

# 2 Dijkstra 算法

## 2.1 核心思想

**贪心 + 优先队列**：维护一个"已确定最短距离"的集合 S，每次从 S 外选取 `dist` 最小的顶点加入 S，然后用它松弛所有出边。

**正确性依赖于边权非负**：当 u 是 S 外 dist 最小的点时，任何绕道其他 S 外点再到 u 的路径都不会更短（因为绕道只会让距离**不减**）。**边权为负时这个论断失效**，Dijkstra 就错了。

## 2.2 反例：负权导致 Dijkstra 出错

```
     A --(1)--> B
     |          |
    (4)       (-3)
     |          |
     v          v
     C <--------+

Dijkstra 从 A 出发：先确定 dist[B]=1，再确定 dist[C]=4（错误！）
实际最短：A -> B -> C = 1 + (-3) = -2
```

## 2.3 堆优化实现（重点掌握）

```python
import heapq


def dijkstra(graph, n, src):
    """graph[u] = [(v, w), ...]，返回 src 到各点的最短距离。
    时间 O(E log V)，空间 O(V)。"""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    parent = [-1] * n
    pq = [(0, src)]                   # (距离, 顶点)
    visited = [False] * n

    while pq:
        d, u = heapq.heappop(pq)
        if visited[u]:                # 惰性删除：跳过陈旧条目
            continue
        visited[u] = True
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent
```

**三个实现要点**：

1. **惰性删除**：Python 的 `heapq` 不支持 decrease-key，所以直接把新距离再压一次；出堆时用 `visited`（或 `if d > dist[u]: continue`）跳过过期条目。
2. 堆中最多有 O(E) 个条目，故复杂度 O(E log E) = O(E log V)。
3. 若只求到单个终点，可在 `u == target` 时提前返回。

**更简洁的等价写法**（不用 visited 数组）：

```python
def dijkstra_v2(graph, n, src):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:               # 过期条目
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

## 2.4 朴素实现 O(V²)

**稠密图（E ≈ V²）时反而更优**，且实现简单：

```python
def dijkstra_dense(matrix, n, src):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    visited = [False] * n
    for _ in range(n):
        u, best = -1, INF
        for i in range(n):                # 线性扫描找最小
            if not visited[i] and dist[i] < best:
                u, best = i, dist[i]
        if u == -1:
            break
        visited[u] = True
        for v in range(n):
            if matrix[u][v] < INF and dist[u] + matrix[u][v] < dist[v]:
                dist[v] = dist[u] + matrix[u][v]
    return dist
```

## 2.5 路径还原

```python
def restore_path(parent, target):
    path = []
    while target != -1:
        path.append(target)
        target = parent[target]
    return path[::-1]
```

## 2.6 例题：兔子与樱花

**OJ 05443: 兔子与樱花**，http://cs101.openjudge.cn/practice/05443/

> 给定带权无向图（地点名为字符串），多次询问两点间最短路并输出完整路径。

```python
import heapq
from collections import defaultdict

n = int(input())
names = [input().strip() for _ in range(n)]
idx = {name: i for i, name in enumerate(names)}

graph = defaultdict(list)
m = int(input())
for _ in range(m):
    a, b, w = input().split()
    graph[idx[a]].append((idx[b], int(w)))
    graph[idx[b]].append((idx[a], int(w)))

INF = float('inf')
q = int(input())
for _ in range(q):
    s, t = input().split()
    src, dst = idx[s], idx[t]
    if src == dst:
        print(s)
        continue
    dist = [INF] * n
    dist[src] = 0
    parent = [-1] * n
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == dst:
            break
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    # 还原路径，格式：A->(w)->B->(w)->C
    path = []
    cur = dst
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    out = [names[path[0]]]
    for i in range(1, len(path)):
        w = dist[path[i]] - dist[path[i - 1]]
        out.append(f"->({w})->{names[path[i]]}")
    print(''.join(out))
```

## 2.7 例题：Subway（建模题）

**OJ 02502: Subway**，http://cs101.openjudge.cn/practice/02502/

> 步行 10 km/h，地铁 40 km/h。给出若干条地铁线路上的站点坐标，求家到学校的最短时间。

**建模**：所有点两两之间连一条"步行边"（权 = 距离/10），同一条地铁线上**相邻**站点之间再连一条"地铁边"（权 = 距离/40），然后跑 Dijkstra。

> **关键**：地铁边只连相邻站，不能连任意两站（否则等于允许中途瞬移）。

---

# 3 Bellman-Ford 算法

## 3.1 核心思想

**对所有边松弛 V−1 轮**。

**为什么是 V−1 轮**：无负环时，任意最短路最多经过 V−1 条边。第 i 轮松弛后，所有"最多经过 i 条边"的最短路都已求出。

```python
def bellman_ford(edges, n, src):
    """edges = [(u, v, w), ...]，返回 (dist, has_negative_cycle)。
    时间 O(V·E)。"""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    for i in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:                    # 提前退出优化
            break

    # 第 n 轮仍能松弛 -> 存在负环
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return dist, True
    return dist, False
```

## 3.2 负环检测

**负环**：环上边权之和为负。存在负环时，绕环可以让路径长度无限减小，**最短路无定义**。

Bellman-Ford 是检测负环的标准方法：跑完 V−1 轮后若还能松弛，就说明有负环。

**应用**：套汇问题（OJ 01860 Currency Exchange）、差分约束系统。

## 3.3 SPFA（队列优化的 Bellman-Ford）

观察：只有 `dist` 被更新过的点，才可能让它的邻居也被更新。用队列只处理这些点。

```python
from collections import deque


def spfa(graph, n, src):
    """graph[u] = [(v, w), ...]。平均很快，最坏仍是 O(VE)。"""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    in_queue = [False] * n
    cnt = [0] * n                  # 每个点入队次数，用于负环检测
    q = deque([src])
    in_queue[src] = True

    while q:
        u = q.popleft()
        in_queue[u] = False
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not in_queue[v]:
                    q.append(v)
                    in_queue[v] = True
                    cnt[v] += 1
                    if cnt[v] >= n:        # 入队 n 次 -> 负环
                        return dist, True
    return dist, False
```

> ⚠️ **"关于 SPFA，它死了"**：SPFA 存在可被精心构造的数据卡到 O(VE)。**非负权图一律用 Dijkstra**，SPFA 只在有负权时使用。

## 3.4 Dijkstra vs Bellman-Ford

| | Dijkstra | Bellman-Ford |
| ---- | ---- | ---- |
| 复杂度 | O(E log V) | O(VE) |
| 负权边 | ❌ | ✅ |
| 负环检测 | ❌ | ✅ |
| 每个点松弛几次 | 出堆时 1 次 | 最多 V−1 次 |
| 思想 | 贪心 | 动态规划 / 迭代 |

---

# 4 Floyd-Warshall 算法

## 4.1 核心思想：区间 DP

`dp[k][i][j]` = 只允许经过编号 ≤ k 的中间点时，i 到 j 的最短距离。

```
dp[k][i][j] = min(dp[k-1][i][j],                  不经过 k
                  dp[k-1][i][k] + dp[k-1][k][j])  经过 k
```

第一维可以滚动掉，得到经典的三重循环：

```python
def floyd_warshall(n, matrix):
    """matrix[i][j] 是邻接矩阵（无边为 INF，对角线为 0）。
    时间 O(V³)，空间 O(V²)。"""
    dist = [row[:] for row in matrix]
    for k in range(n):                      # ⚠️ k 必须在最外层
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == float('inf'):
                continue
            di = dist[i]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return dist
```

> ⚠️ **循环顺序 k-i-j 不能变**。若把 k 放到内层，`dp[k-1]` 的状态就没有全部算完，结果错误。这是 Floyd 最经典的考点。

## 4.2 路径还原

```python
def floyd_with_path(n, matrix):
    dist = [row[:] for row in matrix]
    nxt = [[j if matrix[i][j] < float('inf') else -1 for j in range(n)]
           for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def get_path(nxt, u, v):
    if nxt[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path
```

## 4.3 Floyd 的其他用途

**传递闭包**（判断可达性）：

```python
def transitive_closure(n, reach):
    """reach[i][j] 为布尔，返回可达矩阵。"""
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return reach
```

**最小环**：在 Floyd 的第 k 层之前枚举 i、j，`dist[i][j] + g[j][k] + g[k][i]` 即为经过 k 的最小环。

**负环检测**：跑完后若 `dist[i][i] < 0`，则 i 在某个负环上。

## 4.4 适用范围

V ≤ 400 左右（V³ ≈ 6×10⁷，Python 需要用上面的优化写法或改用 C++）。**优点是代码极短、能处理负权、一次得到所有点对**。

---

# 5 特殊技巧

## 5.1 0-1 BFS

边权只有 0 和 1 时，用**双端队列**代替优先队列：权 0 的边 `appendleft`，权 1 的边 `append`。复杂度 **O(V+E)**，比 Dijkstra 更快。

```python
from collections import deque


def zero_one_bfs(graph, n, src):
    """graph[u] = [(v, w), ...]，w ∈ {0, 1}。"""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)     # 0 权边：同层，放队首
                else:
                    dq.append(v)         # 1 权边：下一层，放队尾
    return dist
```

**典型题**：网格中"打通一堵墙代价 1，走空地代价 0"的最短路。

## 5.2 分层图最短路

允许"免费走 k 条边"之类的问题：把图复制 k+1 层，第 i 层到第 i+1 层的边权为 0。

```python
def layered_dijkstra(graph, n, src, dst, k):
    """最多可以免费经过 k 条边，求最短路。状态 = (顶点, 已用免费次数)。"""
    INF = float('inf')
    dist = [[INF] * (k + 1) for _ in range(n)]
    dist[src][0] = 0
    pq = [(0, src, 0)]
    while pq:
        d, u, used = heapq.heappop(pq)
        if d > dist[u][used]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v][used]:            # 正常走
                dist[v][used] = d + w
                heapq.heappush(pq, (d + w, v, used))
            if used < k and d < dist[v][used + 1]:   # 免费走
                dist[v][used + 1] = d
                heapq.heappush(pq, (d, v, used + 1))
    return min(dist[dst])
```

> **核心思想**：**把附加条件塞进状态里**——这是从图论走向 DP 的通用桥梁。

## 5.3 二分答案 + 最短路 / BFS

"最小化路径上的最大边权"（瓶颈路）类问题：二分一个阈值 x，只保留边权 ≤ x 的边，用 BFS 判连通。

```python
def minimize_max_edge(edges, n, src, dst):
    """最小化 src 到 dst 路径上的最大边权。"""
    weights = sorted({w for _, _, w in edges})
    lo, hi = 0, len(weights) - 1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        limit = weights[mid]
        g = [[] for _ in range(n)]
        for u, v, w in edges:
            if w <= limit:
                g[u].append(v)
                g[v].append(u)
        # BFS 判连通
        seen = [False] * n
        q = deque([src]); seen[src] = True
        while q:
            u = q.popleft()
            for v in g[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
        if seen[dst]:
            ans = limit
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
```

（这类题也可以用 Kruskal / 并查集做，第 14 周会看到更优雅的解法。）

---

# 6 算法选择决策树

```
边权都是 1（或无权）？
├─ 是 → BFS，O(V+E)
└─ 否 → 边权只有 0 和 1？
        ├─ 是 → 0-1 BFS（双端队列），O(V+E)
        └─ 否 → 有负权边？
                ├─ 否 → 需要所有点对？
                │       ├─ 是且 V ≤ 400 → Floyd，O(V³)
                │       ├─ 是且 V 较大 → 每个点跑一次 Dijkstra
                │       └─ 否 → Dijkstra 堆优化，O(E log V)
                └─ 是 → 需要检测负环？
                        ├─ 是 → Bellman-Ford，O(VE)
                        └─ 否 → SPFA（注意可能被卡）
```

---

# 7 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 兔子与樱花 | OJ 05443 | Dijkstra + 路径还原 |
| 2 | 网络延迟时间 | LC 743 | Dijkstra 模板 |
| 3 | 最小体力消耗路径 | LC 1631 | 二分 + BFS / 变形 Dijkstra |
| 4 | K 站中转内最便宜的航班 | LC 787 | 分层图 / Bellman-Ford |
| 5 | 概率最大的路径 | LC 1514 | 变形 Dijkstra（乘积最大） |
| 6 | Subway | OJ 02502 | 图建模 + Dijkstra |
| 7 | Currency Exchange | OJ 01860 | Bellman-Ford 负环 |
| 8 | 阈值距离内邻居最少的城市 | LC 1334 | Floyd |
| 9（选做） | 穿越火线 | OJ 29803 | 二分 + Dijkstra |
| 10（选做） | 二分图 + 最短路综合题 | 自选 | 建模 |

**思考题**：

1. 为什么 Dijkstra 在有负权边时会出错？画一个最小反例并模拟算法执行。
2. Floyd 的三重循环为什么必须把 k 放在最外层？把 k 放在最内层会算出什么？
3. Dijkstra 中"惰性删除"与"真正的 decrease-key"在复杂度上有何区别？为什么 Python 常用前者？
4. 0-1 BFS 为什么正确？请用"双端队列中至多存在两种距离值"的不变式说明。

---

# 8 小结

1. 所有最短路算法的原子操作都是**松弛**，区别在于松弛的顺序与轮数。
2. **Dijkstra**：贪心 + 堆，O(E log V)，**要求非负权**；Python 用惰性删除。
3. **Bellman-Ford**：松弛 V−1 轮，O(VE)，**能处理负权与检测负环**；SPFA 是其队列优化但可被卡。
4. **Floyd**：三重循环 k-i-j，O(V³)，一次求所有点对，代码最短。
5. 特殊技巧：**0-1 BFS**、**分层图**（把条件塞进状态）、**二分答案 + 连通性判定**。

**下周预告**：**最小生成树**（Prim、Kruskal）与**拓扑排序**（Kahn 算法）及 DAG 应用。
