# -*- coding: utf-8 -*-
"""第6周 递归与分治；排序"""

META = {
    'title': '第6周　递归、分治与排序',
    'subtitle': '递归三要素 · 分治框架 · 五大排序与性能对比',
    'footer': '数据结构与算法 · 第6周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握递归思想；掌握分治策略在排序中的应用；能进行算法性能对比'],
}

SLIDES = [
    ('bullets', '本讲内容', [
        '**递归**', '- 三要素、调用栈、重复子问题与记忆化、汉诺塔',
        '**分治法**', '- Divide / Conquer / Combine 三步框架',
        '**五大排序**', '- 冒泡、选择、插入、归并、快排',
        '**性能对比**', '- 稳定性、最坏情况、Timsort',
        '**经典应用**', '- 逆序对、快速选择、三路划分',
    ]),

    ('section', '第 1 节', '递归'),

    ('bullets', '递归三要素', [
        '**基线条件（base case）**：能直接求解的最小问题，必须存在',
        '**递归条件**：把问题**规模缩小**后调用自身',
        '**收敛性**：每次调用都必须朝基线条件逼近',
        '⚠️ 三者缺一，程序就会无限递归直到爆栈',
    ]),

    ('ascii', 'factorial(4) 的调用栈展开', r"""
factorial(4)
 └ 4 * factorial(3)
        └ 3 * factorial(2)
               └ 2 * factorial(1)
                      └ 1              <- 基线，开始回溯
               <- 2*1 = 2
        <- 3*2 = 6
 <- 4*6 = 24

递归深度 = 栈帧数 = 空间复杂度 O(n)
"""),

    ('ascii', '递归的代价：重复子问题', r"""
                fib(5)
            /            \
       fib(4)            fib(3)
      /     \           /     \
   fib(3)  fib(2)   fib(2)  fib(1)
   /   \    /  \     /  \
fib(2) f(1) f(1) f(0) f(1) f(0)

fib(2) 被算了 3 次，fib(3) 被算了 2 次  ->  O(2^n)
""", '朴素 def fib(n): return n if n<2 else fib(n-1)+fib(n-2) 是指数级的'),

    ('code', '记忆化：把 O(2ⁿ) 降到 O(n)', '''from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
''', '⭐ 记忆化递归 = 自顶向下的动态规划（第 7 周）'),

    ('code', '经典例题：汉诺塔', '''def hanoi(n, src, aux, dst, moves):
    if n == 0:
        return
    hanoi(n - 1, src, dst, aux, moves)      # 上面 n-1 个挪到 aux
    moves.append((n, src, dst))             # 最大的挪到 dst
    hanoi(n - 1, aux, src, dst, moves)      # n-1 个从 aux 挪到 dst


n = int(input())
moves = []
hanoi(n, 'A', 'B', 'C', moves)
print(len(moves))                            # 2^n - 1
''', 'T(n) = 2T(n-1) + 1 ⇒ 2ⁿ−1，指数级不可避免（输出本身就有 2ⁿ−1 行）'),

    ('code', '其他递归练习', '''def gcd(a, b):                        # 欧几里得，O(log min(a,b))
    return a if b == 0 else gcd(b, a % b)


def power(a, n):                      # 快速幂，O(log n)
    if n == 0:
        return 1
    half = power(a, n // 2)
    return half * half if n % 2 == 0 else half * half * a


def sum_nested(lst):                  # 嵌套列表求和
    total = 0
    for x in lst:
        total += sum_nested(x) if isinstance(x, list) else x
    return total
'''),

    ('section', '第 2 节', '分治法'),

    ('ascii', 'Divide / Conquer / Combine', r"""
                 problem(n)
                /          \
        problem(n/2)     problem(n/2)      <- Divide  分解
            |                 |
          solve             solve          <- Conquer 递归求解
             \               /
              \             /
               combine  O(f(n))            <- Combine 合并

复杂度递归式：  T(n) = a·T(n/b) + f(n)
"""),

    ('table', '常见递归式的解', [
        ['递归式', '解', '算法'],
        ['T(n) = T(n/2) + O(1)', 'O(log n)', '二分查找'],
        ['T(n) = 2T(n/2) + O(n)', 'O(n log n)', '归并排序'],
        ['T(n) = 2T(n/2) + O(1)', 'O(n)', '二叉树遍历'],
        ['T(n) = T(n/2) + O(n)', 'O(n)', '快速选择（平均）'],
        ['T(n) = 2T(n-1) + O(1)', 'O(2ⁿ)', '汉诺塔'],
    ]),

    ('key', '分治 vs 动态规划的分水岭',
     '子问题是否【重叠】\n归并排序的两半互不相干（分治）；斐波那契共享大量子问题（DP）'),

    ('section', '第 3 节', '五大排序算法'),

    ('code', '冒泡排序 O(n²)：相邻比较，大的往后冒', '''def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:        # 优化：已有序则提前退出
            break
    return a
''', '最好 O(n)（已有序 + 提前退出），平均/最坏 O(n²)；空间 O(1)，稳定'),

    ('code', '选择排序 O(n²)：每轮选最小放到已排序段末尾', '''def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a
''', '时间恒为 O(n²)（与输入无关），但交换次数只有 O(n)；不稳定'),

    ('code', '插入排序 O(n²)：像整理扑克牌', '''def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]      # 后移腾位置
            j -= 1
        a[j + 1] = key
    return a
''', '⭐ 最好 O(n)（已有序）；小数组上常数极小，是 Timsort 与快排的收尾手段'),

    ('code', '归并排序 O(n log n)：分治的典范', '''def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])            # Divide + Conquer
    right = merge_sort(a[mid:])
    return merge(left, right)             # Combine


def merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:           # <= 保证稳定性
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res
''', '稳定、复杂度有保证、可外部排序；代价是 O(n) 额外空间'),

    ('code', '⭐ 归并的经典应用：求逆序对（OJ 02299）', '''def sort_count(a):
    if len(a) <= 1:
        return a, 0
    mid = len(a) // 2
    left, cl = sort_count(a[:mid])
    right, cr = sort_count(a[mid:])
    merged, i, j, cnt = [], 0, 0, cl + cr
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            cnt += len(left) - i          # ⭐ 关键一行
    merged.extend(left[i:]); merged.extend(right[j:])
    return merged, cnt
''', '从右半取走一个元素时，左半剩余的所有元素都与它构成逆序对'),

    ('code', '快速排序：原地 Lomuto 划分 + 随机枢轴', '''import random


def partition(a, lo, hi):
    r = random.randint(lo, hi)          # ⭐ 随机化，规避有序数据的最坏情况
    a[r], a[hi] = a[hi], a[r]
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def quick_sort(a, lo=0, hi=None):
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        p = partition(a, lo, hi)
        quick_sort(a, lo, p - 1)
        quick_sort(a, p + 1, hi)
    return a
''', '平均 O(n log n)，最坏 O(n²)；空间 O(log n)，不稳定；常数最小'),

    ('code', '快速选择：求第 k 小，平均 O(n)', '''def quick_select(a, k):
    """返回第 k 小（k 从 1 开始）。只递归一侧。"""
    lo, hi = 0, len(a) - 1
    while True:
        p = partition(a, lo, hi)
        if p == k - 1:
            return a[p]
        if p < k - 1:
            lo = p + 1
        else:
            hi = p - 1
''', 'T(n) = T(n/2) + O(n) = O(n)　—— LC 215 数组中的第 K 个最大元素'),

    ('section', '第 4 节', '排序算法性能对比'),

    ('table', '⭐ 七种排序对比（必背）', [
        ['算法', '最好', '平均', '最坏', '空间', '稳定'],
        ['冒泡', 'O(n)', 'O(n²)', 'O(n²)', 'O(1)', '✅'],
        ['选择', 'O(n²)', 'O(n²)', 'O(n²)', 'O(1)', '❌'],
        ['插入', 'O(n)', 'O(n²)', 'O(n²)', 'O(1)', '✅'],
        ['希尔', 'O(n log n)', '~O(n^1.3)', 'O(n²)', 'O(1)', '❌'],
        ['归并', 'O(n log n)', 'O(n log n)', 'O(n log n)', 'O(n)', '✅'],
        ['快排', 'O(n log n)', 'O(n log n)', '⚠️ O(n²)', 'O(log n)', '❌'],
        ['堆排', 'O(n log n)', 'O(n log n)', 'O(n log n)', 'O(1)', '❌'],
    ]),

    ('bullets', '稳定性为什么重要', [
        '**稳定**：相等元素排序前后相对次序不变',
        '**多关键字排序依赖稳定性**：按次关键字排完，再按主关键字排即可',
        'Python 的 `sort` / `sorted` 是**稳定**的',
        '- `students.sort(key=lambda s: s[0])` 然后 `students.sort(key=lambda s: -s[1])`',
        '- 结果：按分数降序，同分者按名字升序',
    ]),

    ('bullets', 'Python 内建排序：Timsort', [
        '`list.sort()` / `sorted()` 使用 **Timsort** —— 归并 + 插入排序的混合体',
        '识别数据中已有序的 run，**近似有序的数据接近 O(n)**',
        '**稳定**，最坏 O(n log n)，且用 C 实现，常数远小于手写 Python 排序',
        '⭐ **OJ 实战准则**：除非题目要求手写，一律用 `sorted` / `.sort()`',
    ]),

    ('code', '性能对比实验（本周实验必做）', '''import random, time

for n in (1000, 2000, 4000, 8000):
    rnd = [random.randint(0, 10 ** 6) for _ in range(n)]
    srt = sorted(rnd)
    rev = srt[::-1]
    for name, fn in [('bubble', bubble_sort), ('insertion', insertion_sort),
                     ('merge', merge_sort), ('quick', quick_sort),
                     ('builtin', sorted)]:
        for tag, data in (('random', rnd), ('sorted', srt), ('rev', rev)):
            t0 = time.perf_counter()
            fn(data[:])
            print(f"n={n} {name:10s} {tag:7s} {time.perf_counter()-t0:.4f}s")
''', '需解释的现象：插入排序在已排序数据上为何快？归并为何三种输入耗时一致？'),

    ('code', 'LC 75 颜色分类：荷兰国旗（三路划分）', '''def sort_colors(nums):
    lo, i, hi = 0, 0, len(nums) - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1; i += 1
        elif nums[i] == 2:
            nums[hi], nums[i] = nums[i], nums[hi]
            hi -= 1                    # 换来的元素还没检查，i 不动
        else:
            i += 1
''', '一趟 O(n)，原地 O(1)。大量重复元素时，三路划分能显著加速快排'),

    ('code', 'LC 23 合并 K 个升序链表：分治两两归并', '''def merge_k_lists(lists):
    if not lists:
        return None
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            b = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge2(lists[i], b))
        lists = merged
    return lists[0]
''', 'T(n) = 2T(n/2) + O(n) ⇒ O(N log k)；逐个归并则是 O(Nk)，慢得多'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '汉诺塔问题', 'OJ 04147', '递归'],
        ['2', 'Ultra-QuickSort', 'OJ 02299', '归并求逆序对'],
        ['3', '数组中的第K个最大元素', 'LC 215', '快速选择 / 堆'],
        ['4', '合并K个升序链表', 'LC 23', '分治归并'],
        ['5', '颜色分类', 'LC 75', '三路划分'],
        ['6', '排序链表', 'LC 148', '链表归并排序'],
        ['7（选做）', '最大子数组和（分治版）', 'LC 53', '分治框架'],
    ], '实验三：完成性能对比实验并提交含图表的实验报告'),

    ('bullets', '本讲小结', [
        '递归三要素：基线条件、递归条件、收敛；空间代价是**调用栈**',
        '重复子问题用**记忆化**消除 —— 通向动态规划的桥梁',
        '分治三步：Divide / Conquer / Combine；用递归式 T(n)=aT(n/b)+f(n) 分析',
        '**归并**稳定可求逆序对；**快排**常数最小但需随机化',
        '**下周预告**：两大算法设计范式 —— 贪心与动态规划',
    ]),
]
