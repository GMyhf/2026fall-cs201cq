# 第12周 图的表示与遍历

*Updated 2026-08-31 03:10 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 12 周 / 3 学时
> **教学内容**：图的表示与遍历
> **教学要求**：掌握图的存储结构；熟练实现 BFS 和 DFS

**知识点**：图的术语（顶点 / 边 / 度 / 路径 / 环 / 连通性）、有向图与无向图、带权图、邻接矩阵、邻接表、边集数组、图的 DFS 与 BFS、连通分量、二分图判定（染色法）、无向图与有向图判环、割点与桥（简介）、图的建模能力。

---

# 1 图的基本概念

## 1.1 定义

**图 G = (V, E)**，V 是顶点集，E 是边集。

```
无向图                     有向图
   A --- B                  A --> B
   |  /  |                  ^     |
   | /   |                  |     v
   C --- D                  C <-- D
```

## 1.2 术语表

| 术语 | 含义 |
| ---- | ---- |
| **无向图** | 边无方向，(u,v) = (v,u) |
| **有向图 digraph** | 边有方向，<u,v> ≠ <v,u> |
| **带权图** | 边（或点）带有权值 |
| **度 degree** | 无向图中与顶点相连的边数 |
| **入度 / 出度** | 有向图中指向 / 指出该点的边数 |
| **路径** | 顶点序列，相邻顶点间有边 |
| **简单路径** | 顶点不重复的路径 |
| **环 cycle** | 起点与终点相同的路径 |
| **连通** | 无向图中任意两点间有路径 |
| **连通分量** | 无向图的极大连通子图 |
| **强连通** | 有向图中任意两点互相可达 |
| **完全图** | 任意两点间都有边，无向时 E = n(n−1)/2 |
| **稀疏图 / 稠密图** | E ≈ V / E ≈ V² |
| **DAG** | 有向无环图（第 14 周拓扑排序的对象） |

## 1.3 重要事实

1. 无向图中所有顶点的度之和 = 2|E|（**握手定理**）。
2. n 个顶点的无向连通图至少有 n−1 条边（此时是**树**）。
3. n 个顶点的无向图若有 ≥ n 条边，则必有环。
4. **树 = 无环连通图 = n 个顶点 n−1 条边的连通图**。

---

# 2 图的存储结构

## 2.1 邻接矩阵（Adjacency Matrix）

`g[i][j]` 表示 i 到 j 是否有边（或边权）。

```
    A B C D            A B C D
A [ 0 1 1 0 ]      A [ 0 1 1 ∞ ]
B [ 1 0 1 1 ]      B [ 1 0 1 4 ]     带权图用 ∞ 表示无边
C [ 1 1 0 1 ]      C [ 1 1 0 2 ]
D [ 0 1 1 0 ]      D [ ∞ 4 2 0 ]
```

```python
INF = float('inf')

n = 4
g = [[0] * n for _ in range(n)]         # 无权图

def add_edge_matrix(g, u, v, w=1, directed=False):
    g[u][v] = w
    if not directed:
        g[v][u] = w
```

| | 邻接矩阵 |
| ---- | ---- |
| 空间 | **O(V²)** |
| 判断 (u,v) 是否有边 | **O(1)** |
| 遍历 u 的所有邻居 | O(V) |
| 适合 | **稠密图**、需要频繁查询边、Floyd 算法 |

## 2.2 邻接表（Adjacency List）——最常用

每个顶点存一个邻居列表。

```
A: [B, C]
B: [A, C, D]
C: [A, B, D]
D: [B, C]
```

```python
from collections import defaultdict

# 写法 1：列表的列表（顶点编号 0..n-1，最快）
graph = [[] for _ in range(n)]
def add_edge(u, v, directed=False):
    graph[u].append(v)
    if not directed:
        graph[v].append(u)

# 写法 2：defaultdict（顶点是任意可哈希对象）
graph = defaultdict(list)
graph[u].append(v)

# 带权图
graph = [[] for _ in range(n)]
graph[u].append((v, w))          # (邻居, 权值)
```

| | 邻接表 |
| ---- | ---- |
| 空间 | **O(V + E)** |
| 判断 (u,v) 是否有边 | O(deg(u)) |
| 遍历 u 的所有邻居 | **O(deg(u))** |
| 适合 | **稀疏图**（绝大多数 OJ 题）、BFS/DFS/Dijkstra |

## 2.3 边集数组

只存边的三元组列表，适合 **Kruskal**（第 14 周）和 **Bellman-Ford**（第 13 周）。

```python
edges = [(w, u, v), ...]         # 权值放第一位便于排序
```

## 2.4 三种表示的选择

| 场景 | 推荐 |
| ---- | ---- |
| V ≤ 500 且需要 Floyd | 邻接矩阵 |
| 一般图遍历、最短路 | **邻接表** |
| Kruskal、Bellman-Ford | 边集数组 |
| 网格图（迷宫） | 不显式建图，用坐标 + 方向数组 |

> **网格图的隐式表示**（第 8 周已用过）：`(i, j)` 是顶点，`DIRS4` 给出邻居，不需要真的建出邻接表。

## 2.5 面向对象的图类

```python
class Vertex:
    def __init__(self, key):
        self.key = key
        self.neighbors = {}      # 邻居 -> 权值

    def add_neighbor(self, nbr, weight=0):
        self.neighbors[nbr] = weight

    def get_connections(self):
        return self.neighbors.keys()

    def get_weight(self, nbr):
        return self.neighbors[nbr]

    def __repr__(self):
        return f"Vertex({self.key})"


class Graph:
    def __init__(self, directed=False):
        self.vertices = {}
        self.directed = directed

    def add_vertex(self, key):
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)
        return self.vertices[key]

    def add_edge(self, f, t, weight=0):
        self.add_vertex(f)
        self.add_vertex(t)
        self.vertices[f].add_neighbor(self.vertices[t], weight)
        if not self.directed:
            self.vertices[t].add_neighbor(self.vertices[f], weight)

    def __contains__(self, key):
        return key in self.vertices

    def __iter__(self):
        return iter(self.vertices.values())

    def __len__(self):
        return len(self.vertices)
```

> **OJ 实战**：面向对象版本可读性好但常数大；比赛/考试直接用 `graph = [[] for _ in range(n)]`。

---

# 3 图的遍历

## 3.1 图 vs 树的遍历差异

树的遍历不用 visited（无环、每个结点只有一个父亲），**图必须用 visited**，否则会在环里无限打转。

## 3.2 DFS

```python
def dfs_recursive(graph, u, visited, order):
    visited[u] = True
    order.append(u)
    for v in graph[u]:
        if not visited[v]:
            dfs_recursive(graph, v, visited, order)


def dfs_iterative(graph, start, n):
    visited = [False] * n
    stack = [start]
    order = []
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)
        for v in reversed(graph[u]):     # reversed 让顺序与递归版一致
            if not visited[v]:
                stack.append(v)
    return order
```

## 3.3 BFS

```python
from collections import deque


def bfs(graph, start, n):
    visited = [False] * n
    dist = [-1] * n
    parent = [-1] * n
    q = deque([start])
    visited[start] = True
    dist[start] = 0
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True        # ⚠️ 入队时标记
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
    return order, dist, parent
```

**BFS 求出的 `dist` 是无权图的最短路径长度**；`parent` 数组可以回溯出路径：

```python
def restore_path(parent, target):
    path = []
    while target != -1:
        path.append(target)
        target = parent[target]
    return path[::-1]
```

## 3.4 复杂度

| 表示 | DFS / BFS |
| ---- | ---- |
| 邻接表 | **O(V + E)** |
| 邻接矩阵 | O(V²) |

---

# 4 遍历的应用

## 4.1 连通分量

```python
def count_components(graph, n):
    """无向图连通分量个数与各分量成员。"""
    visited = [False] * n
    components = []
    for s in range(n):
        if visited[s]:
            continue
        comp, stack = [], [s]
        visited[s] = True
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        components.append(comp)
    return components
```

**LeetCode 323 / 547（省份数量）**也可用并查集（第 11 周）——两种解法都要会。

**网格类连通块**：LC 200 岛屿数量、OJ 18160 最大连通域面积。

## 4.2 二分图判定（染色法）

**二分图**：顶点能分成两个集合，使每条边的两个端点分属不同集合。**等价于图中不存在奇数长度的环**。

**LeetCode 785. 判断二分图**，https://leetcode.cn/problems/is-graph-bipartite/

```python
from collections import deque


def is_bipartite(graph):
    n = len(graph)
    color = [0] * n              # 0 未染色，1 和 -1 是两种颜色
    for s in range(n):
        if color[s]:
            continue
        color[s] = 1
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == 0:
                    color[v] = -color[u]     # 染成相反色
                    q.append(v)
                elif color[v] == color[u]:
                    return False             # 相邻同色 -> 有奇环
    return True
```

**应用**：OJ 07734 虫子的生活（第 11 周用并查集做过，这里用染色法是另一种解法）。

## 4.3 无向图判环

```python
def has_cycle_undirected(graph, n):
    visited = [False] * n
    for s in range(n):
        if visited[s]:
            continue
        stack = [(s, -1)]        # (当前点, 父结点)
        visited[s] = True
        while stack:
            u, parent = stack.pop()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, u))
                elif v != parent:      # 访问过且不是来时的父 -> 有环
                    return True
    return False
```

> ⚠️ 若图中有重边，`v != parent` 的判断会出错，需改为记录边的编号。

## 4.4 有向图判环（三色法）

```python
WHITE, GRAY, BLACK = 0, 1, 2      # 未访问 / 在当前递归栈中 / 已完成


def has_cycle_directed(graph, n):
    color = [WHITE] * n

    def dfs(u):
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:      # 指向了递归栈中的点 -> 后向边 -> 有环
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    return any(dfs(u) for u in range(n) if color[u] == WHITE)
```

**LeetCode 207. 课程表**：判断能否修完所有课 = 判断有向图是否无环（也可用拓扑排序，第 14 周）。

## 4.5 路径与连通性问题

```python
def all_paths(graph, src, dst):
    """LC 797：DAG 中所有从 src 到 dst 的路径（回溯）。"""
    res, path = [], [src]

    def dfs(u):
        if u == dst:
            res.append(path[:])
            return
        for v in graph[u]:
            path.append(v)
            dfs(v)
            path.pop()

    dfs(src)
    return res
```

## 4.6 网格图建模：把题目翻译成图

图论最难的往往不是算法，而是**建模**——识别出"什么是顶点、什么是边"。

| 题目 | 顶点 | 边 |
| ---- | ---- | ---- |
| 迷宫最短路 | 格子 (i,j) | 上下左右可走 |
| 词梯（OJ 28046） | 单词 | 差一个字母 |
| 骑士周游（OJ 28050） | 棋盘格 | 马走日 |
| 课程表（LC 207） | 课程 | 先修关系 |
| 倒水问题 | 水量状态 (a,b) | 一次倒水操作 |
| 八数码 | 棋盘布局 | 移动空格 |

**练习：倒水问题**

```python
from collections import deque


def pour_water(cap_a, cap_b, target):
    """两个容量为 cap_a、cap_b 的杯子，量出 target 升水的最少步数。"""
    start = (0, 0)
    q = deque([(start, 0)])
    seen = {start}
    while q:
        (a, b), d = q.popleft()
        if a == target or b == target:
            return d
        nxts = [
            (cap_a, b), (a, cap_b),                     # 装满
            (0, b), (a, 0),                             # 倒空
            (a - min(a, cap_b - b), b + min(a, cap_b - b)),   # A -> B
            (a + min(b, cap_a - a), b - min(b, cap_a - a)),   # B -> A
        ]
        for s in nxts:
            if s not in seen:
                seen.add(s)
                q.append((s, d + 1))
    return -1
```

---

# 5 进阶话题（了解）

## 5.1 割点与桥（Tarjan）

- **割点（cut vertex）**：删掉它会使连通分量增多。
- **桥（bridge）**：删掉它会使连通分量增多的边。

用 DFS 时间戳 `dfn` 与能回溯到的最早祖先 `low` 判定：

```python
def find_bridges(graph, n):
    dfn = [0] * n
    low = [0] * n
    timer = [1]
    bridges = []

    def dfs(u, parent):
        dfn[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if v == parent:
                continue
            if dfn[v] == 0:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > dfn[u]:       # v 的子树回不到 u 及其祖先
                    bridges.append((u, v))
            else:
                low[u] = min(low[u], dfn[v])

    for s in range(n):
        if dfn[s] == 0:
            dfs(s, -1)
    return bridges
```

## 5.2 强连通分量（SCC）

有向图中的极大强连通子图，用 **Tarjan** 或 **Kosaraju** 算法 O(V+E) 求出。SCC 缩点后得到 DAG，可继续做拓扑排序 + DP。这是竞赛内容，本课程只作了解。

---

# 6 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 岛屿数量 | LC 200 | 网格 DFS/BFS |
| 2 | 克隆图 | LC 133 | 图遍历 + 哈希映射 |
| 3 | 判断二分图 | LC 785 | 染色法 |
| 4 | 课程表 | LC 207 | 有向图判环 |
| 5 | 省份数量 | LC 547 | 连通分量（对比并查集解法） |
| 6 | 所有可能的路径 | LC 797 | DAG 路径枚举 |
| 7 | 词梯 | OJ 28046 | 图建模 + BFS |
| 8 | 骑士周游 | OJ 28050 | 图建模 + 回溯剪枝 |
| 9（选做） | 单词接龙 II | LC 126 | BFS 分层 + 回溯路径 |
| 10（选做） | 倒水问题 | 课堂题 | 状态空间建模 |

**实验（第 6 次）**：实现 `Graph` 类，支持邻接表与邻接矩阵两种内部表示；在 V = 1000、E 分别为 2000（稀疏）与 400000（稠密）的两张图上，对比两种表示下 BFS/DFS 的耗时与内存占用。

**思考题**：

1. 什么情况下邻接矩阵比邻接表更优？给出一个具体的 V、E 取值。
2. 无向图判环时若图中有重边，`v != parent` 的写法会出什么错？怎么修？
3. 二分图判定为什么等价于"没有奇环"？给出直观解释。
4. 若把网格迷宫显式建成邻接表，空间是多少？为什么隐式表示更好？

---

# 7 小结

1. 图 = (V, E)；核心是**建模**：识别顶点与边。
2. 存储：**邻接表 O(V+E)** 是默认选择；邻接矩阵 O(V²) 适合稠密图与 Floyd。
3. 遍历必须用 **visited**，入队/入栈时标记；DFS/BFS 均为 O(V+E)。
4. 遍历的经典应用：连通分量、二分图染色、判环、路径枚举。
5. 网格图**不必显式建图**，用坐标 + 方向数组即可。

**下周预告**：带权图上的最短路径——**Dijkstra、Bellman-Ford、Floyd-Warshall**。
