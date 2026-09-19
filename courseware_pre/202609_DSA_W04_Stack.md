# 第4周 栈：ADT、实现、括号匹配、进制转换、调度场算法

*Updated 2026-08-30 10:40 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 4 周 / 3 学时
> **教学内容**：栈：ADT、实现、括号匹配、进制转换、调度场算法
> **教学要求**：掌握栈的 LIFO 特性；能够实现栈并解决括号匹配问题；表达式转换算法

**知识点**：栈 ADT 与 LIFO、顺序栈实现、括号匹配、进制转换、中缀 / 前缀 / 后缀表达式、调度场算法（Shunting Yard）、后缀表达式求值、合法出栈序列、单调栈、递归与系统栈。

---

# 1 栈 ADT

## 1.1 LIFO：后进先出

栈是一种**只允许在一端（栈顶 top）进行插入和删除**的线性表。像一摞盘子：最后放上去的最先被拿走。

```
        push(4)                pop() -> 4
   |  |          | 4|              |  |
   | 3|   ==>    | 3|     ==>      | 3|
   | 2|          | 2|              | 2|
   | 1|          | 1|              | 1|
   +--+          +--+              +--+
   栈底在下，栈顶在上
```

## 1.2 接口定义

| 操作 | 语义 | 复杂度 |
| ---- | ---- | ---- |
| `Stack()` | 创建空栈 | O(1) |
| `push(item)` | 入栈 | 均摊 O(1) |
| `pop()` | 出栈并返回栈顶 | O(1) |
| `peek()` / `top()` | 查看栈顶不弹出 | O(1) |
| `is_empty()` | 判空 | O(1) |
| `size()` | 元素个数 | O(1) |

## 1.3 顺序栈的完整实现

```python
class Stack:
    """基于 Python list 尾部的顺序栈，所有操作均摊 O(1)。"""

    def __init__(self, iterable=None):
        self._items = list(iterable) if iterable else []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return bool(self._items)

    def __repr__(self):
        return f"Stack(bottom->top: {self._items})"
```

> **实战约定**：OJ 上通常**直接用 `list`** 当栈（`append` / `pop` / `[-1]`），不必包装成类——代码更短、常数更小。课堂上写类是为了理解 ADT。

## 1.4 定长数组实现（了解）

若语言不提供动态数组（如 C 中的静态数组），栈用"数组 + 栈顶指针 top"实现：

```python
class ArrayStack:
    def __init__(self, capacity):
        self._data = [None] * capacity
        self._top = -1                    # 栈顶下标，-1 表示空

    def push(self, item):
        if self._top + 1 == len(self._data):
            raise OverflowError("stack overflow")
        self._top += 1
        self._data[self._top] = item

    def pop(self):
        if self._top < 0:
            raise IndexError("stack underflow")
        item = self._data[self._top]
        self._data[self._top] = None
        self._top -= 1
        return item
```

**上溢（overflow）**与**下溢（underflow）**是顺序栈的两类边界错误。

---

# 2 应用一：括号匹配

## 2.1 单一括号

**LeetCode 20. 有效的括号**，https://leetcode.cn/problems/valid-parentheses/

> 给定只包含 `()[]{}` 的字符串，判断括号是否有效配对。

**思路**：左括号入栈；遇右括号时检查栈顶是否为对应的左括号。

```python
def is_valid(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack          # 结束时必须为空
```

时间 O(n)，空间 O(n)。

**三个易错点**：
1. 遇右括号时栈已空 → 无效。
2. 栈顶不匹配 → 无效。
3. 扫描结束栈非空（有左括号没闭合）→ 无效。

## 2.2 输出不匹配位置

**OJ 03704: 括号匹配问题**，http://cs101.openjudge.cn/practice/03704/

> 给一行含 `(`、`)` 与其他字符的字符串，在下一行对应位置输出：多余的左括号标 `$`，多余的右括号标 `?`，其余为空格。

```python
import sys

for line in sys.stdin:
    line = line.rstrip('\n')
    if not line:
        continue
    mark = [' '] * len(line)
    stack = []                       # 存放未匹配左括号的下标
    for i, ch in enumerate(line):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            if stack:
                stack.pop()          # 配对成功
            else:
                mark[i] = '?'        # 多余的右括号
    for i in stack:
        mark[i] = '$'                # 多余的左括号
    print(line)
    print(''.join(mark))
```

**关键改造**：栈里存的不是括号字符，而是**下标**——这样才能回过头去标记位置。

## 2.3 最长有效括号（进阶）

**LeetCode 32. 最长有效括号**，https://leetcode.cn/problems/longest-valid-parentheses/

```python
def longest_valid(s: str) -> int:
    stack = [-1]              # 栈底放一个"上一个未匹配右括号的位置"
    best = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if stack:
                best = max(best, i - stack[-1])
            else:
                stack.append(i)      # 重新设定基准
    return best
```

---

# 3 应用二：进制转换

## 3.1 十进制转任意进制

**原理**：反复除基取余，余数**逆序**输出——正好是栈的用武之地。

```python
DIGITS = "0123456789ABCDEF"


def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    neg, n = n < 0, abs(n)
    stack = []
    while n > 0:
        stack.append(DIGITS[n % base])
        n //= base
    if neg:
        stack.append('-')
    return ''.join(reversed(stack))


print(to_base(233, 2))    # 11101001
print(to_base(233, 8))    # 351
print(to_base(233, 16))   # E9
```

**OJ 02734: 十进制到八进制**，http://cs101.openjudge.cn/practice/02734/

```python
n = int(input())
print(oct(n)[2:] if n else 0)      # Python 内建：bin/oct/hex
```

内建函数：`bin(n)` → `'0b...'`，`oct(n)` → `'0o...'`，`hex(n)` → `'0x...'`；反向用 `int(s, base)`。

## 3.2 任意进制互转

```python
def convert(s: str, src_base: int, dst_base: int) -> str:
    return to_base(int(s, src_base), dst_base)


print(convert("ff", 16, 2))     # 11111111
```

---

# 4 应用三：表达式的三种表示与调度场算法

## 4.1 中缀、前缀、后缀

对表达式 `(1 + 2) * 3`：

| 形式 | 写法 | 特点 |
| ---- | ---- | ---- |
| 中缀 infix | `( 1 + 2 ) * 3` | 人类习惯，需要括号和优先级规则 |
| 前缀 prefix（波兰式） | `* + 1 2 3` | 运算符在前，无需括号 |
| 后缀 postfix（逆波兰式 RPN） | `1 2 + 3 *` | 运算符在后，无需括号，**最易被机器求值** |

> 三种形式其实是同一棵**表达式树**的前序、中序、后序遍历结果（第 9 周会回到这一点）。

```
        *
       / \
      +   3        前序: * + 1 2 3
     / \           中序: 1 + 2 * 3  (需加括号还原)
    1   2          后序: 1 2 + 3 *
```

## 4.2 调度场算法（Shunting Yard）：中缀 → 后缀

由 Dijkstra 提出。维护一个**运算符栈**和一个**输出队列**：

1. 遇操作数：直接输出。
2. 遇左括号 `(`：入栈。
3. 遇右括号 `)`：不断弹栈输出，直到遇到 `(`，弹掉 `(` 不输出。
4. 遇运算符 op：当栈顶是运算符且**优先级 ≥ op**（左结合时）或 **> op**（右结合时），弹出并输出；然后 op 入栈。
5. 扫描结束：把栈中剩余运算符全部弹出输出。

**OJ 24591: 中序表达式转后序表达式**，http://cs101.openjudge.cn/practice/24591/

```python
import sys


PREC = {'+': 1, '-': 1, '*': 2, '/': 2}


def tokenize(expr: str):
    """把字符串切成 token：数字（可能多位/含小数点）与运算符。"""
    tokens, i, n = [], 0, len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == '.':
            j = i
            while j < n and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            tokens.append(ch)
            i += 1
    return tokens


def infix_to_postfix(tokens):
    output, ops = [], []
    for tk in tokens:
        if tk not in PREC and tk not in '()':
            output.append(tk)                    # 操作数
        elif tk == '(':
            ops.append(tk)
        elif tk == ')':
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            ops.pop()                            # 弹掉 '('
        else:                                    # 运算符，均为左结合
            while ops and ops[-1] != '(' and PREC[ops[-1]] >= PREC[tk]:
                output.append(ops.pop())
            ops.append(tk)
    while ops:
        output.append(ops.pop())
    return output


n = int(input())
for _ in range(n):
    print(' '.join(infix_to_postfix(tokenize(input().strip()))))
```

**手工模拟** `( 1 + 2 ) * 3` ：

| 读入 | 运算符栈 | 输出 |
| ---- | ---- | ---- |
| `(` | `(` | |
| `1` | `(` | `1` |
| `+` | `( +` | `1` |
| `2` | `( +` | `1 2` |
| `)` | | `1 2 +` |
| `*` | `*` | `1 2 +` |
| `3` | `*` | `1 2 + 3` |
| 结束 | | `1 2 + 3 *` |

## 4.3 后缀表达式求值

**OJ 02694: 波兰表达式**（前缀）与 **LeetCode 150. 逆波兰表达式求值**（后缀）。

后缀求值极其简单：**操作数入栈，遇运算符弹两个算完再入栈**。

```python
def eval_postfix(tokens):
    stack = []
    for tk in tokens:
        if tk in '+-*/':
            b = stack.pop()          # 注意顺序：先弹的是右操作数
            a = stack.pop()
            if tk == '+':
                stack.append(a + b)
            elif tk == '-':
                stack.append(a - b)
            elif tk == '*':
                stack.append(a * b)
            else:
                stack.append(a / b)
        else:
            stack.append(float(tk))
    return stack[-1]
```

前缀（波兰式）求值：**从右往左**扫描，规则对称：

```python
# OJ 02694 波兰表达式
def eval_prefix(tokens):
    stack = []
    for tk in reversed(tokens):
        if tk in '+-*/':
            a = stack.pop()          # 从右往左，先弹的是左操作数
            b = stack.pop()
            stack.append({'+': a + b, '-': a - b,
                          '*': a * b, '/': a / b if b else 0}[tk])
        else:
            stack.append(float(tk))
    return stack[-1]


print(f"{eval_prefix(input().split()):.6f}")
```

也可以用递归实现前缀求值（第 6 周递归的预热）：

```python
def parse():
    tk = next(it)
    if tk in '+-*/':
        a, b = parse(), parse()
        return eval(f"({a}){tk}({b})")
    return float(tk)


it = iter(input().split())
print(f"{parse():.6f}")
```

---

# 5 应用四：合法出栈序列

**OJ 22068: 合法出栈序列**，http://cs101.openjudge.cn/practice/22068/

> 给定原始序列 `s`（各字符互不相同），再给若干候选序列，判断它们能否由 `s` 经过一系列 push/pop 得到。

**思路**：贪心模拟。依次把 `s` 的字符入栈，每次入栈后检查栈顶是否等于目标序列当前待匹配的字符，是则不断弹出。

```python
def is_valid_pop_sequence(origin: str, target: str) -> bool:
    if len(origin) != len(target):
        return False
    stack, j = [], 0
    for ch in origin:
        stack.append(ch)
        while stack and j < len(target) and stack[-1] == target[j]:
            stack.pop()
            j += 1
    return not stack


import sys

lines = sys.stdin.read().split()
origin = lines[0]
for t in lines[1:]:
    print("YES" if is_valid_pop_sequence(origin, t) else "NO")
```

时间 O(n)：每个元素最多入栈一次、出栈一次。

**相关**：LeetCode 946. 验证栈序列，https://leetcode.cn/problems/validate-stack-sequences/

---

# 6 单调栈：栈的高级应用

**单调栈**是栈中元素保持单调（递增或递减）的栈，用来求"下一个更大/更小元素"，时间 O(n)。

## 6.1 每日温度

**LeetCode 739. 每日温度**，https://leetcode.cn/problems/daily-temperatures/

> 对每一天，求还要等几天才会遇到更高的温度。

```python
def daily_temperatures(temps):
    n = len(temps)
    ans = [0] * n
    stack = []                        # 存下标，对应温度单调递减
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j            # i 就是 j 的"下一个更大元素"位置
        stack.append(i)
    return ans
```

**为什么是 O(n)**：每个下标最多入栈一次、出栈一次，总操作 2n。

## 6.2 柱状图中最大的矩形

**LeetCode 84. 柱状图中最大的矩形**，https://leetcode.cn/problems/largest-rectangle-in-histogram/

```python
def largest_rectangle(heights):
    heights = [0] + heights + [0]      # 首尾哨兵，省去边界判断
    stack, best = [], 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            width = i - stack[-1] - 1  # 左右第一个更矮的柱子之间
            best = max(best, heights[top] * width)
        stack.append(i)
    return best
```

---

# 7 栈与递归：系统调用栈

每次函数调用，运行时系统都会压入一个**栈帧（stack frame）**，保存参数、局部变量和返回地址；函数返回时弹出。所以：

- **递归本质上就是在用系统栈**。
- 任何递归都可以用显式栈改写成迭代（第 6、9 周会做二叉树遍历的迭代版）。
- 递归太深会 `RecursionError`（Python 默认 1000 层）。

```python
import sys
sys.setrecursionlimit(1 << 20)     # OJ 上深递归的标准写法


def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)


# 手动用栈改写为迭代
def factorial_iter(n):
    result, stack = 1, []
    while n > 1:
        stack.append(n)
        n -= 1
    while stack:
        result *= stack.pop()
    return result
```

---

# 8 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 有效的括号 | LC 20 | 括号匹配 |
| 2 | 括号匹配问题 | OJ 03704 | 栈存下标 |
| 3 | 十进制到八进制 | OJ 02734 | 进制转换 |
| 4 | 中序表达式转后序表达式 | OJ 24591 | 调度场算法 |
| 5 | 波兰表达式 | OJ 02694 | 前缀求值 |
| 6 | 逆波兰表达式求值 | LC 150 | 后缀求值 |
| 7 | 合法出栈序列 | OJ 22068 | 栈模拟 |
| 8 | 每日温度 | LC 739 | 单调栈 |
| 9（选做） | 柱状图中最大的矩形 | LC 84 | 单调栈进阶 |
| 10（选做） | 最长有效括号 | LC 32 | 栈 + 下标 |

**思考题**：

1. 调度场算法中，若把 `>=` 改成 `>`，对 `1-2-3` 的结果有什么影响？为什么左结合运算符必须用 `>=`？
2. 如何扩展调度场算法以支持右结合的乘方运算符 `^`（`2^3^2 = 2^(3^2)`）和一元负号？
3. 长度为 n 的入栈序列，合法出栈序列共有多少种？（提示：卡特兰数 Cₙ = C(2n,n)/(n+1)）
4. 用两个栈实现一个队列（LC 232），分析每个操作的均摊复杂度。

---

# 9 小结

1. 栈的核心是 **LIFO**，接口只有 push / pop / peek / is_empty，全部 O(1)。
2. Python 中直接用 `list` 的尾部当栈；**绝不要用头部**（O(n)）。
3. 栈的四类经典应用：**匹配**（括号）、**逆序**（进制转换）、**表达式处理**（调度场 + 后缀求值）、**模拟**（合法出栈序列）。
4. 单调栈把"求下一个更大元素"从 O(n²) 降到 O(n)，是高频考点。
5. 递归 = 系统栈；深递归要调 `setrecursionlimit`。

**下周预告**：另一端也能操作的线性结构——**队列、双端队列**，以及**顺序表 vs 链表**的存储结构之争。
