# 第2周 导论、ADT 与 OOP、Python 基础回顾

*Updated 2026-08-30 10:00 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 2 周 / 3 学时
> **教学内容**：导论、ADT 与 OOP、Python 基础回顾
> **教学要求**：掌握数据结构的基本概念与分类；理解 ADT 与具体实现的分离原则；了解 Python 内建数据类型

**知识点**：数据结构的逻辑结构与存储结构、抽象数据类型（ADT）、算法的定义与要素、Python 内建容器（list / tuple / str / dict / set）、切片与推导式、面向对象三要素（封装 / 继承 / 多态）、魔术方法与运算符重载、`__lt__` 与排序/堆的配合、`dataclass`、快速输入输出。

---

# 0 课程导航

## 0.1 我们要学什么

《数据结构与算法》回答两个问题：

1. **数据怎么存**——用什么结构组织数据，才能让后续操作快？
2. **问题怎么算**——用什么策略处理数据，才能在可接受的时间和空间内得到答案？

一句被反复引用的话（Linus Torvalds）：

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

本课程 48 学时（理论 24 + 实验 12 + 实践 12），第 2–16 周授课，第 17 周期末上机考试。全部数据结构与算法均给出**完整 Python 实现**，而不是伪代码。

## 0.2 全课程知识地图

```
                        数据结构与算法
                              |
        +---------------------+---------------------+
        |                     |                     |
     线性结构               非线性结构             算法策略
        |                     |                     |
  +-----+-----+       +-------+-------+     +-------+--------+
  栈  队列  链表      树      图    散列    递归/分治  贪心  DP  搜索
  W4   W5    W5     W9-W11  W12-W14  W15      W6       W7   W7   W8
```

| 周次 | 主题 | 关键词 |
| ---- | ---- | ---- |
| W2 | 导论、ADT 与 OOP | ADT、封装、魔术方法 |
| W3 | 算法分析 | 大 O、复杂度级别、内建结构性能 |
| W4 | 栈 | LIFO、括号匹配、调度场算法 |
| W5 | 队列、双端队列、链表 | FIFO、顺序表 vs 链表 |
| W6 | 递归与分治、排序 | 归并、快排、逆序对 |
| W7 | 贪心与动态规划 | 最优子结构、状态转移 |
| W8 | 搜索专题 | DFS/BFS、回溯、剪枝 |
| W9 | 树与二叉树遍历 | 前中后序、层序、建树 |
| W10 | 堆、堆排序、二叉搜索树 | heapq、BST |
| W11 | AVL 树、并查集 | 旋转、路径压缩 |
| W12 | 图的表示与遍历 | 邻接表、连通分量 |
| W13 | 最短路 | Dijkstra、Bellman-Ford、Floyd |
| W14 | 最小生成树、拓扑排序 | Prim、Kruskal、Kahn |
| W15 | 散列表、KMP、倒排索引 → RAG | 哈希冲突、next 数组 |
| W16 | 总结与复习 | 知识体系、考点 |
| W17 | 期末上机考试 | 120 分钟 6 题 |

## 0.3 考核方式

| 项目 | 占比 | 说明 |
| ---- | ---- | ---- |
| 平时作业 | 30% | OpenJudge / LeetCode 编程题，考查 PEP 8 代码规范与提交纪律 |
| AI 辅助算法实践小项目 | 10% | 完整项目一个，鼓励使用大模型但**必须声明** |
| 期末上机考试 | 60% | 120 分钟，6 道算法编程题，OJ 平台完成 |

> ⚠️ 上机考试**禁止使用任何 AI 工具**；无法解释自己提交代码者按学术不端处理。

## 0.4 平台与环境

- OpenJudge：http://cs101.openjudge.cn/
- LeetCode 热题 100：https://leetcode.cn/studyplan/top-100-liked/
- 语言：以 Python 3 为主，坚持用 C++ 的同学课程同样支持。
- 环境搭建见仓库中 `Python_Development_Setup_Mac_Windows.md`。

---

# 1 数据结构的基本概念与分类

## 1.1 四个层次

一个数据结构可以从四个层次刻画：

1. **逻辑结构**：数据元素之间的关系，与计算机无关。
2. **存储结构（物理结构）**：逻辑结构在内存中的映射方式。
3. **运算的定义**：这个结构支持哪些操作（这是 ADT 的内容）。
4. **运算的实现**：具体算法与代码。

## 1.2 逻辑结构的分类

| 类别 | 元素间关系 | 例子 |
| ---- | ---- | ---- |
| 集合结构 | 除"同属一个集合"外无其他关系 | `set` |
| 线性结构 | 一对一 | 数组、栈、队列、链表 |
| 树形结构 | 一对多 | 二叉树、堆、字典树 |
| 图状结构 | 多对多 | 有向图、无向图 |

## 1.3 存储结构的分类

| 存储方式 | 特点 | 优点 | 缺点 |
| ---- | ---- | ---- | ---- |
| 顺序存储 | 元素放在连续地址 | 随机访问 O(1) | 插入/删除需搬移，扩容代价 |
| 链式存储 | 靠指针（引用）相连 | 插入/删除 O(1)（已知位置） | 不能随机访问，额外指针开销 |
| 索引存储 | 附加索引表 | 检索快 | 索引占空间，维护成本 |
| 散列存储 | 由关键字算出地址 | 平均 O(1) 查找 | 需处理冲突，无序 |

> **同一个逻辑结构可以有多种存储结构**。例如"线性表"既可以用顺序存储（Python 的 `list`）实现，也可以用链式存储（链表）实现，二者的操作复杂度截然不同——这是第 5 周的核心内容。

## 1.4 算法的五个特性

1. **有穷性**：有限步内结束。
2. **确定性**：每一步含义明确，无歧义。
3. **可行性**：每一步都能由基本运算完成。
4. **输入**：零个或多个。
5. **输出**：一个或多个。

评价一个算法：**正确性 → 可读性 → 健壮性 → 时间/空间效率**。效率分析是第 3 周内容。

---

# 2 抽象数据类型（ADT）

## 2.1 什么是 ADT

**抽象数据类型 = 数据的逻辑模型 + 定义在其上的一组操作**，它只规定"能做什么"（What），不规定"怎么做"（How）。

这正是软件工程中的**信息隐藏（information hiding）**原则：

```
          使用者
            |
     +------v-------+   <-- 接口（ADT）：push / pop / peek / is_empty
     |   抽象屏障    |
     +------v-------+
       具体实现       <-- 数组？链表？使用者不需要知道
```

**为什么要分离？**

- 使用者只需记住接口，心智负担小。
- 实现者可以自由替换内部实现（比如把数组换成链表），不影响使用者代码。
- 便于测试：接口固定，实现可对拍。

## 2.2 一个例子：栈 ADT

| 操作 | 语义 |
| ---- | ---- |
| `Stack()` | 创建空栈 |
| `push(item)` | 压入栈顶 |
| `pop()` | 弹出并返回栈顶元素 |
| `peek()` | 返回栈顶元素但不弹出 |
| `is_empty()` | 是否为空 |
| `size()` | 元素个数 |

同一份接口，可以有两种实现：

```python
class StackByList:
    """用 Python list 的尾部作为栈顶：push/pop 均摊 O(1)。"""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def size(self):
        return len(self._items)


class StackByHead:
    """错误示范：用 list 头部作为栈顶，push/pop 都是 O(n)。"""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.insert(0, item)   # O(n)：要搬移所有元素

    def pop(self):
        return self._items.pop(0)     # O(n)

    def peek(self):
        return self._items[0]

    def is_empty(self):
        return not self._items

    def size(self):
        return len(self._items)
```

两个类**接口完全一样**，都能用来做括号匹配；但第二个在 n = 10^5 时会超时。

> 这就是本课程反复出现的主题：**接口相同，效率可以差出一个数量级**。

---

# 3 Python 基础回顾

## 3.1 内建容器速查

| 类型 | 可变 | 有序 | 典型用途 | 关键操作复杂度 |
| ---- | ---- | ---- | ---- | ---- |
| `list` | ✅ | ✅ | 顺序表、栈 | 索引 O(1)，尾部 append/pop 均摊 O(1)，`insert(0,x)`/`pop(0)` O(n)，`in` O(n) |
| `tuple` | ❌ | ✅ | 不可变记录、可作字典键 | 索引 O(1) |
| `str` | ❌ | ✅ | 文本 | 拼接 O(n+m)，切片 O(k) |
| `dict` | ✅ | 插入序 | 映射、计数、记忆化 | 平均 O(1) 增删查 |
| `set` | ✅ | ❌ | 去重、判重 | 平均 O(1) `in` |

⚠️ **最常见的性能陷阱**：用 `list` 判存在（`x in lst` 是 O(n)），应改用 `set`/`dict`。

```python
# 慢：O(n*m)
seen = []
for x in data:
    if x not in seen:
        seen.append(x)

# 快：O(n)
seen = set()
for x in data:
    if x not in seen:
        seen.add(x)
```

## 3.2 切片、解包与推导式

```python
a = [3, 1, 4, 1, 5, 9, 2, 6]

a[2:5]        # [4, 1, 5]      左闭右开
a[::-1]       # 反转（新建列表，O(n)）
a[::2]        # 步长 2
b = a[:]      # 浅拷贝

first, *rest = a          # 解包：first=3, rest=[1,4,1,5,9,2,6]
x, y = y, x               # 交换，无需临时变量

squares = [i * i for i in range(10) if i % 2 == 0]      # 列表推导
index = {v: i for i, v in enumerate(a)}                 # 字典推导
uniq = {abs(v) for v in a}                              # 集合推导
gen = (i * i for i in range(10 ** 6))                   # 生成器：惰性、省内存
```

## 3.3 二维数组的正确创建方式

```python
n, m = 3, 4
grid = [[0] * m for _ in range(n)]     # ✅ 正确

wrong = [[0] * m] * n                  # ❌ n 行是同一个列表对象的引用！
wrong[0][0] = 1
print(wrong)   # [[1,0,0,0], [1,0,0,0], [1,0,0,0]]  —— 全被改了
```

## 3.4 常用标准库

```python
from collections import deque, defaultdict, Counter
import heapq, bisect, itertools, math, sys

deque()                 # 双端队列，两端 O(1)（第 5 周）
defaultdict(list)       # 带默认值的字典，建邻接表利器（第 12 周）
Counter(s)              # 计数
heapq.heappush/heappop  # 小根堆（第 10 周）
bisect.bisect_left      # 有序数组二分（第 6、10 周）
math.inf                # 正无穷，最短路初始化用（第 13 周）
```

## 3.5 输入输出：OJ 上必须掌握的写法

```python
import sys

# 单行多个整数
n, m = map(int, input().split())

# 一行若干整数变列表
a = list(map(int, input().split()))

# 大量输入时用 sys.stdin（比 input() 快数倍）
data = sys.stdin.read().split()
idx = 0
n = int(data[idx]); idx += 1

# 大量输出时先攒起来再一次性打印
out = []
for x in ans:
    out.append(str(x))
print('\n'.join(out))
```

**多组数据、读到文件尾**：

```python
import sys
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    # 处理一行
```

**递归深度**（第 6、8、9 周会用到）：

```python
import sys
sys.setrecursionlimit(1 << 20)
```

---

# 4 面向对象程序设计（OOP）

## 4.1 为什么数据结构课要讲 OOP

数据结构的本质是"一坨数据 + 一组只允许通过它们操作这坨数据的函数"。这与"类 = 属性 + 方法"完全同构。用类实现 ADT，能天然地把内部表示藏在 `_` 开头的私有属性里，只暴露接口。

## 4.2 类的基本骨架

```python
class Node:
    """链表结点：数据结构中最基本的建筑材料。"""

    __slots__ = ('value', 'next')     # 省内存、防拼写错（可选）

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt

    def __repr__(self):
        return f"Node({self.value!r})"
```

- `__init__` 是构造器，`self` 是实例本身。
- `__repr__` 面向开发者（调试打印），`__str__` 面向用户（`print` 优先用它）。

## 4.3 封装：属性访问控制

```python
class Temperature:
    def __init__(self, celsius=0.0):
        self._celsius = celsius       # 单下划线：约定为内部使用

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self):             # 只读的派生属性
        return self._celsius * 9 / 5 + 32


t = Temperature(25)
print(t.fahrenheit)     # 77.0
t.celsius = 30          # 走 setter，有校验
```

## 4.4 继承与多态

```python
class Shape:
    def area(self):
        raise NotImplementedError("子类必须实现 area")

    def describe(self):
        return f"{type(self).__name__} 的面积是 {self.area():.2f}"


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2


for s in [Rectangle(3, 4), Circle(1)]:
    print(s.describe())      # 同一句调用，行为随对象类型而变 —— 多态
```

## 4.5 运算符重载：常用魔术方法

| 魔术方法 | 触发场景 |
| ---- | ---- |
| `__init__` | 构造 |
| `__repr__` / `__str__` | 打印 |
| `__len__` | `len(obj)` |
| `__getitem__` / `__setitem__` | `obj[i]` |
| `__contains__` | `x in obj` |
| `__iter__` | `for x in obj` |
| `__eq__` | `==`（重写后需同时给 `__hash__` 才能放进 set） |
| `__lt__` | `<`，被 `sorted` 和 `heapq` 使用 |
| `__add__` / `__sub__` / `__mul__` | `+` `-` `*` |

**`__lt__` 与堆、排序的配合**（第 10 周排序建堆时会直接用到）：

```python
import heapq
from functools import total_ordering


@total_ordering                 # 只写 __eq__ 和 __lt__，自动补全 <= > >=
class Task:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task({self.priority}, {self.name!r})"


h = []
for t in [Task(3, 'c'), Task(1, 'a'), Task(2, 'b')]:
    heapq.heappush(h, t)
print(heapq.heappop(h))    # Task(1, 'a')
```

## 4.6 dataclass：少写样板代码

```python
from dataclasses import dataclass, field


@dataclass(order=True)
class Point:
    x: int = 0
    y: int = 0

    def dist2(self):
        return self.x ** 2 + self.y ** 2


p = Point(3, 4)
print(p)                 # Point(x=3, y=4)   自动生成 __repr__
print(p == Point(3, 4))  # True              自动生成 __eq__
print(sorted([Point(2, 1), Point(1, 9)]))    # order=True 自动生成比较
```

---

# 5 例题精讲

## 5.1 例题一：实现分数类 Fraction

**27653: Fraction 类**，http://cs101.openjudge.cn/practice/27653/

> 输入四个整数 `a b c d`，表示两个分数 a/b 与 c/d，输出它们的和（最简分数，形如 `p/q`）。

这道题是 OOP 的经典练手题：把"分数"抽象为一个类，重载 `+` 和 `__str__`。

```python
import math


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

    def __sub__(self, other):
        return Fraction(self.num * other.den - other.num * self.den,
                        self.den * other.den)

    def __mul__(self, other):
        return Fraction(self.num * other.num, self.den * other.den)

    def __eq__(self, other):
        return self.num == other.num and self.den == other.den

    def __lt__(self, other):
        return self.num * other.den < other.num * self.den

    def __str__(self):
        return f"{self.num}/{self.den}"

    __repr__ = __str__


a, b, c, d = map(int, input().split())
print(Fraction(a, b) + Fraction(c, d))
```

**要点**：
1. 在构造器里就完成"约分 + 符号规范化"，保证任何时刻对象都处于合法状态——这叫**类不变式（class invariant）**。
2. `__add__` 返回**新对象**而不是修改自身，符合不可变值语义。

## 5.2 例题二：用 ADT 思维设计一个"最小栈"

**LeetCode 155. 最小栈**，https://leetcode.cn/problems/min-stack/

> 设计一个栈，支持 push、pop、top，并能在**常数时间**内检索到最小元素。

朴素做法：每次求最小遍历一遍，O(n)。正确做法：**辅助栈同步记录前缀最小值**。

```python
class MinStack:
    def __init__(self):
        self._data = []
        self._mins = []          # _mins[i] = _data[:i+1] 的最小值

    def push(self, val: int) -> None:
        self._data.append(val)
        self._mins.append(val if not self._mins else min(val, self._mins[-1]))

    def pop(self) -> None:
        self._data.pop()
        self._mins.pop()

    def top(self) -> int:
        return self._data[-1]

    def getMin(self) -> int:
        return self._mins[-1]
```

四个操作全部 O(1)，空间 O(n)。

> **思维方式**：当"查询"太慢时，考虑在**修改的时候顺手维护**一些额外信息。这是贯穿整门课的核心思想（前缀和、堆、并查集、线段树都是它的变体）。

## 5.3 例题三：Python 内建类型的正确使用

**LeetCode 1. 两数之和**，https://leetcode.cn/problems/two-sum/

```python
class Solution:
    def twoSum(self, nums, target):
        pos = {}                       # 值 -> 下标
        for i, v in enumerate(nums):
            if target - v in pos:      # dict 查找平均 O(1)
                return [pos[target - v], i]
            pos[v] = i
        return []
```

暴力双重循环是 O(n²)，用字典把"查找配对值"从 O(n) 降到 O(1)，整体 O(n)。**用空间换时间**是算法设计最常见的一步棋。

---

# 6 代码规范（PEP 8 要点）

平时作业的一部分分数用于考查代码规范：

- 缩进 4 个空格，不用 Tab。
- 变量与函数用 `snake_case`，类名用 `CamelCase`，常量用 `UPPER_CASE`。
- 运算符两侧、逗号后加空格：`a = b + c`，`f(x, y)`。
- 每行不超过 79（或团队约定的 100）字符。
- 函数/类写 docstring 说明用途。
- 不要写 `l`、`O` 这类易混变量名。

```python
# ✅ 推荐
def merge_sort(arr: list[int]) -> list[int]:
    """返回 arr 的升序副本，时间 O(n log n)。"""
    ...

# ❌ 不推荐
def MS(A):
    ...
```

---

# 7 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | Fraction 类 | OJ 27653 | 类、运算符重载 |
| 2 | 两数之和 | LC 1 | dict 哈希 |
| 3 | 最小栈 | LC 155 | ADT 设计、辅助结构 |
| 4 | 有效的括号 | LC 20 | 栈（为第 4 周预热） |
| 5 | 只出现一次的数字 | LC 136 | 位运算 / set |

**思考题**：

1. `StackByList` 和 `StackByHead` 接口一致，请分别用 n = 10⁵ 次 push/pop 实测运行时间，解释差距来源。
2. 为什么重写了 `__eq__` 的类，如果不重写 `__hash__`，就不能放进 `set`？
3. `[[0]*m]*n` 为什么是错的？画出内存引用图说明。

---

# 8 小结

1. 数据结构 = 逻辑结构 + 存储结构 + 运算；同一逻辑结构可有多种存储结构，效率不同。
2. ADT 把"接口"与"实现"分离，是本课程组织所有数据结构的统一框架。
3. Python 的 `list`/`dict`/`set` 各有其复杂度特征，选错容器就会超时。
4. 用类来实现 ADT：`__init__` 建立不变式，魔术方法提供自然语法，`_` 前缀隐藏内部表示。

**下周预告**：如何**定量**地说"这个实现比那个快"？——大 O 记法与算法复杂度分析。
