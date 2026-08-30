# -*- coding: utf-8 -*-
"""第8周 搜索专题"""

META = {
    'title': '第8周　搜索专题',
    'subtitle': 'DFS / BFS · 回溯与剪枝',
    'footer': '数据结构与算法 · 第8周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握 DFS/BFS 回溯搜索的实现与剪枝'],
}

SLIDES = [
    ('key', '搜索的统一视角',
     '任何搜索问题都是在一棵【解空间树】上行走\n结点 = 状态，边 = 一次决策，叶子 = 完整解或死路'),

    ('table', 'DFS vs BFS', [
        ['', 'DFS 深度优先', 'BFS 广度优先'],
        ['数据结构', '栈（递归）', '队列 deque'],
        ['走法', '一条路走到黑，再回头', '一层一层扩展'],
        ['空间', 'O(深度)', 'O(该层宽度)'],
        ['擅长', '求所有解、路径枚举、连通性', '⭐ 最短步数、层级信息'],
        ['第一个找到的解', '不保证最短', '⭐ 保证最短（边权全为 1）'],
    ]),

    ('ascii', '同一棵解空间树的两种遍历', r"""
             起点
           /  |  \
         A    B    C          DFS: 起点 A D E B ...
        / \        |          BFS: 起点 A B C D E ...
       D   E       F
"""),

    ('section', '第 1 节', 'DFS 深度优先搜索'),

    ('code', 'DFS 递归框架', '''def dfs(state):
    if is_goal(state):
        record(state)
        return
    for nxt in next_states(state):
        if not visited(nxt):
            mark(nxt)
            dfs(nxt)
            unmark(nxt)        # 回溯时撤销（若需要）
'''),

    ('code', 'OJ 18160 最大连通域面积（八连通）', '''import sys
sys.setrecursionlimit(1 << 20)

DIRS8 = [(-1, -1), (-1, 0), (-1, 1),
         (0, -1),           (0, 1),
         (1, -1),  (1, 0),  (1, 1)]


def dfs(grid, i, j, n, m):
    if not (0 <= i < n and 0 <= j < m) or grid[i][j] != 'W':
        return 0
    grid[i][j] = '.'                    # ⭐ 就地标记，省一个 visited 数组
    area = 1
    for di, dj in DIRS8:
        area += dfs(grid, i + di, j + dj, n, m)
    return area
''', '四连通版本只需换成 DIRS4 = [(-1,0),(1,0),(0,-1),(0,1)]'),

    ('code', '迭代式 DFS（避免爆栈）', '''def dfs_iter(grid, si, sj, n, m):
    stack = [(si, sj)]
    grid[si][sj] = '.'
    area = 0
    while stack:
        i, j = stack.pop()
        area += 1
        for di, dj in DIRS8:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 'W':
                grid[ni][nj] = '.'      # ⚠️ 入栈时就标记
                stack.append((ni, nj))
    return area
''', '⚠️ 标记时机：入栈/入队时立刻标记，否则同一格子会被重复压入，退化成指数级'),

    ('section', '第 2 节', 'BFS 广度优先搜索'),

    ('code', 'BFS 标准框架', '''from collections import deque


def bfs(start, is_goal, neighbors):
    q = deque([start])
    visited = {start}
    dist = {start: 0}
    while q:
        cur = q.popleft()
        if is_goal(cur):
            return dist[cur]
        for nxt in neighbors(cur):
            if nxt not in visited:
                visited.add(nxt)          # ⚠️ 入队时标记
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return -1
'''),

    ('code', 'OJ 19930 寻宝：网格最短路', '''from collections import deque
DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

m, n = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(m)]

q = deque([(0, 0, 0)])              # (行, 列, 步数)
grid[0][0] = 0                      # 就地标记为已访问
ans = -1
while q:
    i, j, d = q.popleft()
    for di, dj in DIRS4:
        ni, nj = i + di, j + dj
        if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] != 0:
            if grid[ni][nj] == 2:
                ans = d + 1
                q.clear(); break
            grid[ni][nj] = 0
            q.append((ni, nj, d + 1))
print(ans if ans >= 0 else "NO")
'''),

    ('code', '分层 BFS 与多源 BFS', '''# 分层：需要知道"当前在第几层"
while q:
    for _ in range(len(q)):         # ⭐ 固定住本层的大小
        cur = q.popleft()
        ...
    level += 1


# 多源（LC 542 01 矩阵）：所有源点一起入队
for i in range(m):
    for j in range(n):
        if mat[i][j] == 0:
            dist[i][j] = 0
            q.append((i, j))        # 一次 BFS 求"到最近源点的距离"
''', '相关题：LC 994 腐烂的橘子（多源 + 分层）'),

    ('code', 'OJ 28046 词梯：状态空间 BFS + 建桶', '''from collections import deque, defaultdict


def word_ladder(begin, end, word_list):
    words = set(word_list)
    # ⭐ 建"桶"：hot -> _ot, h_t, ho_  加速找相邻单词
    buckets = defaultdict(list)
    for w in words | {begin}:
        for i in range(len(w)):
            buckets[w[:i] + '_' + w[i + 1:]].append(w)

    q = deque([(begin, 1)])
    visited = {begin}
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for nxt in buckets[w[:i] + '_' + w[i + 1:]]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, d + 1))
    return 0
''', '建桶把"两两比较是否只差一个字母"从 O(N²L) 降到 O(NL) —— 本题的关键优化'),

    ('bullets', '双向 BFS', [
        '从起点和终点**同时 BFS**，相遇即停',
        '搜索树规模从 O(b^d) 降到 **O(b^(d/2))** —— 指数级加速',
        '实现要点：每次**扩展较小的一侧**（`if len(front) > len(back): swap`）',
        '适用：起点终点都已知、分支因子较大的状态空间（如八数码、单词接龙）',
    ]),

    ('section', '第 3 节', '回溯法'),

    ('key', '⭐ 回溯三步框架',
     '做选择 → 递归 → 撤销选择\n结果要【深拷贝】：res.append(path[:])'),

    ('code', '回溯通用模板', '''def backtrack(path, choices):
    if is_solution(path):
        result.append(path[:])         # ⚠️ 必须拷贝
        return
    for choice in choices:
        if not is_valid(choice, path):
            continue                    # 剪枝
        path.append(choice)             # 做选择
        backtrack(path, next_choices)   # 递归
        path.pop()                      # 撤销选择
'''),

    ('code', 'LC 78 子集 / LC 39 组合总和', '''def subsets(nums):
    res, path = [], []

    def dfs(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return res


def combination_sum(candidates, target):
    candidates.sort()
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:]); return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                   # ⭐ 排序后剪枝
            path.append(candidates[i])
            dfs(i, remain - candidates[i])    # 可重复用 -> 传 i
            path.pop()

    dfs(0, target)
    return res
'''),

    ('key', '⭐ 去重口诀',
     '排序后，同一层中相同的值只取第一个\nif i > start and a[i] == a[i-1]: continue'),

    ('code', 'LC 47 全排列 II（含去重）', '''def permute_unique(nums):
    nums.sort()
    res, path = [], []
    used = [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:]); return
        for i, v in enumerate(nums):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue                # ⭐ 同层去重
            used[i] = True
            path.append(v)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return res
'''),

    ('code', 'OJ 02754 八皇后：O(1) 冲突检测', '''def solve_n_queens(n):
    res = []
    cols = [0] * n
    used_col = [False] * n
    used_diag1 = [False] * (2 * n)    # r - c + n  主对角线 ↘
    used_diag2 = [False] * (2 * n)    # r + c      副对角线 ↙

    def dfs(r):
        if r == n:
            res.append(cols[:]); return
        for c in range(n):
            if used_col[c] or used_diag1[r - c + n] or used_diag2[r + c]:
                continue                       # ⭐ O(1) 冲突检测
            cols[r] = c
            used_col[c] = used_diag1[r-c+n] = used_diag2[r+c] = True
            dfs(r + 1)
            used_col[c] = used_diag1[r-c+n] = used_diag2[r+c] = False

    dfs(0)
    return res


print(len(solve_n_queens(8)))       # 92
''', '同一主对角线上 r−c 相同，同一副对角线上 r+c 相同'),

    ('code', 'OJ 04123 马走日：回溯计数', '''MOVES = [(1, 2), (2, 1), (2, -1), (1, -2),
         (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def count_tours(n, m, x, y):
    visited = [[False] * m for _ in range(n)]
    visited[x][y] = True
    total = 0

    def dfs(i, j, cnt):
        nonlocal total
        if cnt == n * m:
            total += 1
            return
        for di, dj in MOVES:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj]:
                visited[ni][nj] = True
                dfs(ni, nj, cnt + 1)
                visited[ni][nj] = False      # ⭐ 回溯
    dfs(x, y, 1)
    return total
'''),

    ('bullets', 'OJ 28050 骑士周游：Warnsdorff 启发式', [
        'n = 8 时朴素回溯的搜索规模是天文数字，**必须剪枝**',
        '**Warnsdorff 规则**：每次优先走“后继可选步数最少”的格子',
        '`nxts.sort(key=lambda p: degree(*p))`',
        '这一行把近乎不可完成的搜索变成**近乎线性**',
    ]),

    ('table', '⭐ 剪枝技巧总结', [
        ['类型', '做法', '例子'],
        ['可行性剪枝', '当前状态已不可能合法，立即返回', 'remain < 0'],
        ['最优性剪枝', '当前代价已 ≥ 已知最优解', '分支限界'],
        ['排序剪枝', '先排序，遇到不满足即 break', 'candidates[i] > remain'],
        ['去重剪枝', '同层相同元素只取一次', 'LC 40 / 47'],
        ['对称性剪枝', '利用对称只搜一半', 'N 皇后第一行只搜前 n/2 列'],
        ['记忆化', '缓存已算过的状态', '记忆化搜索 = DP'],
        ['启发式排序', '优先扩展更有希望的分支', 'Warnsdorff、数独 MRV'],
    ], '一个好的剪枝往往带来指数级加速，比换语言、抠常数有效得多'),

    ('table', 'DFS vs BFS：怎么选', [
        ['需求', '选择'],
        ['求最短步数（边权都是 1）', '**BFS**'],
        ['求所有解 / 方案数', 'DFS + 回溯'],
        ['判断连通性 / 求连通块', '都行，DFS 代码更短'],
        ['状态空间巨大、只要一个解', 'DFS 或双向 BFS'],
        ['递归深度可能很大', 'BFS 或迭代式 DFS'],
        ['有权图最短路', '都不行 → Dijkstra（第 13 周）'],
    ]),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '最大连通域面积 / 岛屿数量', 'OJ 18160 / LC 200', '网格 DFS'],
        ['2', '寻宝', 'OJ 19930', '网格 BFS'],
        ['3', '01 矩阵 / 腐烂的橘子', 'LC 542 / 994', '多源 BFS、分层 BFS'],
        ['4', '词梯', 'OJ 28046', '状态空间 BFS + 建桶'],
        ['5', '全排列 II / 组合总和 II', 'LC 47 / 40', '回溯去重'],
        ['6', '八皇后', 'OJ 02754', '回溯 + O(1) 冲突检测'],
        ['7', '马走日', 'OJ 04123', '回溯计数'],
        ['8（选做）', '骑士周游 / 解数独', 'OJ 28050 / LC 37', '启发式剪枝'],
    ]),

    ('bullets', '本讲小结', [
        '搜索 = 在**解空间树**上遍历；DFS 用栈，BFS 用 `deque`',
        '⚠️ **入队 / 入栈时立刻标记 visited**，否则会重复扩展',
        'BFS 求无权图最短路；DFS + 回溯求所有解',
        '回溯三步：**做选择 → 递归 → 撤销**；结果要**深拷贝**',
        '**剪枝是搜索的灵魂**：可行性、最优性、去重、对称性、启发式',
        '**下周预告**：第一个非线性结构 —— 树',
    ]),
]
