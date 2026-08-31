# 第11周 AVL 树；并查集

*Updated 2026-08-31 04:20 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 11 周 / 3 学时
> **教学内容**：AVL 树；并查集
> **教学要求**：理解平衡树的旋转操作；掌握并查集的实现与应用

**知识点**：平衡因子、AVL 树的定义与高度界、四种失衡（LL / RR / LR / RL）与旋转、AVL 插入与删除、红黑树简介、并查集（Disjoint Set Union）、路径压缩、按秩 / 按大小合并、连通分量计数、带权并查集、种类并查集、Kruskal 的基础。

---

# 第一部分：AVL 树

# 1 为什么需要平衡

第 10 周结尾我们看到：BST 按升序插入会退化成链表，操作从 O(log n) 变成 O(n)。

```
插入 1,2,3,4,5:        期望的平衡形态:
  1                          3
   \                       /   \
    2                     2     4
     \                   /       \
      3       vs        1         5
       \
        4               高度 O(log n)
         \
          5             高度 O(n)
```

**平衡二叉树**通过在插入/删除时做局部调整（旋转），把树高强行控制在 O(log n)。

---

# 2 AVL 树的定义

**AVL 树**（Adelson-Velsky & Landis, 1962）是**任意结点的左右子树高度差不超过 1** 的二叉搜索树。

定义**平衡因子（Balance Factor）**：

```
BF(node) = height(node.left) - height(node.right)
```

AVL 树要求所有结点满足 **BF ∈ {−1, 0, +1}**。

## 2.1 高度界的证明

设 N(h) 为高度为 h 的 AVL 树的**最少**结点数：

```
N(0) = 1        (只有根)
N(1) = 2
N(h) = 1 + N(h-1) + N(h-2)      (一边高 h-1，另一边至少 h-2)
```

这与斐波那契数列同构，可得 N(h) ≈ φ^h / √5（φ 为黄金比 1.618）。反解得

```
h ≤ 1.44 · log₂(n + 2) − 0.328 = O(log n)
```

**结论：AVL 树的高度最多比完全二叉树高约 44%**，所有操作稳定 O(log n)。

---

# 3 旋转：维持平衡的手术刀

插入或删除后，从被修改结点向上回溯，第一个 BF 绝对值 > 1 的结点就是**失衡结点**。根据失衡的形态分四种情况。

## 3.1 LL 型（左左）→ 右旋

新结点插在**左子树的左子树**上。

```
      z (BF=+2)                  y
     / \                       /   \
    y   T4    右旋 z          x     z
   / \        ------->       / \   / \
  x   T3                    T1 T2 T3 T4
 / \
T1  T2
```

```python
def rotate_right(z):
    """右旋：z 的左孩子 y 上位。"""
    y = z.left
    z.left = y.right
    y.right = z
    update_height(z)          # 先更新下面的
    update_height(y)
    return y                  # 新的子树根
```

## 3.2 RR 型（右右）→ 左旋

新结点插在**右子树的右子树**上，与 LL 镜像对称。

```
    z (BF=-2)                     y
   / \                          /   \
  T1  y      左旋 z            z     x
     / \     ------->         / \   / \
    T2  x                    T1 T2 T3 T4
       / \
      T3  T4
```

```python
def rotate_left(z):
    """左旋：z 的右孩子 y 上位。"""
    y = z.right
    z.right = y.left
    y.left = z
    update_height(z)
    update_height(y)
    return y
```

## 3.3 LR 型（左右）→ 先左旋后右旋

新结点插在**左子树的右子树**上。单次右旋无效，需要先把它转成 LL 型。

```
      z              z                x
     / \            / \             /   \
    y   T4         x   T4          y     z
   / \    ==>     / \      ==>    / \   / \
  T1  x          y   T3          T1 T2 T3 T4
     / \        / \
    T2  T3     T1  T2

   对 y 左旋      对 z 右旋
```

## 3.4 RL 型（右左）→ 先右旋后左旋

与 LR 镜像。

## 3.5 判定表（必背）

| BF(z) | BF(子结点) | 类型 | 操作 |
| ---- | ---- | ---- | ---- |
| +2 | ≥ 0 | LL | `rotate_right(z)` |
| +2 | < 0 | LR | `rotate_left(z.left)` 后 `rotate_right(z)` |
| −2 | ≤ 0 | RR | `rotate_left(z)` |
| −2 | > 0 | RL | `rotate_right(z.right)` 后 `rotate_left(z)` |

---

# 4 AVL 树的完整实现

```python
class AVLNode:
    __slots__ = ('key', 'left', 'right', 'height')

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1          # 叶结点高度为 1（空树为 0）


def height(node):
    return node.height if node else 0


def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))


def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0


def rotate_right(z):
    y = z.left
    z.left = y.right
    y.right = z
    update_height(z)
    update_height(y)
    return y


def rotate_left(z):
    y = z.right
    z.right = y.left
    y.left = z
    update_height(z)
    update_height(y)
    return y


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


def avl_insert(node, key):
    if node is None:
        return AVLNode(key)
    if key < node.key:
        node.left = avl_insert(node.left, key)
    elif key > node.key:
        node.right = avl_insert(node.right, key)
    else:
        return node                              # 重复键，忽略
    return rebalance(node)


def avl_delete(node, key):
    if node is None:
        return None
    if key < node.key:
        node.left = avl_delete(node.left, key)
    elif key > node.key:
        node.right = avl_delete(node.right, key)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        succ = node.right
        while succ.left:
            succ = succ.left                     # 中序后继
        node.key = succ.key
        node.right = avl_delete(node.right, succ.key)
    return rebalance(node)


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = avl_insert(self.root, key)

    def delete(self, key):
        self.root = avl_delete(self.root, key)

    def __contains__(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def preorder(self):
        res = []

        def dfs(node):
            if node:
                res.append(node.key)
                dfs(node.left)
                dfs(node.right)

        dfs(self.root)
        return res

    def height(self):
        return height(self.root)
```

**验证退化不再发生**：

```python
t = AVLTree()
for i in range(1, 100000):
    t.insert(i)              # 升序插入 —— BST 会退化，AVL 不会
print(t.height())            # 约 17~24，而非 99999
```

## 4.1 插入 vs 删除的旋转次数

| | 旋转次数 |
| ---- | ---- |
| 插入 | **至多 1 次**（单旋或双旋算 1 次调整），之后树高不变，无需继续向上 |
| 删除 | 可能需要 **O(log n) 次**，因为子树变矮会向上传播 |

## 4.2 AVL 树与红黑树的比较

| | AVL | 红黑树 |
| ---- | ---- | ---- |
| 平衡条件 | 严格（高度差 ≤ 1） | 宽松（最长路 ≤ 2 倍最短路） |
| 树高 | ~1.44 log n | ~2 log n |
| 查找 | **更快** | 稍慢 |
| 插入/删除 | 旋转更多 | **旋转更少** |
| 典型应用 | 读多写少（数据库索引） | C++ `std::map`、Java `TreeMap`、Linux 内核 |

> **实践提示**：Python 标准库不含平衡树。OJ 上需要"有序 + 动态插删"时，用 `bisect.insort`（小规模）、树状数组 / 线段树（大规模），或手写 AVL / Treap。

---

# 第二部分：并查集

# 5 并查集（Disjoint Set Union, DSU）

## 5.1 要解决的问题

维护若干个**不相交集合**，支持两种操作：

- `find(x)`：查询 x 属于哪个集合（返回代表元）
- `union(x, y)`：把 x 和 y 所在的两个集合**合并**

典型问句："a 和 b 是不是一伙的？""现在还剩几个连通块？"

## 5.2 基本思想：森林

每个集合用一棵树表示，**树根就是代表元**。用 `parent` 数组记录每个结点的父亲，根的父亲是自己。

```
集合 {1,2,3}, {4,5}:

      1          4
     / \         |
    2   3        5

parent = [_, 1, 1, 1, 4, 4]
```

## 5.3 朴素实现及其问题

```python
def find(x):
    while parent[x] != x:
        x = parent[x]
    return x


def union(x, y):
    parent[find(x)] = find(y)
```

**问题**：若每次都把根挂到另一个根下，可能形成一条链，`find` 退化成 O(n)。

## 5.4 优化一：路径压缩（Path Compression）

`find` 时把路径上的所有结点**直接挂到根**下。

```
   find(4) 之前:        之后:
       1                   1
       |                / | | \
       2               2  3 4  5
       |
       3
       |
       4
```

```python
def find(x):
    """递归版路径压缩。"""
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]


def find_iter(x):
    """迭代版：两趟扫描，避免递归爆栈（推荐 OJ 使用）。"""
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root
```

## 5.5 优化二：按秩 / 按大小合并（Union by Rank / Size）

总是把**矮的树**挂到**高的树**下，避免树长高。

```python
def union_by_rank(x, y):
    rx, ry = find(x), find(y)
    if rx == ry:
        return False
    if rank[rx] < rank[ry]:
        rx, ry = ry, rx
    parent[ry] = rx
    if rank[rx] == rank[ry]:
        rank[rx] += 1
    return True
```

## 5.6 完整实现（推荐模板）

```python
class DSU:
    """并查集：路径压缩 + 按大小合并，单次操作近似 O(1)。"""

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n                # 连通分量个数

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:     # 路径压缩
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

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def group_size(self, x):
        return self.size[self.find(x)]
```

## 5.7 复杂度

同时使用路径压缩与按秩合并时，m 次操作的总时间为 **O(m · α(n))**，其中 α 是**反阿克曼函数**。对任何实际的 n（哪怕 n = 10^80），α(n) < 5，因此**可以认为单次操作是常数时间**。

| 优化 | 单次操作复杂度 |
| ---- | ---- |
| 无优化 | O(n) |
| 仅路径压缩 | O(log n) 均摊 |
| 仅按秩合并 | O(log n) |
| **两者都用** | **O(α(n)) ≈ O(1)** |

---

# 6 并查集的应用

## 6.1 连通分量计数

**OJ 02524: 宗教信仰**（经典模板题）

```python
import sys

data = sys.stdin.read().split()
p = 0
case = 0
out = []
while True:
    n, m = int(data[p]), int(data[p + 1]); p += 2
    if n == 0 and m == 0:
        break
    case += 1
    dsu = DSU(n + 1)
    for _ in range(m):
        a, b = int(data[p]), int(data[p + 1]); p += 2
        dsu.union(a, b)
    groups = len({dsu.find(i) for i in range(1, n + 1)})
    out.append(f"Case {case}: {groups}")
print('\n'.join(out))
```

**LeetCode 547. 省份数量**：

```python
def find_circle_num(is_connected):
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return dsu.count
```

## 6.2 传染问题

**OJ 01611: The Suspects**，http://cs101.openjudge.cn/practice/01611/

> n 个学生分在 m 个小组，0 号是嫌疑人，同组中只要有一个嫌疑人则全组都是。求嫌疑人总数。

```python
import sys

data = sys.stdin.read().split()
p = 0
out = []
while True:
    n, m = int(data[p]), int(data[p + 1]); p += 2
    if n == 0 and m == 0:
        break
    dsu = DSU(n)
    for _ in range(m):
        k = int(data[p]); p += 1
        members = [int(data[p + i]) for i in range(k)]; p += k
        for i in range(1, k):
            dsu.union(members[0], members[i])      # 同组全部合并
    out.append(str(dsu.group_size(0)))
print('\n'.join(out))
```

## 6.3 判断图中是否有环 / 冗余连接

**LeetCode 684. 冗余连接**：

```python
def find_redundant_connection(edges):
    dsu = DSU(len(edges) + 1)
    for a, b in edges:
        if not dsu.union(a, b):      # 已经连通，这条边构成环
            return [a, b]
```

**无向图判环**：加边时若两端已连通，则有环。这正是 **Kruskal 最小生成树**（第 14 周）的核心判据。

## 6.4 带权并查集：维护到根的关系

**OJ 07734: 虫子的生活**，http://cs101.openjudge.cn/practice/07734/

> 判断交互关系中是否存在同性恋（即是否存在奇环）。用"到根的奇偶距离"表示性别关系。

```python
class WeightedDSU:
    """rel[x] = x 与其父结点的关系（0 同类，1 异类），模 2 运算。"""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rel = [0] * n

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
            return (self.rel[x] ^ self.rel[y]) == d      # 一致则 True
        self.parent[rx] = ry
        self.rel[rx] = self.rel[x] ^ self.rel[y] ^ d
        return True
```

## 6.5 种类并查集（扩展域）

另一种思路：给每个元素开 k 个"分身"表示 k 种类别。

**OJ 01703: 发现它，抓住它（Find them, Catch them）** —— 判断两人是否属于同一个帮派（两个帮派）：

```python
# 开 2n 个结点：i 表示"i 在帮派 A"，i+n 表示"i 在帮派 B"
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
```

**食物链问题**（三种类别）用 3n 个结点，同理。

## 6.6 并查集 + 离线：按秩回退

某些问题需要"删边"，而并查集不支持删除。常见对策：
1. **离线处理，时间倒流**：把删边变成"倒着加边"。
2. **可撤销并查集**：只用按秩合并（不压缩路径），记录操作栈以便回滚，单次 O(log n)。

---

# 7 AVL 与并查集的对比

| | AVL 树 | 并查集 |
| ---- | ---- | ---- |
| 维护什么 | **有序**的动态集合 | **不相交集合的划分** |
| 核心操作 | 查找、插入、删除、前驱后继 | find、union |
| 单次复杂度 | O(log n) | O(α(n)) ≈ O(1) |
| 树的形态 | 严格控制高度 | 越扁越好，但不关心顺序 |
| 能否查询"第 k 小" | ✅（加 size 域） | ❌ |
| 能否查询"是否同组" | ❌ | ✅ |

---

# 8 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 平衡二叉树 | LC 110 | 平衡判定 |
| 2 | AVL 树的插入（课堂题） | 自测 | 四种旋转 |
| 3 | 将有序数组转换为二叉搜索树 | LC 108 | 平衡建树 |
| 4 | 宗教信仰 | OJ 02524 | 并查集计数 |
| 5 | The Suspects | OJ 01611 | 并查集 + size |
| 6 | 省份数量 | LC 547 | 连通分量 |
| 7 | 冗余连接 | LC 684 | 并查集判环 |
| 8 | 虫子的生活 | OJ 07734 | 带权 / 种类并查集 |
| 9 | 岛屿数量 | LC 200 | 并查集解法（对比第 8 周的 DFS 解法） |
| 10（选做） | 发现它，抓住它 | OJ 01703 | 扩展域并查集 |
| 11（选做） | 账户合并 | LC 721 | 并查集 + 哈希 |

**实验（第 5 次）**：实现 `AVLTree`，分别用"升序插入"和"随机插入"各 10⁵ 个键，记录并对比 BST 与 AVL 的树高与查找耗时，绘图说明平衡的价值。

**思考题**：

1. 为什么 AVL 插入至多旋转一次，而删除可能旋转 O(log n) 次？
2. 手工模拟：依次插入 10, 20, 30, 40, 50, 25，画出每一步的 AVL 树与旋转类型。
3. 只用路径压缩（不按秩合并），单次 `find` 的均摊复杂度是多少？为什么仍然很好？
4. 并查集为什么不能高效支持"删除一条边"？可撤销并查集为什么要放弃路径压缩？

---

# 9 小结

1. AVL 树用 **BF ∈ {−1,0,1}** 把树高锁定在 1.44 log n，代价是插删时要旋转。
2. 四种失衡 **LL / RR / LR / RL**，判定看"失衡结点的 BF 符号 + 其重侧孩子的 BF 符号"。
3. 并查集用森林表示集合，**路径压缩 + 按秩合并**后单次操作近似 O(1)。
4. 并查集的三类经典用法：**连通分量计数**、**判环**（Kruskal 的基础）、**带权/种类关系维护**。
5. 二者互补：AVL 管"顺序"，并查集管"分组"。

**下周预告**：把树推广到最一般的非线性结构——**图**的表示与遍历。
