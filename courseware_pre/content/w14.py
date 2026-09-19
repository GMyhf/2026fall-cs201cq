# -*- coding: utf-8 -*-
"""第14周 最小生成树；拓扑排序"""

META = {
    'title': '第14周　最小生成树与拓扑排序',
    'subtitle': 'Prim · Kruskal · Kahn 算法 · DAG 应用',
    'footer': '数据结构与算法 · 第14周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握 MST 算法；理解拓扑排序的原理与实现'],
}

SLIDES = [
    ('section', '第一部分', '最小生成树（MST）'),

    ('ascii', '生成树与最小生成树', r"""
     图 G                     一棵 MST
   A --1-- B                A --1-- B
   |\      |                |       |
   4 \3    2       ==>      |       2
   |   \   |                |       |
   C --5-- D                C       D
                            \___3___/     总权 = 1+2+3 = 6

生成树：包含全部 n 个顶点、n−1 条边、无环的极小连通子图
MST：所有生成树中边权之和最小的那棵
""", '应用：铺设网络/管道的最低成本、聚类分析、图像分割、TSP 近似'),

    ('key', '⭐ 割性质（Cut Property）',
     '把顶点集任意划分为 (S, V−S)，跨越这个割的所有边中，\n权值最小的边一定属于某棵 MST'),

    ('bullets', '割性质的证明（交换论证）', [
        '设最小横切边 e 不在 MST T 中',
        '把 e 加入 T 会形成一个环，环中必有另一条横切边 f',
        '由 e 是最小横切边，w(f) ≥ w(e)',
        '用 e 替换 f 得到的仍是生成树，且权值不增　∎',
        '⭐ 这是 **Prim 和 Kruskal 都正确**的根本原因',
    ]),

    ('bullets', '环性质与唯一性', [
        '**环性质**：任意环中权值**最大**的边一定不在某棵 MST 中',
        '若所有边权**互不相同**，MST **唯一**',
        '若有相同权值的边，MST 可能不唯一，但**权值和唯一**',
    ]),

    ('section', '第 1 节', 'Prim 算法：从点出发生长'),

    ('key', '⚠️ Prim 与 Dijkstra 的唯一实质差别',
     'Dijkstra 比较的是「从源点出发的总距离 dist[u] + w」\n'
     'Prim 比较的是「到集合的单条边权 w」　—— 代码只差一个加号'),

    ('code', 'Prim 堆优化（推荐）', '''import heapq


def prim(graph, n, start=0):
    """graph[u] = [(v, w), ...]，返回 (MST 总权值, 边列表)。O(E log V)。"""
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
'''),

    ('code', '朴素 Prim O(V²)：稠密图更优（OJ 01258 Agri-Net）', '''def prim_dense(matrix, n):
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
                lowcost[v] = matrix[u][v]      # ⭐ 与 Dijkstra 的唯一区别
    return total
''', 'Agri-Net 是完全图（E = V²），用 O(V²) 版本最合适'),

    ('section', '第 2 节', 'Kruskal 算法：从边出发'),

    ('bullets', '思想：排序 + 并查集判环', [
        '把所有边按权值**升序排序**',
        '依次考察每条边：若两端**不在同一连通块**就选它',
        '否则丢弃（选了会形成环）',
        '⭐ 用**并查集**（第 11 周）O(α) 判断是否同一连通块',
    ]),

    ('code', 'Kruskal 实现', '''def kruskal(edges, n):
    """edges = [(w, u, v), ...]，O(E log E)，瓶颈在排序。"""
    edges.sort()
    dsu = DSU(n)
    total, chosen = 0, []
    for w, u, v in edges:
        if dsu.union(u, v):            # ⭐ 不成环则选它
            total += w
            chosen.append((u, v, w))
            if len(chosen) == n - 1:   # 已有 n-1 条边，提前结束
                break
    return (total, chosen) if len(chosen) == n - 1 else (-1, [])
''', 'OJ 05442 兔子与星空的模板解法'),

    ('table', '⭐ Prim vs Kruskal', [
        ['', 'Prim', 'Kruskal'],
        ['出发点', '顶点', '边'],
        ['数据结构', '优先队列', '排序 + **并查集**'],
        ['复杂度', 'O(E log V) / O(V²)', 'O(E log E)'],
        ['适合', '**稠密图**（用 O(V²) 版）', '**稀疏图**'],
        ['中间状态', '始终是一棵树', '是一片森林'],
        ['不连通图', '只得到一个连通分量', '⭐ 天然得到最小生成森林'],
    ]),

    ('code', '⭐ MST 就是瓶颈生成树', '''def bottleneck(edges, n, src, dst):
    """最小化 src 到 dst 路径上的最大边权。"""
    edges.sort()
    dsu = DSU(n)
    for w, u, v in edges:
        dsu.union(u, v)
        if dsu.find(src) == dsu.find(dst):
            return w               # 最后加的那条边就是答案
    return -1
''', '第 13 周用「二分答案 + BFS」O(E log W) 做的题，这里 O(E log E) 一遍就过'),

    ('bullets', 'MST 的其他变形', [
        '**最大生成树**：边权取负后跑 Kruskal，或排序改为降序',
        '**次小生成树**、**最小度限制生成树**、**Steiner 树** —— 竞赛内容，了解即可',
        '课程要求：熟练掌握 Prim 与 Kruskal 两套模板',
    ]),

    ('section', '第二部分', '拓扑排序'),

    ('ascii', '把“依赖关系”变成“可执行顺序”', r"""
    课程先修关系                    拓扑序（不唯一）
    数学 --> 算法 --> AI            数学, 编程, 算法, 数据结构, AI
      \             /               编程, 数学, 算法, 数据结构, AI
    编程 --> 数据结构

对每条有向边 u -> v，u 都排在 v 前面
"""),

    ('bullets', '存在性与唯一性', [
        '有向图存在拓扑序 **⟺ 它是 DAG（无环）**',
        '拓扑序**一般不唯一**',
        '当且仅当每一步都恰有一个入度为 0 的点时**唯一**（即存在哈密顿路径）',
        '**应用**：课程安排、任务调度、编译依赖（Makefile）、软件包安装、DAG 上的 DP',
    ]),

    ('bullets', '⭐ Kahn 算法（BFS 入度法）', [
        '① 统计所有顶点的**入度**',
        '② 把入度为 0 的顶点全部入队',
        '③ 取出 u 加入结果，把它的出边“删掉”（邻居入度减 1），减到 0 就入队',
        '④ 若结果中顶点数 < n，说明**有环**',
    ]),

    ('code', 'Kahn 算法模板', '''from collections import deque


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
''', 'OJ 09202 舰队、海域出击！：cnt < n 即为有环。LC 207/210 课程表'),

    ('code', '字典序最小的拓扑序：队列换成小根堆', '''import heapq


def topo_sort_lexicographic(graph, n):
    indeg = [0] * n
    for u in range(n):
        for v in graph[u]:
            indeg[v] += 1
    h = [u for u in range(n) if indeg[u] == 0]
    heapq.heapify(h)                             # ⭐ 换成堆
    order = []
    while h:
        u = heapq.heappop(h)
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    return order if len(order) == n else None
''', '复杂度 O((V+E) log V)'),

    ('code', 'DFS 逆后序法', '''def topo_sort_dfs(graph, n):
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
    return order[::-1]                 # ⭐ 逆序
'''),

    ('table', 'Kahn vs DFS 逆后序', [
        ['', 'Kahn (BFS)', 'DFS 逆后序'],
        ['判环', '结果长度 < n', '遇到 GRAY 结点'],
        ['求字典序最小', '⭐ 容易（换堆即可）', '困难'],
        ['递归深度风险', '无', '有（需 setrecursionlimit）'],
        ['推荐', '⭐ **首选**', '需与 SCC 结合时用'],
    ]),

    ('section', '第三部分', 'DAG 上的动态规划'),

    ('key', '为什么 DAG 适合 DP',
     '拓扑序保证了「计算一个点时，它的所有前驱都已算完」\n这正是 DP 需要的【无后效性】'),

    ('code', 'DAG 最长路：O(V+E)', '''def dag_longest_path(graph, n):
    """graph[u] = [(v, w), ...]"""
    order = topo_sort_kahn([[v for v, _ in graph[u]] for u in range(n)], n)
    if order is None:
        raise ValueError("图中有环")
    dp = [0] * n
    for u in order:                   # ⭐ 按拓扑序处理
        for v, w in graph[u]:
            dp[v] = max(dp[v], dp[u] + w)
    return max(dp)


def count_paths(graph, n, src, dst):      # DAG 路径计数
    order = topo_sort_kahn(graph, n)
    cnt = [0] * n
    cnt[src] = 1
    for u in order:
        for v in graph[u]:
            cnt[v] += cnt[u]
    return cnt[dst]
''', '⚠️ 一般图的最长路是 NP-hard，但 DAG 上的最长路是线性的'),

    ('code', '记忆化搜索版：无需显式拓扑排序', '''from functools import lru_cache


def longest_increasing_path(matrix):      # LC 329
    """矩阵中"从小到大"的移动关系天然构成 DAG。"""
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
'''),

    ('code', '关键路径（AOE 网）', '''def critical_path(graph, n, src, dst):
    """ve[i]=事件最早发生时间；vl[i]=最迟发生时间。"""
    order = topo_sort_kahn(...)

    ve = [0] * n
    for u in order:                              # 正推最早时间
        for v, w in graph[u]:
            ve[v] = max(ve[v], ve[u] + w)

    total = ve[dst]
    vl = [total] * n
    for u in reversed(order):                    # 逆推最迟时间
        for v, w in graph[u]:
            vl[u] = min(vl[u], vl[v] - w)

    critical = [(u, v, w) for u in range(n) for v, w in graph[u]
                if ve[u] == vl[v] - w]           # 时间余量为 0
    return total, critical
''', '关键路径 = 源点到汇点的【最长路径】，决定整个工程的最短工期'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', 'Agri-Net', 'OJ 01258', '朴素 Prim（稠密图）'],
        ['2', '兔子与星空', 'OJ 05442', 'Kruskal'],
        ['3', '连接所有点的最小费用', 'LC 1584', 'MST 建模'],
        ['4', '最低成本联通所有城市', 'LC 1135', 'Kruskal 模板'],
        ['5', '舰队、海域出击！', 'OJ 09202', 'Kahn 判环'],
        ['6', '课程表 II', 'LC 210', '拓扑排序输出序列'],
        ['7', '矩阵中的最长递增路径', 'LC 329', 'DAG + 记忆化'],
        ['8（选做）', '找到最终的安全状态 / 关键路径', 'LC 802 / 课堂题', '反图拓扑、AOE'],
    ], '实验七：在同一批随机图上实测 Prim(堆) / Prim(朴素) / Kruskal，验证稀疏稠密的经验法则'),

    ('bullets', '本讲小结', [
        'MST 的理论基础是**割性质**：最小横切边一定属于某棵 MST',
        '**Prim** 从点生长（优先队列），**Kruskal** 从边选取（排序 + 并查集）',
        '**MST 同时也是瓶颈生成树** —— 让“最小化最大边权”类问题有了优雅解法',
        '**拓扑排序**只对 DAG 存在；Kahn 算法 O(V+E)，顺便判环，换堆即得字典序最小',
        'DAG 的拓扑序提供 DP 的**无后效性**：最长路、路径计数、关键路径都是线性的',
        '**下周预告**：散列表、KMP，以及倒排索引 → RAG',
    ]),
]
