# -*- coding: utf-8 -*-
"""第4周 栈"""

META = {
    'title': '第4周　栈（Stack）',
    'subtitle': 'ADT 与实现 · 括号匹配 · 进制转换 · 调度场算法',
    'footer': '数据结构与算法 · 第4周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握栈的 LIFO 特性；能够实现栈并解决括号匹配问题；表达式转换算法'],
}

SLIDES = [
    ('bullets', '本讲内容', [
        '**栈 ADT**', '- LIFO 特性、接口定义、顺序栈实现',
        '**应用一：匹配**', '- 括号匹配、输出不匹配位置、最长有效括号',
        '**应用二：逆序**', '- 进制转换',
        '**应用三：表达式处理**', '- 中缀/前缀/后缀、调度场算法、后缀求值',
        '**应用四：模拟与进阶**', '- 合法出栈序列、单调栈、栈与递归',
    ]),

    ('section', '第 1 节', '栈 ADT'),

    ('ascii', 'LIFO：后进先出', r"""
        push(4)                pop() -> 4
   |  |          | 4|              |  |
   | 3|   ==>    | 3|     ==>      | 3|
   | 2|          | 2|              | 2|
   | 1|          | 1|              | 1|
   +--+          +--+              +--+

   栈底在下，栈顶在上；只允许在栈顶插入与删除
""", '像一摞盘子：最后放上去的最先被拿走'),

    ('table', '栈的接口', [
        ['操作', '语义', '复杂度'],
        ['Stack()', '创建空栈', 'O(1)'],
        ['push(item)', '入栈', '均摊 O(1)'],
        ['pop()', '出栈并返回栈顶', 'O(1)'],
        ['peek() / top()', '查看栈顶不弹出', 'O(1)'],
        ['is_empty() / size()', '判空 / 元素个数', 'O(1)'],
    ]),

    ('code', '顺序栈的完整实现', '''class Stack:
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
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)
''', '⭐ 实战约定：OJ 上直接用 list 当栈（append / pop / [-1]），代码更短、常数更小'),

    ('bullets', '定长数组实现（了解）', [
        '若语言不提供动态数组（如 C 的静态数组），用**数组 + 栈顶指针 top**',
        '`top = -1` 表示空栈；push 时 `top += 1`，pop 时 `top -= 1`',
        '**上溢 overflow**：push 时 top 已到达数组末尾',
        '**下溢 underflow**：pop 时 top < 0',
    ]),

    ('section', '第 2 节', '应用一：括号匹配'),

    ('code', 'LC 20 有效的括号', '''def is_valid(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack          # 结束时必须为空
''', '时间 O(n)，空间 O(n)'),

    ('bullets', '括号匹配的三个易错点', [
        '遇右括号时**栈已空** → 无效',
        '栈顶与当前右括号**不配对** → 无效',
        '扫描结束**栈非空**（有左括号没闭合）→ 无效',
        '⚠️ 很多人只写前两个判断，漏掉第三个',
    ]),

    ('code', 'OJ 03704 括号匹配问题：栈里存下标', '''import sys

for line in sys.stdin:
    line = line.rstrip('\\n')
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
''', '关键改造：栈里存的不是括号字符而是【下标】—— 这样才能回头标记位置'),

    ('code', 'LC 32 最长有效括号（进阶）', '''def longest_valid(s: str) -> int:
    stack = [-1]              # 栈底放"上一个未匹配右括号的位置"
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
'''),

    ('section', '第 3 节', '应用二：进制转换'),

    ('code', '反复除基取余，余数逆序输出', '''DIGITS = "0123456789ABCDEF"


def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    neg, n = n < 0, abs(n)
    stack = []
    while n > 0:
        stack.append(DIGITS[n % base])   # 余数入栈
        n //= base
    if neg:
        stack.append('-')
    return ''.join(reversed(stack))      # 逆序输出 —— 正是栈的用武之地


print(to_base(233, 2))    # 11101001
print(to_base(233, 16))   # E9
''', 'Python 内建：bin / oct / hex；反向用 int(s, base)'),

    ('section', '第 4 节', '应用三：表达式的三种表示'),

    ('table', '中缀、前缀、后缀', [
        ['形式', '写法', '特点'],
        ['中缀 infix', '( 1 + 2 ) * 3', '人类习惯，需要括号和优先级规则'],
        ['前缀 prefix（波兰式）', '* + 1 2 3', '运算符在前，无需括号'],
        ['后缀 postfix（逆波兰式）', '1 2 + 3 *', '运算符在后，⭐ 最易被机器求值'],
    ]),

    ('ascii', '三种形式其实是同一棵表达式树的三种遍历', r"""
        *
       / \
      +   3          前序遍历 = 前缀:  * + 1 2 3
     / \             中序遍历 = 中缀:  1 + 2 * 3  (需补括号)
    1   2            后序遍历 = 后缀:  1 2 + 3 *
""", '这一点会在第 9 周“树的遍历”中再次出现'),

    ('bullets', '调度场算法（Shunting Yard）：中缀 → 后缀', [
        '由 Dijkstra 提出；维护一个**运算符栈**和一个**输出队列**',
        '遇**操作数**：直接输出',
        '遇 **(**：入栈；遇 **)**：不断弹栈输出直到遇 (，弹掉 ( 不输出',
        '遇**运算符 op**：当栈顶优先级 ≥ op（左结合）时弹出输出，然后 op 入栈',
        '扫描结束：把栈中剩余运算符全部弹出输出',
    ]),

    ('code', 'OJ 24591 中序表达式转后序表达式', '''PREC = {'+': 1, '-': 1, '*': 2, '/': 2}


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
''', '⚠️ 左结合必须用 >=，写成 > 会让 10-3-2 算错'),

    ('table', '手工模拟 ( 1 + 2 ) * 3', [
        ['读入', '运算符栈', '输出'],
        ['(', '(', ''],
        ['1', '(', '1'],
        ['+', '( +', '1'],
        ['2', '( +', '1 2'],
        [')', '（空）', '1 2 +'],
        ['*', '*', '1 2 +'],
        ['3', '*', '1 2 + 3'],
        ['结束', '（空）', '1 2 + 3 *'],
    ]),

    ('code', '后缀求值：操作数入栈，遇运算符弹两个', '''def eval_postfix(tokens):
    stack = []
    for tk in tokens:
        if tk in '+-*/':
            b = stack.pop()          # ⚠️ 先弹的是右操作数
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
''', 'LC 150 逆波兰表达式求值'),

    ('code', 'OJ 02694 波兰表达式：从右往左，规则对称', '''def eval_prefix(tokens):
    stack = []
    for tk in reversed(tokens):
        if tk in '+-*/':
            a = stack.pop()          # 从右往左，先弹的是左操作数
            b = stack.pop()
            stack.append({'+': a + b, '-': a - b,
                          '*': a * b, '/': a / b}[tk])
        else:
            stack.append(float(tk))
    return stack[-1]


print(f"{eval_prefix(input().split()):.6f}")
'''),

    ('section', '第 5 节', '应用四：模拟与单调栈'),

    ('code', 'OJ 22068 合法出栈序列', '''def is_valid_pop_sequence(origin: str, target: str) -> bool:
    if len(origin) != len(target):
        return False
    stack, j = [], 0
    for ch in origin:
        stack.append(ch)                       # 依次入栈
        while stack and j < len(target) and stack[-1] == target[j]:
            stack.pop()                        # 能弹就弹（贪心）
            j += 1
    return not stack


import sys
lines = sys.stdin.read().split()
origin = lines[0]
for t in lines[1:]:
    print("YES" if is_valid_pop_sequence(origin, t) else "NO")
''', '时间 O(n)：每个元素最多入栈一次、出栈一次。相关：LC 946 验证栈序列'),

    ('key', '单调栈', '栈中元素保持单调，用来求“下一个更大 / 更小元素”\n把 O(n²) 降到 O(n)'),

    ('code', 'LC 739 每日温度', '''def daily_temperatures(temps):
    n = len(temps)
    ans = [0] * n
    stack = []                        # 存下标，对应温度单调递减
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j            # i 就是 j 的"下一个更大元素"位置
        stack.append(i)
    return ans
''', '为什么是 O(n)：每个下标最多入栈一次、出栈一次，总操作 2n'),

    ('code', 'LC 84 柱状图中最大的矩形', '''def largest_rectangle(heights):
    heights = [0] + heights + [0]      # 首尾哨兵，省去边界判断
    stack, best = [], 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            width = i - stack[-1] - 1  # 左右第一个更矮的柱子之间
            best = max(best, heights[top] * width)
        stack.append(i)
    return best
'''),

    ('bullets', '栈与递归：系统调用栈', [
        '每次函数调用，运行时会压入一个**栈帧**（参数、局部变量、返回地址）',
        '**递归本质上就是在用系统栈**',
        '任何递归都可以用显式栈改写成迭代（第 9 周做二叉树遍历的迭代版）',
        '递归太深会 RecursionError —— OJ 上写 `sys.setrecursionlimit(1 << 20)`',
    ]),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '有效的括号', 'LC 20', '括号匹配'],
        ['2', '括号匹配问题', 'OJ 03704', '栈存下标'],
        ['3', '十进制到八进制', 'OJ 02734', '进制转换'],
        ['4', '中序表达式转后序表达式', 'OJ 24591', '调度场算法'],
        ['5', '波兰表达式 / 逆波兰表达式求值', 'OJ 02694 / LC 150', '前缀、后缀求值'],
        ['6', '合法出栈序列', 'OJ 22068', '栈模拟'],
        ['7', '每日温度', 'LC 739', '单调栈'],
        ['8（选做）', '柱状图中最大的矩形 / 最长有效括号', 'LC 84 / LC 32', '单调栈进阶'],
    ]),

    ('bullets', '本讲小结', [
        '栈的核心是 **LIFO**，接口只有 push / pop / peek / is_empty，全部 O(1)',
        'Python 中直接用 list 的**尾部**当栈；**绝不要用头部**（O(n)）',
        '四类经典应用：**匹配**、**逆序**、**表达式处理**、**模拟**',
        '**单调栈**把“求下一个更大元素”从 O(n²) 降到 O(n)，是高频考点',
        '**下周预告**：队列、双端队列，以及顺序表 vs 链表的存储结构之争',
    ]),
]
