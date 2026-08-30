# -*- coding: utf-8 -*-
"""第2周 导论、ADT 与 OOP、Python 基础回顾"""

META = {
    'title': '第2周　导论、ADT 与 OOP',
    'subtitle': 'Python 基础回顾 · 抽象数据类型 · 面向对象',
    'footer': '数据结构与算法 · 第2周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》（48 学时 / 3 学分）',
             '教学要求：掌握数据结构的基本概念与分类；理解 ADT 与具体实现的'
             '分离原则；了解 Python 内建数据类型'],
}

SLIDES = [
    ('bullets', '本讲内容', [
        '**课程导航**', '- 我们要学什么、怎么考、用什么平台',
        '**数据结构的基本概念**', '- 逻辑结构、存储结构、算法的五个特性',
        '**抽象数据类型 ADT**', '- 接口与实现的分离原则',
        '**Python 基础回顾**', '- 内建容器的复杂度特征、常见性能陷阱',
        '**面向对象 OOP**', '- 封装、继承、多态、魔术方法',
    ]),

    ('section', '第 0 节', '课程导航', '我们要学什么，怎么考'),

    ('key', '为什么学数据结构与算法',
     '数据怎么存 + 问题怎么算\n= 在可接受的时间与空间内解决实际问题'),

    ('bullets', '课程定位', [
        'Linus Torvalds：“糟糕的程序员关心代码，优秀的程序员关心数据结构及其关系。”',
        '48 学时 = 理论 24 + 实验 12 + 实践 12，第 2–16 周授课，第 17 周上机考试',
        '**所有数据结构与算法均给出完整 Python 实现，而非伪代码**',
        '先修要求：《计算概论》或《程序设计基础》（Python 或 C++ 基础）',
        '坚持使用 C++ 的同学，课程同样支持',
    ]),

    ('ascii', '全课程知识地图', r"""
                        数据结构与算法
                              |
        +---------------------+---------------------+
        |                     |                     |
     线性结构               非线性结构             算法策略
        |                     |                     |
  +-----+-----+       +-------+-------+     +-------+--------+
  栈  队列  链表      树      图    散列    递归/分治  贪心  DP  搜索
  W4   W5    W5     W9-W11  W12-W14  W15      W6       W7   W7   W8
""", '本学期的四条主线：线性结构 → 非线性结构 → 算法策略 → 综合应用'),

    ('table', '考核方式', [
        ['考核项目', '占比', '说明'],
        ['平时作业', '30%', 'OpenJudge / LeetCode 编程题，考查 PEP 8 规范与提交纪律'],
        ['AI 辅助算法实践小项目', '10%', '完整项目一个，鼓励用大模型但须声明'],
        ['期末上机考试', '60%', '120 分钟 6 题，OJ 平台完成'],
    ], '⚠️ 上机考试禁止使用任何 AI 工具；无法解释自己提交代码者按学术不端处理'),

    ('section', '第 1 节', '数据结构的基本概念'),

    ('bullets', '刻画一个数据结构的四个层次', [
        '**逻辑结构**：数据元素之间的关系，与计算机无关',
        '**存储结构（物理结构）**：逻辑结构在内存中的映射方式',
        '**运算的定义**：这个结构支持哪些操作 —— 这就是 ADT 的内容',
        '**运算的实现**：具体算法与代码',
    ]),

    ('table', '逻辑结构的分类', [
        ['类别', '元素间关系', '例子'],
        ['集合结构', '除“同属一个集合”外无其他关系', 'set'],
        ['线性结构', '一对一', '数组、栈、队列、链表'],
        ['树形结构', '一对多', '二叉树、堆、字典树'],
        ['图状结构', '多对多', '有向图、无向图'],
    ]),

    ('table', '存储结构的分类', [
        ['存储方式', '特点', '优点', '缺点'],
        ['顺序存储', '元素放在连续地址', '随机访问 O(1)', '插入删除需搬移'],
        ['链式存储', '靠指针（引用）相连', '已知位置插删 O(1)', '不能随机访问'],
        ['索引存储', '附加索引表', '检索快', '索引占空间'],
        ['散列存储', '由关键字算出地址', '平均 O(1) 查找', '需处理冲突、无序'],
    ], '同一个逻辑结构可以有多种存储结构 —— 线性表既能用顺序表也能用链表实现'),

    ('bullets', '算法的五个特性', [
        '**有穷性**：有限步内结束',
        '**确定性**：每一步含义明确，无歧义',
        '**可行性**：每一步都能由基本运算完成',
        '**输入**：零个或多个；**输出**：一个或多个',
        '评价顺序：正确性 → 可读性 → 健壮性 → 时间/空间效率',
    ]),

    ('section', '第 2 节', '抽象数据类型（ADT）', '接口与实现的分离'),

    ('ascii', 'ADT：只说“能做什么”，不说“怎么做”', r"""
          使用者
            |
     +------v-------+   <-- 接口（ADT）：push / pop / peek / is_empty
     |   抽象屏障    |
     +------v-------+
       具体实现       <-- 数组？链表？使用者不需要知道
""", '信息隐藏（information hiding）：使用者只需记住接口，实现者可自由替换内部表示'),

    ('table', '例：栈 ADT 的接口', [
        ['操作', '语义'],
        ['Stack()', '创建空栈'],
        ['push(item)', '压入栈顶'],
        ['pop()', '弹出并返回栈顶元素'],
        ['peek()', '返回栈顶元素但不弹出'],
        ['is_empty() / size()', '是否为空 / 元素个数'],
    ]),

    ('code', '同一接口，两种实现', '''class StackByList:
    """用 list 尾部作为栈顶：push/pop 均摊 O(1)。"""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)          # O(1)

    def pop(self):
        return self._items.pop()          # O(1)


class StackByHead:
    """错误示范：用 list 头部作为栈顶。"""

    def push(self, item):
        self._items.insert(0, item)       # O(n)：要搬移所有元素

    def pop(self):
        return self._items.pop(0)         # O(n)
''', '接口完全一样，都能做括号匹配；但 n = 10⁵ 时第二个会超时'),

    ('key', '本课程的核心主题', '接口相同，效率可以差出一个数量级'),

    ('section', '第 3 节', 'Python 基础回顾'),

    ('table', '内建容器速查（务必记住）', [
        ['类型', '可变', '有序', '关键操作复杂度'],
        ['list', '✅', '✅', '索引 O(1)；尾部 append/pop 均摊 O(1)；insert(0,x) O(n)；in O(n)'],
        ['tuple', '❌', '✅', '索引 O(1)；不可变，可作字典键'],
        ['str', '❌', '✅', '拼接 O(n+m)；切片 O(k)'],
        ['dict', '✅', '插入序', '增删查平均 O(1)'],
        ['set', '✅', '❌', 'add / in / discard 平均 O(1)'],
    ], '⚠️ 最常见的性能陷阱：用 list 判存在（O(n)），应改用 set / dict'),

    ('code', '三个必须避开的写法', '''# ❌ O(n²)：list 判存在              # ✅ O(n)
seen = []                            seen = set()
for x in data:                       for x in data:
    if x not in seen:                    if x not in seen:
        seen.append(x)                       seen.add(x)

# ❌ O(n²)：循环拼接字符串           # ✅ O(total_len)
s = ''                               s = ''.join(words)
for w in words:
    s += w

# ❌ 三行是同一个列表对象！          # ✅ 正确
wrong = [[0] * m] * n                grid = [[0] * m for _ in range(n)]
''', '这三个陷阱会贯穿整个学期，OJ 上的 TLE 大多源于此'),

    ('code', 'OJ 上必须掌握的输入输出', '''import sys

n, m = map(int, input().split())            # 单行多个整数
a = list(map(int, input().split()))         # 一行整数变列表

data = sys.stdin.read().split()             # 大量输入：比 input() 快数倍
idx = 0
n = int(data[idx]); idx += 1

out = []                                    # 大量输出：先攒后打
for x in ans:
    out.append(str(x))
print('\\n'.join(out))

sys.setrecursionlimit(1 << 20)              # 深递归（W6/W8/W9 会用到）
''', '这一页请抄进你的 cheat sheet'),

    ('code', '常用标准库（贯穿全学期）', '''from collections import deque, defaultdict, Counter
import heapq, bisect, itertools, math, sys

deque()                 # 双端队列，两端 O(1)          —— W5
defaultdict(list)       # 带默认值的字典，建邻接表利器  —— W12
Counter(s)              # 计数                          —— W15
heapq.heappush/heappop  # 小根堆                        —— W10
bisect.bisect_left      # 有序数组二分                  —— W6 / W10
math.inf                # 正无穷，最短路初始化用        —— W13
'''),

    ('section', '第 4 节', '面向对象程序设计（OOP）'),

    ('key', '为什么数据结构课要讲 OOP',
     '数据结构 = 一坨数据 + 一组操作它的函数\n类 = 属性 + 方法　——　两者完全同构'),

    ('code', '类的基本骨架', '''class Node:
    """链表结点：数据结构中最基本的建筑材料。"""

    __slots__ = ('value', 'next')       # 省内存、防拼写错（可选）

    def __init__(self, value, nxt=None):
        self.value = value              # self 是实例本身
        self.next = nxt

    def __repr__(self):                 # 面向开发者（调试打印）
        return f"Node({self.value!r})"
'''),

    ('table', '常用魔术方法', [
        ['魔术方法', '触发场景'],
        ['__init__ / __repr__ / __str__', '构造 / 打印'],
        ['__len__ / __getitem__ / __contains__', 'len(obj) / obj[i] / x in obj'],
        ['__iter__', 'for x in obj'],
        ['__eq__', '== （重写后需同时给 __hash__ 才能放进 set）'],
        ['__lt__', '< ，被 sorted 和 heapq 使用'],
        ['__add__ / __sub__ / __mul__', '+ - *'],
    ]),

    ('code', '__lt__ 与堆、排序的配合（W10 会直接用到）', '''import heapq
from functools import total_ordering


@total_ordering                 # 只写 __eq__ 和 __lt__，自动补全 <= > >=
class Task:
    def __init__(self, priority, name):
        self.priority, self.name = priority, name

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority


h = []
for t in [Task(3, 'c'), Task(1, 'a'), Task(2, 'b')]:
    heapq.heappush(h, t)
print(heapq.heappop(h))         # Task(1, 'a')
'''),

    ('section', '第 5 节', '例题精讲'),

    ('code', '例1　OJ 27653 Fraction 类', '''import math


class Fraction:
    def __init__(self, num, den):
        if den == 0:
            raise ZeroDivisionError("分母不能为 0")
        if den < 0:                       # 规范化：负号放到分子
            num, den = -num, -den
        g = math.gcd(abs(num), den)
        if g:
            num, den = num // g, den // g
        self.num, self.den = num, den

    def __add__(self, other):
        return Fraction(self.num * other.den + other.num * self.den,
                        self.den * other.den)

    def __str__(self):
        return f"{self.num}/{self.den}"


a, b, c, d = map(int, input().split())
print(Fraction(a, b) + Fraction(c, d))
''', '要点：构造器里完成约分与符号规范化 —— 保证对象始终处于合法状态（类不变式）'),

    ('code', '例2　LC 155 最小栈：O(1) 取最小', '''class MinStack:
    def __init__(self):
        self._data = []
        self._mins = []          # _mins[i] = _data[:i+1] 的最小值

    def push(self, val: int) -> None:
        self._data.append(val)
        self._mins.append(val if not self._mins else min(val, self._mins[-1]))

    def pop(self) -> None:
        self._data.pop()
        self._mins.pop()

    def getMin(self) -> int:
        return self._mins[-1]        # O(1)
''', '思维方式：查询太慢时，考虑在“修改的时候顺手维护”额外信息'),

    ('key', '贯穿全课程的两个思想',
     '① 用空间换时间　　② 在修改时顺手维护信息，让查询变快'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', 'Fraction 类', 'OJ 27653', '类、运算符重载'],
        ['2', '两数之和', 'LC 1', 'dict 哈希'],
        ['3', '最小栈', 'LC 155', 'ADT 设计、辅助结构'],
        ['4', '有效的括号', 'LC 20', '栈（为第 4 周预热）'],
        ['5', '只出现一次的数字', 'LC 136', '位运算 / set'],
    ]),

    ('bullets', '本讲小结', [
        '数据结构 = 逻辑结构 + 存储结构 + 运算；**同一逻辑结构可有多种存储结构**',
        'ADT 把接口与实现分离，是本课程组织所有数据结构的统一框架',
        'Python 的 list / dict / set 各有复杂度特征，**选错容器就会超时**',
        '用类实现 ADT：__init__ 建立不变式，魔术方法提供自然语法',
        '**下周预告**：如何定量地说“这个实现比那个快”？—— 大 O 与复杂度分析',
    ]),
]
