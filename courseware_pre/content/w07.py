# -*- coding: utf-8 -*-
"""第7周 贪心与动态规划"""

META = {
    'title': '第7周　贪心与动态规划',
    'subtitle': '贪心选择性质 · 最优子结构 · 状态与转移方程',
    'footer': '数据结构与算法 · 第7周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握贪心选择性质与最优子结构；掌握动态规划的状态定义与状态转移方程设计'],
}

SLIDES = [
    ('table', '算法设计范式全景', [
        ['范式', '核心思想', '何时适用', '周次'],
        ['枚举 / 暴力', '遍历所有可能', '规模极小', 'W3'],
        ['分治', '分解为独立子问题', '子问题**不重叠**', 'W6'],
        ['贪心', '每步取局部最优', '有贪心选择性质', '**W7**'],
        ['动态规划', '记录并复用子问题解', '子问题**重叠** + 最优子结构', '**W7**'],
        ['回溯 / 搜索', '系统枚举 + 剪枝', '解空间树', 'W8'],
    ], '分治 vs DP 的分水岭：子问题是否重叠'),

    ('section', '第 1 节', '贪心算法'),

    ('bullets', '贪心正确的两个前提', [
        '**贪心选择性质**：全局最优解可以通过一系列局部最优选择达到',
        '**最优子结构**：做出贪心选择后，剩余子问题的最优解与该选择组合仍是全局最优',
        '⚠️ **贪心不总是对的**：面额 {1, 3, 4} 凑 6，贪心取 4+1+1 = 3 枚，最优是 3+3 = 2 枚',
        '**贪心的正确性必须证明**，常用交换论证（exchange argument）',
    ]),

    ('code', 'LC 435 无重叠区间：按右端点排序', '''def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])       # ⭐ 按结束时间排序
    count, end = 1, intervals[0][1]
    for s, e in intervals[1:]:
        if s >= end:                          # 不重叠，选它
            count += 1
            end = e
    return len(intervals) - count
''', '⚠️ 若按左端点或区间长度排序，都能构造出反例 —— 排序键的选择是考点'),

    ('key', '交换论证：为什么按右端点排序是对的',
     '设最优解的第一个区间是 X，我们选的是右端点最小的 A。\n'
     '把 X 换成 A：A 的右端点 ≤ X 的右端点，后面能选的区间只多不少'),

    ('code', 'LC 56 合并区间：这里按左端点排序', '''def merge(intervals):
    intervals.sort(key=lambda x: x[0])       # 注意与上一题不同
    res = []
    for s, e in intervals:
        if res and s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)  # 有交集，合并
        else:
            res.append([s, e])
    return res
'''),

    ('code', 'LC 55 / 45 跳跃游戏', '''def can_jump(nums):                # 能否到达终点
    reach = 0
    for i, v in enumerate(nums):
        if i > reach:
            return False           # 到不了 i
        reach = max(reach, i + v)
    return True


def jump(nums):                    # 最少跳跃次数
    steps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:               # 到达当前这一跳的边界
            steps += 1
            end = far
    return steps
'''),

    ('code', 'Huffman 编码：堆 + 贪心（第 10 周再讲堆）', '''import heapq


def huffman_cost(weights):
    """每次取权值最小的两个合并，合并代价为二者之和。"""
    heapq.heapify(weights)
    total = 0
    while len(weights) > 1:
        a = heapq.heappop(weights)
        b = heapq.heappop(weights)
        total += a + b
        heapq.heappush(weights, a + b)
    return total
''', '正确性：权值最小的两个字符一定在最深层且互为兄弟（否则交换可使 WPL 更小）'),

    ('bullets', '贪心的证明思路', [
        '**交换论证**：假设最优解与贪心解不同，找第一个分歧点，说明改成贪心不会更差',
        '**数学归纳**：证明“前 k 步贪心选择可扩展为最优解”',
        '**反证法**：假设贪心不是最优，推出矛盾',
        '⭐ 考场上时间紧时，至少要能**举出反例说明某贪心策略错误**',
    ]),

    ('section', '第 2 节', '动态规划'),

    ('bullets', 'DP 的两个必要条件', [
        '**最优子结构**：原问题的最优解包含子问题的最优解',
        '**重叠子问题**：递归求解时同一子问题被反复计算',
        '缺了重叠子问题，那是分治；缺了最优子结构，DP 也无从下手',
    ]),

    ('key', '⭐ DP 五步法（解题模板）',
     '① 确定状态　② 写转移方程　③ 初始条件与边界\n④ 确定计算顺序　⑤ 确定答案位置与空间优化'),

    ('table', '记忆化搜索 vs 递推', [
        ['', '记忆化搜索（自顶向下）', '递推（自底向上）'],
        ['思维难度', '低（照着递归写）', '中（要想清顺序）'],
        ['常数', '大（函数调用开销）', '小'],
        ['栈深风险', '可能爆栈', '无'],
        ['状态稀疏时', '⭐ 占优（只算需要的）', '全算'],
    ]),

    ('code', '线性 DP 三连：爬楼梯 / 打家劫舍 / LIS', '''def climb_stairs(n):               # LC 70: dp[i] = dp[i-1] + dp[i-2]
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def rob(nums):                     # LC 198: dp[i]=max(dp[i-1], dp[i-2]+v)
    prev, cur = 0, 0
    for v in nums:
        prev, cur = cur, max(cur, prev + v)
    return cur


def length_of_lis_n2(nums):        # LC 300: O(n^2)
    dp = [1] * len(nums)           # dp[i] = 以 nums[i] 结尾的 LIS 长度
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if dp else 0
'''),

    ('code', '⭐ LIS 的 O(n log n) 解法：贪心 + 二分', '''import bisect


def length_of_lis(nums):
    tails = []          # tails[k] = 长度为 k+1 的上升子序列的最小可能结尾
    for v in nums:
        i = bisect.bisect_left(tails, v)     # 严格上升用 bisect_left
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
    return len(tails)
''', '⚠️ tails 不是 LIS 本身，只是长度正确。非严格上升（允许相等）改用 bisect_right'),

    ('code', 'LC 1143 最长公共子序列（二维 DP 模板）', '''def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
''', 'dp[i][j] = s1[:i] 与 s2[:j] 的 LCS 长度；可用滚动数组压到 O(n) 空间'),

    ('code', 'LC 72 编辑距离', '''def min_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                # 全删
    for j in range(n + 1):
        dp[0][j] = j                # 全插
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # 删除
                                   dp[i][j - 1],      # 插入
                                   dp[i - 1][j - 1])  # 替换
    return dp[m][n]
'''),

    ('section', '第 3 节', '背包问题'),

    ('code', '01 背包：每件最多取一次', '''# 二维版本（便于理解）
dp = [[0] * (C + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for c in range(C + 1):
        dp[i][c] = dp[i - 1][c]                          # 不取第 i 件
        if c >= w[i - 1]:
            dp[i][c] = max(dp[i][c],
                           dp[i - 1][c - w[i - 1]] + v[i - 1])   # 取


# ⭐ 一维滚动版本（必须掌握）
dp = [0] * (C + 1)
for i in range(n):
    for c in range(C, w[i] - 1, -1):     # ⚠️ 容量倒序！
        dp[c] = max(dp[c], dp[c - w[i]] + v[i])
''', '为什么倒序？正序时 dp[c-w[i]] 已是本轮更新过的值 = 允许取多次 = 完全背包'),

    ('code', '完全背包：每件可取无限次 —— 容量正序', '''dp = [0] * (C + 1)
for i in range(n):
    for c in range(w[i], C + 1):         # ✅ 正序
        dp[c] = max(dp[c], dp[c - w[i]] + v[i])


# LC 322 零钱兑换：求最小件数
def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for c in coins:
        for x in range(c, amount + 1):
            dp[x] = min(dp[x], dp[x - c] + 1)
    return -1 if dp[amount] == INF else dp[amount]
'''),

    ('code', '⭐ 组合数 vs 排列数：只差循环顺序', '''def change(amount, coins):           # LC 518：组合数（不计顺序）
    dp = [1] + [0] * amount
    for c in coins:                  # 外层【物品】
        for x in range(c, amount + 1):
            dp[x] += dp[x - c]
    return dp[amount]


def combination_sum4(nums, target):  # LC 377：排列数（计顺序）
    dp = [1] + [0] * target
    for x in range(1, target + 1):   # 外层【容量】
        for v in nums:
            if v <= x:
                dp[x] += dp[x - v]
    return dp[target]
''', '口诀：01 倒序、完全正序；求组合数外层物品，求排列数外层容量'),

    ('table', '背包问题变形速查', [
        ['题型', '转移方程', '初始化'],
        ['最大价值', 'dp[c] = max(dp[c], dp[c-w]+v)', '全 0（可不装满）'],
        ['恰好装满判定', 'dp[c] = dp[c] or dp[c-w]', 'dp[0]=True'],
        ['方案数', 'dp[c] += dp[c-w]', 'dp[0]=1'],
        ['最少件数', 'dp[c] = min(dp[c], dp[c-w]+1)', 'dp[0]=0，其余 INF'],
    ]),

    ('code', 'LC 416 分割等和子集：恰好装满判定', '''def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for v in nums:
        for c in range(target, v - 1, -1):     # 01 背包 -> 倒序
            dp[c] = dp[c] or dp[c - v]
    return dp[target]
'''),

    ('bullets', '多重背包：二进制拆分', [
        '每件物品有 k 个：朴素做法拆成 k 个 01 物品，复杂度 O(nCk)',
        '**二进制拆分**：把 k 拆成 1, 2, 4, …，只需 **O(log k)** 个物品',
        '因为 1,2,4,…,2^m 的子集和能表示 0 到 2^(m+1)−1 的任意整数',
        '复杂度降到 O(nC log k)',
    ]),

    ('section', '第 4 节', '区间 DP 与选择策略'),

    ('code', 'LC 5 最长回文子串：按区间长度递增', '''def longest_palindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]     # dp[i][j] = s[i..j] 是否回文
    start, best = 0, 1
    for i in range(n):
        dp[i][i] = True
    for length in range(2, n + 1):            # ⭐ 区间长度从小到大
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] != s[j]:
                continue
            if length == 2 or dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > best:
                    start, best = i, length
    return s[start:start + best]
''', '石子合并同理：dp[i][j] = min(dp[i][k] + dp[k+1][j]) + sum(i..j)，O(n³)'),

    ('table', '贪心 vs DP：如何选择', [
        ['判据', '贪心', '动态规划'],
        ['需要回头考虑其他选择吗', '否', '是'],
        ['复杂度', '通常 O(n log n)（含排序）', '状态数 × 转移代价'],
        ['正确性', '**需要证明**', '状态定义正确即可'],
        ['典型信号', '“最少/最多个数”且有明显排序依据', '“方案数”“最值”且选择互相制约'],
    ], '考场判断法：先想贪心，立刻尝试构造反例；构造不出且能给出交换论证就用贪心'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '无重叠区间 / 合并区间', 'LC 435 / 56', '区间贪心'],
        ['2', '跳跃游戏 II', 'LC 45', '贪心'],
        ['3', '爬楼梯 / 打家劫舍', 'LC 70 / 198', '线性 DP'],
        ['4', '最长递增子序列', 'LC 300', 'LIS，O(n log n)'],
        ['5', '最长公共子序列 / 编辑距离', 'LC 1143 / 72', '二维 DP'],
        ['6', '分割等和子集', 'LC 416', '01 背包'],
        ['7', '零钱兑换 I / II', 'LC 322 / 518', '完全背包、组合数'],
        ['8（选做）', '最长回文子串', 'LC 5', '区间 DP'],
    ]),

    ('bullets', '本讲小结', [
        '贪心 = 局部最优 + 不回溯；**必须验证贪心选择性质**，最快方式是找反例',
        'DP 两前提：最优子结构 + 重叠子问题；核心难点是**状态定义**',
        '**DP 五步法**：状态 → 转移 → 初始化 → 顺序 → 答案与优化',
        '背包家族：01（**倒序**）、完全（**正序**）、多重（二进制拆分）',
        '**下周预告**：搜索专题 —— 把解空间当作一棵树来遍历',
    ]),
]
