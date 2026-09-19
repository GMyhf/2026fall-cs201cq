# -*- coding: utf-8 -*-
"""第9周 树的概念与二叉树的遍历"""

META = {
    'title': '第9周　树与二叉树的遍历',
    'subtitle': '树的术语 · 二叉树性质 · 前中后序与层序 · 由序列建树',
    'footer': '数据结构与算法 · 第9周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握树的定义与表示方法；熟练实现二叉树的各种遍历'],
}

SLIDES = [
    ('section', '第 1 节', '树的基本概念'),

    ('ascii', '树是递归定义的结构', r"""
                A            <- 根 root，深度 0
              / | \
             B  C  D         <- 深度 1
            / \    |
           E   F   G         <- 深度 2
              / \
             H   I           <- 深度 3，树高 = 3

n = 0 为空树；n > 0 时有且仅有一个根，其余结点分为 m 个互不相交的子树
""", '递归定义 ⇒ 树的算法几乎都是递归的'),

    ('table', '术语表', [
        ['术语', '含义'],
        ['结点的度', '该结点的子树个数（孩子数）'],
        ['叶结点', '度为 0 的结点'],
        ['结点的深度 depth', '从根到该结点的边数（根为 0）—— 自顶向下数'],
        ['结点的高度 height', '该结点到最深叶子的边数（叶为 0）—— 自底向上数'],
        ['森林', 'm 棵互不相交的树的集合'],
    ], '⚠️ 深度 vs 高度是考试常混淆点'),

    ('key', '树与图的关系',
     '树是【无环连通图】的特例\nn 个结点的树恰有 n − 1 条边，任意两点间有唯一路径'),

    ('section', '第 2 节', '二叉树'),

    ('bullets', '⭐ 五条重要性质（必背）', [
        '第 i 层（从 1 开始）至多有 **2^(i−1)** 个结点',
        '深度为 k 的二叉树至多有 **2^k − 1** 个结点',
        '叶结点数 n₀ 与度为 2 的结点数 n₂ 满足 **n₀ = n₂ + 1**',
        'n 个结点的**完全二叉树**深度为 **⌊log₂n⌋ + 1**',
        '完全二叉树按层序编号（根为 1）：左孩子 **2i**，右孩子 **2i+1**，父 **⌊i/2⌋**',
    ]),

    ('key', '性质 3 的证明',
     'n = n₀ + n₁ + n₂　　总边数 n − 1 = 0·n₀ + 1·n₁ + 2·n₂\n两式联立即得 n₀ = n₂ + 1'),

    ('ascii', '满二叉树 vs 完全二叉树', r"""
      满二叉树                完全二叉树                非完全
         1                        1                       1
       /   \                    /   \                   /   \
      2     3                  2     3                 2     3
     / \   / \                / \   /                 / \     \
    4   5 6   7              4   5 6                  4   5     7

完全二叉树：除最后一层外都填满，最后一层从左到右连续
=> 可以用数组紧凑存储  =>  这是第 10 周"堆"的基础
"""),

    ('code', '三种存储方式', '''# (1) 链式存储（最通用）
class TreeNode:
    __slots__ = ('val', 'left', 'right')

    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


# (2) 顺序存储（数组）—— 只适合完全二叉树
tree = [None, 1, 2, 3, 4, 5, 6, 7]      # 下标 0 空置，根在 1
# 结点 i: 左孩子 2i, 右孩子 2i+1, 父 i//2


# (3) 左儿子右兄弟 —— 把多叉树转成二叉树
class MultiNode:
    def __init__(self, val):
        self.val = val
        self.first_child = None      # 长子
        self.next_sibling = None     # 下一个兄弟
'''),

    ('ascii', '左儿子右兄弟：多叉树 → 二叉树', r"""
   多叉树                    左儿子右兄弟表示
     A                            A
   / | \                         /
  B  C  D          ==>          B
 / \                           / \
E   F                         E   C
                               \    \
                                F    D

这个变换让任何多叉树问题都能用二叉树算法处理
"""),

    ('section', '第 3 节', '二叉树的遍历'),

    ('ascii', '四种遍历', r"""
         1
       /   \
      2     3
     / \     \
    4   5     6

前序 preorder   根→左→右    1 2 4 5 3 6
中序 inorder    左→根→右    4 2 5 1 3 6
后序 postorder  左→右→根    4 5 2 6 3 1
层序 level      逐层从左到右  1 2 3 4 5 6
""", '记忆法：前/中/后指的是【根】被访问的时机'),

    ('code', '递归实现：只差 append 那一行的位置', '''def preorder(node, res):
    if not node: return
    res.append(node.val)          # 根
    preorder(node.left, res)      # 左
    preorder(node.right, res)     # 右


def inorder(node, res):
    if not node: return
    inorder(node.left, res)
    res.append(node.val)          # 根在中间
    inorder(node.right, res)


def postorder(node, res):
    if not node: return
    postorder(node.left, res)
    postorder(node.right, res)
    res.append(node.val)          # 根在最后
''', '时间 O(n)，空间 O(h)（h 为树高）'),

    ('code', '迭代实现：前序与后序', '''def preorder_iter(root):          # 栈，先压右后压左
    if not root: return []
    res, stack = [], [root]
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.right: stack.append(node.right)     # 先右
        if node.left:  stack.append(node.left)      # 后左 -> 先出栈
    return res


def postorder_iter(root):         # 技巧：按"根→右→左"再反转
    if not root: return []
    res, stack = [], [root]
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.left:  stack.append(node.left)      # 注意：先左后右
        if node.right: stack.append(node.right)
    return res[::-1]                                 # 反转
'''),

    ('code', '迭代中序：一路向左压栈（考试高频）', '''def inorder_iter(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left               # 一直向左
        cur = stack.pop()
        res.append(cur.val)              # 访问
        cur = cur.right                  # 转向右子树
    return res
''', '这段模板在第 10 周 BST 的“第 k 小”里会再次用到'),

    ('code', '⭐ 双色标记法：一套模板搞定三种遍历', '''WHITE, GRAY = 0, 1


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
            else:
                items = [(GRAY, node), (WHITE, node.right), (WHITE, node.left)]
            stack.extend(items)
        else:
            res.append(node.val)
    return res
''', '强烈推荐：改一行就换一种遍历，不用记三套代码'),

    ('code', '层序遍历（BFS）', '''from collections import deque


def level_order(root):
    """LC 102：返回二维列表，每层一个子列表。"""
    if not root: return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):        # ⭐ 固定本层大小
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res
''', '变形：LC 107 自底向上 res[::-1]；LC 103 锯齿形；LC 199 右视图取 level[-1]'),

    ('section', '第 4 节', '由遍历序列重建二叉树'),

    ('key', '⭐ 关键定理',
     '前序 + 中序 → 唯一确定 ✅　　后序 + 中序 → 唯一确定 ✅\n'
     '前序 + 后序 → 不唯一 ❌（无法区分只有一个孩子时是左还是右）'),

    ('ascii', '建树原理', r"""
前序: [1] [2 4 5] [3 6]
       根  左子树  右子树

中序: [4 2 5] [1] [3 6]
      左子树   根  右子树

前序第一个是根 -> 在中序中定位根 -> 得知左右子树规模 -> 切分前序 -> 递归
"""),

    ('code', 'LC 105 / OJ 22158 前序+中序建树', '''def build_from_pre_in(preorder, inorder):
    """O(n)：用哈希表定位根在中序中的位置。"""
    idx = {v: i for i, v in enumerate(inorder)}
    it = iter(preorder)

    def build(lo, hi):
        if lo > hi:
            return None
        val = next(it)
        node = TreeNode(val)
        mid = idx[val]
        node.left = build(lo, mid - 1)      # ⚠️ 必须先左后右
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)
''', '⚠️ 用 inorder.index() 每层扫描会退化成 O(n²)；切片建树还会多 O(n²) 空间'),

    ('code', 'LC 106 后序+中序建树', '''def build_from_post_in(inorder, postorder):
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
'''),

    ('code', 'OJ 24729 括号嵌套树：A(B(E),C,D(F,G))', '''def parse(s):
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
''', '用栈解析嵌套结构 —— 与第 4 周的括号匹配同源'),

    ('code', '表达式树：呼应第 4 周', '''def build_expr_tree(postfix_tokens):
    """由后缀表达式构建表达式树。"""
    stack = []
    for tk in postfix_tokens:
        node = TreeNode(tk)
        if tk in '+-*/':
            node.right = stack.pop()     # 注意顺序
            node.left = stack.pop()
        stack.append(node)
    return stack[-1]

# 前序遍历 = 前缀表达式（波兰式）
# 中序遍历 = 中缀表达式（需补括号）
# 后序遍历 = 后缀表达式（逆波兰式）
'''),

    ('section', '第 5 节', '树的基本算法'),

    ('code', '深度、结点数、叶子数', '''def max_depth(root):               # LC 104
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def count_nodes(root):
    return 0 if not root else \\
        1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaves(root):
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)
'''),

    ('code', '⭐ LC 543 树的直径：树形 DP 的通用套路', '''def diameter_of_binary_tree(root):
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
''', '模式：递归函数返回“向上汇报值”，外部变量记录“经过当前结点的答案”'),

    ('code', '判断与变换', '''def is_symmetric(root):            # LC 101 对称二叉树
    def same(a, b):
        if not a and not b: return True
        if not a or not b or a.val != b.val: return False
        return same(a.left, b.right) and same(a.right, b.left)
    return same(root, root)


def invert_tree(root):             # LC 226 翻转二叉树
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def lowest_common_ancestor(root, p, q):    # LC 236 LCA
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root          # p、q 分居两侧，当前就是 LCA
    return left or right
'''),

    ('code', 'LC 297 序列化：前序 + 空结点标记', '''def serialize(root):
    res = []
    def dfs(node):
        if not node:
            res.append('#'); return      # ⭐ 空结点也要记
        res.append(str(node.val))
        dfs(node.left); dfs(node.right)
    dfs(root)
    return ','.join(res)


def deserialize(data):
    it = iter(data.split(','))
    def build():
        val = next(it)
        if val == '#':
            return None
        node = TreeNode(int(val))
        node.left = build(); node.right = build()
        return node
    return build()
''', '前序 + 空标记可唯一确定一棵二叉树 —— 解决了“前序单独不唯一”的问题'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '二叉树的中序遍历', 'LC 94', '递归 + 迭代'],
        ['2', '二叉树的层序遍历', 'LC 102', 'BFS 分层'],
        ['3', '根据前中序序列建树', 'OJ 22158', '建树 + 后序输出'],
        ['4', '从中序与后序构造二叉树', 'LC 106', '建树'],
        ['5', '括号嵌套树', 'OJ 24729', '多叉树解析'],
        ['6', '二叉树的直径', 'LC 543', '树形 DP'],
        ['7', '对称二叉树 / 最近公共祖先', 'LC 101 / 236', '递归'],
        ['8（选做）', '序列化与反序列化 / 最大路径和', 'LC 297 / 124', '前序+空标记'],
    ]),

    ('bullets', '本讲小结', [
        '树是**递归定义**的结构，算法首选递归',
        '五条性质要背，尤其 **n₀ = n₂ + 1** 和完全二叉树的下标关系',
        '前/中/后序只差“根被访问的时机”；迭代版推荐**双色标记法**',
        '**前序+中序** 或 **后序+中序** 可唯一建树；单序列需加空结点标记',
        '树形问题套路：递归返回“向上汇报值”，外部变量记录答案',
        '**下周预告**：两种特殊二叉树 —— 堆与二叉搜索树',
    ]),
]
