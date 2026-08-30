# -*- coding: utf-8 -*-
"""第12周 图的表示与遍历"""

META = {
    'title': '第12周　图的表示与遍历',
    'subtitle': '邻接矩阵 vs 邻接表 · DFS / BFS · 连通分量与二分图',
    'footer': '数据结构与算法 · 第12周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握图的存储结构；熟练实现 BFS 和 DFS'],
}

SLIDES = [
    ('section', '第 1 节', '图的基本概念'),

    ('ascii', '图 G = (V, E)', r"""
   无向图                     有向图
   A --- B                    A --> B
   |  /  |                    ^     |
   | /   |                    |     v
   C --- D                    C <-- D

V 是顶点集，E 是边集
"""),

    ('table', '术语表', [
        ['术语', '含义'],
        ['度 degree', '无向图中与顶点相连的边数'],
        ['入度 / 出度', '有向图中指向 / 指出该点的边数'],
        ['连通分量', '无向图的极大连通子图'],
        ['强连通', '有向图中任意两点互相可达'],
        ['稀疏图 / 稠密图', 'E ≈ V / E ≈ V²'],
        ['DAG', '有向无环图 —— 第 14 周拓扑排序的对象'],
    ]),

    ('bullets', '⭐ 四个重要事实', [
        '无向图中所有顶点的度之和 = **2|E|**（握手定理）',
        'n 个顶点的无向连通图**至少有 n−1 条边**（此时它是一棵树）',
        'n 个顶点的无向图若有 **≥ n 条边，则必有环**',
        '**树 = 无环连通图 = n 个顶点 n−1 条边的连通图**',
    ]),

    ('section', '第 2 节', '图的存储结构'),

    ('ascii', '邻接矩阵：g[i][j] 表示 i→j 是否有边', r"""
    A B C D                 A B C D
A [ 0 1 1 0 ]          A [ 0 1 1 ∞ ]
B [ 1 0 1 1 ]          B [ 1 0 1 4 ]     带权图用 ∞ 表示无边
C [ 1 1 0 1 ]          C [ 1 1 0 2 ]
D [ 0 1 1 0 ]          D [ ∞ 4 2 0 ]

空间 O(V²)  |  判断边 O(1)  |  遍历邻居 O(V)
适合：稠密图、需频繁查询边、Floyd 算法
"""),

    ('code', '⭐ 邻接表：最常用', '''from collections import defaultdict

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
''', '空间 O(V+E) | 遍历邻居 O(deg(u)) | 适合稀疏图（绝大多数 OJ 题）'),

    ('table', '三种表示的选择', [
        ['场景', '推荐'],
        ['V ≤ 500 且需要 Floyd', '邻接矩阵'],
        ['一般图遍历、最短路', '⭐ 邻接表'],
        ['Kruskal、Bellman-Ford', '边集数组 [(w, u, v), ...]'],
        ['网格图（迷宫）', '⭐ 不显式建图，用坐标 + 方向数组'],
    ], '网格图的隐式表示：(i,j) 是顶点，DIRS4 给出邻居 —— 第 8 周已经用过'),

    ('section', '第 3 节', '图的遍历'),

    ('key', '⚠️ 图与树的遍历差异',
     '树的遍历不用 visited（无环、每个结点只有一个父亲）\n图必须用 visited，否则会在环里无限打转'),

    ('code', 'DFS：递归版与迭代版', '''def dfs_recursive(graph, u, visited, order):
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
'''),

    ('code', 'BFS：顺带求出无权图最短路', '''from collections import deque


def bfs(graph, start, n):
    visited = [False] * n
    dist = [-1] * n
    parent = [-1] * n
    q = deque([start])
    visited[start] = True
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True        # ⚠️ 入队时标记
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
    return dist, parent


def restore_path(parent, target):        # 回溯出路径
    path = []
    while target != -1:
        path.append(target)
        target = parent[target]
    return path[::-1]
'''),

    ('table', '遍历复杂度', [
        ['表示', 'DFS / BFS'],
        ['邻接表', '⭐ O(V + E)'],
        ['邻接矩阵', 'O(V²)'],
    ]),

    ('section', '第 4 节', '遍历的应用'),

    ('code', '应用一：连通分量', '''def count_components(graph, n):
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
''', 'LC 200 岛屿数量、LC 547 省份数量也可用并查集（第 11 周）—— 两种解法都要会'),

    ('code', '应用二：LC 785 二分图判定（染色法）', '''from collections import deque


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
''', '⭐ 二分图 ⟺ 图中不存在奇数长度的环'),

    ('code', '应用三：无向图判环', '''def has_cycle_undirected(graph, n):
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
''', '⚠️ 若图中有重边，v != parent 的判断会出错，需改为记录边的编号'),

    ('code', '应用四：有向图判环（三色法）', '''WHITE, GRAY, BLACK = 0, 1, 2      # 未访问 / 在当前递归栈 / 已完成


def has_cycle_directed(graph, n):
    color = [WHITE] * n

    def dfs(u):
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:      # 指向递归栈中的点 -> 后向边 -> 有环
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    return any(dfs(u) for u in range(n) if color[u] == WHITE)
''', 'LC 207 课程表：判断能否修完所有课 = 判断有向图是否无环'),

    ('section', '第 5 节', '图论最难的一步：建模'),

    ('key', '建模',
     '图论题的难点往往不是算法，而是识别出\n【什么是顶点，什么是边】'),

    ('table', '⭐ 常见建模对照表', [
        ['题目', '顶点', '边'],
        ['迷宫最短路', '格子 (i, j)', '上下左右可走'],
        ['词梯（OJ 28046）', '单词', '差一个字母'],
        ['骑士周游（OJ 28050）', '棋盘格', '马走日'],
        ['课程表（LC 207）', '课程', '先修关系'],
        ['倒水问题', '水量状态 (a, b)', '一次倒水操作'],
        ['八数码', '棋盘布局', '移动空格'],
    ]),

    ('code', '建模练习：倒水问题', '''from collections import deque


def pour_water(cap_a, cap_b, target):
    """两个容量为 cap_a、cap_b 的杯子，量出 target 升水的最少步数。"""
    q = deque([((0, 0), 0)])
    seen = {(0, 0)}
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
''', '顶点是"状态"而不是"位置" —— 这是状态空间搜索的通用思路'),

    ('code', '进阶了解：割点与桥（Tarjan）', '''def find_bridges(graph, n):
    """dfn[u] = 访问时间戳；low[u] = 能回溯到的最早祖先。"""
    dfn = [0] * n; low = [0] * n; timer = [1]; bridges = []

    def dfs(u, parent):
        dfn[u] = low[u] = timer[0]; timer[0] += 1
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
''', '强连通分量（SCC）用 Tarjan / Kosaraju，O(V+E)；属竞赛内容，本课程只作了解'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '岛屿数量', 'LC 200', '网格 DFS / BFS'],
        ['2', '克隆图', 'LC 133', '图遍历 + 哈希映射'],
        ['3', '判断二分图', 'LC 785', '染色法'],
        ['4', '课程表', 'LC 207', '有向图判环'],
        ['5', '省份数量', 'LC 547', '连通分量（对比并查集）'],
        ['6', '所有可能的路径', 'LC 797', 'DAG 路径枚举'],
        ['7', '词梯', 'OJ 28046', '图建模 + BFS'],
        ['8（选做）', '骑士周游 / 倒水问题', 'OJ 28050 / 课堂题', '建模 + 剪枝'],
    ], '实验六：实现同时支持邻接表与邻接矩阵的 Graph 类，对比稀疏/稠密图上的耗时与内存'),

    ('bullets', '本讲小结', [
        '图 = (V, E)；核心是**建模**：识别顶点与边',
        '存储：**邻接表 O(V+E)** 是默认选择；邻接矩阵适合稠密图与 Floyd',
        '遍历必须用 **visited**，入队 / 入栈时标记；DFS / BFS 均为 O(V+E)',
        '经典应用：连通分量、二分图染色、判环、路径枚举',
        '网格图**不必显式建图**，用坐标 + 方向数组即可',
        '**下周预告**：带权图上的最短路径',
    ]),
]
