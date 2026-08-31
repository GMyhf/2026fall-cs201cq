# 第15周 散列表、KMP、倒排索引 → RAG

*Updated 2026-08-31 04:20 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*
https://github.com/GMyhf/2026fall-cs201cq

> **大纲对应**：第 15 周 / 3 学时
> **教学内容**：散列表、KMP、倒排索引 → RAG
> **教学要求**：掌握散列表的实现原理；理解 KMP 算法的 next 数组计算；了解散列与倒排索引在 RAG 检索系统中的应用

**知识点**：散列函数、装填因子、冲突解决（开放定址 / 链地址）、再散列、Python `dict` 与 `set` 的实现、字符串哈希、朴素串匹配、KMP 的 next（失配）数组、Trie 前缀树、倒排索引、TF-IDF、BM25、向量检索与近似最近邻、RAG 检索增强生成。

---

# 第一部分：散列表

# 1 从数组到散列表

数组按下标访问是 O(1)，但我们通常想用**任意的键**（字符串、元组）而不是 0..n−1 的整数来索引。

**散列表（Hash Table）的核心思想**：用一个**散列函数 h(key)** 把任意键映射成数组下标，从而实现平均 O(1) 的插入、查找、删除。

```
   key = "apple"
        |
        v   h(key) = hash("apple") % 11 = 4
   +---+---+---+---+-------+---+---+
   | 0 | 1 | 2 | 3 | apple | 5 | ...
   +---+---+---+---+-------+---+---+
                       4
```

## 1.1 散列函数的设计

一个好的散列函数应当：

1. **计算快**（O(键长)）。
2. **均匀分布**（尽量减少冲突）。
3. **确定性**（同一个键永远得到同一个值）。

**常见构造法**：

```python
# 除留余数法（最常用）：m 取素数效果更好
def h_div(key, m):
    return key % m


# 折叠法：把长数字分段相加
def h_fold(phone: str, m):
    parts = [int(phone[i:i + 2]) for i in range(0, len(phone), 2)]
    return sum(parts) % m


# 平方取中法
def h_mid_square(key, m):
    s = str(key * key)
    mid = s[len(s) // 2 - 1: len(s) // 2 + 1]
    return int(mid) % m


# 字符串散列：多项式滚动哈希（BKDR / Horner 形式）
def h_string(s: str, m, base=31):
    v = 0
    for ch in s:
        v = (v * base + ord(ch)) % m
    return v
```

> **注意加权**：`sum(ord(c) for c in s)` 这种不加权的写法会让 "abc"、"bca"、"cab" 冲突——**位置信息必须参与计算**。

## 1.2 装填因子

```
装填因子 λ = 已存元素个数 / 表长
```

λ 越大，冲突越多，性能越差。工程上通常在 λ > 0.7（或 2/3）时**扩容再散列（rehash）**：表长翻倍，把所有元素重新插入。

| λ | 开放定址（线性探测）平均查找次数 |
| ---- | ---- |
| 0.5 | 成功 1.5，失败 2.5 |
| 0.75 | 成功 2.5，失败 8.5 |
| 0.9 | 成功 5.5，失败 50.5 |

---

# 2 冲突解决

不同的键映射到同一个槽位，称为**冲突（collision）**。由鸽巢原理，冲突不可避免。

## 2.1 开放定址法（Open Addressing）

冲突时按某种探测序列去找下一个空槽。

| 方法 | 探测序列 | 问题 |
| ---- | ---- | ---- |
| **线性探测** | h, h+1, h+2, … | **一次聚集**（primary clustering） |
| **二次探测** | h, h+1², h+2², … | 二次聚集，可能探测不到全表 |
| **双重散列** | h, h+h₂(k), h+2h₂(k), … | 效果最好 |

```python
class OpenAddressingHashTable:
    """线性探测的散列表。删除用墓碑标记。"""

    _EMPTY = object()
    _DELETED = object()

    def __init__(self, capacity=11):
        self._cap = capacity
        self._keys = [self._EMPTY] * capacity
        self._vals = [None] * capacity
        self._size = 0

    def _probe(self, key):
        """返回 key 所在或应插入的槽位下标。"""
        idx = hash(key) % self._cap
        first_deleted = -1
        for _ in range(self._cap):
            k = self._keys[idx]
            if k is self._EMPTY:
                return first_deleted if first_deleted >= 0 else idx
            if k is self._DELETED:
                if first_deleted < 0:
                    first_deleted = idx
            elif k == key:
                return idx
            idx = (idx + 1) % self._cap        # 线性探测
        raise RuntimeError("hash table full")

    def _rehash(self):
        old = [(k, v) for k, v in zip(self._keys, self._vals)
               if k is not self._EMPTY and k is not self._DELETED]
        self._cap = self._cap * 2 + 1          # 保持奇数（更接近素数）
        self._keys = [self._EMPTY] * self._cap
        self._vals = [None] * self._cap
        self._size = 0
        for k, v in old:
            self[k] = v

    def __setitem__(self, key, value):
        if (self._size + 1) / self._cap > 0.7:
            self._rehash()
        idx = self._probe(key)
        if self._keys[idx] is self._EMPTY or self._keys[idx] is self._DELETED:
            self._size += 1
        self._keys[idx] = key
        self._vals[idx] = value

    def __getitem__(self, key):
        idx = self._probe(key)
        if self._keys[idx] == key:
            return self._vals[idx]
        raise KeyError(key)

    def __delitem__(self, key):
        idx = self._probe(key)
        if self._keys[idx] != key:
            raise KeyError(key)
        self._keys[idx] = self._DELETED        # 墓碑，不能置 EMPTY
        self._vals[idx] = None
        self._size -= 1

    def __contains__(self, key):
        idx = self._probe(key)
        return self._keys[idx] == key

    def __len__(self):
        return self._size
```

> ⚠️ **开放定址法删除必须用墓碑**：直接置空会切断探测链，导致后面的元素查不到。

## 2.2 链地址法（Separate Chaining）

每个槽位挂一个链表（或列表），冲突元素都放进去。

```python
class ChainingHashTable:
    def __init__(self, capacity=11):
        self._cap = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % self._cap]

    def __setitem__(self, key, value):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value)
                return
        b.append((key, value))
        self._size += 1
        if self._size / self._cap > 2:      # 链地址法可以容忍 λ > 1
            self._rehash()

    def __getitem__(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                self._size -= 1
                return
        raise KeyError(key)

    def _rehash(self):
        items = [(k, v) for b in self._buckets for k, v in b]
        self._cap = self._cap * 2 + 1
        self._buckets = [[] for _ in range(self._cap)]
        self._size = 0
        for k, v in items:
            self[k] = v

    def __len__(self):
        return self._size
```

| | 开放定址 | 链地址 |
| ---- | ---- | ---- |
| 内存 | 紧凑，缓存友好 | 有指针开销 |
| 装填因子上限 | 必须 < 1 | 可以 > 1 |
| 删除 | 需墓碑，麻烦 | 简单 |
| 聚集问题 | 有 | 无 |
| 最坏查找 | O(n) | O(链长) |

## 2.3 Python 的 dict / set 是怎么实现的

CPython 的 `dict` 采用**开放定址 + 随机化探测**（`perturb` 机制），并从 3.6 起使用**紧凑布局**（indices 数组 + entries 数组），因此保持了插入顺序。

- 平均 O(1)，**最坏 O(n)**（人为构造大量冲突时，称为**哈希碰撞攻击**）。
- Python 对 `str` 的哈希默认加了**随机盐**（`PYTHONHASHSEED`）以缓解此类攻击。
- 只有**可哈希（不可变）**对象能作键：`int`、`str`、`tuple`（内部元素也须可哈希）、`frozenset`。

```python
hash("abc")          # 每次运行程序结果不同（随机盐）
hash((1, 2, 3))      # 元组可哈希
hash([1, 2, 3])      # ❌ TypeError: unhashable type: 'list'
```

**自定义类作键**必须同时实现 `__hash__` 和 `__eq__`，且满足：`a == b ⟹ hash(a) == hash(b)`。

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))       # 用元组的哈希，简单可靠
```

---

# 第二部分：字符串匹配

# 3 朴素匹配与 KMP

## 3.1 问题

在文本 T（长 n）中找模式串 P（长 m）的所有出现位置。

## 3.2 朴素算法 O(nm)

```python
def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    res = []
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            res.append(i)
    return res
```

**问题**：失配时，`i` 只往前挪一位，**已经比较过的信息全部丢弃**。

```
T: a a a a a b
P: a a a b
       ^ 失配，朴素算法把 i 挪到 1 重新从头比
```

## 3.3 KMP 的核心洞察

失配时，我们已经知道 `P[0..j-1]` 与文本匹配。若 `P[0..j-1]` 有一个长度为 k 的**最长相等前后缀**，那么可以直接把模式串滑到"前缀 k 对齐"的位置，**文本指针 i 完全不用回退**。

```
P = "ababc"，已匹配 "abab" 后在 c 处失配
"abab" 的最长相等前后缀是 "ab"（长度 2）
=> 下次从 P[2] 开始比较，i 不动
```

## 3.4 next（失配）数组

定义 `nxt[i]` = `P[0..i]` 的**最长相等真前后缀**的长度。

```
P:      a  b  a  b  c  a  b  a  b
nxt:    0  0  1  2  0  1  2  3  4
```

手工推导 `P = "ababc"`：

| i | P[0..i] | 最长相等真前后缀 | nxt[i] |
| - | ---- | ---- | ---- |
| 0 | a | 无（真前后缀不能是自身） | 0 |
| 1 | ab | 无 | 0 |
| 2 | aba | "a" | 1 |
| 3 | abab | "ab" | 2 |
| 4 | ababc | 无 | 0 |

**构建代码**（本质是模式串自己和自己做 KMP）：

```python
def build_next(pattern):
    """nxt[i] = pattern[0..i] 的最长相等真前后缀长度。O(m)。"""
    m = len(pattern)
    nxt = [0] * m
    k = 0                              # 当前最长相等前后缀的长度
    for i in range(1, m):
        while k > 0 and pattern[i] != pattern[k]:
            k = nxt[k - 1]             # 回退到更短的候选前缀
        if pattern[i] == pattern[k]:
            k += 1
        nxt[i] = k
    return nxt
```

## 3.5 KMP 匹配

```python
def kmp_search(text, pattern):
    """返回 pattern 在 text 中所有出现的起始下标。O(n + m)。"""
    if not pattern:
        return []
    nxt = build_next(pattern)
    res = []
    j = 0                              # 已匹配的模式串长度
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = nxt[j - 1]             # 失配，模式串右滑，i 不回退
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            res.append(i - j + 1)
            j = nxt[j - 1]             # 继续找下一个（允许重叠）
    return res
```

**复杂度证明（均摊）**：`j` 每次至多加 1（共 n 次），而 while 循环每次都让 `j` 减少，`j` 非负，所以总的减少次数 ≤ 总的增加次数 = n。因此整体 **O(n + m)**。

## 3.6 KMP 的典型应用

```python
def min_period(s):
    """求字符串的最小循环节长度。若 n % (n - nxt[n-1]) == 0 则整周期。"""
    n = len(s)
    nxt = build_next(s)
    p = n - nxt[n - 1]
    return p if n % p == 0 else n


def repeated_substring_pattern(s):
    """LC 459：判断字符串能否由子串重复构成。"""
    n = len(s)
    nxt = build_next(s)
    return nxt[n - 1] > 0 and n % (n - nxt[n - 1]) == 0
```

**OJ 相关**：01961 前缀中的周期、02406 字符串乘方（都是求循环节）。

## 3.7 字符串哈希（Rabin-Karp）

另一条路：把子串映射成数字，O(1) 比较。

```python
MOD = (1 << 61) - 1
BASE = 131


def build_hash(s):
    """前缀哈希 + 幂表，支持 O(1) 查询任意子串哈希。"""
    n = len(s)
    h = [0] * (n + 1)
    pw = [1] * (n + 1)
    for i, ch in enumerate(s):
        h[i + 1] = (h[i] * BASE + ord(ch)) % MOD
        pw[i + 1] = pw[i] * BASE % MOD
    return h, pw


def sub_hash(h, pw, l, r):
    """s[l:r] 的哈希值，O(1)。"""
    return (h[r] - h[l] * pw[r - l]) % MOD
```

- 优点：实现简单，能处理"任意两子串是否相等""最长公共子串"等 KMP 难做的问题。
- 缺点：有**碰撞概率**；对抗性数据下可能被 hack（用随机 BASE 与大模数缓解）。

## 3.8 Trie 前缀树

```python
class Trie:
    """LC 208。插入/查询 O(L)，L 为串长。"""

    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word):
        node = self
        for ch in word:
            node = node.children.setdefault(ch, Trie())
        node.is_end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find(prefix) is not None

    def _find(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

Trie 是**倒排索引与自动补全**的基础结构，也是下面 RAG 一节中"词典"的实现之一。

---

# 第三部分：倒排索引 → RAG

# 4 倒排索引

## 4.1 正排 vs 倒排

| | 正排索引（forward index） | **倒排索引（inverted index）** |
| ---- | ---- | ---- |
| 结构 | 文档 → 它包含的词 | **词 → 包含它的文档列表** |
| 回答 | "文档 5 里有什么词？" | **"哪些文档含有'算法'？"** |
| 用途 | 存储原文 | **搜索引擎的核心** |

```
文档集：
  d1: "数据 结构 与 算法"
  d2: "算法 分析 与 复杂度"
  d3: "数据 分析"

倒排索引：
  数据   -> [d1, d3]
  结构   -> [d1]
  算法   -> [d1, d2]
  分析   -> [d2, d3]
  复杂度 -> [d2]
```

**为什么快**：查询"算法"时不必扫描全部文档，**一次哈希查找**（散列表！）就拿到候选文档列表。倒排索引 = 散列表 + 排序好的 posting list。

## 4.2 一个可运行的迷你搜索引擎

```python
import math
import re
from collections import defaultdict, Counter


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)     # term -> {doc_id: 词频}
        self.doc_len = {}                  # doc_id -> 文档词数
        self.docs = {}                     # doc_id -> 原文
        self.n_docs = 0

    @staticmethod
    def tokenize(text):
        """极简分词：英文按单词，中文按字（生产中用 jieba 等）。"""
        return re.findall(r'[a-zA-Z]+|[一-鿿]', text.lower())

    def add(self, doc_id, text):
        tokens = self.tokenize(text)
        self.docs[doc_id] = text
        self.doc_len[doc_id] = len(tokens)
        self.n_docs += 1
        for term, tf in Counter(tokens).items():
            self.index[term][doc_id] = tf      # 建立倒排

    # ---------- 布尔检索 ----------
    def search_and(self, query):
        """所有词都出现的文档：posting list 求交集。"""
        terms = self.tokenize(query)
        if not terms:
            return set()
        result = set(self.index.get(terms[0], {}))
        for t in terms[1:]:
            result &= set(self.index.get(t, {}))
        return result

    def search_or(self, query):
        result = set()
        for t in self.tokenize(query):
            result |= set(self.index.get(t, {}))
        return result

    # ---------- TF-IDF 排序检索 ----------
    def idf(self, term):
        df = len(self.index.get(term, {}))
        return math.log((self.n_docs + 1) / (df + 1)) + 1     # 平滑

    def search_tfidf(self, query, top_k=5):
        scores = defaultdict(float)
        for term in self.tokenize(query):
            idf = self.idf(term)
            for doc_id, tf in self.index.get(term, {}).items():
                scores[doc_id] += (tf / self.doc_len[doc_id]) * idf
        return sorted(scores.items(), key=lambda x: -x[1])[:top_k]

    # ---------- BM25（工业界标准）----------
    def search_bm25(self, query, top_k=5, k1=1.5, b=0.75):
        avgdl = sum(self.doc_len.values()) / max(self.n_docs, 1)
        scores = defaultdict(float)
        for term in self.tokenize(query):
            idf = self.idf(term)
            for doc_id, tf in self.index.get(term, {}).items():
                dl = self.doc_len[doc_id]
                num = tf * (k1 + 1)
                den = tf + k1 * (1 - b + b * dl / avgdl)
                scores[doc_id] += idf * num / den
        return sorted(scores.items(), key=lambda x: -x[1])[:top_k]


# ---------- 演示 ----------
idx = InvertedIndex()
idx.add(1, "数据结构与算法是计算机科学的基础")
idx.add(2, "算法分析关注时间复杂度与空间复杂度")
idx.add(3, "数据分析常用于机器学习")
idx.add(4, "图算法包括最短路和最小生成树")

print(idx.search_and("数据 算法"))          # 同时含两词的文档
print(idx.search_bm25("算法 复杂度"))       # 按相关性排序
```

## 4.3 TF-IDF 与 BM25

**TF-IDF** = 词频 × 逆文档频率：

```
TF(t, d)  = t 在 d 中出现的次数 / d 的总词数        —— 词在本文档中越频繁越重要
IDF(t)    = log(N / df(t))                        —— 词在越少的文档中出现越有区分度
score     = TF × IDF
```

直觉：像"的""是"这类词在每篇文档都出现，IDF 接近 0，自动被降权。

**BM25** 是 TF-IDF 的改进，加入了两个修正：
- **词频饱和**：一个词出现 100 次不应该比出现 10 次重要 10 倍（`k1` 控制）。
- **文档长度归一化**：长文档天然含更多词，需要惩罚（`b` 控制）。

BM25 至今仍是**工业界最强的稀疏检索基线**，Elasticsearch 的默认打分函数。

---

# 5 从倒排索引到 RAG

## 5.1 稀疏检索的局限

倒排索引依赖**字面词匹配**，遇到下面的情况就失效：

- 查询"如何加快程序运行速度" vs 文档"算法优化技巧" —— **同义但不同词**。
- 查询"苹果的股价" vs 文档"苹果富含维生素" —— **同词但不同义**。

## 5.2 稠密检索（向量检索）

用**嵌入模型（embedding model）**把文本映射成高维向量，语义相近的文本向量距离也近。

```python
import math


def cosine_similarity(a, b):
    """余弦相似度：衡量两个向量的方向接近程度，范围 [-1, 1]。"""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def brute_force_search(query_vec, doc_vecs, top_k=5):
    """暴力最近邻：O(N·d)。N 很大时需要 ANN 索引。"""
    scored = [(cosine_similarity(query_vec, v), i)
              for i, v in enumerate(doc_vecs)]
    scored.sort(reverse=True)
    return scored[:top_k]
```

**N 达到百万级时暴力搜索太慢**，需要**近似最近邻（ANN）**索引——而这些索引全部建立在本课程学过的数据结构之上：

| ANN 方法 | 用到的数据结构 | 本课程对应章节 |
| ---- | ---- | ---- |
| **HNSW**（分层可导航小世界图） | **图** + 分层跳表 | W12 图、W5 链表 |
| **IVF**（倒排文件） | **聚类 + 倒排索引** | 本周 |
| **LSH**（局部敏感哈希） | **散列表** | 本周 |
| **KD-Tree / Ball Tree** | **树** | W9–W11 |
| **PQ**（乘积量化） | 分块 + 查表 | — |

> 💡 **这就是本课程的落点**：向量数据库（FAISS、Milvus、Qdrant）不是魔法，它们是**图、树、散列表在高维空间中的工程化应用**。学好数据结构，才能理解现代 AI 基础设施。

## 5.3 RAG：检索增强生成

**RAG（Retrieval-Augmented Generation）**让大语言模型在回答前先"查资料"，解决三个痛点：

1. **知识截止**：模型训练数据有时间上限。
2. **幻觉**：模型会编造看似合理的错误内容。
3. **私域知识**：模型没见过你的公司文档、课程讲义。

**完整流水线**：

```
【离线：建索引】
  文档 --分块--> chunks --嵌入--> 向量 --建索引--> 向量库
                    \                              (HNSW / IVF)
                     \--分词--> 倒排索引 (BM25)

【在线：查询】
  用户提问
     |
     +--> 稀疏检索 (BM25，倒排索引)  --+
     |                                  +--> 混合排序 --> 重排序 --> Top-K
     +--> 稠密检索 (向量最近邻)      --+     (RRF)      (Rerank)
                                                                |
                                                                v
                              把 Top-K 片段拼进 Prompt，交给 LLM 生成答案
```

## 5.4 一个最小 RAG 原型

```python
class MiniRAG:
    """演示用：BM25 稀疏检索 + 向量稠密检索 + RRF 融合。"""

    def __init__(self, embed_fn=None):
        self.bm25 = InvertedIndex()
        self.chunks = []
        self.vectors = []
        self.embed_fn = embed_fn        # 真实场景接入嵌入模型 API

    # ---------- 离线建库 ----------
    @staticmethod
    def chunk(text, size=200, overlap=50):
        """滑动窗口分块，overlap 保证跨块的句子不被切断。"""
        res, i = [], 0
        while i < len(text):
            res.append(text[i:i + size])
            i += size - overlap
        return res

    def add_document(self, text):
        for c in self.chunk(text):
            cid = len(self.chunks)
            self.chunks.append(c)
            self.bm25.add(cid, c)
            if self.embed_fn:
                self.vectors.append(self.embed_fn(c))

    # ---------- 在线检索 ----------
    def retrieve(self, query, top_k=3):
        sparse = [doc_id for doc_id, _ in self.bm25.search_bm25(query, top_k * 2)]
        dense = []
        if self.embed_fn and self.vectors:
            qv = self.embed_fn(query)
            dense = [i for _, i in brute_force_search(qv, self.vectors, top_k * 2)]
        merged = self.reciprocal_rank_fusion([sparse, dense])
        return [self.chunks[i] for i in merged[:top_k]]

    @staticmethod
    def reciprocal_rank_fusion(rank_lists, k=60):
        """RRF：把多路排序结果融合，score = Σ 1/(k + rank)。"""
        scores = defaultdict(float)
        for lst in rank_lists:
            for rank, doc_id in enumerate(lst):
                scores[doc_id] += 1.0 / (k + rank + 1)
        return [d for d, _ in sorted(scores.items(), key=lambda x: -x[1])]

    # ---------- 生成 ----------
    def build_prompt(self, query, top_k=3):
        context = "\n\n---\n\n".join(self.retrieve(query, top_k))
        return (f"请仅依据以下资料回答问题。若资料中没有答案，请明确说明。\n\n"
                f"【资料】\n{context}\n\n【问题】{query}\n\n【回答】")
```

## 5.5 RAG 中每一步用到的数据结构

| RAG 环节 | 数据结构 / 算法 | 本课程周次 |
| ---- | ---- | ---- |
| 文本分块 | 字符串处理、滑动窗口 | W3、W5 |
| 关键词索引 | **散列表 + 倒排索引** | **W15** |
| 关键词匹配 | **KMP / Trie** | **W15** |
| 词频统计 | 哈希表（Counter） | W2、W15 |
| 向量索引 | **图（HNSW）/ 树（KD-Tree）/ 哈希（LSH）** | W9–W12 |
| Top-K 召回 | **堆** | W10 |
| 多路结果融合 | 排序 + 哈希 | W6、W15 |
| 依赖调度（Agent 工作流） | **拓扑排序** | W14 |

**这张表是本课程"传统算法与现代 AI 融合"的具体注脚**：一个 RAG 系统，几乎把整学期的数据结构用了一遍。

## 5.6 AI 辅助算法实践小项目建议（占总评 10%）

结合本周内容，推荐以下选题（任选其一，或自拟）：

1. **课程讲义问答机器人**：把本课程 16 周讲义建成 RAG 索引，实现"提问 → 检索 → 引用讲义作答"。
2. **OJ 题目推荐系统**：用 TF-IDF/BM25 对题面建索引，输入知识点关键词返回相关题目并按难度排序。
3. **代码相似度检测**：用字符串哈希 + LCS/编辑距离实现查重原型。
4. **算法可视化工具**：把排序、最短路、AVL 旋转过程动画化（`pygame` / `matplotlib`）。
5. **中文分词 + 倒排索引搜索引擎**：用 `jieba` 分词，实现完整的布尔检索 + BM25 排序。

**评分维度**：功能完整性、算法合理性、代码规范（PEP 8）、文档质量、Git 提交记录。
**⚠️ 允许使用大模型辅助，但必须在 README 中显式声明使用方式与范围。**

---

# 6 本周作业

| # | 题目 | 平台 / 编号 | 考点 |
| - | ---- | ---- | ---- |
| 1 | 设计哈希映射 | LC 706 | 手写散列表 |
| 2 | 两数之和 | LC 1 | 哈希查找 |
| 3 | 字母异位词分组 | LC 49 | 哈希键设计 |
| 4 | 最长连续序列 | LC 128 | set 的 O(n) 技巧 |
| 5 | 找出字符串中第一个匹配项的下标 | LC 28 | KMP |
| 6 | 重复的子字符串 | LC 459 | next 数组求循环节 |
| 7 | 字符串乘方 | OJ 02406 | KMP 循环节 |
| 8 | 实现 Trie（前缀树） | LC 208 | Trie |
| 9 | 单词搜索 II | LC 212 | Trie + 回溯 |
| 10（选做） | 实现迷你搜索引擎 | 课堂题 | 倒排索引 + BM25 |

**思考题**：

1. 为什么开放定址法删除元素必须用"墓碑"？直接置空会发生什么？举一个具体的探测序列说明。
2. 手工推导 `P = "aabaaab"` 的 next 数组，并说明在 `T = "aabaaabaabaaab"` 中匹配时指针如何移动。
3. 字符串哈希的碰撞概率如何估计？为什么模数要取大质数、BASE 要随机？
4. BM25 中的 `k1` 与 `b` 分别控制什么？把 `b` 设为 0 意味着什么？
5. 为什么稠密向量检索无法完全替代 BM25？举一个 BM25 明显更好的查询例子。

---

# 7 小结

1. 散列表用**散列函数**把键映射到下标，实现平均 O(1)；冲突用**开放定址**或**链地址**解决；λ 过大时**再散列**。
2. Python 的 `dict`/`set` 是开放定址 + 随机化探测；自定义类作键要同时实现 `__hash__` 与 `__eq__`。
3. **KMP** 用 next 数组避免文本指针回退，把串匹配从 O(nm) 降到 **O(n+m)**；next 数组的含义是"最长相等真前后缀长度"。
4. **倒排索引**（词 → 文档列表）本质是散列表，配合 **TF-IDF / BM25** 打分，是搜索引擎的基石。
5. **RAG** = 检索 + 生成；其中的向量索引（HNSW / IVF / LSH）正是**图、树、散列表**在高维空间的工程化应用——本课程所学，全部用得上。

**下周预告**：**课程总结与复习**，知识体系梳理、经典算法回顾、上机考试要点讲解。
