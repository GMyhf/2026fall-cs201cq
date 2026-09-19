# 第9周 树的概念与二叉树的遍历

*Updated 2026-08-30 12:20 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 9 周 / 3 学时
> **教学内容**：树的概念与二叉树的遍历
> **教学要求**：掌握树的定义与表示方法；熟练实现二叉树的各种遍历

**知识点**：树的术语（根 / 叶 / 度 / 深度 / 高度）、二叉树的性质、满二叉树与完全二叉树、二叉树的存储（链式 / 顺序 / 左儿子右兄弟）、前中后序遍历（递归 + 迭代）、层序遍历、由遍历序列重建二叉树、括号嵌套树、表达式树、树的深度 / 直径 / 镜像。

---

# 1 树的基本概念

## 1.1 定义

**树**是 n（n ≥ 0）个结点的有限集合：
- n = 0 时为**空树**；
- n > 0 时有且仅有一个**根结点（root）**，其余结点分为 m 个互不相交的子集，每个子集本身又是一棵树，称为根的**子树**。

这是一个**递归定义**——所以树的算法几乎都是递归的。

```
                A            <- 根 root，深度 0
              / | \
             B  C  D         <- 深度 1
            / \    |
           E   F   G         <- 深度 2
              / \
             H   I           <- 深度 3，树高 = 3
```

## 1.2 术语表

| 术语 | 含义 |
| ---- | ---- |
| 结点的**度** | 该结点的子树个数（孩子数） |
| 树的度 | 所有结点度的最大值 |
| **叶结点** | 度为 0 的结点（E、H、I、C、G） |
| 分支结点 | 度不为 0 的结点 |
| 父/子/兄弟 | B 是 E 的父，E、F 是兄弟 |
| 结点的**深度 depth** | 从根到该结点的边数（根为 0） |
| 结点的**高度 height** | 该结点到最深叶子的边数（叶为 0） |
| 树的高度 | 根的高度 |
| **层 level** | 深度 + 1（有的教材层从 1 开始） |
| **森林** | m 棵互不相交的树的集合 |
| 路径 | 结点序列，每对相邻结点是父子关系 |

⚠️ **深度 vs 高度**是考试常混淆点：深度**自顶向下**数，高度**自底向上**数。

## 1.3 树 vs 图

树是**无环连通图**的特例：n 个结点的树恰有 **n − 1 条边**，任意两点间有**唯一路径**。第 12 周会从图的角度重新审视树。

---

# 2 二叉树

## 2.1 定义与形态

**二叉树**：每个结点**至多两个**子树，且**区分左右**（左子树与右子树不能交换）。

五种基本形态：空、只有根、只有左子树、只有右子树、左右都有。

## 2.2 重要性质（必背）

1. 第 i 层（从 1 开始）至多有 **2^(i−1)** 个结点。
2. 深度为 k 的二叉树至多有 **2^k − 1** 个结点。
3. 对任意二叉树，若叶结点数为 n₀、度为 2 的结点数为 n₂，则 **n₀ = n₂ + 1**。
4. n 个结点的**完全二叉树**深度为 **⌊log₂n⌋ + 1**。
5. 完全二叉树按层序编号（根为 1），结点 i 的左孩子为 **2i**，右孩子为 **2i+1**，父结点为 **⌊i/2⌋**。

**性质 3 的证明**：设度为 1 的结点数为 n₁，总结点数 n = n₀ + n₁ + n₂；总边数 = n − 1 = 0·n₀ + 1·n₁ + 2·n₂。两式联立得 n₀ = n₂ + 1。∎

## 2.3 满二叉树与完全二叉树

```
      满二叉树                    完全二叉树                   非完全
         1                            1                          1
       /   \                        /   \                      /   \
      2     3                      2     3                    2     3
     / \   / \                    / \   /                    / \     \
    4   5 6   7                  4   5 6                    4   5     7
```

- **满二叉树**：每层都填满，深度 k 时恰有 2^k − 1 个结点。
- **完全二叉树**：除最后一层外都填满，最后一层结点**从左到右连续**。
  → **完全二叉树可以用数组紧凑存储**，这是第 10 周堆的基础。

## 2.4 三种存储方式

**(1) 链式存储（最通用）**

```python
class TreeNode:
    __slots__ = ('val', 'left', 'right')

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"
```

**(2) 顺序存储（数组）**——只适合完全二叉树

```python
tree = [None, 1, 2, 3, 4, 5, 6, 7]      # 下标 0 空置，根在 1
# 结点 i: 左孩子 2i, 右孩子 2i+1, 父 i//2
```

**(3) 左儿子右兄弟（把多叉树转成二叉树）**

```python
class MultiNode:
    def __init__(self, val):
        self.val = val
        self.first_child = None      # 长子
        self.next_sibling = None     # 下一个兄弟
```

```
   多叉树              左儿子右兄弟表示
     A                      A
   / | \                   /
  B  C  D       ==>       B
 / \                     / \
E   F                   E   C
                         \    \
                          F    D
```

**这个变换让任何多叉树问题都能用二叉树算法处理**（OJ 04081 树的转换即考此点）。

---

# 3 二叉树的遍历

## 3.1 四种遍历

以下面这棵树为例：

```
         1
       /   \
      2     3
     / \     \
    4   5     6
```

| 遍历 | 顺序 | 结果 |
| ---- | ---- | ---- |
| **前序** preorder | 根 → 左 → 右 | 1 2 4 5 3 6 |
| **中序** inorder | 左 → 根 → 右 | 4 2 5 1 3 6 |
| **后序** postorder | 左 → 右 → 根 | 4 5 2 6 3 1 |
| **层序** level-order | 逐层从左到右 | 1 2 3 4 5 6 |

**记忆法**：前/中/后指的是**根**被访问的时机。

## 3.2 递归实现（三行的美感）

```python
def preorder(node, res):
    if not node:
        return
    res.append(node.val)          # 根
    preorder(node.left, res)      # 左
    preorder(node.right, res)     # 右


def inorder(node, res):
    if not node:
        return
    inorder(node.left, res)
    res.append(node.val)
    inorder(node.right, res)


def postorder(node, res):
    if not node:
        return
    postorder(node.left, res)
    postorder(node.right, res)
    res.append(node.val)
```

三者只是那一行 `res.append` 的**位置不同**。时间 O(n)，空间 O(h)（h 为树高）。

## 3.3 迭代实现（考试高频）

**前序**——用栈，先压右后压左：

```python
def preorder_iter(root):
    if not root:
        return []
    res, stack = [], [root]
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.right:
            stack.append(node.right)     # 先右
        if node.left:
            stack.append(node.left)      # 后左 -> 先出栈
    return res
```

**中序**——一路向左压栈，弹出时访问再转右：

```python
def inorder_iter(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left               # 一直向左
        cur = stack.pop()
        res.append(cur.val)              # 访问
        cur = cur.right                  # 转向右子树
    return res
```

**后序**——技巧：按"根→右→左"遍历再反转，即得"左→右→根"：

```python
def postorder_iter(root):
    if not root:
        return []
    res, stack = [], [root]
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.left:
            stack.append(node.left)      # 注意：先左后右
        if node.right:
            stack.append(node.right)
    return res[::-1]                     # 反转
```

**通用双色标记法**（一套模板搞定三种遍历，强烈推荐）：

```python
WHITE, GRAY = 0, 1


def traverse(root, order='in'):
    res, stack = [], [(WHITE, root)]
    while stack:
        color, node = stack.pop()
        if node is None:
            continue
        if color == WHITE:
            # 按遍历顺序的【逆序】压栈
            if order == 'pre':
                items = [(WHITE, node.right), (WHITE, node.left), (GRAY, node)]
            elif order == 'in':
                items = [(WHITE, node.right), (GRAY, node), (WHITE, node.left)]
            else:  # post
                items = [(GRAY, node), (WHITE, node.right), (WHITE, node.left)]
            stack.extend(items)
        else:
            res.append(node.val)
    return res
```

## 3.4 层序遍历（BFS）

```python
from collections import deque


def level_order(root):
    """LC 102：返回二维列表，每层一个子列表。"""
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):        # 固定本层大小
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
```

**变形**：
- LC 107 自底向上层序 → `res[::-1]`
- LC 103 锯齿形层序 → 奇数层 `level[::-1]`
- LC 199 二叉树的右视图 → 每层取 `level[-1]`

---

# 4 由遍历序列重建二叉树

## 4.1 关键定理

- **前序 + 中序** → 唯一确定二叉树 ✅
- **后序 + 中序** → 唯一确定二叉树 ✅
- **前序 + 后序** → **不唯一** ❌（无法区分只有一个孩子时是左还是右）

**原理**：前序的第一个元素是根；在中序中找到根的位置，左边是左子树的中序，右边是右子树的中序，由此可知左右子树的规模，再切分前序。

```
前序: [1] [2 4 5] [3 6]
        根  左子树   右子树
中序: [4 2 5] [1] [3 6]
      左子树   根   右子树
```

## 4.2 前序 + 中序建树

**OJ 22158: 根据二叉树前中序序列建树**，http://cs101.openjudge.cn/practice/22158/
**LeetCode 105**，https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

```python
def build_from_pre_in(preorder, inorder):
    """O(n)：用哈希表定位根在中序中的位置。"""
    idx = {v: i for i, v in enumerate(inorder)}
    it = iter(preorder)

    def build(lo, hi):
        if lo > hi:
            return None
        val = next(it)
        node = TreeNode(val)
        mid = idx[val]
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)
```

**OJ 22158 完整程序**（多组数据，输出后序）：

```python
import sys


def build(pre, ino):
    if not pre:
        return None
    root = TreeNode(pre[0])
    k = ino.index(pre[0])
    root.left = build(pre[1:k + 1], ino[:k])
    root.right = build(pre[k + 1:], ino[k + 1:])
    return root


def postorder(node, res):
    if node:
        postorder(node.left, res)
        postorder(node.right, res)
        res.append(node.val)


lines = sys.stdin.read().split()
for i in range(0, len(lines), 2):
    root = build(lines[i], lines[i + 1])
    res = []
    postorder(root, res)
    print(''.join(res))
```

## 4.3 后序 + 中序建树

**LeetCode 106**：后序的**最后一个**元素是根，其余同理。

```python
def build_from_post_in(inorder, postorder):
    idx = {v: i for i, v in enumerate(inorder)}
    it = iter(reversed(postorder))       # 从后往前取根

    def build(lo, hi):
        if lo > hi:
            return None
        val = next(it)
        node = TreeNode(val)
        mid = idx[val]
        node.right = build(mid + 1, hi)  # ⚠️ 必须先建右子树
        node.left = build(lo, mid - 1)
        return node

    return build(0, len(inorder) - 1)
```

## 4.4 括号嵌套树

**OJ 24729: 括号嵌套树**，http://cs101.openjudge.cn/practice/24729/

> 形如 `A(B(E),C,D(F,G))` 的字符串表示一棵多叉树，求其前序与后序遍历。

```python
import sys


class Node:
    def __init__(self, val):
        self.val = val
        self.children = []


def parse(s):
    stack, root, cur = [], None, None
    for ch in s:
        if ch.isalpha():
            cur = Node(ch)
            if stack:
                stack[-1].children.append(cur)
            else:
                root = cur
        elif ch == '(':
            stack.append(cur)            # 进入一层，cur 成为新的父
        elif ch == ')':
            cur = stack.pop()            # 退出一层
        # ',' 忽略
    return root


def pre(node, res):
    res.append(node.val)
    for c in node.children:
        pre(c, res)


def post(node, res):
    for c in node.children:
        post(c, res)
    res.append(node.val)


root = parse(input().strip())
a, b = [], []
pre(root, a)
post(root, b)
print(''.join(a))
print(''.join(b))
```

**相关**：OJ 27637 括号嵌套二叉树。

## 4.5 表达式树

第 4 周的中缀/前缀/后缀表达式，本质是同一棵表达式树的三种遍历：

```python
def build_expr_tree(postfix_tokens):
    """由后缀表达式构建表达式树。"""
    stack = []
    for tk in postfix_tokens:
        node = TreeNode(tk)
        if tk in '+-*/':
            node.right = stack.pop()     # 注意顺序
            node.left = stack.pop()
        stack.append(node)
    return stack[-1]


def eval_tree(node):
    if node.left is None:
        return float(node.val)
    a, b = eval_tree(node.left), eval_tree(node.right)
    return {'+': a + b, '-': a - b, '*': a * b, '/': a / b}[node.val]
```

- **前序遍历** = 前缀表达式（波兰式）
- **中序遍历** = 中缀表达式（需补括号）
- **后序遍历** = 后缀表达式（逆波兰式）

---

# 5 树的基本算法

## 5.1 深度与高度

```python
def max_depth(root):
    """LC 104：树的最大深度（结点数计）。"""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def count_nodes(root):
    return 0 if not root else 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaves(root):
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)
```

## 5.2 树的直径

**LeetCode 543. 二叉树的直径**，https://leetcode.cn/problems/diameter-of-binary-tree/

> 任意两结点间最长路径的长度（边数）。

```python
def diameter_of_binary_tree(root):
    best = 0

    def depth(node):
        nonlocal best
        if not node:
            return 0
        l, r = depth(node.left), depth(node.right)
        best = max(best, l + r)       # 经过 node 的最长路径
        return 1 + max(l, r)          # 返回给父结点的是"向下的深度"

    depth(root)
    return best
```

> **模式**：递归函数返回"向上汇报的值"，同时用外部变量记录"经过当前结点的答案"。这是树形 DP 的通用套路。

## 5.3 判断与变换

```python
def is_symmetric(root):
    """LC 101：对称二叉树。"""
    def same(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return same(a.left, b.right) and same(a.right, b.left)
    return same(root, root)


def invert_tree(root):
    """LC 226：翻转二叉树。"""
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def is_balanced(root):
    """LC 110：是否平衡（左右子树高度差 <= 1），为第 11 周 AVL 预热。"""
    def height(node):
        if not node:
            return 0
        l = height(node.left)
        if l < 0:
            return -1
        r = height(node.right)
        if r < 0 or abs(l - r) > 1:
            return -1
        return 1 + max(l, r)
    return height(root) >= 0
```

## 5.4 最近公共祖先（LCA）

**LeetCode 236**，https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/

```python
def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root          # p、q 分居两侧，当前就是 LCA
    return left or right
```

## 5.5 树的序列化与反序列化

**LeetCode 297**：

```python
def serialize(root):
    res = []

    def dfs(node):
        if not node:
            res.append('#')
            return
        res.append(str(node.val))
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return ','.join(res)


def deserialize(data):
    it = iter(data.split(','))

    def build():
        val = next(it)
        if val == '#':
            return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node

    return build()
```

> 前序 + **空结点标记**（`#`）可以唯一确定一棵二叉树——这解决了 4.1 中"前序单独不唯一"的问题。

---

# 6 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 二叉树的中序遍历 | LC 94 | 递归 + 迭代 |
| 2 | 二叉树的层序遍历 | LC 102 | BFS 分层 |
| 3 | 根据二叉树前中序序列建树 | OJ 22158 | 建树 + 后序输出 |
| 4 | 从中序与后序遍历序列构造二叉树 | LC 106 | 建树 |
| 5 | 括号嵌套树 | OJ 24729 | 多叉树解析 |
| 6 | 二叉树的最大深度 | LC 104 | 递归 |
| 7 | 二叉树的直径 | LC 543 | 树形 DP |
| 8 | 对称二叉树 | LC 101 | 双指针递归 |
| 9 | 二叉树的最近公共祖先 | LC 236 | LCA |
| 10（选做） | 二叉树的序列化与反序列化 | LC 297 | 前序 + 空标记 |
| 11（选做） | 二叉树中的最大路径和 | LC 124 | 树形 DP |

**思考题**：

1. 为什么"前序 + 后序"不能唯一确定二叉树？举一个反例。加上什么条件后可以？
2. 用双色标记法写出后序遍历，验证它与"前序反转法"结果一致。
3. 一棵有 n 个结点的二叉树，其递归遍历的空间复杂度最坏是多少？最好是多少？
4. 把多叉树用"左儿子右兄弟"转成二叉树后，多叉树的**前序**对应二叉树的哪种遍历？**后序**呢？

---

# 7 小结

1. 树是递归定义的结构，所以树的算法**首选递归**。
2. 二叉树五条性质要背，尤其 n₀ = n₂ + 1 和完全二叉树的数组下标关系。
3. 前/中/后序的差别只在"根被访问的时机"；迭代版本用栈，推荐**双色标记法**通用模板。
4. **前序+中序** 或 **后序+中序** 可唯一建树；单独一种序列需加空结点标记。
5. 树形问题的通用套路：递归返回"向上汇报值"，外部变量记录"经过当前结点的答案"。

**下周预告**：两种有特殊性质的二叉树——**堆**（完全二叉树 + 堆序）与**二叉搜索树**（中序有序）。
