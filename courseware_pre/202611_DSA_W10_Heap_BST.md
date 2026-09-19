# 第10周 堆、堆排序、二叉搜索树

*Updated 2026-08-30 12:40 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 10 周 / 3 学时
> **教学内容**：堆、堆排序、二叉搜索树
> **教学要求**：理解堆的性质与操作；掌握 BST 的基本操作及其时间复杂度

**知识点**：二叉堆（完全二叉树 + 堆序性）、数组表示、上浮 / 下沉、O(n) 建堆、堆排序、优先队列、`heapq` 用法与大根堆技巧、Top-K、中位数双堆、Huffman 树、二叉搜索树的定义与中序性质、BST 的查找 / 插入 / 删除、BST 退化问题。

---

# 1 二叉堆

## 1.1 定义

**二叉堆**是满足以下两个条件的二叉树：

1. **结构性**：是一棵**完全二叉树**（除最后一层外填满，最后一层从左到右连续）。
2. **堆序性**：
   - **小根堆（min-heap）**：每个结点的值 ≤ 其孩子的值 → 根是最小值。
   - **大根堆（max-heap）**：每个结点的值 ≥ 其孩子的值 → 根是最大值。

⚠️ 堆**只保证父子有序，不保证兄弟或同层有序**——堆不是排好序的数组。

```
小根堆:
            1
          /   \
         3     2
        / \   / \
       6   5 4   8

数组表示（1-based）: [_, 1, 3, 2, 6, 5, 4, 8]
```

## 1.2 数组表示

完全二叉树可以紧凑存进数组，无需指针：

| 表示 | 左孩子 | 右孩子 | 父 |
| ---- | ---- | ---- | ---- |
| 1-based（根在下标 1） | `2i` | `2i+1` | `i // 2` |
| 0-based（根在下标 0） | `2i+1` | `2i+2` | `(i-1) // 2` |

## 1.3 核心操作：上浮与下沉

**上浮（sift up / percolate up）**：插入新元素后，它可能比父亲小，与父亲交换直到满足堆序。

**下沉（sift down / percolate down）**：删除根后把末尾元素放到根，它可能比孩子大，与**较小的孩子**交换直到满足堆序。

两者都沿着一条从叶到根（或根到叶）的路径走，长度 O(log n)。

## 1.4 完整实现（1-based 小根堆）

```python
class BinaryHeap:
    """1-based 数组实现的小根堆。下标 0 占位不用。"""

    def __init__(self, items=None):
        self._heap = [0]
        self._size = 0
        if items:
            self.build(items)

    # ---------- 内部：上浮与下沉 ----------
    def _sift_up(self, i):
        while i // 2 > 0:
            if self._heap[i] < self._heap[i // 2]:
                self._heap[i], self._heap[i // 2] = self._heap[i // 2], self._heap[i]
                i //= 2
            else:
                break

    def _min_child(self, i):
        if 2 * i + 1 > self._size:
            return 2 * i                        # 只有左孩子
        return 2 * i if self._heap[2 * i] < self._heap[2 * i + 1] else 2 * i + 1

    def _sift_down(self, i):
        while 2 * i <= self._size:
            mc = self._min_child(i)
            if self._heap[i] > self._heap[mc]:
                self._heap[i], self._heap[mc] = self._heap[mc], self._heap[i]
                i = mc
            else:
                break

    # ---------- 对外接口 ----------
    def push(self, item):
        """插入，O(log n)。"""
        self._heap.append(item)
        self._size += 1
        self._sift_up(self._size)

    def pop(self):
        """弹出最小值，O(log n)。"""
        if self._size == 0:
            raise IndexError("pop from empty heap")
        top = self._heap[1]
        self._heap[1] = self._heap[self._size]  # 末尾元素放到根
        self._heap.pop()
        self._size -= 1
        if self._size:
            self._sift_down(1)
        return top

    def peek(self):
        if self._size == 0:
            raise IndexError("empty heap")
        return self._heap[1]

    def build(self, items):
        """O(n) 建堆：从最后一个非叶结点开始，依次下沉。"""
        self._heap = [0] + list(items)
        self._size = len(items)
        for i in range(self._size // 2, 0, -1):
            self._sift_down(i)

    def __len__(self):
        return self._size
```

## 1.5 为什么建堆是 O(n) 而不是 O(n log n)

朴素做法是 n 次 `push`，每次 O(log n)，共 O(n log n)。

**自底向上建堆**：从最后一个非叶结点（下标 `n//2`）开始逐个下沉。关键在于**大多数结点很矮**：

| 高度 h | 该高度的结点数 | 每个的下沉代价 |
| ---- | ---- | ---- |
| 0（叶） | ~n/2 | 0 |
| 1 | ~n/4 | 1 |
| 2 | ~n/8 | 2 |
| … | | |
| log n | 1 | log n |

总代价 = Σ (n / 2^(h+1)) · h = n · Σ h/2^(h+1) ≤ n · 1 = **O(n)**。

（用到 Σ_{h≥0} h/2^h = 2。）

---

# 2 heapq：Python 的标准堆

`heapq` 实现的是 **0-based 小根堆**，直接操作普通 list。

```python
import heapq

h = []
heapq.heappush(h, 5)            # O(log n)
heapq.heappush(h, 1)
smallest = heapq.heappop(h)     # O(log n)，弹出最小
top = h[0]                      # O(1)，查看最小但不弹

a = [5, 3, 8, 1]
heapq.heapify(a)                # O(n)，原地建堆

heapq.heappushpop(h, x)         # 先 push 再 pop，比分开快
heapq.heapreplace(h, x)         # 先 pop 再 push

heapq.nlargest(k, iterable)     # Top-K 大
heapq.nsmallest(k, iterable)    # Top-K 小
heapq.merge(*iterables)         # 归并多个有序序列（惰性）
```

## 2.1 大根堆的三种做法

Python 只有小根堆，实现大根堆：

```python
# 方法 1：取负数（数值型首选）
heapq.heappush(h, -x)
largest = -heapq.heappop(h)

# 方法 2：元组第一维取负（带附加数据）
heapq.heappush(h, (-priority, data))

# 方法 3：包装类，反向定义 __lt__
class MaxItem:
    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val      # 反向
```

## 2.2 元组比较的陷阱

```python
heapq.heappush(h, (dist, node))      # ✅ node 是 int，可比较

# ❌ 若 dist 相同，会去比较第二维；若第二维是自定义对象且没有 __lt__ 会报错
heapq.heappush(h, (dist, some_object))

# ✅ 加一个自增序号打破平局
counter = itertools.count()
heapq.heappush(h, (dist, next(counter), some_object))
```

---

# 3 堆排序

```python
def heap_sort(a):
    """原地大根堆排序，O(n log n) 时间，O(1) 额外空间，不稳定。"""
    n = len(a)

    def sift_down(start, end):
        root = start
        while 2 * root + 1 <= end:
            child = 2 * root + 1
            if child + 1 <= end and a[child] < a[child + 1]:
                child += 1                       # 取较大的孩子
            if a[root] < a[child]:
                a[root], a[child] = a[child], a[root]
                root = child
            else:
                return

    # 1) 建大根堆，O(n)
    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n - 1)

    # 2) 反复把堆顶（最大值）换到末尾，缩小堆范围，O(n log n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(0, end - 1)

    return a
```

**与其他 O(n log n) 排序对比**：

| | 归并 | 快排 | 堆排 |
| ---- | ---- | ---- | ---- |
| 最坏 | O(n log n) | O(n²) | **O(n log n)** |
| 额外空间 | O(n) | O(log n) | **O(1)** |
| 稳定 | ✅ | ❌ | ❌ |
| 实测常数 | 中 | **小** | 大（缓存不友好） |

**OJ 04078: 实现堆结构** 是本节的模板题。

---

# 4 优先队列的应用

## 4.1 Top-K 问题

**LeetCode 215. 第 K 个最大元素**：维护大小为 k 的**小根堆**，堆顶即第 k 大。

```python
import heapq


def kth_largest(nums, k):
    h = nums[:k]
    heapq.heapify(h)
    for v in nums[k:]:
        if v > h[0]:
            heapq.heapreplace(h, v)
    return h[0]
```

O(n log k)，当 k 远小于 n 时优于排序的 O(n log n)，且**支持数据流**（数据不能全部装进内存）。

**LeetCode 347. 前 K 个高频元素**：

```python
from collections import Counter


def top_k_frequent(nums, k):
    cnt = Counter(nums)
    return [v for v, _ in cnt.most_common(k)]
    # 或： return heapq.nlargest(k, cnt, key=cnt.get)
```

## 4.2 数据流中位数：对顶堆

**LeetCode 295. 数据流的中位数**，https://leetcode.cn/problems/find-median-from-data-stream/

用**大根堆存较小的一半**、**小根堆存较大的一半**，保持两堆size差 ≤ 1。

```python
import heapq


class MedianFinder:
    def __init__(self):
        self.small = []      # 大根堆（存负值），较小的一半
        self.large = []      # 小根堆，较大的一半

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        # 保证 small 的最大值 <= large 的最小值
        heapq.heappush(self.large, -heapq.heappop(self.small))
        # 保持 len(small) >= len(large)
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

**OJ 相关**：动态中位数问题。

## 4.3 合并 K 个有序链表 / 序列

```python
import heapq


def merge_k_sorted(lists):
    h = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(h)
    res = []
    while h:
        val, i, j = heapq.heappop(h)
        res.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(h, (lists[i][j + 1], i, j + 1))
    return res
```

O(N log k)。

## 4.4 Huffman 编码树

**OJ 22161: 哈夫曼编码树**

每次取两个最小权值合并，构造出**带权路径长度（WPL）最小**的二叉树。

```python
import heapq


class HuffNode:
    def __init__(self, weight, key, char=None, left=None, right=None):
        self.weight = weight
        self.key = key          # 子树中最小的字符，用于权值相同时打破平局
        self.char = char        # 只有叶结点非 None
        self.left = left
        self.right = right

    def __lt__(self, other):
        # 权值相同时比较子树最小字符，保证不同实现得到同一棵树
        if self.weight != other.weight:
            return self.weight < other.weight
        return self.key < other.key


def build_huffman(freq: dict):
    h = [HuffNode(w, c, c) for c, w in freq.items()]
    heapq.heapify(h)
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        merged = HuffNode(a.weight + b.weight, min(a.key, b.key),
                          None, a, b)
        heapq.heappush(h, merged)
    return h[0]


def build_codes(node, prefix='', table=None):
    if table is None:
        table = {}
    if node.left is None and node.right is None:
        table[node.char] = prefix or '0'
        return table
    build_codes(node.left, prefix + '0', table)
    build_codes(node.right, prefix + '1', table)
    return table
```

**贪心正确性**：权值最小的两个字符一定在最深层且互为兄弟（否则交换可使 WPL 更小）。

## 4.5 其他典型应用

- **Dijkstra 最短路**（第 13 周）：优先队列取出当前最近的结点。
- **Prim 最小生成树**（第 14 周）：优先队列取出最小横切边。
- **任务调度 / 会议室**：LC 253 会议室 II。
- **OJ 18164 剪绳子**、LC 1046 最后一块石头的重量：贪心 + 堆。

---

# 5 二叉搜索树（BST）

## 5.1 定义与核心性质

**二叉搜索树**是满足以下条件的二叉树：对任意结点 x，
- 左子树中所有结点的键 **< x.key**
- 右子树中所有结点的键 **> x.key**
- 左右子树也都是 BST

**最重要的性质：BST 的中序遍历是升序序列。**

```
            8
          /   \
         3     10
        / \      \
       1   6      14
          / \     /
         4   7   13

中序: 1 3 4 6 7 8 10 13 14   <- 升序
```

## 5.2 查找

```python
def search(root, key):
    """迭代版，O(h)。"""
    cur = root
    while cur:
        if key == cur.val:
            return cur
        cur = cur.left if key < cur.val else cur.right
    return None


def search_rec(root, key):
    if root is None or root.val == key:
        return root
    return search_rec(root.left, key) if key < root.val \
        else search_rec(root.right, key)
```

## 5.3 插入

```python
def insert(root, key):
    """返回新的子树根，O(h)。重复键直接忽略。"""
    if root is None:
        return TreeNode(key)
    if key < root.val:
        root.left = insert(root.left, key)
    elif key > root.val:
        root.right = insert(root.right, key)
    return root
```

**新结点总是插入为叶结点**——这是 BST 插入的关键认知。

## 5.4 删除（三种情况，重点）

```python
def find_min(node):
    while node.left:
        node = node.left
    return node


def delete(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        # 情况 1 & 2：至多一个孩子，直接用孩子顶替
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        # 情况 3：两个孩子，用右子树的最小值（中序后继）顶替
        succ = find_min(root.right)
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root
```

```
删除 3（有两个孩子）：

        8                         8
      /   \                     /   \
     3     10       ==>        4     10
    / \      \                / \      \
   1   6      14             1   6      14
      / \                       / \
     4   7                     _   7
     ^ 中序后继顶上来
```

也可以用**左子树的最大值（中序前驱）**顶替，效果相同。

## 5.5 完整的 BST 类

```python
class BST:
    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, key):
        def _ins(node):
            if node is None:
                self._size += 1
                return TreeNode(key)
            if key < node.val:
                node.left = _ins(node.left)
            elif key > node.val:
                node.right = _ins(node.right)
            return node
        self.root = _ins(self.root)

    def __contains__(self, key):
        cur = self.root
        while cur:
            if key == cur.val:
                return True
            cur = cur.left if key < cur.val else cur.right
        return False

    def inorder(self):
        res, stack, cur = [], [], self.root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right
        return res

    def min(self):
        cur = self.root
        while cur and cur.left:
            cur = cur.left
        return cur.val if cur else None

    def max(self):
        cur = self.root
        while cur and cur.right:
            cur = cur.right
        return cur.val if cur else None

    def __len__(self):
        return self._size
```

## 5.6 复杂度与退化问题

| 操作 | 平均（随机插入） | 最坏（退化） |
| ---- | ---- | ---- |
| 查找 / 插入 / 删除 | O(log n) | **O(n)** |

**退化**：按升序插入 1,2,3,…,n，BST 变成一条右斜链，退化成链表：

```
插入 1,2,3,4,5:
  1
   \
    2
     \
      3
       \
        4
         \
          5      树高 = n-1，所有操作 O(n)
```

**解决方案**：
1. **自平衡树**：AVL 树（第 11 周）、红黑树、Treap。
2. **随机化**：随机打乱插入顺序，或用 Treap。
3. 实践中直接用 `dict`（哈希表，第 15 周）——若不需要有序性。

## 5.7 BST 的典型题

```python
def is_valid_bst(root):
    """LC 98：验证 BST。用上下界比"只比较父子"更可靠。"""
    def check(node, lo, hi):
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return check(node.left, lo, node.val) and check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))


def kth_smallest(root, k):
    """LC 230：BST 中第 k 小 —— 中序遍历第 k 个。"""
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right


def lca_bst(root, p, q):
    """LC 235：BST 的 LCA —— 利用有序性，O(h)。"""
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            return cur


def sorted_array_to_bst(nums):
    """LC 108：有序数组 -> 平衡 BST。取中点作根。"""
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(nums[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(nums) - 1)
```

## 5.8 Python 中的"有序容器"替代方案

Python 标准库没有平衡树，常用替代：

```python
import bisect

# 有序列表：查找 O(log n)，但插入/删除 O(n)（要搬移）
a = []
bisect.insort(a, x)              # 插入并保持有序
i = bisect.bisect_left(a, x)     # 二分查找位置

# 第三方库（多数 OJ 不可用，本地可用）
# from sortedcontainers import SortedList   # 插入/删除/查找均 O(log n)
```

> **OJ 实战**：n ≤ 10⁵ 时 `bisect.insort` 的 O(n) 搬移常数极小（C 实现的 memmove），通常够用；更大规模需要树状数组或线段树。

---

# 6 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 实现堆结构 | OJ 04078 | 手写堆 |
| 2 | 数组中的第K个最大元素 | LC 215 | 小根堆 Top-K |
| 3 | 前 K 个高频元素 | LC 347 | Counter + 堆 |
| 4 | 数据流的中位数 | LC 295 | 对顶堆 |
| 5 | 最后一块石头的重量 | LC 1046 | 大根堆模拟 |
| 6 | 哈夫曼编码树 | OJ 22161 | 堆 + 贪心建树 |
| 7 | 验证二叉搜索树 | LC 98 | BST 性质 |
| 8 | 二叉搜索树中第K小的元素 | LC 230 | 中序遍历 |
| 9 | 删除二叉搜索树中的节点 | LC 450 | BST 删除三种情况 |
| 10 | 将有序数组转换为二叉搜索树 | LC 108 | 平衡建树 |
| 11（选做） | 会议室 II | LC 253 | 优先队列调度 |

**实验（第 4 次）**：实现 `BinaryHeap` 与 `BST` 两个类并配单元测试；实测"随机插入 10⁵ 个键"与"升序插入 10⁵ 个键"两种情况下 BST 的平均查找时间与树高，验证退化现象。

**思考题**：

1. 证明自底向上建堆的时间复杂度是 O(n)。
2. 堆能在 O(log n) 内取出最小值，那能在 O(log n) 内**查找任意元素**吗？为什么？
3. BST 删除时用"右子树最小值"和"左子树最大值"顶替，结果树形一样吗？
4. 为什么随机顺序插入 n 个键的 BST 期望树高是 O(log n)？

---

# 7 小结

1. 二叉堆 = 完全二叉树 + 堆序性；用**数组**存储，父子下标可算。
2. `push`/`pop` 是 O(log n)（上浮/下沉），**建堆是 O(n)**。
3. `heapq` 是小根堆；大根堆取负数。元组比较要小心第二维。
4. 堆的杀手锏：**Top-K**、**对顶堆求中位数**、**Huffman**、**Dijkstra/Prim 的优先队列**。
5. BST 的中序遍历是升序；查找/插入/删除 O(h)，**h 最坏是 n**——这就是下周 AVL 树要解决的问题。

**下周预告**：**AVL 树**（用旋转维持平衡）与**并查集**（近乎 O(1) 的集合合并与查询）。
