# -*- coding: utf-8 -*-
"""第3周 算法分析：大 O、复杂度级别、Python 内建结构性能"""

META = {
    'title': '第3周　算法分析',
    'subtitle': '大 O 记法 · 复杂度级别 · Python 内建结构性能',
    'footer': '数据结构与算法 · 第3周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握渐近符号衡量算法效率的方法；能够分析简单算法的时间复杂度'],
}

SLIDES = [
    ('bullets', '本讲内容', [
        '**为什么需要复杂度分析**', '- 计时测量的局限；从操作计数到增长函数',
        '**渐近记号**', '- 大 O / 大 Ω / 大 Θ；化简规则',
        '**常见复杂度级别**', '- 从 O(1) 到 O(n!)；数据范围反推算法',
        '**Python 内建结构性能**', '- list / dict / set / deque / str 的操作代价',
        '**空间复杂度与递归式**', '- 调用栈开销；分治复杂度的递归树',
    ]),

    ('section', '第 1 节', '为什么需要复杂度分析'),

    ('bullets', '计时测量靠不住', [
        '实测运行时间受**机器、语言、编译器、系统负载**影响，无法跨环境比较',
        '同一份代码在你的笔记本和 OJ 服务器上可能差 5 倍',
        '我们需要一种**与机器无关**的度量',
        '**做法**：数一数算法执行了多少次“基本操作”，考察它随输入规模 n 如何增长',
    ]),

    ('code', '从计数到函数', '''def sum_of_n(n):
    total = 0                 # 1 次赋值
    for i in range(1, n + 1): # 循环 n 次
        total = total + i     # 每次 1 次加法 + 1 次赋值
    return total

# 基本操作次数 T(n) = 1 + 2n
''', 'n = 10⁶ 时，常数 1 与系数 2 都无关紧要 —— 决定量级的是 n 这一项，故 T(n) = O(n)'),

    ('section', '第 2 节', '渐近记号'),

    ('key', '大 O 的定义',
     '若存在正常数 c 与 n₀，使得对所有 n ≥ n₀ 都有 T(n) ≤ c·g(n)，\n'
     '则记 T(n) = O(g(n))'),

    ('table', '三种渐近记号', [
        ['记号', '含义', '直观理解'],
        ['O(g)', '上界', 'T 的增长不快于 g'],
        ['Ω(g)', '下界', 'T 的增长不慢于 g'],
        ['Θ(g)', '紧确界', 'T 与 g 同阶（既是 O 又是 Ω）'],
    ], '严格说“归并排序是 Θ(n log n)”，但工程与竞赛中习惯统一写 O(n log n)'),

    ('bullets', '化简规则', [
        '**去掉常系数**：O(3n) = O(n)',
        '**只保留最高阶项**：O(n² + 100n + 5000) = O(n²)',
        '**顺序结构取最大**：先 O(n) 再 O(n²)，总体 O(n²)',
        '**嵌套循环取乘积**：外层 n 次、内层 m 次 ⇒ O(nm)',
        '**对数的底数无关紧要**：log₂n 与 log₁₀n 只差常数倍，统一写 log n',
    ]),

    ('code', '课堂练习：判断下面各段的复杂度', '''for i in range(n):            # O(n)
    for j in range(n):        # O(n)
        ...                   # 总计 O(n^2)

for i in range(n):
    for j in range(i):        # 平均 n/2
        ...                   # n(n-1)/2 = O(n^2)

i = 1
while i < n:                  # i = 1,2,4,8,...
    i *= 2                    # 执行 log2(n) 次 -> O(log n)

for i in range(n):
    j = 1
    while j < n:
        j *= 2                # 内层 O(log n) -> 总计 O(n log n)
'''),

    ('section', '第 3 节', '常见复杂度级别'),

    ('table', '复杂度阶梯', [
        ['复杂度', '名称', '典型算法', 'n=10⁶ 时操作数'],
        ['O(1)', '常数', '数组随机访问、哈希查找', '1'],
        ['O(log n)', '对数', '二分查找、平衡树单次操作', '20'],
        ['O(n)', '线性', '遍历、前缀和', '10⁶'],
        ['O(n log n)', '线性对数', '归并 / 快排 / 堆排', '2×10⁷'],
        ['O(n²)', '平方', '冒泡 / 选择 / 插入排序', '10¹² ❌'],
        ['O(n³)', '立方', 'Floyd-Warshall', '10¹⁸ ❌'],
        ['O(2ⁿ) / O(n!)', '指数 / 阶乘', '子集枚举 / 全排列', '天文数字'],
    ]),

    ('ascii', '增长速度对比', r"""
时间
 ^                                  2^n   n^2
 |                                 /     /
 |                                /     /        n log n
 |                               /     /        /
 |                              /     /       /          n
 |                             /    /      /        ____/
 |                            /   /    __/    _____/
 |                           / _/ __--/ _____/            log n
 |                        _--=--==------------------------------
 +--------------------------------------------------------------> n
"""),

    ('table', '⭐ 数据范围反推算法（考场第一步）', [
        ['n 的范围', '可接受复杂度', '常见做法'],
        ['n ≤ 10–12', 'O(n!)', '全排列枚举'],
        ['n ≤ 20–25', 'O(2ⁿ)', '子集枚举、状压 DP、折半搜索'],
        ['n ≤ 100', 'O(n³)', 'Floyd、区间 DP'],
        ['n ≤ 1000–2000', 'O(n²)', '二维 DP、朴素图算法'],
        ['n ≤ 10⁵', 'O(n log n)', '排序、堆、二分、Dijkstra'],
        ['n ≤ 10⁶–10⁷', 'O(n)', '双指针、单调栈、前缀和'],
        ['n ≥ 10⁸', 'O(log n) / O(1)', '数学公式、快速幂'],
    ], 'Python 每秒约 10⁷ 量级简单操作，C++ 约 10⁸–10⁹ —— 读完题先看 n 的范围'),

    ('bullets', '最好、最坏与平均情况', [
        '以顺序查找为例：**最好** O(1)（第一个命中）、**最坏** O(n)、**平均** O(n)',
        '若无特别说明，**算法复杂度默认指最坏情况**',
        '**快速排序是著名例外**：最坏 O(n²)，平均 O(n log n)',
        '- 通过随机化枢轴，使最坏情况几乎不会发生（第 6 周详述）',
    ]),

    ('section', '第 4 节', '均摊分析与内建结构性能'),

    ('bullets', '为什么 list.append 算 O(1)', [
        'Python 的 list 是**动态数组**：容量满了就申请更大的一块，把旧元素搬过去',
        '单次 append 若触发扩容是 O(n)，但扩容不是每次都发生',
        '从容量 1 增长到 n，总搬移次数约 1+2+4+…+n < 2n',
        '**n 次 append 总代价 O(n)，均摊每次 O(1)** —— 这叫均摊分析',
    ]),

    ('table', 'list 的操作复杂度', [
        ['操作', '复杂度', '说明'],
        ['a[i] / a[i] = x / len(a)', 'O(1)', '随机访问，长度被缓存'],
        ['a.append(x) / a.pop()', '均摊 O(1)', '尾部操作'],
        ['a.pop(0) / a.insert(0, x)', '⚠️ O(n)', '要搬移后续所有元素'],
        ['x in a', '⚠️ O(n)', '应改用 set'],
        ['a.sort()', 'O(n log n)', 'Timsort，近似有序时接近 O(n)'],
        ['a[i:j] / a + b', 'O(j-i) / O(n+m)', '切片与拼接都是拷贝'],
    ]),

    ('table', 'dict / set / deque / str', [
        ['结构', '操作', '复杂度'],
        ['dict', 'd[k] / d[k]=v / del / k in d', '平均 O(1)，最坏 O(n)'],
        ['set', 'add / in / discard', '平均 O(1)'],
        ['deque', 'append / appendleft / pop / popleft', '⭐ 全部 O(1)'],
        ['deque', 'd[i]（中间随机访问）', 'O(n)'],
        ['str', 's += t（循环中）', '⚠️ O(n²)，应改用 join'],
    ], 'BFS 一定要用 deque —— 用 list.pop(0) 会把 O(n) 的 BFS 变成 O(n²)'),

    ('code', '实测对比（本周实验必做）', '''import timeit

N = 100000

t_list = timeit.timeit('a.pop(0)',
                       setup=f'a = list(range({N}))', number=N // 10)

t_deque = timeit.timeit('a.popleft()',
                        setup=f'from collections import deque; '
                              f'a = deque(range({N}))', number=N // 10)

print(f"list.pop(0)    : {t_list:.4f}s")
print(f"deque.popleft(): {t_deque:.4f}s")   # 通常快 2~3 个数量级
''', '亲手测一遍，把“复杂度”从概念变成肌肉记忆'),

    ('section', '第 5 节', '空间复杂度与递归式'),

    ('code', '空间复杂度：统计输入之外的额外存储', '''def total(a):              # 空间 O(1)：只用了常数个变量
    s = 0
    for x in a:
        s += x
    return s


def doubled(a):            # 空间 O(n)：新建了等长列表
    return [x * 2 for x in a]


def rec_sum(a, i=0):       # 空间 O(n)：递归深度 n，每层一个栈帧
    if i == len(a):
        return 0
    return a[i] + rec_sum(a, i + 1)
''', '⚠️ 递归的空间代价常被忽略：深度 n 的递归占用 O(n) 调用栈，Python 默认上限 1000'),

    ('table', '分治递归式速查', [
        ['递归式', '解', '例子'],
        ['T(n) = T(n/2) + O(1)', 'O(log n)', '二分查找'],
        ['T(n) = T(n/2) + O(n)', 'O(n)', '快速选择（平均）'],
        ['T(n) = 2T(n/2) + O(1)', 'O(n)', '二叉树遍历'],
        ['T(n) = 2T(n/2) + O(n)', 'O(n log n)', '归并排序'],
        ['T(n) = 2T(n-1) + O(1)', 'O(2ⁿ)', '汉诺塔'],
    ]),

    ('ascii', '递归树直观法：归并排序', r"""
层号     子问题规模     子问题个数     本层总代价
 0          n              1             n
 1         n/2             2             n
 2         n/4             4             n
 ...                                    ...
log n       1              n             n
                                   ------------
                     共 log n + 1 层，每层 n  =>  O(n log n)
"""),

    ('section', '第 6 节', '例题精讲'),

    ('code', '例1　LC 303 区域和检索：前缀和', '''class NumArray:
    def __init__(self, nums):
        self.pre = [0] * (len(nums) + 1)
        for i, v in enumerate(nums):
            self.pre[i + 1] = self.pre[i] + v   # pre[i] = nums[0..i-1] 之和

    def sumRange(self, left: int, right: int) -> int:
        return self.pre[right + 1] - self.pre[left]
''', '朴素做法每次查询 O(n)，q 次共 O(nq)；预处理后单次 O(1)，总计 O(n+q)'),

    ('code', '例2　LC 53 最大子数组和：从 O(n³) 到 O(n)', '''def brute3(a):                     # O(n^3)
    return max(sum(a[i:j + 1])
               for i in range(len(a)) for j in range(i, len(a)))


def brute2(a):                     # O(n^2)：滚动累加，省掉 sum
    best = a[0]
    for i in range(len(a)):
        cur = 0
        for j in range(i, len(a)):
            cur += a[j]
            best = max(best, cur)
    return best


def kadane(a):                     # O(n)
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)      # 要么接在前面，要么从 x 重新开始
        best = max(best, cur)
    return best
''', '三个版本答案相同，n = 10⁵ 时只有第三个能过 —— 复杂度就是能不能过题的分水岭'),

    ('code', '例3　LC 704 二分查找：O(log n)', '''def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2       # Python 大整数不会溢出
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


import bisect
i = bisect.bisect_left(a, x)       # 第一个 >= x
j = bisect.bisect_right(a, x)      # 第一个 > x
cnt = j - i                        # x 出现次数
'''),

    ('code', '课堂练习：判断复杂度', '''# (1)
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            pass                    # 答：C(n,3) = O(n^3)

# (2)
i = n
while i > 0:
    for j in range(i):
        pass
    i //= 2                         # 答：n + n/2 + n/4 + ... = O(n)

# (3)
res = []
for x in a:
    res.insert(0, x)                # 答：1+2+...+n = O(n^2)
                                    # 应改成 append 后 reverse
'''),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '区域和检索 - 数组不可变', 'LC 303', '前缀和，O(1) 查询'],
        ['2', '最大子数组和', 'LC 53', 'O(n) 线性扫描'],
        ['3', '二分查找', 'LC 704', 'O(log n)'],
        ['4', '搜索插入位置', 'LC 35', '二分边界'],
        ['5', '移动零', 'LC 283', '双指针 O(n) 原地'],
    ], '实验一：对 n = 10³~10⁶ 实测四组对比，双对数坐标作图，验证斜率与理论复杂度一致'),

    ('bullets', '本讲小结', [
        '大 O 描述**增长趋势**，忽略常数与低阶项；选型先看阶，再抠常数',
        '复杂度阶梯：1 < log n < n < n log n < n² < n³ < 2ⁿ < n!',
        '**拿到题先看 n 的范围**，反推允许的复杂度，再选算法',
        'Python 三大 TLE 来源：`list.pop(0)`、`x in list`、循环 `str +=`',
        '**下周预告**：第一个真正的数据结构 —— 栈',
    ]),
]
