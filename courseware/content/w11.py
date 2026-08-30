# -*- coding: utf-8 -*-
"""第11周 AVL 树；并查集"""

META = {
    'title': '第11周　AVL 树与并查集',
    'subtitle': '平衡因子与四种旋转 · 路径压缩与按秩合并',
    'footer': '数据结构与算法 · 第11周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：理解平衡树的旋转操作；掌握并查集的实现与应用'],
}

SLIDES = [
    ('ascii', '上周遗留的问题：BST 会退化', r"""
按升序插入 1..5:              期望的平衡形态:
  1                                 3
   \                              /   \
    2                            2     4
     \                          /       \
      3          vs            1         5
       \
        4                      高度 O(log n)
         \
          5    高度 O(n)
""", '平衡二叉树通过插删时的局部调整（旋转），把树高强行控制在 O(log n)'),

    ('section', '第一部分', 'AVL 树'),

    ('key', 'AVL 树的定义',
     '任意结点的左右子树高度差不超过 1 的二叉搜索树\n'
     'BF(node) = height(left) − height(right) ∈ {−1, 0, +1}'),

    ('bullets', 'AVL 树的高度界', [
        '设 N(h) 为高度 h 的 AVL 树的**最少**结点数',
        'N(0)=1，N(1)=2，**N(h) = 1 + N(h−1) + N(h−2)** —— 与斐波那契同构',
        '可得 N(h) ≈ φ^h / √5（φ 为黄金比 1.618）',
        '反解：**h ≤ 1.44 · log₂(n+2) − 0.328 = O(log n)**',
        '⭐ 结论：AVL 树的高度最多比完全二叉树高约 **44%**，操作稳定 O(log n)',
    ]),

    ('ascii', 'LL 型（左左）→ 右旋', r"""
      z (BF=+2)                  y
     / \                       /   \
    y   T4    右旋 z          x     z
   / \        ------->       / \   / \
  x   T3                    T1 T2 T3 T4
 / \
T1  T2

新结点插在【左子树的左子树】上
"""),

    ('ascii', 'RR 型（右右）→ 左旋（与 LL 镜像）', r"""
    z (BF=-2)                     y
   / \                          /   \
  T1  y      左旋 z            z     x
     / \     ------->         / \   / \
    T2  x                    T1 T2 T3 T4
       / \
      T3  T4
"""),

    ('ascii', 'LR 型（左右）→ 先左旋后右旋', r"""
      z              z                x
     / \            / \             /   \
    y   T4         x   T4          y     z
   / \    ==>     / \      ==>    / \   / \
  T1  x          y   T3          T1 T2 T3 T4
     / \        / \
    T2  T3     T1  T2

   对 y 左旋      对 z 右旋

单次右旋无效，需要先把它转成 LL 型。RL 型与之镜像。
"""),

    ('table', '⭐ 四种失衡的判定表（必背）', [
        ['BF(z)', 'BF(子结点)', '类型', '操作'],
        ['+2', '≥ 0', 'LL', 'rotate_right(z)'],
        ['+2', '< 0', 'LR', 'rotate_left(z.left) 后 rotate_right(z)'],
        ['−2', '≤ 0', 'RR', 'rotate_left(z)'],
        ['−2', '> 0', 'RL', 'rotate_right(z.right) 后 rotate_left(z)'],
    ], '判定看：失衡结点的 BF 符号 + 其重侧孩子的 BF 符号'),

    ('code', '旋转的实现', '''def height(node):
    return node.height if node else 0


def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))


def rotate_right(z):
    """右旋：z 的左孩子 y 上位。"""
    y = z.left
    z.left = y.right
    y.right = z
    update_height(z)          # ⚠️ 先更新下面的 z，再更新 y
    update_height(y)
    return y                  # 返回新的子树根


def rotate_left(z):
    y = z.right
    z.right = y.left
    y.left = z
    update_height(z)
    update_height(y)
    return y
'''),

    ('code', '⭐ rebalance：一个函数搞定四种情况', '''def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0


def rebalance(node):
    """更新高度并在失衡时旋转，返回该子树新的根。"""
    update_height(node)
    bf = balance_factor(node)
    if bf > 1:                                   # 左重
        if balance_factor(node.left) < 0:        # LR
            node.left = rotate_left(node.left)
        return rotate_right(node)                # LL
    if bf < -1:                                  # 右重
        if balance_factor(node.right) > 0:       # RL
            node.right = rotate_right(node.right)
        return rotate_left(node)                 # RR
    return node
'''),

    ('code', 'AVL 插入与删除', '''def avl_insert(node, key):
    if node is None:
        return AVLNode(key)
    if key < node.key:
        node.left = avl_insert(node.left, key)
    elif key > node.key:
        node.right = avl_insert(node.right, key)
    else:
        return node                              # 重复键，忽略
    return rebalance(node)                       # ⭐ 回溯时逐层再平衡


def avl_delete(node, key):
    if node is None: return None
    if key < node.key:   node.left = avl_delete(node.left, key)
    elif key > node.key: node.right = avl_delete(node.right, key)
    else:
        if node.left is None:  return node.right
        if node.right is None: return node.left
        succ = node.right
        while succ.left: succ = succ.left        # 中序后继
        node.key = succ.key
        node.right = avl_delete(node.right, succ.key)
    return rebalance(node)
'''),

    ('code', '验证：退化不再发生', '''t = AVLTree()
for i in range(1, 100000):
    t.insert(i)              # 升序插入 —— BST 会退化，AVL 不会

print(t.height())            # 17  （而非 99999）
''', '同样的输入，普通 BST 树高 99999，AVL 只有 17'),

    ('table', '插入 vs 删除的旋转次数', [
        ['操作', '旋转次数', '原因'],
        ['插入', '⭐ 至多 1 次', '旋转后子树高度恢复原值，无需继续向上'],
        ['删除', 'O(log n) 次', '子树变矮会一路向上传播'],
    ]),

    ('table', 'AVL 树 vs 红黑树', [
        ['', 'AVL', '红黑树'],
        ['平衡条件', '严格（高度差 ≤ 1）', '宽松（最长路 ≤ 2 倍最短路）'],
        ['树高', '~1.44 log n', '~2 log n'],
        ['查找', '⭐ 更快', '稍慢'],
        ['插入 / 删除', '旋转更多', '⭐ 旋转更少'],
        ['典型应用', '读多写少（数据库索引）', 'C++ std::map、Java TreeMap、Linux 内核'],
    ]),

    ('section', '第二部分', '并查集（Disjoint Set Union）'),

    ('bullets', '要解决的问题', [
        '维护若干个**不相交集合**，支持两种操作：',
        '- `find(x)`：查询 x 属于哪个集合（返回代表元）',
        '- `union(x, y)`：把 x 和 y 所在的两个集合**合并**',
        '典型问句：“a 和 b 是不是一伙的？”“现在还剩几个连通块？”',
    ]),

    ('ascii', '基本思想：用森林表示集合', r"""
集合 {1,2,3}, {4,5}:

      1          4
     / \         |
    2   3        5

parent = [_, 1, 1, 1, 4, 4]     树根就是代表元

朴素实现的问题：可能形成一条链，find 退化成 O(n)
"""),

    ('ascii', '⭐ 优化一：路径压缩', r"""
   find(4) 之前:        find(4) 之后:
       1                     1
       |                  / | | \
       2                 2  3 4  5
       |
       3                把路径上所有结点直接挂到根下
       |
       4
"""),

    ('code', '路径压缩的两种写法', '''def find(x):
    """递归版：简洁，但深链时可能爆栈。"""
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]


def find_iter(x):
    """⭐ 迭代版：两趟扫描，OJ 推荐。"""
    root = x
    while parent[root] != root:      # 第一趟：找到根
        root = parent[root]
    while parent[x] != root:         # 第二趟：全部挂到根下
        parent[x], x = root, parent[x]
    return root
'''),

    ('code', '⭐ 完整模板（路径压缩 + 按大小合并）', '''class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n                # 连通分量个数

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:         # 路径压缩
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        """合并成功返回 True，本来就同一集合返回 False。"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry]:     # 小树挂到大树下
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        self.count -= 1
        return True
''', '这段模板请默写下来 —— 第 14 周 Kruskal 会直接用'),

    ('table', '⭐ 复杂度：两个优化缺一不可', [
        ['优化', '单次操作复杂度'],
        ['无优化', 'O(n)'],
        ['仅路径压缩', 'O(log n) 均摊'],
        ['仅按秩合并', 'O(log n)'],
        ['**两者都用**', '⭐ **O(α(n)) ≈ O(1)**'],
    ], 'α 是反阿克曼函数；对任何实际的 n（哪怕 10⁸⁰）都有 α(n) < 5'),

    ('section', '第三部分', '并查集的应用'),

    ('code', '应用一：连通分量计数', '''# OJ 02524 宗教信仰 / LC 547 省份数量
def find_circle_num(is_connected):
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return dsu.count            # 直接读出连通分量个数
'''),

    ('code', '应用二：OJ 01611 The Suspects（传染）', '''dsu = DSU(n)
for _ in range(m):
    k = int(data[p]); p += 1
    members = [int(data[p + i]) for i in range(k)]; p += k
    for i in range(1, k):
        dsu.union(members[0], members[i])      # 同组全部合并

print(dsu.group_size(0))       # 与 0 号同组的人数
''', 'size 数组在这里直接给出答案'),

    ('code', '应用三：判环 / 冗余连接', '''def find_redundant_connection(edges):    # LC 684
    dsu = DSU(len(edges) + 1)
    for a, b in edges:
        if not dsu.union(a, b):      # 已经连通，这条边构成环
            return [a, b]
''', '⭐ 无向图判环：加边时若两端已连通则有环 —— 这正是 Kruskal 的核心判据'),

    ('code', '应用四：带权并查集（OJ 07734 虫子的生活）', '''class WeightedDSU:
    """rel[x] = x 与其父结点的关系（0 同类，1 异类），模 2 运算。"""

    def find(self, x):
        if self.parent[x] == x:
            return x
        root = self.find(self.parent[x])
        self.rel[x] ^= self.rel[self.parent[x]]     # 压缩时累加关系
        self.parent[x] = root
        return root

    def union(self, x, y, d=1):
        """断言 x 与 y 的关系为 d，返回是否与已知信息矛盾。"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return (self.rel[x] ^ self.rel[y]) == d
        self.parent[rx] = ry
        self.rel[rx] = self.rel[x] ^ self.rel[y] ^ d
        return True
'''),

    ('code', '应用五：种类并查集（扩展域）', '''# OJ 01703：两个帮派。开 2n 个结点：
#   i   表示"i 在帮派 A"
#   i+n 表示"i 在帮派 B"
dsu = DSU(2 * n)

# D a b：a 与 b 不同帮派
dsu.union(a, b + n)
dsu.union(a + n, b)

# A a b：查询
if dsu.connected(a, b):
    print("In the same gang.")
elif dsu.connected(a, b + n):
    print("In different gangs.")
else:
    print("Not sure yet.")
''', '食物链问题（三种类别）用 3n 个结点，同理'),

    ('table', 'AVL 树 vs 并查集：互补的两种结构', [
        ['', 'AVL 树', '并查集'],
        ['维护什么', '**有序**的动态集合', '**不相交集合的划分**'],
        ['核心操作', '查找、插入、删除、前驱后继', 'find、union'],
        ['单次复杂度', 'O(log n)', 'O(α(n)) ≈ O(1)'],
        ['能查“第 k 小”吗', '✅（加 size 域）', '❌'],
        ['能查“是否同组”吗', '❌', '✅'],
    ], 'AVL 管“顺序”，并查集管“分组”'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '平衡二叉树', 'LC 110', '平衡判定'],
        ['2', 'AVL 树的插入（手工模拟）', '课堂题', '四种旋转'],
        ['3', '宗教信仰 / 省份数量', 'OJ 02524 / LC 547', '并查集计数'],
        ['4', 'The Suspects', 'OJ 01611', '并查集 + size'],
        ['5', '冗余连接', 'LC 684', '并查集判环'],
        ['6', '虫子的生活', 'OJ 07734', '带权 / 种类并查集'],
        ['7', '岛屿数量（并查集解法）', 'LC 200', '对比第 8 周 DFS 解法'],
        ['8（选做）', 'Find them, Catch them / 账户合并', 'OJ 01703 / LC 721', '扩展域'],
    ], '实验五：实现 AVLTree；对比 BST 与 AVL 在升序 / 随机插入下的树高与查找耗时'),

    ('bullets', '本讲小结', [
        'AVL 用 **BF ∈ {−1,0,1}** 把树高锁定在 1.44 log n，代价是插删时旋转',
        '四种失衡 **LL / RR / LR / RL**，判定看两个 BF 的符号',
        '并查集用森林表示集合，**路径压缩 + 按秩合并** ⇒ 近似 O(1)',
        '三类经典用法：**连通分量计数**、**判环**、**带权/种类关系**',
        '**下周预告**：把树推广到最一般的非线性结构 —— 图',
    ]),
]
