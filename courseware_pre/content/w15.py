# -*- coding: utf-8 -*-
"""第15周 散列表、KMP、倒排索引 → RAG"""

META = {
    'title': '第15周　散列表、KMP 与倒排索引 → RAG',
    'subtitle': '冲突解决 · next 数组 · TF-IDF / BM25 · 检索增强生成',
    'footer': '数据结构与算法 · 第15周 · 闫宏飞 · 2026 Fall',
    'info': ['重庆人工智能学院　《数据结构与算法》',
             '教学要求：掌握散列表的实现原理；理解 KMP 算法的 next 数组计算；'
             '了解散列与倒排索引在 RAG 检索系统中的应用'],
}

SLIDES = [
    ('section', '第一部分', '散列表'),

    ('ascii', '核心思想：用散列函数把键映射成下标', r"""
   key = "apple"
        |
        v   h(key) = hash("apple") % 11 = 4
   +---+---+---+---+-------+---+---+
   | 0 | 1 | 2 | 3 | apple | 5 |...|
   +---+---+---+---+-------+---+---+
                       4

实现平均 O(1) 的插入、查找、删除
"""),

    ('code', '散列函数的常见构造法', '''def h_div(key, m):                    # 除留余数法（最常用）
    return key % m                    # m 取素数效果更好


def h_fold(phone: str, m):            # 折叠法：长数字分段相加
    parts = [int(phone[i:i+2]) for i in range(0, len(phone), 2)]
    return sum(parts) % m


def h_string(s: str, m, base=31):     # 字符串：多项式滚动哈希
    v = 0
    for ch in s:
        v = (v * base + ord(ch)) % m
    return v
''', '⚠️ sum(ord(c) for c in s) 这种不加权的写法会让 "abc"/"bca"/"cab" 冲突'),

    ('table', '装填因子 λ = 已存元素数 / 表长', [
        ['λ', '线性探测：成功查找', '线性探测：失败查找'],
        ['0.5', '1.5', '2.5'],
        ['0.75', '2.5', '8.5'],
        ['0.9', '5.5', '50.5'],
    ], 'λ > 0.7（或 2/3）时扩容【再散列 rehash】：表长翻倍，所有元素重新插入'),

    ('table', '冲突解决：开放定址法', [
        ['方法', '探测序列', '问题'],
        ['线性探测', 'h, h+1, h+2, …', '一次聚集（primary clustering）'],
        ['二次探测', 'h, h+1², h+2², …', '二次聚集，可能探测不到全表'],
        ['双重散列', 'h, h+h₂(k), h+2h₂(k), …', '效果最好'],
    ], '由鸽巢原理，冲突不可避免'),

    ('code', '⚠️ 开放定址法删除必须用「墓碑」', '''class OpenAddressingHashTable:
    _EMPTY = object()
    _DELETED = object()          # 墓碑标记

    def _probe(self, key):
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
''', '直接置空会切断探测链，导致后面的元素查不到 —— 必须留墓碑'),

    ('table', '开放定址 vs 链地址', [
        ['', '开放定址', '链地址'],
        ['内存', '紧凑，缓存友好', '有指针开销'],
        ['装填因子上限', '必须 < 1', '可以 > 1'],
        ['删除', '需墓碑，麻烦', '⭐ 简单'],
        ['聚集问题', '有', '无'],
    ]),

    ('bullets', 'Python 的 dict / set 是怎么实现的', [
        'CPython 采用**开放定址 + 随机化探测**（perturb 机制）',
        '3.6 起使用**紧凑布局**（indices 数组 + entries 数组），因此保持插入顺序',
        '平均 O(1)，**最坏 O(n)**（人为构造大量冲突 = 哈希碰撞攻击）',
        'Python 对 `str` 的哈希默认加**随机盐**（PYTHONHASHSEED）以缓解此类攻击',
        '只有**可哈希（不可变）**对象能作键：int、str、tuple、frozenset',
    ]),

    ('code', '自定义类作键：必须同时实现 __hash__ 与 __eq__', '''class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) and \\
               (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))       # 用元组的哈希，简单可靠
''', '必须满足：a == b  ⟹  hash(a) == hash(b)'),

    ('section', '第二部分', '字符串匹配：KMP'),

    ('ascii', '朴素算法 O(nm) 的浪费', r"""
T: a a a a a b
P: a a a b
       ^ 失配

朴素算法把 i 挪到 1 重新从头比 —— 已经比较过的信息全部丢弃
"""),

    ('key', '⭐ KMP 的核心洞察',
     '失配时我们已知 P[0..j-1] 与文本匹配。\n'
     '若它有长度为 k 的最长相等前后缀，就把模式串滑到「前缀 k 对齐」处，\n'
     '文本指针 i 完全不用回退'),

    ('table', 'next 数组：P[0..i] 的最长相等真前后缀长度', [
        ['i', 'P[0..i]', '最长相等真前后缀', 'nxt[i]'],
        ['0', 'a', '无（真前后缀不能是自身）', '0'],
        ['1', 'ab', '无', '0'],
        ['2', 'aba', '"a"', '1'],
        ['3', 'abab', '"ab"', '2'],
        ['4', 'ababc', '无', '0'],
    ]),

    ('code', '⭐ 构建 next 数组（本质是模式串自己和自己做 KMP）', '''def build_next(pattern):
    """nxt[i] = pattern[0..i] 的最长相等真前后缀长度。O(m)。"""
    m = len(pattern)
    nxt = [0] * m
    k = 0                              # 当前最长相等前后缀的长度
    for i in range(1, m):
        while k > 0 and pattern[i] != pattern[k]:
            k = nxt[k - 1]             # ⭐ 回退到更短的候选前缀
        if pattern[i] == pattern[k]:
            k += 1
        nxt[i] = k
    return nxt


print(build_next("ababc"))      # [0, 0, 1, 2, 0]
'''),

    ('code', 'KMP 匹配：O(n + m)', '''def kmp_search(text, pattern):
    if not pattern:
        return []
    nxt = build_next(pattern)
    res, j = [], 0                     # j = 已匹配的模式串长度
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = nxt[j - 1]             # 失配，模式串右滑，i 不回退
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            res.append(i - j + 1)
            j = nxt[j - 1]             # 继续找下一个（允许重叠）
    return res
''', '均摊证明：j 每次至多加 1（共 n 次），while 每次让 j 减少，j 非负 ⇒ 总计 O(n+m)'),

    ('code', 'KMP 的典型应用：求循环节', '''def min_period(s):
    """最小循环节长度。若 n % (n - nxt[n-1]) == 0 则为整周期。"""
    n = len(s)
    nxt = build_next(s)
    p = n - nxt[n - 1]
    return p if n % p == 0 else n


def repeated_substring_pattern(s):     # LC 459
    n = len(s)
    nxt = build_next(s)
    return nxt[n - 1] > 0 and n % (n - nxt[n - 1]) == 0
''', 'OJ 01961 前缀中的周期、OJ 02406 字符串乘方 都是这个模板'),

    ('code', '另一条路：字符串哈希（Rabin-Karp）', '''MOD = (1 << 61) - 1
BASE = 131


def build_hash(s):
    """前缀哈希 + 幂表，支持 O(1) 查询任意子串哈希。"""
    n = len(s)
    h = [0] * (n + 1); pw = [1] * (n + 1)
    for i, ch in enumerate(s):
        h[i + 1] = (h[i] * BASE + ord(ch)) % MOD
        pw[i + 1] = pw[i] * BASE % MOD
    return h, pw


def sub_hash(h, pw, l, r):             # s[l:r] 的哈希，O(1)
    return (h[r] - h[l] * pw[r - l]) % MOD
''', '优点：能处理"任意两子串是否相等""最长公共子串"；缺点：有碰撞概率'),

    ('code', 'Trie 前缀树（LC 208）', '''class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word):            # O(L)
        node = self
        for ch in word:
            node = node.children.setdefault(ch, Trie())
        node.is_end = True

    def _find(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def starts_with(self, prefix):
        return self._find(prefix) is not None
''', 'Trie 是倒排索引与自动补全的基础结构'),

    ('section', '第三部分', '倒排索引 → RAG'),

    ('ascii', '正排 vs 倒排', r"""
文档集：
  d1: "数据 结构 与 算法"
  d2: "算法 分析 与 复杂度"
  d3: "数据 分析"

倒排索引（词 -> 包含它的文档列表）：
  数据   -> [d1, d3]
  结构   -> [d1]
  算法   -> [d1, d2]
  分析   -> [d2, d3]
  复杂度 -> [d2]

查询"算法"时不必扫描全部文档，一次哈希查找就拿到候选列表
""", '⭐ 倒排索引 = 散列表 + 排好序的 posting list'),

    ('code', '迷你搜索引擎：建索引与布尔检索', '''from collections import defaultdict, Counter
import re, math


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)     # term -> {doc_id: 词频}
        self.doc_len = {}
        self.n_docs = 0

    @staticmethod
    def tokenize(text):
        return re.findall(r'[a-zA-Z]+|[\\u4e00-\\u9fff]', text.lower())

    def add(self, doc_id, text):
        tokens = self.tokenize(text)
        self.doc_len[doc_id] = len(tokens)
        self.n_docs += 1
        for term, tf in Counter(tokens).items():
            self.index[term][doc_id] = tf      # 建立倒排

    def search_and(self, query):               # posting list 求交集
        terms = self.tokenize(query)
        result = set(self.index.get(terms[0], {}))
        for t in terms[1:]:
            result &= set(self.index.get(t, {}))
        return result
'''),

    ('code', 'TF-IDF 与 BM25 打分', '''    def idf(self, term):
        df = len(self.index.get(term, {}))
        return math.log((self.n_docs + 1) / (df + 1)) + 1     # 平滑

    def search_tfidf(self, query, top_k=5):
        scores = defaultdict(float)
        for term in self.tokenize(query):
            idf = self.idf(term)
            for doc_id, tf in self.index.get(term, {}).items():
                scores[doc_id] += (tf / self.doc_len[doc_id]) * idf
        return sorted(scores.items(), key=lambda x: -x[1])[:top_k]

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
'''),

    ('bullets', 'TF-IDF 与 BM25 的直觉', [
        '**TF**：词在本文档中越频繁越重要',
        '**IDF**：词在越少的文档中出现，区分度越高（“的”“是”IDF≈0，自动降权）',
        '**BM25 的两个修正**：',
        '- **词频饱和**（k1）：出现 100 次不该比 10 次重要 10 倍',
        '- **文档长度归一化**（b）：长文档天然含更多词，需要惩罚',
        '⭐ BM25 至今仍是工业界最强的**稀疏检索基线**，Elasticsearch 的默认打分函数',
    ]),

    ('bullets', '⚠️ 稀疏检索的局限', [
        '倒排索引依赖**字面词匹配**',
        '查询“如何加快程序运行速度” vs 文档“算法优化技巧” —— **同义但不同词**',
        '查询“苹果的股价” vs 文档“苹果富含维生素” —— **同词但不同义**',
        '→ 需要**稠密检索（向量检索）**：用嵌入模型把文本映射成高维向量',
    ]),

    ('table', '⭐ 向量索引（ANN）用的全是本课程学过的结构', [
        ['ANN 方法', '用到的数据结构', '本课程对应'],
        ['HNSW（分层可导航小世界图）', '**图** + 分层跳表', 'W12 图、W5 链表'],
        ['IVF（倒排文件）', '聚类 + **倒排索引**', '本周'],
        ['LSH（局部敏感哈希）', '**散列表**', '本周'],
        ['KD-Tree / Ball Tree', '**树**', 'W9–W11'],
    ], '向量数据库（FAISS、Milvus、Qdrant）不是魔法，是图/树/散列表在高维空间的工程化'),

    ('ascii', 'RAG 完整流水线', r"""
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
""", 'RAG 解决三个痛点：知识截止、幻觉、私域知识'),

    ('code', '最小 RAG 原型：多路召回 + RRF 融合', '''class MiniRAG:
    @staticmethod
    def chunk(text, size=200, overlap=50):
        """滑动窗口分块，overlap 保证跨块句子不被切断。"""
        res, i = [], 0
        while i < len(text):
            res.append(text[i:i + size])
            i += size - overlap
        return res

    @staticmethod
    def reciprocal_rank_fusion(rank_lists, k=60):
        """RRF：把多路排序结果融合，score = Σ 1/(k + rank)。"""
        scores = defaultdict(float)
        for lst in rank_lists:
            for rank, doc_id in enumerate(lst):
                scores[doc_id] += 1.0 / (k + rank + 1)
        return [d for d, _ in sorted(scores.items(), key=lambda x: -x[1])]

    def build_prompt(self, query, top_k=3):
        context = "\\n\\n---\\n\\n".join(self.retrieve(query, top_k))
        return (f"请仅依据以下资料回答问题。若资料中没有答案，请明确说明。\\n"
                f"【资料】\\n{context}\\n\\n【问题】{query}\\n\\n【回答】")
'''),

    ('table', '⭐ RAG 中每一步用到的数据结构', [
        ['RAG 环节', '数据结构 / 算法', '周次'],
        ['文本分块', '字符串处理、滑动窗口', 'W3、W5'],
        ['关键词索引', '**散列表 + 倒排索引**', '**W15**'],
        ['关键词匹配', '**KMP / Trie**', '**W15**'],
        ['向量索引', '**图 / 树 / 哈希**', 'W9–W12'],
        ['Top-K 召回', '**堆**', 'W10'],
        ['Agent 工作流依赖调度', '**拓扑排序**', 'W14'],
    ], '一个 RAG 系统，几乎把整学期的数据结构用了一遍'),

    ('bullets', 'AI 辅助算法实践小项目选题建议（占总评 10%）', [
        '**课程讲义问答机器人**：把 16 周讲义建成 RAG 索引，引用讲义作答',
        '**OJ 题目推荐系统**：TF-IDF/BM25 对题面建索引，按知识点与难度返回',
        '**代码相似度检测**：字符串哈希 + LCS / 编辑距离实现查重原型',
        '**算法可视化工具**：排序、最短路、AVL 旋转过程动画化',
        '**中文分词 + 倒排索引搜索引擎**：jieba 分词 + 布尔检索 + BM25',
        '⚠️ 评分看功能完整性、算法合理性、代码规范、文档与提交记录；**用大模型须声明**',
    ]),

    ('table', '本周作业', [
        ['#', '题目', '平台 / 编号', '考点'],
        ['1', '设计哈希映射', 'LC 706', '手写散列表'],
        ['2', '两数之和 / 字母异位词分组', 'LC 1 / 49', '哈希查找、哈希键设计'],
        ['3', '最长连续序列', 'LC 128', 'set 的 O(n) 技巧'],
        ['4', '找出字符串中第一个匹配项的下标', 'LC 28', 'KMP'],
        ['5', '重复的子字符串', 'LC 459', 'next 数组求循环节'],
        ['6', '字符串乘方', 'OJ 02406', 'KMP 循环节'],
        ['7', '实现 Trie / 单词搜索 II', 'LC 208 / 212', 'Trie、Trie + 回溯'],
        ['8（选做）', '实现迷你搜索引擎', '课堂题', '倒排索引 + BM25'],
    ]),

    ('bullets', '本讲小结', [
        '散列表用散列函数映射到下标，平均 O(1)；冲突用**开放定址**或**链地址**',
        '⚠️ 开放定址删除要用**墓碑**；自定义类作键要同时实现 `__hash__` 与 `__eq__`',
        '**KMP** 用 next 数组避免文本指针回退，O(nm) → **O(n+m)**',
        '**倒排索引**本质是散列表，配合 **TF-IDF / BM25** 打分是搜索引擎的基石',
        '⭐ **RAG 中的向量索引正是图、树、散列表在高维空间的工程化应用**',
        '**下周预告**：课程总结与复习、上机考试要点',
    ]),
]
