# -*- coding: utf-8 -*-
"""第5周 队列、双端队列；顺序表与链表"""

META = {
    'title': '第5周　队列、双端队列与链表',
    'subtitle': 'FIFO · 循环队列 · 单调队列 · 顺序表 vs 链表',
    'footer': '数据结构与算法 · 第5周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：理解队列 FIFO 特性；能够实现队列与双端队列；'
             '理解顺序表与链表在存储与操作上的差异；掌握链表实现技巧；'
             '分析插入/删除的时间复杂度'],
}

SLIDES = [
    ('bullets', '本讲内容', [
        '**队列 ADT**', '- FIFO、循环队列、collections.deque',
        '**双端队列**', '- 回文判断、单调队列、约瑟夫问题',
        '**顺序表 vs 链表**', '- 存储结构对比与复杂度权衡',
        '**链表的实现**', '- 无序表、有序表、双向链表、哨兵结点',
        '**链表经典题型**', '- 反转、合并、快慢指针',
    ]),

    ('section', '第 1 节', '队列 ADT'),

    ('ascii', 'FIFO：先进先出', r"""
    enqueue ->  [ 5 ][ 4 ][ 3 ][ 2 ][ 1 ]  -> dequeue
                rear                 front

    只允许队尾入队、队首出队；像排队买票，先来先服务
"""),

    ('code', '⚠️ 用 list 实现队列的陷阱', '''class BadQueue:
    """dequeue 是 O(n)：pop(0) 要搬移所有后续元素。"""

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)      # O(1)

    def dequeue(self):
        return self._items.pop(0)     # O(n)  <-- 灾难
''', 'n 次出队总代价 O(n²) —— BFS 用它必然超时'),

    ('code', '双指针写法：惰性删除（BFS 常用）', '''q = [start]
head = 0
while head < len(q):
    cur = q[head]
    head += 1
    # ... 处理 cur，把新元素 q.append(...)
''', '代价是空间不回收；但 BFS 中每个结点只入队一次，无妨'),

    ('ascii', '循环队列：取模实现“绕回”，避免搬移', r"""
容量 8，front = 5，rear = 2（下一个入队位置）

索引:  0    1    2    3    4    5    6    7
      [c]  [d]  [ ]  [ ]  [ ]  [a]  [b]  [ ]
                ^rear          ^front

判空/判满难题：front == rear 时既可能空也可能满
三种解法：(1) 牺牲一个单元 (2) 额外计数器 (3) 标志位
"""),

    ('code', '循环队列实现（用计数器）', '''class CircularQueue:
    def __init__(self, capacity):
        self._data = [None] * capacity
        self._cap = capacity
        self._front = 0
        self._size = 0

    def enqueue(self, item):
        if self._size == self._cap:
            raise OverflowError("queue is full")
        rear = (self._front + self._size) % self._cap
        self._data[rear] = item
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        item = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return item
''', '对应练习：LC 622 设计循环队列'),

    ('code', '⭐ collections.deque：实战首选', '''from collections import deque

q = deque()
q.append(x)        # 入队（右端）   O(1)
v = q.popleft()    # 出队（左端）   O(1)
q[0]               # 队首          O(1)
len(q)             # 大小          O(1)

dq = deque(maxlen=3)     # 定长队列，超出自动挤掉另一端
''', 'deque 底层是双向链表连接的块数组：两端 O(1)，中间随机访问 O(n)'),

    ('section', '第 2 节', '双端队列'),

    ('table', 'list vs deque', [
        ['操作', 'list', 'deque'],
        ['append / pop（右端）', '均摊 O(1)', 'O(1)'],
        ['appendleft / popleft（左端）', '⚠️ O(n)', '⭐ O(1)'],
        ['随机访问 d[i]', 'O(1)', 'O(n)'],
    ]),

    ('code', '应用：回文判断', '''from collections import deque


def is_palindrome(s: str) -> bool:
    d = deque(c for c in s.lower() if c.isalnum())
    while len(d) > 1:
        if d.popleft() != d.pop():     # 两端同时取
            return False
    return True
'''),

    ('key', '单调队列', '队列中存下标，对应值单调递减\n队首永远是当前窗口的最大值 —— O(n)'),

    ('code', 'LC 239 滑动窗口最大值', '''from collections import deque


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
''', '每个下标最多入队、出队各一次 ⇒ O(n)。朴素做法 O(nk) 在 n=10⁵ 时会 TLE'),

    ('bullets', '单调栈与单调队列：一对孪生技巧', [
        '**单调栈**（第 4 周）：求“下一个更大 / 更小元素”',
        '**单调队列**（本周）：求“滑动窗口极值”',
        '共同思想：**及时丢掉永远不会成为答案的元素**',
        '共同效果：把 O(n²) 压到 O(n)，靠的是“每个元素进出各一次”的均摊分析',
    ]),

    ('code', 'OJ 02746 约瑟夫问题：两种解法', '''from collections import deque

# 解法 1：deque 旋转法（直观）
while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    d = deque(range(1, n + 1))
    while len(d) > 1:
        d.rotate(-(m - 1))      # 把第 m 个人转到队首
        d.popleft()             # 出列
    print(d[0])


# 解法 2：数学递推，O(n)，无需数据结构
def josephus(n, m):
    ans = 0                      # f(1) = 0
    for i in range(2, n + 1):
        ans = (ans + m) % i      # f(n) = (f(n-1) + m) % n
    return ans + 1               # 转成 1-based
'''),

    ('section', '第 3 节', '顺序表 vs 链表'),

    ('ascii', '两种存储结构', r"""
顺序表（数组）：元素连续存放
   内存:  [a0][a1][a2][a3][a4]
   地址:  100 104 108 112 116     ->  a[3] 地址直接算出，O(1)

链表：元素分散存放，每个结点额外存"下一个结点的引用"
   head -> [a0|.]-> [a1|.]-> [a2|.]-> [a3|/]
           存数据 存指针                  None
"""),

    ('table', '⭐ 复杂度对比（务必背下来）', [
        ['操作', '顺序表', '单链表'],
        ['按下标访问 a[i]', '⭐ O(1)', 'O(n)（要从头走）'],
        ['头部插入 / 删除', 'O(n)', '⭐ O(1)'],
        ['尾部插入', '均摊 O(1)', 'O(1) 有尾指针 / O(n) 无'],
        ['已知结点位置后插删', 'O(n)（搬移）', '⭐ O(1)（改指针）'],
        ['按值查找', 'O(n)', 'O(n)'],
        ['空间开销', '紧凑，可能预留空位', '每结点多存 1~2 个引用'],
        ['缓存友好性', '⭐ 好（连续内存）', '差（指针跳转）'],
    ], '结论：频繁随机访问用顺序表；频繁在已知位置插删用链表。理论复杂度不是唯一考量'),

    ('section', '第 4 节', '链表的实现'),

    ('code', '结点与无序链表', '''class Node:
    __slots__ = ('value', 'next')

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class UnorderedList:
    def __init__(self):
        self.head = None

    def add(self, item):                  # 头插，O(1)
        self.head = Node(item, self.head)

    def search(self, item):               # O(n)
        cur = self.head
        while cur is not None:
            if cur.value == item:
                return True
            cur = cur.next
        return False
''', '删除操作的核心难点是“找前驱” —— 单链表所有插删代码的共同麻烦'),

    ('code', '⭐ 哨兵结点（dummy head）：消除边界判断', '''# 没有哨兵：要区分"删头结点"与"删中间结点"
def remove(self, item):
    prev, cur = None, self.head
    while cur:
        if cur.value == item:
            if prev is None:
                self.head = cur.next      # 特判！
            else:
                prev.next = cur.next
            return True
        prev, cur = cur, cur.next


# 有哨兵：所有结点都有前驱，代码统一
def remove(self, item):
    prev = self.dummy
    while prev.next:
        if prev.next.value == item:
            prev.next = prev.next.next    # 无需特判
            return True
        prev = prev.next
''', '写链表代码前先问自己：加个 dummy 能不能省掉特判？'),

    ('code', '有序链表：插入时找位置', '''class OrderedList:
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
''', '⚠️ 关键认知：有序【数组】可二分 O(log n)；有序【链表】不行，仍是 O(n)'),

    ('key', '为什么有序链表不能二分',
     '链表无法 O(1) 跳到中间位置\n要做到 O(log n)，需要跳表或平衡树（第 11 周）'),

    ('bullets', '双向链表', [
        '每个结点同时存 `prev` 与 `next`；配合**头尾哨兵**，两端插删都是 O(1)',
        '**已知结点时删除也是 O(1)** —— 不需要再找前驱',
        '典型应用：**LRU 缓存**（哈希表定位结点 + 双链表 O(1) 移动），LC 146',
        'Python 的 `collections.deque` 内部就是块状双向链表',
    ]),

    ('section', '第 5 节', '链表经典题型'),

    ('code', 'LC 206 反转链表', '''def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next        # 1. 存住后继
        cur.next = prev       # 2. 掉头
        prev, cur = cur, nxt  # 3. 前进
    return prev               # 新头


def reverse_list_rec(head):            # 递归版
    if head is None or head.next is None:
        return head
    new_head = reverse_list_rec(head.next)
    head.next.next = head
    head.next = None
    return new_head
''', '口诀：先存后继，再改指针'),

    ('code', 'LC 21 合并两个有序链表（哨兵登场）', '''def merge_two_lists(l1, l2):
    dummy = tail = Node(None)
    while l1 and l2:
        if l1.value <= l2.value:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2               # 接上剩余部分
    return dummy.next
'''),

    ('code', '快慢指针：找中点、判环、找入环点', '''def middle_node(head):                 # LC 876
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow


def detect_cycle(head):                # LC 142：返回入环结点
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:               # 相遇
            p = head
            while p is not slow:       # 从头和相遇点同速前进
                p, slow = p.next, slow.next
            return p                   # 再次相遇即入口
    return None
'''),

    ('code', 'LC 19 删除链表的倒数第 N 个结点', '''def remove_nth_from_end(head, n):
    dummy = Node(None, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next          # fast 先走 n 步
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next    # slow 停在待删结点的前驱
    return dummy.next
'''),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '约瑟夫问题', 'OJ 02746', 'deque 模拟 / 递推'],
        ['2', '设计循环队列', 'LC 622', '循环队列'],
        ['3', '用栈实现队列', 'LC 232', 'ADT 转换、均摊分析'],
        ['4', '滑动窗口最大值', 'LC 239', '单调队列'],
        ['5', '反转链表 / 合并两个有序链表', 'LC 206 / 21', '指针操作、哨兵'],
        ['6', '环形链表 II', 'LC 142', '快慢指针'],
        ['7', '删除链表的倒数第 N 个结点', 'LC 19', '双指针'],
        ['8（选做）', 'LRU 缓存 / 排序链表', 'LC 146 / 148', '哈希+双链表 / 链表归并'],
    ], '实验二：实现 UnorderedList、OrderedList、CircularQueue 并配单元测试'),

    ('bullets', '本讲小结', [
        '队列 = **FIFO**，实战一律用 `deque`；数组实现要用**循环队列**避免搬移',
        '**单调队列**解决滑动窗口极值，O(n)',
        '顺序表 vs 链表的取舍：**随机访问 vs 任意位置插删**，另需考虑缓存友好性',
        '链表编程三板斧：**哨兵结点**、**快慢指针**、**先存后继再改指针**',
        '**下周预告**：递归与分治，以及五大经典排序算法',
    ]),
]
