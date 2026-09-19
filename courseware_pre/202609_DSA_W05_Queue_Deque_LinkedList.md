# 第5周 队列、双端队列；顺序表与链表

*Updated 2026-08-30 11:00 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 5 周 / 3 学时
> **教学内容**：队列、双端队列；列表的实现——顺序表与链表的对比；链表的实现——无序列表与有序列表
> **教学要求**：理解队列 FIFO 特性；能够实现队列与双端队列；理解顺序表与链表在存储与操作上的差异；掌握链表实现技巧；分析插入/删除的时间复杂度

**知识点**：队列 ADT 与 FIFO、循环队列、`collections.deque`、双端队列、约瑟夫问题、滑动窗口最大值（单调队列）、顺序表 vs 链表、单链表 / 双链表 / 循环链表、哨兵结点、无序表与有序表、链表反转 / 合并 / 判环 / 找中点。

---

# 1 队列 ADT

## 1.1 FIFO：先进先出

队列只允许在**队尾（rear）入队**、**队首（front）出队**。像排队买票：先来先服务。

```
    enqueue ->  [ 5 ][ 4 ][ 3 ][ 2 ][ 1 ]  -> dequeue
                rear                 front
```

| 操作 | 语义 | 期望复杂度 |
| ---- | ---- | ---- |
| `Queue()` | 创建空队列 | O(1) |
| `enqueue(item)` | 队尾入队 | O(1) |
| `dequeue()` | 队首出队并返回 | O(1) |
| `front()` | 查看队首 | O(1) |
| `is_empty()` | 判空 | O(1) |
| `size()` | 元素个数 | O(1) |

## 1.2 用 list 实现队列的陷阱

```python
class BadQueue:
    """❌ dequeue 是 O(n)：pop(0) 要搬移所有后续元素。"""

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)      # O(1)

    def dequeue(self):
        return self._items.pop(0)     # O(n)  <-- 灾难
```

n 次出队总代价 O(n²)。**BFS 用它必然超时。**

## 1.3 双指针实现（惰性删除）

若只需一次性处理（如 BFS），可以用"头指针 + 不真删"的写法，简单且快：

```python
q = [start]
head = 0
while head < len(q):
    cur = q[head]
    head += 1
    # ... 处理 cur，把新元素 q.append(...)
```

代价是空间不回收，但 BFS 中每个结点只入队一次，无妨。

## 1.4 循环队列（数组实现，重点掌握）

用固定容量数组 + 首尾指针，取模实现"绕回"，避免搬移。

```
容量 8，front=5，rear=2（下一个入队位置）
索引:  0    1    2    3    4    5    6    7
      [c]  [d]  [ ]  [ ]  [ ]  [a]  [b]  [ ]
                ^rear          ^front
```

**判空 / 判满的经典难题**：`front == rear` 既可能空也可能满。三种解法——(1) 牺牲一个单元；(2) 额外计数器；(3) 标志位。这里用计数器：

```python
class CircularQueue:
    """固定容量的循环队列，所有操作 O(1)。"""

    def __init__(self, capacity):
        self._data = [None] * capacity
        self._cap = capacity
        self._front = 0
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._cap

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("queue is full")
        rear = (self._front + self._size) % self._cap
        self._data[rear] = item
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return item

    def front(self):
        if self.is_empty():
            raise IndexError("empty queue")
        return self._data[self._front]

    def __len__(self):
        return self._size
```

对应练习：**LeetCode 622. 设计循环队列**，https://leetcode.cn/problems/design-circular-queue/

## 1.5 collections.deque：实战首选

```python
from collections import deque

q = deque()
q.append(x)        # 入队（右端）   O(1)
v = q.popleft()    # 出队（左端）   O(1)
q[0]               # 队首          O(1)
len(q)             # 大小          O(1)

dq = deque(maxlen=3)     # 定长队列，超出自动挤掉另一端
```

`deque` 底层是**双向链表连接的块（block）数组**，两端 O(1)，中间随机访问 O(n)。

---

# 2 双端队列（Deque）

两端都能进出的线性结构，是栈与队列的超集。

| 操作 | list | deque |
| ---- | ---- | ---- |
| `append` / `pop`（右端） | 均摊 O(1) | O(1) |
| `appendleft` / `popleft`（左端） | O(n) | **O(1)** |
| 随机访问 `d[i]` | O(1) | O(n) |

## 2.1 应用：回文判断

```python
from collections import deque


def is_palindrome(s: str) -> bool:
    d = deque(c for c in s.lower() if c.isalnum())
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True
```

## 2.2 应用：单调队列 —— 滑动窗口最大值

**LeetCode 239. 滑动窗口最大值**，https://leetcode.cn/problems/sliding-window-maximum/

> 长度为 k 的窗口在数组上滑动，输出每个窗口的最大值。n 可达 10⁵，朴素 O(nk) 会 TLE。

**单调队列**：队列中存下标，对应值**单调递减**；队首永远是当前窗口最大值。

```python
from collections import deque


def max_sliding_window(nums, k):
    dq = deque()          # 存下标，nums[dq] 单调递减
    ans = []
    for i, v in enumerate(nums):
        # 1) 队尾出：比新元素小的都不可能再当最大值
        while dq and nums[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        # 2) 队首出：滑出窗口的下标
        if dq[0] <= i - k:
            dq.popleft()
        # 3) 窗口成形后记录答案
        if i >= k - 1:
            ans.append(nums[dq[0]])
    return ans
```

每个下标最多入队、出队各一次 ⇒ **O(n)**。

> 单调栈（第 4 周）与单调队列（本周）是一对孪生技巧：都靠"及时丢掉永远不会成为答案的元素"把 O(n²) 压到 O(n)。

## 2.3 应用：约瑟夫问题

**OJ 02746: 约瑟夫问题**，http://cs101.openjudge.cn/practice/02746/

> n 个人围成一圈编号 1..n，从第 1 个人开始报数，每数到第 m 个人出列，求最后剩下者的编号。

**deque 旋转法**（直观）：

```python
from collections import deque

while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    d = deque(range(1, n + 1))
    while len(d) > 1:
        d.rotate(-(m - 1))      # 把第 m 个人转到队首
        d.popleft()             # 出列
    print(d[0])
```

**数学递推法**（O(n)，无需数据结构）：设 f(n) 为 n 个人时幸存者的 0-based 编号，

```
f(1) = 0
f(n) = (f(n-1) + m) % n
```

```python
def josephus(n, m):
    ans = 0
    for i in range(2, n + 1):
        ans = (ans + m) % i
    return ans + 1              # 转成 1-based
```

---

# 3 顺序表 vs 链表

## 3.1 两种存储结构

**顺序表（数组）**：元素连续存放，第 i 个元素地址 = 起始地址 + i × 元素大小。

```
内存:  [a0][a1][a2][a3][a4]
地址:  100 104 108 112 116     -> a[3] 地址直接算出，O(1)
```

**链表**：元素分散存放，每个结点额外存放"下一个结点的引用"。

```
head -> [a0|.]-> [a1|.]-> [a2|.]-> [a3|/]
        存数据 存指针                 None
```

## 3.2 复杂度对比（务必背下来）

| 操作 | 顺序表 | 单链表 |
| ---- | ---- | ---- |
| 按下标访问 `a[i]` | **O(1)** | O(n)（要从头走） |
| 头部插入/删除 | O(n) | **O(1)** |
| 尾部插入 | 均摊 O(1) | O(1)（有尾指针）/ O(n)（无） |
| **已知结点位置**后插入/删除 | O(n)（搬移） | **O(1)**（改指针） |
| 按值查找 | O(n) | O(n) |
| 空间开销 | 紧凑，但可能预留空位 | 每结点多存 1~2 个引用 |
| 缓存友好性 | **好**（连续内存） | 差（指针跳转） |

**结论**：
- 频繁**随机访问** → 顺序表。
- 频繁在**已知位置**插删、且元素个数变化剧烈 → 链表。
- 现代 CPU 缓存效应使得中小规模数据下数组常常反而更快——理论复杂度不是唯一考量。

---

# 4 链表的实现

## 4.1 结点

```python
class Node:
    __slots__ = ('value', 'next')

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt

    def __repr__(self):
        return f"Node({self.value!r})"
```

## 4.2 无序链表（UnorderedList）

```python
class UnorderedList:
    """无序单链表：头插 O(1)，查找/删除 O(n)。"""

    def __init__(self):
        self.head = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def add(self, item):
        """头插，O(1)。"""
        self.head = Node(item, self.head)
        self._size += 1

    def search(self, item):
        cur = self.head
        while cur is not None:
            if cur.value == item:
                return True
            cur = cur.next
        return False

    def remove(self, item):
        """删除第一个等于 item 的结点，O(n)。"""
        prev, cur = None, self.head
        while cur is not None:
            if cur.value == item:
                if prev is None:
                    self.head = cur.next     # 删的是头结点
                else:
                    prev.next = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def append(self, item):
        """尾插，O(n)（没有尾指针）。"""
        node = Node(item)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
        self._size += 1

    def index(self, item):
        cur, i = self.head, 0
        while cur is not None:
            if cur.value == item:
                return i
            cur, i = cur.next, i + 1
        return -1

    def __len__(self):
        return self._size

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __repr__(self):
        return " -> ".join(map(repr, self)) or "empty"
```

**删除操作的核心是"找前驱"**——这是单链表所有插删代码的共同难点。

## 4.3 哨兵结点（dummy head）：消除边界判断

上面的 `remove` 需要区分"删头结点"与"删中间结点"。加一个不存数据的**哨兵头结点**后，所有结点都有前驱，代码统一：

```python
class ListWithDummy:
    def __init__(self):
        self.dummy = Node(None)      # 永不删除
        self._size = 0

    def remove(self, item):
        prev = self.dummy
        while prev.next is not None:
            if prev.next.value == item:
                prev.next = prev.next.next     # 统一写法，无需特判
                self._size -= 1
                return True
            prev = prev.next
        return False
```

> **哨兵是链表题的第一原则**：写链表代码前先问自己"加个 dummy 能不能省掉特判"。

## 4.4 有序链表（OrderedList）

保持元素升序，`add` 需要找到插入位置：

```python
class OrderedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def add(self, item):
        """插入并保持有序，O(n)。"""
        prev, cur = None, self.head
        while cur is not None and cur.value < item:
            prev, cur = cur, cur.next
        node = Node(item, cur)
        if prev is None:
            self.head = node
        else:
            prev.next = node
        self._size += 1

    def search(self, item):
        """有序表可提前退出，但仍是 O(n)——链表无法二分。"""
        cur = self.head
        while cur is not None:
            if cur.value == item:
                return True
            if cur.value > item:
                return False        # 提前剪枝
            cur = cur.next
        return False
```

⚠️ **关键认知**：有序**数组**可以二分查找 O(log n)，有序**链表**不行（无法 O(1) 跳到中间），仍是 O(n)。要在链表上做到 O(log n)，需要跳表（skip list）或平衡树（第 11 周）。

## 4.5 双向链表

```python
class DNode:
    __slots__ = ('value', 'prev', 'next')

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """带头尾哨兵的双向链表：两端插删 O(1)，已知结点删除 O(1)。"""

    def __init__(self):
        self.head = DNode(None)
        self.tail = DNode(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self._size = 0

    def _insert_after(self, node, value):
        new = DNode(value)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        self._size += 1
        return new

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1
        return node.value

    def push_front(self, value):
        return self._insert_after(self.head, value)

    def push_back(self, value):
        return self._insert_after(self.tail.prev, value)

    def pop_front(self):
        if self._size == 0:
            raise IndexError("empty")
        return self._unlink(self.head.next)

    def pop_back(self):
        if self._size == 0:
            raise IndexError("empty")
        return self._unlink(self.tail.prev)

    def __len__(self):
        return self._size
```

**双链表是 LRU 缓存的核心**（哈希表定位结点 + 双链表 O(1) 移动），见 LeetCode 146。

---

# 5 链表经典题型

## 5.1 反转链表

**LeetCode 206. 反转链表**，https://leetcode.cn/problems/reverse-linked-list/

```python
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next        # 1. 存住后继
        cur.next = prev       # 2. 掉头
        prev, cur = cur, nxt  # 3. 前进
    return prev               # 新头
```

递归版：

```python
def reverse_list_rec(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_list_rec(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

## 5.2 合并两个有序链表

**LeetCode 21**，https://leetcode.cn/problems/merge-two-sorted-lists/

```python
def merge_two_lists(l1, l2):
    dummy = tail = Node(None)          # 哨兵登场
    while l1 and l2:
        if l1.value <= l2.value:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2               # 接上剩余部分
    return dummy.next
```

## 5.3 快慢指针：找中点、判环

**LeetCode 876. 链表的中间结点** / **141. 环形链表**

```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow                # 偶数个时返回后一个中点


def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def detect_cycle(head):
    """LC 142：返回入环结点。相遇后，从头和相遇点同速前进，再次相遇即入口。"""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p, slow = p.next, slow.next
            return p
    return None
```

## 5.4 删除倒数第 n 个结点

**LeetCode 19**，https://leetcode.cn/problems/remove-nth-node-from-end-of-list/

```python
def remove_nth_from_end(head, n):
    dummy = Node(None, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next          # fast 先走 n 步
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next    # slow 停在待删结点的前驱
    return dummy.next
```

---

# 6 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 约瑟夫问题 | OJ 02746 | deque 模拟 / 递推 |
| 2 | 设计循环队列 | LC 622 | 循环队列 |
| 3 | 用栈实现队列 | LC 232 | ADT 转换、均摊分析 |
| 4 | 滑动窗口最大值 | LC 239 | 单调队列 |
| 5 | 反转链表 | LC 206 | 链表指针操作 |
| 6 | 合并两个有序链表 | LC 21 | 哨兵结点 |
| 7 | 环形链表 II | LC 142 | 快慢指针 |
| 8 | 删除链表的倒数第 N 个结点 | LC 19 | 双指针 |
| 9（选做） | LRU 缓存 | LC 146 | 哈希 + 双链表 |
| 10（选做） | 排序链表 | LC 148 | 链表归并排序（第 6 周预习） |

**实验（第 2 次）**：实现 `UnorderedList`、`OrderedList` 与 `CircularQueue`，用 `unittest` 编写测试；再对比"链表头插 n 次"与"list.insert(0,x) n 次"的实测耗时。

**思考题**：

1. 循环队列若不用计数器，为什么"牺牲一个存储单元"就能区分空与满？此时判满条件怎么写？
2. 单链表删除**给定结点**（不给头指针）能做到 O(1) 吗？（提示：LC 237，把后继的值搬过来）
3. 为什么有序链表不能二分查找？跳表是怎么绕开这个限制的？
4. `deque` 的 `rotate(-k)` 复杂度是多少？约瑟夫问题用 rotate 模拟的总复杂度是？

---

# 7 小结

1. 队列 = **FIFO**，实战一律用 `collections.deque`；数组实现要用**循环队列**避免搬移。
2. 双端队列是栈与队列的统一；**单调队列**解决滑动窗口极值，O(n)。
3. 顺序表 vs 链表的取舍：**随机访问 vs 任意位置插删**，另需考虑缓存友好性。
4. 链表编程三板斧：**哨兵结点**、**快慢指针**、**先存后继再改指针**。
5. 有序链表不能二分——这为第 10、11 周的树形结构埋下伏笔。

**下周预告**：**递归与分治**，以及五大经典排序算法的实现与性能对比。
