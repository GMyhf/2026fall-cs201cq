# -*- coding: utf-8 -*-
"""第16周 课程总结与复习"""

META = {
    'title': '第16周　课程总结与复习',
    'subtitle': '知识体系梳理 · 模板代码库 · 上机考试要点',
    'footer': '数据结构与算法 · 第16周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：系统梳理知识结构；掌握重点算法与数据结构'],
}

SLIDES = [
    ('ascii', '知识体系总图', r"""
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
"""),

    ('table', '一句话回顾每一周（上）', [
        ['周', '一句话', '最该记住的'],
        ['W2', 'ADT 分离接口与实现', 'list/dict/set 的复杂度差异'],
        ['W3', '大 O 描述增长趋势', '**看数据范围反推算法**'],
        ['W4', '栈是 LIFO', '括号匹配、调度场、**单调栈**'],
        ['W5', '队列是 FIFO', 'deque、**单调队列**、链表哨兵'],
        ['W6', '分治与排序', '归并求逆序对、**用内建 sorted**'],
        ['W7', '贪心要证明，DP 要状态', '背包正序/倒序、LIS O(n log n)'],
        ['W8', '搜索是遍历解空间树', '**入队时标记 visited**、回溯三步'],
    ]),

    ('table', '一句话回顾每一周（下）', [
        ['周', '一句话', '最该记住的'],
        ['W9', '树的算法都是递归', '前中后序、前序+中序建树'],
        ['W10', '堆是完全二叉树+堆序', 'heapq、Top-K、对顶堆'],
        ['W11', '平衡与分组', 'AVL 四种旋转、**并查集模板**'],
        ['W12', '图 = 建模', '邻接表、连通分量、二分图染色'],
        ['W13', '松弛是共同原子操作', '**Dijkstra 堆优化模板**'],
        ['W14', '割性质与拓扑序', 'Kruskal = 排序+并查集、**Kahn**'],
        ['W15', '哈希与匹配', 'KMP 的 next 数组、倒排索引'],
    ]),

    ('section', '第 1 节', '复杂度速查表（必背）'),

    ('table', '数据结构操作复杂度', [
        ['结构', '查找', '插入', '删除', '有序遍历'],
        ['数组 / list', 'O(n) / O(1) 按下标', '尾 O(1)，中 O(n)', '同左', '需先排序'],
        ['单链表', 'O(n)', '已知位置 O(1)', '已知位置 O(1)', 'O(n)'],
        ['**哈希表**', '**O(1)** 平均', 'O(1)', 'O(1)', '❌ 无序'],
        ['**二叉堆**', 'O(n) 任意元素', 'O(log n)', 'O(log n) 仅堆顶', '❌'],
        ['BST（平均）', 'O(log n)', 'O(log n)', 'O(log n)', '✅ 中序'],
        ['**AVL / 红黑树**', '**O(log n)**', 'O(log n)', 'O(log n)', '✅'],
        ['**并查集**', '**O(α)≈O(1)**', 'O(α)', '❌ 不支持', '❌'],
        ['Trie', 'O(L)', 'O(L)', 'O(L)', '✅ 字典序'],
    ]),

    ('table', '算法复杂度', [
        ['算法', '时间', '空间', '前提'],
        ['二分查找', 'O(log n)', 'O(1)', '有序'],
        ['归并 / 堆排', 'O(n log n)', 'O(n) / O(1)', '—'],
        ['快排', '平均 O(n log n)，最坏 O(n²)', 'O(log n)', '建议随机化'],
        ['DFS / BFS', 'O(V+E)', 'O(V)', '—'],
        ['Dijkstra（堆）', 'O(E log V)', 'O(V)', '**非负权**'],
        ['Bellman-Ford', 'O(VE)', 'O(V)', '可负权、检测负环'],
        ['Floyd', 'O(V³)', 'O(V²)', 'V ≤ 400'],
        ['Prim / Kruskal', 'O(E log V) / O(E log E)', 'O(V)', '无向图'],
        ['拓扑排序 / KMP', 'O(V+E) / O(n+m)', 'O(V) / O(m)', 'DAG / —'],
    ]),

    ('table', '⭐ 数据规模 → 算法选择（考场第一步）', [
        ['n', '允许复杂度', '典型算法'],
        ['≤ 12', 'O(n!)', '全排列枚举'],
        ['≤ 20', 'O(2ⁿ)', '状压 DP、子集枚举'],
        ['≤ 100', 'O(n³)', 'Floyd、区间 DP'],
        ['≤ 1000', 'O(n²)', '二维 DP、朴素图算法'],
        ['≤ 10⁵', 'O(n log n)', '排序、堆、二分、Dijkstra'],
        ['≤ 10⁶', 'O(n)', '双指针、前缀和、单调栈/队列'],
        ['≥ 10⁸', 'O(log n) / O(1)', '数学公式、快速幂'],
    ]),

    ('section', '第 2 节', '必背模板代码库'),

    ('key', '⚠️ 上机考试禁止使用任何 AI 工具',
     '这一节的 12 个模板必须能【默写】\n考前把它们手抄一遍'),

    ('code', '① 快速 IO　② 二分', '''import sys
data = sys.stdin.read().split()
p = 0
n = int(data[p]); p += 1
out = []
sys.stdout.write('\\n'.join(out) + '\\n')
sys.setrecursionlimit(1 << 20)


import bisect
i = bisect.bisect_left(a, x)      # 第一个 >= x
j = bisect.bisect_right(a, x)     # 第一个 > x


def binary_answer(lo, hi, check):
    """求满足 check 的最小值。check 需单调。"""
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
'''),

    ('code', '③ 单调栈　④ 单调队列', '''def next_greater(a):
    """每个元素右边第一个更大元素的下标，无则 -1。"""
    n = len(a); res = [-1] * n; stack = []
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
'''),

    ('code', '⑤ 并查集', '''class DSU:
    def __init__(self, n):
        self.p = list(range(n)); self.sz = [1] * n; self.count = n

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
'''),

    ('code', '⑥ Dijkstra　⑦ 拓扑排序　⑧ Kruskal', '''import heapq

def dijkstra(graph, n, src):
    INF = float('inf'); dist = [INF] * n; dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist


def topo(graph, n):
    indeg = [0] * n
    for u in range(n):
        for v in graph[u]: indeg[v] += 1
    q = deque(u for u in range(n) if indeg[u] == 0); order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return order if len(order) == n else None
'''),

    ('code', '⑨ 网格 BFS　⑩ 回溯', '''DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def grid_bfs(grid, sr, sc):
    m, n = len(grid), len(grid[0])
    dist = [[-1] * n for _ in range(m)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        i, j = q.popleft()
        for di, dj in DIRS4:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and dist[ni][nj] < 0 \\
                    and grid[ni][nj] != '#':
                dist[ni][nj] = dist[i][j] + 1
                q.append((ni, nj))
    return dist


def backtrack():
    if len(path) == len(nums):
        res.append(path[:]); return
    for i, v in enumerate(nums):
        if used[i]: continue
        if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
        used[i] = True; path.append(v)
        backtrack()
        path.pop(); used[i] = False
'''),

    ('code', '⑪ 背包　⑫ KMP + 迭代中序', '''# 01 背包：容量倒序
dp = [0] * (C + 1)
for i in range(n):
    for c in range(C, w[i] - 1, -1):
        dp[c] = max(dp[c], dp[c - w[i]] + v[i])

# 完全背包：容量正序
for i in range(n):
    for c in range(w[i], C + 1):
        dp[c] = max(dp[c], dp[c - w[i]] + v[i])


def build_next(p):
    nxt = [0] * len(p); k = 0
    for i in range(1, len(p)):
        while k > 0 and p[i] != p[k]: k = nxt[k - 1]
        if p[i] == p[k]: k += 1
        nxt[i] = k
    return nxt


def inorder(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur: stack.append(cur); cur = cur.left
        cur = stack.pop(); res.append(cur.val); cur = cur.right
    return res
'''),

    ('section', '第 3 节', '常见题型 → 解法映射'),

    ('table', '看到关键词，首先想到……（上）', [
        ['题面关键词', '首先想到'],
        ['“下一个更大 / 更小”', '单调栈'],
        ['“滑动窗口最大值”', '单调队列'],
        ['“第 K 大 / 小”', '堆 / 快速选择'],
        ['“中位数（数据流）”', '对顶堆'],
        ['“最短步数”“最少操作” + 边权为 1', 'BFS'],
        ['“最短路径” + 带权非负', 'Dijkstra'],
        ['“所有点对最短路” + n ≤ 400', 'Floyd'],
        ['“最小代价连通所有点”', 'MST（Prim / Kruskal）'],
    ]),

    ('table', '看到关键词，首先想到……（下）', [
        ['题面关键词', '首先想到'],
        ['“是否同一组”“合并集合”', '并查集'],
        ['“先修课”“依赖顺序”', '拓扑排序'],
        ['“所有方案”“排列组合”', '回溯'],
        ['“方案数”“最值” + 选择互相制约', 'DP'],
        ['“区间不重叠”“最多安排几个”', '贪心（按右端点排序）'],
        ['“子串匹配”“循环节”', 'KMP'],
        ['“前缀”“自动补全”', 'Trie'],
        ['“区间和查询”', '前缀和'],
        ['“最大化最小值”“最小化最大值”', '二分答案'],
    ]),

    ('section', '第 4 节', '上机考试要点'),

    ('table', '考试形式', [
        ['项目', '说明'],
        ['时长 / 题量', '**120 分钟 / 6 道**算法编程题'],
        ['平台 / 语言', 'OJ 在线评测 / Python 3（支持 C++）'],
        ['占比', '总评 **60%**'],
        ['工具', '⚠️ **禁止使用任何 AI 工具**'],
        ['学术诚信', '无法解释自己提交的代码 → 按学术不端处理'],
    ]),

    ('ascii', '⏱ 时间分配建议', r"""
0–10 min    通读全部 6 题，按预估难度排序，标出"必拿分"的题
10–40 min   拿下 2–3 道简单题（模拟、排序、哈希、基础 DP）
40–90 min   攻中等题（图论、DP、树、搜索）
90–110 min  攻最后 1–2 题；无思路则回头检查已提交题的边界
110–120 min 检查输出格式、多组数据、边界（n = 0 / 1）
""", '关键策略：先易后难；看数据范围定算法；卡住超过 15 分钟果断换题'),

    ('table', '⚠️ 高频失分点清单（上）', [
        ['失分点', '对策'],
        ['多组数据没循环读', '看清“直到 EOF”或“读到 0 0 结束”'],
        ['输出格式（大小写、空格、Case #x:）', '逐字对照样例输出'],
        ['浮点输出精度', '用 f"{x:.2f}"，别用 round'],
        ['下标 0-based / 1-based 混淆', '建图统一开 n+1 大小'],
        ['`list.pop(0)` 做 BFS', '一律用 `deque.popleft()`'],
        ['`x in list` 判存在', '改用 `set`'],
        ['循环里 `str +=`', "改用 `''.join`"],
    ]),

    ('table', '⚠️ 高频失分点清单（下）', [
        ['失分点', '对策'],
        ['递归爆栈', '`sys.setrecursionlimit(1 << 20)`'],
        ['Dijkstra 用在负权图', '改用 Bellman-Ford / SPFA'],
        ['01 背包写成正序', '记住“01 倒序、完全正序”'],
        ['BFS 出队时才标记 visited', '入队时立即标记'],
        ['忘记 n=0 / 空输入的边界', '提交前先想极端情况'],
        ['`[[0]*m]*n` 建二维数组', '用 `[[0]*m for _ in range(n)]`'],
        ['大量输出逐行 print', "攒进列表最后 `'\\n'.join` 一次输出"],
    ]),

    ('bullets', 'Python 超时自救清单（按性价比排序）', [
        '`input()` → `sys.stdin.read().split()`',
        '`list.pop(0)` → `deque.popleft()`',
        '`x in list` → `x in set`',
        "循环拼接字符串 → `''.join`",
        '手写排序 → 内建 `sorted`',
        '递归 → 迭代 + 显式栈',
        '⭐ 仍超时 → 检查复杂度是不是**选错了算法**（这才是根因）',
    ]),

    ('table', '考前 7 天计划', [
        ['天', '内容'],
        ['D-7', '默写第 2 节全部模板，不看讲义'],
        ['D-6', '重刷线性结构 + 排序（W4–W6）错题'],
        ['D-5', '重刷 DP + 贪心（W7），背包再过一遍'],
        ['D-4', '重刷搜索（W8）：BFS / DFS / 回溯各 3 题'],
        ['D-3', '重刷树与堆（W9–W11）'],
        ['D-2', '重刷图论（W12–W14）：Dijkstra、MST、拓扑各 2 题'],
        ['D-1', '**限时模拟**：随机 6 题，严格计时 120 分钟'],
        ['D-0', '只看模板与失分点清单，不做新题，早睡'],
    ]),

    ('section', '第 5 节', '综合复习题'),

    ('bullets', '判断题（考查概念）', [
        '堆是完全二叉树，因此中序遍历有序。　**❌ 堆只保证父子有序**',
        '快速排序的最坏时间复杂度是 O(n log n)。　**❌ 是 O(n²)**',
        'Dijkstra 可以处理有负权边但无负环的图。　**❌ 不能**',
        '并查集可以高效支持删除某条边。　**❌ 不支持**',
        '前序遍历序列可以唯一确定一棵二叉树。　**❌ 需配合中序或空标记**',
        '拓扑排序的结果一定唯一。　**❌ 一般不唯一**',
        'AVL 树删除结点最多需要一次旋转。　**❌ 可能 O(log n) 次**',
    ]),

    ('code', '综合编程题 B：树上打家劫舍（树形 DP）', '''def rob_tree(root):
    """给定一棵二叉树，求不相邻结点的最大权值和。"""
    def dfs(node):
        if not node:
            return 0, 0                # (选它的最优, 不选它的最优)
        l_take, l_skip = dfs(node.left)
        r_take, r_skip = dfs(node.right)
        take = node.val + l_skip + r_skip
        skip = max(l_take, l_skip) + max(r_take, r_skip)
        return take, skip
    return max(dfs(root))
''', '其他现场演练题：A 图+堆（Dijkstra）、C 并查集+排序（Kruskal）、D 字符串+哈希'),

    ('bullets', '本周作业', [
        '完成一套限时 **120 分钟的 6 题模拟卷**（题目由课程组发布）',
        '**默写**第 2 节的 12 个模板，交手写扫描件或代码文件',
        '整理个人**错题本**：列出本学期所有 WA/TLE 题目、错因分类、正确做法',
    ]),

    ('bullets', '本讲小结与寄语', [
        '主线：**用什么结构存 → 用什么策略算 → 复杂度是多少 → 能不能过题**',
        '数据结构的价值：**用空间换时间**、**在修改时顺手维护信息**',
        '四大算法范式：**分治、贪心、动态规划、搜索**',
        '会写代码 ≠ 会算法；**会分析复杂度、会选择结构**才是本课要培养的能力',
        '上机考试考的不是记忆力，而是**在压力下把模板准确快速地组合起来**',
    ]),

    ('key', '寄语',
     '你们手写的每一个堆、每一次 BFS、每一张倒排索引，\n'
     '都真实地运行在今天的搜索引擎与向量数据库里。祝考试顺利。'),
]
