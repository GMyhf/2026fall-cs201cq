# 第8周 搜索专题：DFS / BFS、回溯与剪枝

*Updated 2026-08-30 12:00 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 8 周 / 3 学时
> **教学内容**：搜索专题：DFS/BFS 回溯与剪枝
> **教学要求**：掌握 DFS/BFS 回溯搜索的实现与剪枝

**知识点**：解空间树、DFS（递归 / 显式栈）、BFS（队列 / 层序）、visited 标记、网格四连通与八连通、回溯法框架（选择—递归—撤销）、剪枝（可行性 / 最优性 / 对称性）、排列 / 组合 / 子集、N 皇后、数独、Flood Fill、连通块、最短步数 BFS、双向 BFS、记忆化搜索。

---

# 1 搜索的统一视角：解空间树

任何搜索问题都可以看作在一棵**解空间树**上行走：

- **结点** = 一个状态（棋盘布局、当前路径、走到的格子…）
- **边** = 一次决策（放一个皇后、走一步、选或不选一个元素）
- **叶子** = 一个完整解（或死路）

两种遍历方式：

| | DFS 深度优先 | BFS 广度优先 |
| ---- | ---- | ---- |
| 数据结构 | 栈（递归） | 队列 `deque` |
| 走法 | 一条路走到黑，再回头 | 一层一层扩展 |
| 空间 | O(深度) | O(该层宽度) |
| 擅长 | 求所有解、路径枚举、连通性 | **最短步数**、层级信息 |
| 找到的第一个解 | 不保证最短 | **保证最短**（边权全为 1 时） |

```
             起点
           /  |  \
         A    B    C          DFS: 起点 A D E B ...
        / \        |          BFS: 起点 A B C D E ...
       D   E       F
```

---

# 2 DFS 深度优先搜索

## 2.1 递归框架

```python
def dfs(state):
    if is_goal(state):
        record(state)
        return
    for nxt in next_states(state):
        if not visited(nxt):
            mark(nxt)
            dfs(nxt)
            unmark(nxt)        # 回溯时撤销（若需要）
```

## 2.2 网格 DFS：连通块

**OJ 18160: 最大连通域面积**，http://cs101.openjudge.cn/practice/18160/

> 给定 n×m 的字符矩阵，`W` 表示连通域内的格子，求最大连通域（**八连通**）的面积。

```python
import sys
sys.setrecursionlimit(1 << 20)

DIRS8 = [(-1, -1), (-1, 0), (-1, 1),
         (0, -1),           (0, 1),
         (1, -1),  (1, 0),  (1, 1)]


def dfs(grid, i, j, n, m):
    """返回从 (i,j) 出发能到达的连通域面积，边访问边置空防重复。"""
    if not (0 <= i < n and 0 <= j < m) or grid[i][j] != 'W':
        return 0
    grid[i][j] = '.'                    # 就地标记，省一个 visited 数组
    area = 1
    for di, dj in DIRS8:
        area += dfs(grid, i + di, j + dj, n, m)
    return area


data = sys.stdin.read().split()
p = 0
T = int(data[p]); p += 1
for _ in range(T):
    n, m = int(data[p]), int(data[p + 1]); p += 2
    grid = [list(data[p + r]) for r in range(n)]; p += n
    best = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'W':
                best = max(best, dfs(grid, i, j, n, m))
    print(best)
```

**四连通版本**只需把 `DIRS8` 换成：

```python
DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
```

**相关题目**：LC 200 岛屿数量、LC 695 岛屿的最大面积、OJ 02386 Lake Counting。

## 2.3 迭代式 DFS（避免爆栈）

```python
def dfs_iter(grid, si, sj, n, m):
    stack = [(si, sj)]
    grid[si][sj] = '.'
    area = 0
    while stack:
        i, j = stack.pop()
        area += 1
        for di, dj in DIRS8:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 'W':
                grid[ni][nj] = '.'      # 入栈时就标记，避免重复入栈
                stack.append((ni, nj))
    return area
```

> ⚠️ **标记时机**：入栈/入队时立刻标记，而不是出栈时——否则同一个格子会被重复压入，退化成指数级。

## 2.4 Flood Fill

**LeetCode 733. 图像渲染**，https://leetcode.cn/problems/flood-fill/

```python
def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    n, m = len(image), len(image[0])

    def fill(i, j):
        if not (0 <= i < n and 0 <= j < m) or image[i][j] != old:
            return
        image[i][j] = color
        for di, dj in DIRS4:
            fill(i + di, j + dj)

    fill(sr, sc)
    return image
```

---

# 3 BFS 广度优先搜索

## 3.1 标准框架

```python
from collections import deque


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
```

## 3.2 网格最短路

**OJ 19930: 寻宝**，http://cs101.openjudge.cn/practice/19930/

> 从 (0,0) 出发，`1` 可走、`2` 是宝藏、`0` 是障碍，求最少步数，走不到输出 `NO`。

```python
from collections import deque

DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

m, n = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(m)]

if grid[0][0] == 0:
    print("NO")
else:
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
                    q.clear()
                    break
                grid[ni][nj] = 0
                q.append((ni, nj, d + 1))
    print(ans if ans >= 0 else "NO")
```

## 3.3 分层 BFS（按层处理）

有时需要知道"当前在第几层"，或对整层做处理：

```python
def bfs_by_level(start, neighbors):
    q = deque([start])
    visited = {start}
    level = 0
    while q:
        for _ in range(len(q)):         # 固定住本层的大小
            cur = q.popleft()
            for nxt in neighbors(cur):
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        level += 1
    return level
```

## 3.4 多源 BFS

多个起点同时入队，一次 BFS 求"到最近源点的距离"。

**LeetCode 542. 01 矩阵**，https://leetcode.cn/problems/01-matrix/

```python
def update_matrix(mat):
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    q = deque()
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                dist[i][j] = 0
                q.append((i, j))        # 所有 0 一起作为源点入队
    while q:
        i, j = q.popleft()
        for di, dj in DIRS4:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and dist[ni][nj] < 0:
                dist[ni][nj] = dist[i][j] + 1
                q.append((ni, nj))
    return dist
```

**相关**：LC 994 腐烂的橘子（多源 + 分层）。

## 3.5 状态空间 BFS

状态不一定是网格坐标，也可以是任意可哈希对象。

**LeetCode 127. 单词接龙 / OJ 28046: 词梯**，http://cs101.openjudge.cn/practice/28046/

```python
from collections import deque, defaultdict


def word_ladder(begin, end, word_list):
    words = set(word_list)
    if end not in words:
        return 0
    # 建"桶"：hot -> _ot, h_t, ho_   加速找相邻单词
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
```

> **建桶技巧**把"两两比较是否只差一个字母"的 O(N²L) 降到 O(NL)，是本题的关键优化。

## 3.6 双向 BFS

从起点和终点同时 BFS，相遇即停。搜索树规模从 O(b^d) 降到 O(b^(d/2))。

```python
def bidirectional_bfs(start, goal, neighbors):
    if start == goal:
        return 0
    front, back = {start}, {goal}
    visited = {start, goal}
    steps = 0
    while front and back:
        if len(front) > len(back):
            front, back = back, front     # 总是扩展较小的一侧
        steps += 1
        nxt_layer = set()
        for cur in front:
            for nxt in neighbors(cur):
                if nxt in back:
                    return steps
                if nxt not in visited:
                    visited.add(nxt)
                    nxt_layer.add(nxt)
        front = nxt_layer
    return -1
```

---

# 4 回溯法

## 4.1 三步框架：选择 → 递归 → 撤销

```python
def backtrack(path, choices):
    if is_solution(path):
        result.append(path[:])         # ⚠️ 必须拷贝
        return
    for choice in choices:
        if not is_valid(choice, path):
            continue                    # 剪枝
        path.append(choice)             # 做选择
        backtrack(path, next_choices)   # 递归
        path.pop()                      # 撤销选择
```

## 4.2 子集

**LeetCode 78. 子集**，https://leetcode.cn/problems/subsets/

```python
def subsets(nums):
    res, path = [], []

    def dfs(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return res
```

## 4.3 组合（含去重）

**LeetCode 39/40. 组合总和 I / II**

```python
def combination_sum(candidates, target):
    candidates.sort()
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                   # 剪枝：排序后后面只会更大
            path.append(candidates[i])
            dfs(i, remain - candidates[i])    # 可重复用同一元素 -> 传 i
            path.pop()

    dfs(0, target)
    return res


def combination_sum2(candidates, target):
    """每个元素只能用一次，且解集不含重复组合。"""
    candidates.sort()
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue                # ⚠️ 同层去重
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            dfs(i + 1, remain - candidates[i])
            path.pop()

    dfs(0, target)
    return res
```

> **去重口诀**：排序后，**同一层**中相同的值只取第一个（`i > start and a[i] == a[i-1]` 则跳过）。

## 4.4 全排列

**LeetCode 46/47. 全排列 I / II**

```python
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, v in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(v)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return res


def permute_unique(nums):
    nums.sort()
    res, path = [], []
    used = [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, v in enumerate(nums):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue                # 同层去重：前一个相同元素未被使用
            used[i] = True
            path.append(v)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return res
```

## 4.5 N 皇后

**OJ 02754: 八皇后 / LeetCode 51**

```python
def solve_n_queens(n):
    res = []
    cols = [0] * n            # cols[r] = 第 r 行皇后所在列
    used_col = [False] * n
    used_diag1 = [False] * (2 * n)    # r - c + n
    used_diag2 = [False] * (2 * n)    # r + c

    def dfs(r):
        if r == n:
            res.append(cols[:])
            return
        for c in range(n):
            if used_col[c] or used_diag1[r - c + n] or used_diag2[r + c]:
                continue                       # O(1) 冲突检测
            cols[r] = c
            used_col[c] = used_diag1[r - c + n] = used_diag2[r + c] = True
            dfs(r + 1)
            used_col[c] = used_diag1[r - c + n] = used_diag2[r + c] = False

    dfs(0)
    return res


solutions = solve_n_queens(8)
print(len(solutions))       # 92
```

**关键剪枝**：用三个布尔数组把"是否冲突"的判断从 O(n) 降到 **O(1)**。
- 同一主对角线（↘）上 `r - c` 相同。
- 同一副对角线（↙）上 `r + c` 相同。

**OJ 02754 八皇后**要求按字典序输出第 b 个解：

```python
solutions = solve_n_queens(8)
strs = sorted(''.join(str(c + 1) for c in s) for s in solutions)
n = int(input())
for _ in range(n):
    print(strs[int(input()) - 1])
```

## 4.6 马走日 / 骑士周游

**OJ 04123: 马走日**，http://cs101.openjudge.cn/practice/04123/

```python
import sys

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2),
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
                visited[ni][nj] = False      # 回溯

    dfs(x, y, 1)
    return total


T = int(input())
for _ in range(T):
    n, m, x, y = map(int, input().split())
    print(count_tours(n, m, x, y))
```

**OJ 28050: 骑士周游**（n=8 需要 Warnsdorff 启发式剪枝）：

> **Warnsdorff 规则**：每次优先走"后继可选步数最少"的格子。这把一个天文数字级的搜索变成近乎线性。

```python
def knight_tour(n, sr, sc):
    visited = [[False] * n for _ in range(n)]

    def degree(i, j):
        return sum(1 for di, dj in MOVES
                   if 0 <= i + di < n and 0 <= j + dj < n
                   and not visited[i + di][j + dj])

    def dfs(i, j, cnt):
        visited[i][j] = True
        if cnt == n * n:
            return True
        nxts = [(i + di, j + dj) for di, dj in MOVES
                if 0 <= i + di < n and 0 <= j + dj < n
                and not visited[i + di][j + dj]]
        nxts.sort(key=lambda p: degree(*p))      # Warnsdorff 启发式
        for ni, nj in nxts:
            if dfs(ni, nj, cnt + 1):
                return True
        visited[i][j] = False
        return False

    return dfs(sr, sc, 1)
```

## 4.7 数独

**LeetCode 37. 解数独**，https://leetcode.cn/problems/sudoku-solver/

```python
def solve_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties = []

    for i in range(9):
        for j in range(9):
            ch = board[i][j]
            if ch == '.':
                empties.append((i, j))
            else:
                rows[i].add(ch); cols[j].add(ch)
                boxes[i // 3 * 3 + j // 3].add(ch)

    def dfs(k):
        if k == len(empties):
            return True
        i, j = empties[k]
        b = i // 3 * 3 + j // 3
        for ch in '123456789':
            if ch in rows[i] or ch in cols[j] or ch in boxes[b]:
                continue
            board[i][j] = ch
            rows[i].add(ch); cols[j].add(ch); boxes[b].add(ch)
            if dfs(k + 1):
                return True
            board[i][j] = '.'
            rows[i].discard(ch); cols[j].discard(ch); boxes[b].discard(ch)
        return False

    dfs(0)
```

**进阶剪枝（MRV, Minimum Remaining Values）**：每次优先填"候选数最少"的空格，可把耗时降低一到两个数量级。

> 本仓库中的 `game_Sudoku.py` 就实现了一个带回溯求解器的数独游戏，可以对照阅读。

---

# 5 剪枝技巧总结

| 类型 | 做法 | 例子 |
| ---- | ---- | ---- |
| **可行性剪枝** | 当前状态已不可能合法，立即返回 | 组合总和中 `remain < 0` |
| **最优性剪枝** | 当前代价已 ≥ 已知最优解 | 分支限界、最优装载 |
| **排序剪枝** | 先排序，遇到不满足即 `break` | `candidates[i] > remain: break` |
| **去重剪枝** | 同层相同元素只取一次 | LC 40 / 47 |
| **对称性剪枝** | 利用对称只搜一半 | N 皇后第一行只搜前 n/2 列 |
| **记忆化** | 缓存已算过的状态 | 记忆化搜索 = DP |
| **启发式排序** | 优先扩展更有希望的分支 | Warnsdorff、MRV |

**剪枝的性价比**：一个好的剪枝往往能带来指数级的加速，比换语言、抠常数有效得多。

---

# 6 DFS vs BFS：怎么选

| 需求 | 选择 |
| ---- | ---- |
| 求**最短步数**（边权都是 1） | **BFS** |
| 求**所有解 / 方案数** | DFS + 回溯 |
| 判断**连通性 / 求连通块** | 都行，DFS 代码更短 |
| 状态空间巨大、只要一个解 | DFS（可能更快撞到解）或双向 BFS |
| 递归深度可能很大 | BFS 或迭代式 DFS（防爆栈） |
| 有权图最短路 | 都不行 → Dijkstra（第 13 周） |

---

# 7 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 最大连通域面积 | OJ 18160 | 网格 DFS，八连通 |
| 2 | 岛屿数量 | LC 200 | Flood Fill |
| 3 | 寻宝 | OJ 19930 | 网格 BFS |
| 4 | 01 矩阵 | LC 542 | 多源 BFS |
| 5 | 腐烂的橘子 | LC 994 | 分层 BFS |
| 6 | 词梯 | OJ 28046 | 状态空间 BFS + 建桶 |
| 7 | 全排列 II | LC 47 | 回溯去重 |
| 8 | 组合总和 II | LC 40 | 回溯去重 + 剪枝 |
| 9 | 八皇后 | OJ 02754 | 回溯 + O(1) 冲突检测 |
| 10 | 马走日 | OJ 04123 | 回溯计数 |
| 11（选做） | 骑士周游 | OJ 28050 | Warnsdorff 启发式 |
| 12（选做） | 解数独 | LC 37 | 回溯 + 约束传播 |

**思考题**：

1. BFS 中"入队时标记 visited"和"出队时标记"有什么区别？后者会导致什么后果？
2. 为什么 BFS 能保证最短路，而 DFS 不能？如果边权不全为 1 呢？
3. LC 47 的去重条件写成 `used[i-1]` 为 True 时跳过，还对吗？为什么？
4. 估算 8×8 骑士周游不加剪枝的搜索规模，说明 Warnsdorff 为什么有效。

---

# 8 小结

1. 搜索 = 在**解空间树**上遍历；DFS 用栈（递归），BFS 用队列（`deque`）。
2. **入队/入栈时立刻标记 visited**，否则会重复扩展。
3. BFS 求无权图最短路；DFS + 回溯求所有解。
4. 回溯三步：**做选择 → 递归 → 撤销选择**；结果要**深拷贝**。
5. 剪枝是搜索的灵魂：可行性、最优性、去重、对称性、启发式。

**下周预告**：第一个非线性结构——**树**，以及二叉树的各种遍历。
