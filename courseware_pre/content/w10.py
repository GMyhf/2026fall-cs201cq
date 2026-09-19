# -*- coding: utf-8 -*-
"""第10周 堆、堆排序、二叉搜索树"""

META = {
    'title': '第10周　堆与二叉搜索树',
    'subtitle': '二叉堆 · 堆排序 · 优先队列 · BST',
    'footer': '数据结构与算法 · 第10周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：理解堆的性质与操作；掌握 BST 的基本操作及其时间复杂度'],
}

SLIDES = [
    ('section', '第 1 节', '二叉堆'),

    ('ascii', '二叉堆 = 完全二叉树 + 堆序性', r"""
小根堆:
            1
          /   \
         3     2
        / \   / \
       6   5 4   8

数组表示（1-based）: [_, 1, 3, 2, 6, 5, 4, 8]

⚠️ 堆只保证【父子有序】，不保证兄弟或同层有序 —— 堆不是排好序的数组
"""),

    ('table', '数组表示的下标关系', [
        ['表示', '左孩子', '右孩子', '父'],
        ['1-based（根在 1）', '2i', '2i+1', 'i // 2'],
        ['0-based（根在 0）', '2i+1', '2i+2', '(i-1) // 2'],
    ], '完全二叉树可以紧凑存进数组，无需任何指针'),

    ('bullets', '两个核心操作', [
        '**上浮（sift up）**：插入新元素后，若比父亲小就交换，直到满足堆序',
        '**下沉（sift down）**：删除根后把末尾元素放到根，与**较小的孩子**交换下沉',
        '两者都沿着一条根—叶路径走，长度 **O(log n)**',
    ]),

    ('code', '二叉堆实现（1-based 小根堆）', '''class BinaryHeap:
    def __init__(self):
        self._heap = [0]        # 下标 0 占位不用
        self._size = 0

    def _sift_up(self, i):
        while i // 2 > 0 and self._heap[i] < self._heap[i // 2]:
            self._heap[i], self._heap[i//2] = self._heap[i//2], self._heap[i]
            i //= 2

    def _min_child(self, i):
        if 2 * i + 1 > self._size:
            return 2 * i                        # 只有左孩子
        return 2*i if self._heap[2*i] < self._heap[2*i+1] else 2*i+1

    def _sift_down(self, i):
        while 2 * i <= self._size:
            mc = self._min_child(i)
            if self._heap[i] <= self._heap[mc]:
                break
            self._heap[i], self._heap[mc] = self._heap[mc], self._heap[i]
            i = mc
'''),

    ('code', 'push / pop / build', '''    def push(self, item):                    # O(log n)
        self._heap.append(item)
        self._size += 1
        self._sift_up(self._size)

    def pop(self):                           # O(log n)
        top = self._heap[1]
        self._heap[1] = self._heap[self._size]   # 末尾元素放到根
        self._heap.pop()
        self._size -= 1
        if self._size:
            self._sift_down(1)
        return top

    def build(self, items):                  # ⭐ O(n) 建堆
        self._heap = [0] + list(items)
        self._size = len(items)
        for i in range(self._size // 2, 0, -1):   # 从最后一个非叶结点开始
            self._sift_down(i)
'''),

    ('table', '⭐ 为什么建堆是 O(n) 而不是 O(n log n)', [
        ['高度 h', '该高度的结点数', '每个的下沉代价'],
        ['0（叶）', '~n/2', '0'],
        ['1', '~n/4', '1'],
        ['2', '~n/8', '2'],
        ['…', '…', '…'],
        ['log n', '1', 'log n'],
    ], '总代价 = Σ (n / 2^(h+1))·h = n·Σ h/2^(h+1) ≤ n·1 = O(n)　（用到 Σ h/2^h = 2）'),

    ('section', '第 2 节', 'heapq 与堆排序'),

    ('code', 'heapq：Python 的标准小根堆', '''import heapq

h = []
heapq.heappush(h, 5)            # O(log n)
smallest = heapq.heappop(h)     # O(log n)，弹出最小
top = h[0]                      # O(1)，查看最小但不弹

a = [5, 3, 8, 1]
heapq.heapify(a)                # ⭐ O(n)，原地建堆

heapq.heappushpop(h, x)         # 先 push 再 pop，比分开快
heapq.heapreplace(h, x)         # 先 pop 再 push
heapq.nlargest(k, iterable)     # Top-K 大
heapq.merge(*iterables)         # 归并多个有序序列（惰性）
'''),

    ('code', '大根堆的三种做法 + 元组陷阱', '''# 方法 1：取负数（数值型首选）
heapq.heappush(h, -x)
largest = -heapq.heappop(h)

# 方法 2：元组第一维取负（带附加数据）
heapq.heappush(h, (-priority, data))

# 方法 3：包装类，反向定义 __lt__
class MaxItem:
    def __lt__(self, other):
        return self.val > other.val      # 反向


# ⚠️ 元组比较陷阱：dist 相同时会去比第二维
heapq.heappush(h, (dist, some_object))   # 对象无 __lt__ 会报错

import itertools
counter = itertools.count()
heapq.heappush(h, (dist, next(counter), some_object))   # ✅ 加序号打破平局
'''),

    ('code', '堆排序：原地 O(1) 空间', '''def heap_sort(a):
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

    for start in range(n // 2 - 1, -1, -1):      # 1) 建大根堆 O(n)
        sift_down(start, n - 1)
    for end in range(n - 1, 0, -1):              # 2) 反复换堆顶到末尾
        a[0], a[end] = a[end], a[0]
        sift_down(0, end - 1)
    return a
'''),

    ('table', '三种 O(n log n) 排序对比', [
        ['', '归并', '快排', '堆排'],
        ['最坏', 'O(n log n)', '⚠️ O(n²)', '⭐ O(n log n)'],
        ['额外空间', 'O(n)', 'O(log n)', '⭐ O(1)'],
        ['稳定', '✅', '❌', '❌'],
        ['实测常数', '中', '⭐ 小', '大（缓存不友好）'],
    ]),

    ('section', '第 3 节', '优先队列的应用'),

    ('code', 'Top-K：维护大小为 k 的小根堆', '''import heapq


def kth_largest(nums, k):
    """LC 215：O(n log k)，且支持数据流。"""
    h = nums[:k]
    heapq.heapify(h)
    for v in nums[k:]:
        if v > h[0]:
            heapq.heapreplace(h, v)
    return h[0]          # 堆顶即第 k 大
''', 'k 远小于 n 时优于排序的 O(n log n)，且数据不必全部装进内存'),

    ('code', '⭐ LC 295 数据流的中位数：对顶堆', '''class MedianFinder:
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
'''),

    ('code', 'OJ 22161 Huffman 编码树', '''import heapq


def build_huffman(freq: dict):
    h = [HuffNode(w, c, c) for c, w in freq.items()]
    heapq.heapify(h)
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        merged = HuffNode(a.weight + b.weight, min(a.key, b.key), None, a, b)
        heapq.heappush(h, merged)
    return h[0]
''', '贪心正确性：权值最小的两个字符一定在最深层且互为兄弟'),

    ('bullets', '堆的其他经典应用', [
        '**Dijkstra 最短路**（第 13 周）：优先队列取出当前最近的结点',
        '**Prim 最小生成树**（第 14 周）：优先队列取出最小横切边',
        '**任务调度 / 会议室**：LC 253 会议室 II',
        '**贪心 + 堆**：OJ 18164 剪绳子、LC 1046 最后一块石头的重量',
    ]),

    ('section', '第 4 节', '二叉搜索树（BST）'),

    ('ascii', 'BST 的定义与核心性质', r"""
            8
          /   \
         3     10
        / \      \
       1   6      14
          / \     /
         4   7   13

对任意结点 x：左子树全部 < x < 右子树全部

⭐ 最重要的性质：中序遍历 = 升序序列
   1  3  4  6  7  8  10  13  14
"""),

    ('code', '查找与插入', '''def search(root, key):                 # O(h)
    cur = root
    while cur:
        if key == cur.val:
            return cur
        cur = cur.left if key < cur.val else cur.right
    return None


def insert(root, key):                 # O(h)
    if root is None:
        return TreeNode(key)           # ⭐ 新结点总是插入为叶结点
    if key < root.val:
        root.left = insert(root.left, key)
    elif key > root.val:
        root.right = insert(root.right, key)
    return root
'''),

    ('code', '⭐ 删除：三种情况（重点）', '''def delete(root, key):
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
        # 情况 3：两个孩子，用右子树最小值（中序后继）顶替
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root
''', '也可用左子树最大值（中序前驱）顶替，效果相同'),

    ('ascii', '删除有两个孩子的结点', r"""
删除 3：

        8                         8
      /   \                     /   \
     3     10       ==>        4     10
    / \      \                / \      \
   1   6      14             1   6      14
      / \                       / \
     4   7                     _   7
     ^ 中序后继顶上来
"""),

    ('ascii', '⚠️ BST 的退化问题', r"""
按升序插入 1,2,3,4,5：

  1
   \
    2
     \
      3
       \
        4
         \
          5      树高 = n-1，所有操作退化成 O(n)
""", '解决方案：① 自平衡树（AVL / 红黑树，第 11 周）② 随机化 ③ 直接用 dict'),

    ('table', 'BST 复杂度', [
        ['操作', '平均（随机插入）', '最坏（退化）'],
        ['查找 / 插入 / 删除', 'O(log n)', '⚠️ O(n)'],
    ], '随机顺序插入 n 个键的期望树高是 O(log n)，但输入顺序不由我们决定'),

    ('code', 'BST 典型题', '''def is_valid_bst(root):            # LC 98：用上下界，别只比较父子
    def check(node, lo, hi):
        if node is None: return True
        if not (lo < node.val < hi): return False
        return check(node.left, lo, node.val) and \\
               check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))


def kth_smallest(root, k):         # LC 230：中序遍历第 k 个
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right


def lca_bst(root, p, q):           # LC 235：利用有序性，O(h)
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:   cur = cur.left
        elif p.val > cur.val and q.val > cur.val: cur = cur.right
        else: return cur
'''),

    ('code', 'Python 中的“有序容器”替代方案', '''import bisect

# 有序列表：查找 O(log n)，但插入/删除 O(n)（要搬移）
a = []
bisect.insort(a, x)              # 插入并保持有序
i = bisect.bisect_left(a, x)     # 二分查找位置

# 第三方（多数 OJ 不可用，本地可用）
# from sortedcontainers import SortedList   # 均 O(log n)
''', 'n ≤ 10⁵ 时 bisect.insort 的搬移是 C 实现的 memmove，常数极小，通常够用'),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '实现堆结构', 'OJ 04078', '手写堆'],
        ['2', '数组中的第K个最大元素', 'LC 215', '小根堆 Top-K'],
        ['3', '前 K 个高频元素', 'LC 347', 'Counter + 堆'],
        ['4', '数据流的中位数', 'LC 295', '对顶堆'],
        ['5', '哈夫曼编码树', 'OJ 22161', '堆 + 贪心建树'],
        ['6', '验证二叉搜索树 / 第K小', 'LC 98 / 230', 'BST 性质、中序'],
        ['7', '删除二叉搜索树中的节点', 'LC 450', 'BST 删除三种情况'],
        ['8', '将有序数组转换为 BST', 'LC 108', '平衡建树'],
    ], '实验四：实现 BinaryHeap 与 BST；实测随机插入 vs 升序插入的树高与查找时间'),

    ('bullets', '本讲小结', [
        '二叉堆 = **完全二叉树 + 堆序性**；用数组存储，父子下标可算',
        'push / pop 是 O(log n)（上浮 / 下沉），**建堆是 O(n)**',
        '`heapq` 是小根堆；大根堆取负数；元组比较小心第二维',
        '堆的杀手锏：**Top-K**、**对顶堆求中位数**、**Huffman**、**Dijkstra/Prim**',
        'BST 中序遍历升序；操作 O(h)，**h 最坏是 n** —— 这就是下周要解决的问题',
    ]),
]
