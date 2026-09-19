# -*- coding: utf-8 -*-
"""第13周 最短路"""

META = {
    'title': '第13周　最短路径',
    'subtitle': 'Dijkstra · Bellman-Ford · Floyd-Warshall',
    'footer': '数据结构与算法 · 第13周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握单源与多源最短路径算法；理解不同算法的适用场景'],
}

SLIDES = [
    ('table', '最短路问题分类', [
        ['问题', '算法', '复杂度', '允许负权'],
        ['无权图单源', 'BFS', 'O(V+E)', '—'],
        ['边权 0/1 单源', '0-1 BFS（双端队列）', 'O(V+E)', '—'],
        ['非负权单源', '**Dijkstra**（堆优化）', 'O(E log V)', '❌'],
        ['含负权单源', '**Bellman-Ford**', 'O(VE)', '✅ 可检测负环'],
        ['含负权（实践）', 'SPFA', '平均 O(kE)，最坏 O(VE)', '✅'],
        ['所有点对', '**Floyd-Warshall**', 'O(V³)', '✅（无负环）'],
    ]),

    ('key', '最短路的最优子结构',
     '若 p 是 v₀ 到 vₖ 的最短路，则其任意子路径也是最短路\n'
     '证明（剪切-粘贴）：否则用更短的替换它，整条路会更短，矛盾'),

    ('key', '⭐ 松弛（Relaxation）：所有算法的共同原子操作',
     'if dist[u] + w(u,v) < dist[v]:\n'
     '    dist[v] = dist[u] + w(u,v);  parent[v] = u'),

    ('bullets', '三种算法的区别只在于……', [
        '**松弛哪些边**、**以什么顺序**、**松弛多少轮**',
        '**Dijkstra**：每次贪心选出 dist 最小的点，松弛它的出边（每点松弛 1 次）',
        '**Bellman-Ford**：对所有边松弛 V−1 轮',
        '**Floyd**：枚举中间点 k，松弛所有点对',
    ]),

    ('section', '第 1 节', 'Dijkstra 算法'),

    ('bullets', '核心思想：贪心 + 优先队列', [
        '维护"已确定最短距离"的集合 S',
        '每次从 S 外选取 **dist 最小**的顶点加入 S，用它松弛所有出边',
        '**正确性依赖边权非负**：当 u 是 S 外 dist 最小的点时，绕道其他 S 外点再到 u 不会更短',
        '⚠️ **边权为负时这个论断失效**，Dijkstra 就错了',
    ]),

    ('ascii', '⚠️ 负权反例', r"""
     A --(1)--> B
     |          |
    (4)       (-3)
     |          |
     v          v
     C <--------+

Dijkstra 从 A 出发：先确定 dist[B]=1，再确定 dist[C]=4  ← 错误！
实际最短：A -> B -> C = 1 + (-3) = -2
"""),

    ('code', '⭐ Dijkstra 堆优化（必背模板）', '''import heapq


def dijkstra(graph, n, src):
    """graph[u] = [(v, w), ...]，时间 O(E log V)。"""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:               # ⭐ 惰性删除：跳过过期条目
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist
''', 'Python 的 heapq 不支持 decrease-key，所以直接把新距离再压一次，出堆时跳过陈旧条目'),

    ('code', '带路径还原的版本', '''def dijkstra_path(graph, n, src):
    INF = float('inf')
    dist, parent = [INF] * n, [-1] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, parent


def restore_path(parent, target):
    path = []
    while target != -1:
        path.append(target); target = parent[target]
    return path[::-1]
''', 'OJ 05443 兔子与樱花：需输出完整路径 A->(w)->B->(w)->C'),

    ('code', '朴素 O(V²) 版：稠密图反而更优', '''def dijkstra_dense(matrix, n, src):
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
            if dist[u] + matrix[u][v] < dist[v]:
                dist[v] = dist[u] + matrix[u][v]
    return dist
'''),

    ('bullets', '建模题：OJ 02502 Subway', [
        '步行 10 km/h，地铁 40 km/h，求家到学校的最短**时间**',
        '**建模**：所有点两两连一条“步行边”（权 = 距离/10）',
        '同一条地铁线上**相邻**站点之间再连一条“地铁边”（权 = 距离/40）',
        '⚠️ **关键**：地铁边只连相邻站，不能连任意两站（否则等于允许中途瞬移）',
        '然后跑标准 Dijkstra',
    ]),

    ('section', '第 2 节', 'Bellman-Ford 与 SPFA'),

    ('bullets', '为什么松弛 V−1 轮', [
        '无负环时，任意最短路**最多经过 V−1 条边**',
        '第 i 轮松弛后，所有“最多经过 i 条边”的最短路都已求出',
        '所以 V−1 轮后一定收敛',
        '⭐ **第 V 轮仍能松弛 ⇒ 存在负环**',
    ]),

    ('code', 'Bellman-Ford + 负环检测', '''def bellman_ford(edges, n, src):
    """edges = [(u, v, w), ...]，返回 (dist, has_negative_cycle)。"""
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:                    # 提前退出优化
            break

    for u, v, w in edges:                  # 第 n 轮：还能松弛就是负环
        if dist[u] != INF and dist[u] + w < dist[v]:
            return dist, True
    return dist, False
''', '负环存在时最短路无定义（绕环可让路径长度无限减小）。应用：套汇问题、差分约束'),

    ('code', 'SPFA：队列优化的 Bellman-Ford', '''from collections import deque


def spfa(graph, n, src):
    """只有 dist 被更新过的点才可能让邻居也被更新。"""
    INF = float('inf')
    dist = [INF] * n; dist[src] = 0
    in_queue = [False] * n
    cnt = [0] * n                  # 入队次数，用于负环检测
    q = deque([src]); in_queue[src] = True

    while q:
        u = q.popleft(); in_queue[u] = False
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not in_queue[v]:
                    q.append(v); in_queue[v] = True
                    cnt[v] += 1
                    if cnt[v] >= n:        # 入队 n 次 -> 负环
                        return dist, True
    return dist, False
''', '⚠️ “关于 SPFA，它死了”：可被构造数据卡到 O(VE)。非负权图一律用 Dijkstra'),

    ('table', 'Dijkstra vs Bellman-Ford', [
        ['', 'Dijkstra', 'Bellman-Ford'],
        ['复杂度', 'O(E log V)', 'O(VE)'],
        ['负权边', '❌', '✅'],
        ['负环检测', '❌', '✅'],
        ['每个点松弛几次', '出堆时 1 次', '最多 V−1 次'],
        ['思想', '贪心', '动态规划 / 迭代'],
    ]),

    ('section', '第 3 节', 'Floyd-Warshall'),

    ('key', 'Floyd 的本质是区间 DP',
     'dp[k][i][j] = 只允许经过编号 ≤ k 的中间点时，i 到 j 的最短距离\n'
     'dp[k][i][j] = min(dp[k−1][i][j], dp[k−1][i][k] + dp[k−1][k][j])'),

    ('code', '三重循环 k-i-j', '''def floyd_warshall(n, matrix):
    """matrix[i][j] 是邻接矩阵（无边为 INF，对角线为 0）。O(V³)。"""
    dist = [row[:] for row in matrix]
    for k in range(n):                      # ⚠️ k 必须在最外层
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == float('inf'):
                continue                    # 常数优化
            di = dist[i]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return dist
''', '⚠️ 循环顺序 k-i-j 不能变！k 放内层则 dp[k−1] 尚未算完，结果错误 —— Floyd 最经典考点'),

    ('code', 'Floyd 的其他用途', '''# 传递闭包（可达性）
for k in range(n):
    for i in range(n):
        if reach[i][k]:
            for j in range(n):
                if reach[k][j]:
                    reach[i][j] = True

# 负环检测：跑完后若 dist[i][i] < 0，则 i 在某个负环上

# 最小环：在第 k 层之前枚举 i、j
#   dist[i][j] + g[j][k] + g[k][i]  即为经过 k 的最小环
''', '适用范围 V ≤ 400（V³ ≈ 6×10⁷）。优点：代码极短、能处理负权、一次得到所有点对'),

    ('section', '第 4 节', '特殊技巧'),

    ('code', '⭐ 0-1 BFS：边权只有 0 和 1 时', '''from collections import deque


def zero_one_bfs(graph, n, src):
    INF = float('inf')
    dist = [INF] * n; dist[src] = 0
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
''', 'O(V+E)，比 Dijkstra 更快。典型题：网格中“打通一堵墙代价 1，走空地代价 0”'),

    ('code', '⭐ 分层图：把附加条件塞进状态', '''def layered_dijkstra(graph, n, src, dst, k):
    """最多免费经过 k 条边。状态 = (顶点, 已用免费次数)。"""
    INF = float('inf')
    dist = [[INF] * (k + 1) for _ in range(n)]
    dist[src][0] = 0
    pq = [(0, src, 0)]
    while pq:
        d, u, used = heapq.heappop(pq)
        if d > dist[u][used]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v][used]:               # 正常走
                dist[v][used] = d + w
                heapq.heappush(pq, (d + w, v, used))
            if used < k and d < dist[v][used + 1]:  # 免费走
                dist[v][used + 1] = d
                heapq.heappush(pq, (d, v, used + 1))
    return min(dist[dst])
''', 'LC 787 K 站中转内最便宜的航班。核心思想：从图论走向 DP 的通用桥梁'),

    ('bullets', '二分答案 + 连通性判定', [
        '题型：**最小化路径上的最大边权**（瓶颈路）',
        '做法：二分阈值 x，只保留边权 ≤ x 的边，用 BFS / 并查集判 src 与 dst 是否连通',
        '复杂度 O(E log W)',
        '⭐ 第 14 周会看到更优雅的解法：**MST 就是瓶颈生成树**',
    ]),

    ('ascii', '⭐ 算法选择决策树', r"""
边权都是 1（或无权）？
├─ 是 → BFS，O(V+E)
└─ 否 → 边权只有 0 和 1？
        ├─ 是 → 0-1 BFS（双端队列），O(V+E)
        └─ 否 → 有负权边？
                ├─ 否 → 需要所有点对？
                │       ├─ 是且 V ≤ 400 → Floyd，O(V³)
                │       ├─ 是且 V 较大  → 每点跑一次 Dijkstra
                │       └─ 否 → Dijkstra 堆优化，O(E log V)
                └─ 是 → 需要检测负环？
                        ├─ 是 → Bellman-Ford，O(VE)
                        └─ 否 → SPFA（注意可能被卡）
"""),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '兔子与樱花', 'OJ 05443', 'Dijkstra + 路径还原'],
        ['2', '网络延迟时间', 'LC 743', 'Dijkstra 模板'],
        ['3', '最小体力消耗路径', 'LC 1631', '二分 + BFS / 变形 Dijkstra'],
        ['4', 'K 站中转内最便宜的航班', 'LC 787', '分层图 / Bellman-Ford'],
        ['5', '概率最大的路径', 'LC 1514', '变形 Dijkstra（乘积最大）'],
        ['6', 'Subway', 'OJ 02502', '图建模 + Dijkstra'],
        ['7', '阈值距离内邻居最少的城市', 'LC 1334', 'Floyd'],
        ['8（选做）', '穿越火线', 'OJ 29803', '二分 + Dijkstra'],
    ]),

    ('bullets', '本讲小结', [
        '所有最短路算法的原子操作都是**松弛**，区别在于顺序与轮数',
        '**Dijkstra**：贪心 + 堆，O(E log V)，**要求非负权**；Python 用惰性删除',
        '**Bellman-Ford**：松弛 V−1 轮，能处理负权与**检测负环**；SPFA 可被卡',
        '**Floyd**：三重循环 **k 必须最外层**，O(V³)，一次求所有点对',
        '特殊技巧：**0-1 BFS**、**分层图**、**二分答案 + 连通性判定**',
        '**下周预告**：最小生成树与拓扑排序',
    ]),
]
