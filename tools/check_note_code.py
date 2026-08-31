#!/usr/bin/env python3
"""check_note_code.py — 讲义里的算法代码，逐个做随机性质测试。

闸门（verify_courseware.py）只验语法：代码能被 parse，不代表它算得对。
这里把讲义中的实现**原样抽出来执行**，与暴力解 / 标准库交叉对拍。

分工：
  verify_courseware.py  管"文档之间是否自洽"（配对、大纲、链接、语法、可重生成、题号）
  check_note_code.py    管"讲义里的代码算得对不对"

用法:
  python3 tools/check_note_code.py            # 全部
  python3 tools/check_note_code.py W04 W09    # 只跑指定周次
"""
import ast
import random
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CW = ROOT / "courseware"
FENCE = re.compile(r"```python\n(.*?)```", re.S)

_MD_CACHE: dict[str, list[str]] = {}
CASES: list[tuple[str, str, object]] = []
random.seed(20260831)


def note(week: str) -> list[str]:
    if week not in _MD_CACHE:
        hits = sorted(CW.glob(f"2026*_DSA_{week}_*.md"))
        if not hits:
            raise FileNotFoundError(week)
        _MD_CACHE[week] = FENCE.findall(hits[0].read_text(encoding="utf-8"))
    return _MD_CACHE[week]


def strip_driver(src: str) -> str:
    """只保留顶层的 import / def / class / 常量赋值，剥掉 OJ 驱动代码。

    讲义的代码块常在定义之后跟一段读 stdin 的驱动（`n = int(input())`、
    `data = sys.stdin.read().split()`）。直接 exec 会阻塞或抛异常；
    宽泛地吞异常又会掩盖定义本身的真错误。所以按 AST 精确剔除。
    """
    tree = ast.parse(src)
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom,
                             ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            keep.append(node)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
            # 只保留能在空环境里独立求值的常量赋值（PREC / DIGITS / MOVES / DIRS8…）。
            # ⚠️ 先按名字排除有副作用的右侧：`n = int(input())` 真去 eval 会阻塞读 stdin。
            seg = ast.get_source_segment(src, node) or ""
            if "input(" in seg or "stdin" in seg or "open(" in seg:
                continue
            try:
                eval(compile(ast.Expression(node.value), "<const>", "eval"), {})
            except Exception:
                continue                   # 依赖驱动代码的赋值（如 origin = lines[0]）
            keep.append(node)
    tree.body = keep
    return ast.unparse(tree)


def load(week: str, *markers: str, ns: dict | None = None) -> dict:
    """把含有各 marker 的代码块（剥掉驱动代码后）exec 进同一命名空间。"""
    ns = ns if ns is not None else {}
    blocks = note(week)
    for marker in markers:
        for b in blocks:
            if marker in b:
                exec(compile(strip_driver(b), f"<{week}:{marker}>", "exec"), ns)
                break
        else:
            raise LookupError(f"{week} 中找不到含 {marker!r} 的代码块")
    return ns


def case(week: str, name: str):
    def deco(fn):
        CASES.append((week, name, fn))
        return fn
    return deco


# ===================================================== W04 栈
@case("W04", "括号匹配 is_valid vs 参考实现")
def _():
    is_valid = load("W04", "def is_valid(s: str)")["is_valid"]

    def ref(s):
        st, pair = [], {")": "(", "]": "[", "}": "{"}
        for c in s:
            if c in "([{":
                st.append(c)
            elif c in pair:
                if not st or st.pop() != pair[c]:
                    return False
        return not st

    for _ in range(3000):
        s = "".join(random.choice("()[]{}") for _ in range(random.randint(0, 12)))
        assert is_valid(s) == ref(s), s


@case("W04", "进制转换 to_base 与 int(s,base) 互逆")
def _():
    to_base = load("W04", "def to_base(n: int, base: int)")["to_base"]
    for _ in range(2000):
        n, b = random.randint(-10 ** 6, 10 ** 6), random.randint(2, 16)
        assert int(to_base(n, b), b) == n, (n, b)


@case("W04", "调度场 + 后缀求值 vs Python eval")
def _():
    ns = load("W04", "def tokenize(expr: str)", "def infix_to_postfix(tokens)",
              "def eval_postfix(tokens)")

    def gen(d=0):
        if d > 2 or random.random() < 0.4:
            return str(random.randint(1, 9))
        a, op, b = gen(d + 1), random.choice("+-*"), gen(d + 1)
        return f"( {a} {op} {b} )" if random.random() < 0.6 else f"{a} {op} {b}"

    for _ in range(1500):
        e = gen()
        got = ns["eval_postfix"](ns["infix_to_postfix"](ns["tokenize"](e)))
        assert abs(got - eval(e)) < 1e-9, (e, got)


@case("W04", "前缀（波兰式）求值 eval_prefix")
def _():
    ns = load("W04", "def eval_prefix(tokens)")

    def gen(d=0):
        if d > 2 or random.random() < 0.4:
            v = str(random.randint(1, 9))
            return [v], v
        op = random.choice("+-*")
        la, ea = gen(d + 1)
        lb, eb = gen(d + 1)
        return [op] + la + lb, f"({ea}){op}({eb})"

    for _ in range(1500):
        toks, e = gen()
        assert abs(ns["eval_prefix"](toks) - eval(e)) < 1e-9, (toks, e)


@case("W04", "合法出栈序列 vs 全排列暴力")
def _():
    from itertools import permutations
    f = load("W04", "def is_valid_pop_sequence(origin: str, target: str)")["is_valid_pop_sequence"]

    def brute(origin, target):
        res, st = set(), []

        def go(i, cur):
            if len(cur) == len(origin):
                res.add(cur); return
            if i < len(origin):
                st.append(origin[i]); go(i + 1, cur); st.pop()
            if st:
                x = st.pop(); go(i, cur + x); st.append(x)
        go(0, "")
        return target in res

    for n in range(1, 6):
        origin = "abcdef"[:n]
        for p in permutations(origin):
            t = "".join(p)
            assert f(origin, t) == brute(origin, t), (origin, t)


@case("W04", "单调栈 daily_temperatures / largest_rectangle vs 暴力")
def _():
    ns = load("W04", "def daily_temperatures(temps)", "def largest_rectangle(heights)")
    for _ in range(400):
        a = [random.randint(1, 12) for _ in range(random.randint(1, 14))]
        want = [next((j - i for j in range(i + 1, len(a)) if a[j] > a[i]), 0)
                for i in range(len(a))]
        assert ns["daily_temperatures"](a) == want, a
        best = max(min(a[i:j + 1]) * (j - i + 1)
                   for i in range(len(a)) for j in range(i, len(a)))
        assert ns["largest_rectangle"](a[:]) == best, a


@case("W04", "最长有效括号 vs 暴力")
def _():
    f = load("W04", "def longest_valid(s: str)")["longest_valid"]

    def ok(s):
        d = 0
        for c in s:
            d += 1 if c == "(" else -1
            if d < 0:
                return False
        return d == 0

    for _ in range(800):
        s = "".join(random.choice("()") for _ in range(random.randint(0, 14)))
        want = max((j - i for i in range(len(s)) for j in range(i, len(s) + 1)
                    if ok(s[i:j])), default=0)
        assert f(s) == want, s


# ===================================================== W05 队列与链表
@case("W05", "循环队列 CircularQueue vs deque 模型")
def _():
    from collections import deque
    CQ = load("W05", "class CircularQueue")["CircularQueue"]
    for _ in range(300):
        cap = random.randint(1, 6)
        q, model = CQ(cap), deque()
        for _ in range(60):
            if random.random() < 0.5 and len(model) < cap:
                v = random.randint(0, 99)
                q.enqueue(v); model.append(v)
            elif model:
                assert q.dequeue() == model.popleft()
            assert len(q) == len(model)
            if model:
                assert q.front() == model[0]


@case("W05", "单调队列 max_sliding_window vs 暴力")
def _():
    f = load("W05", "def max_sliding_window(nums, k)")["max_sliding_window"]
    for _ in range(600):
        n = random.randint(1, 14)
        a = [random.randint(-20, 20) for _ in range(n)]
        k = random.randint(1, n)
        assert f(a, k) == [max(a[i:i + k]) for i in range(n - k + 1)], (a, k)


@case("W05", "约瑟夫递推 vs deque 模拟")
def _():
    from collections import deque
    f = load("W05", "def josephus(n, m)")["josephus"]
    for n in range(1, 40):
        for m in range(1, 12):
            d = deque(range(1, n + 1))
            while len(d) > 1:
                d.rotate(-(m - 1)); d.popleft()
            assert f(n, m) == d[0], (n, m)


@case("W05", "回文判断 is_palindrome")
def _():
    f = load("W05", "def is_palindrome(s: str)")["is_palindrome"]
    for _ in range(2000):
        s = "".join(random.choice("aAbB, .1") for _ in range(random.randint(0, 12)))
        clean = [c for c in s.lower() if c.isalnum()]
        assert f(s) == (clean == clean[::-1]), s


@case("W05", "无序表 / 有序表 vs list 模型")
def _():
    ns = load("W05", "class Node:", "class UnorderedList", "class OrderedList")
    for _ in range(200):
        ul, model = ns["UnorderedList"](), []
        for _ in range(30):
            r, v = random.random(), random.randint(0, 9)
            if r < 0.5:
                ul.add(v); model.insert(0, v)
            elif r < 0.7:
                assert ul.search(v) == (v in model)
            else:
                got = ul.remove(v)
                exp = v in model
                if exp:
                    model.remove(v)
                assert got == exp
            assert list(ul) == model
    ol = ns["OrderedList"]()
    for v in [random.randint(0, 30) for _ in range(40)]:
        ol.add(v)
        assert ol.search(v) is True
    assert ol.search(999) is False


@case("W05", "链表：反转 / 合并 / 中点 / 判环 / 删倒数第 N")
def _():
    ns = load("W05", "class Node:", "def reverse_list(head)", "def reverse_list_rec(head)",
              "def merge_two_lists(l1, l2)", "def middle_node(head)",
              "def detect_cycle(head)", "def remove_nth_from_end(head, n)")
    Node = ns["Node"]

    def build(vals):
        h = None
        for v in reversed(vals):
            h = Node(v, h)
        return h

    def tolist(h):
        out = []
        while h:
            out.append(h.value); h = h.next
        return out

    for _ in range(400):
        vals = [random.randint(0, 20) for _ in range(random.randint(0, 10))]
        assert tolist(ns["reverse_list"](build(vals))) == vals[::-1]
        assert tolist(ns["reverse_list_rec"](build(vals))) == vals[::-1]
        a = sorted(random.randint(0, 15) for _ in range(random.randint(0, 6)))
        b = sorted(random.randint(0, 15) for _ in range(random.randint(0, 6)))
        assert tolist(ns["merge_two_lists"](build(a), build(b))) == sorted(a + b)
        if vals:
            assert ns["middle_node"](build(vals)).value == vals[len(vals) // 2]
            n = random.randint(1, len(vals))
            want = vals[:len(vals) - n] + vals[len(vals) - n + 1:]
            assert tolist(ns["remove_nth_from_end"](build(vals), n)) == want
        assert ns["detect_cycle"](build(vals)) is None
        if len(vals) >= 2:
            h = build(vals)
            nodes, cur = [], h
            while cur:
                nodes.append(cur); cur = cur.next
            k = random.randrange(len(nodes))
            nodes[-1].next = nodes[k]
            assert ns["detect_cycle"](h) is nodes[k]



# ===================================================== W08 搜索与回溯
@case("W08", "子集 / 组合总和去重 / 全排列去重 vs itertools 暴力")
def _():
    from itertools import combinations, permutations
    ns = load("W08", "def subsets(nums)", "def combination_sum(candidates, target)",
              "def permute_unique(nums)")
    for _ in range(200):
        nums = random.sample(range(10), random.randint(0, 6))
        got = sorted(map(sorted, ns["subsets"](nums)))
        want = sorted(sorted(c) for r in range(len(nums) + 1)
                      for c in combinations(nums, r))
        assert got == want, nums
    for _ in range(200):
        a = sorted(random.sample(range(1, 9), random.randint(1, 5)))
        t = random.randint(1, 12)
        got = sorted(map(tuple, ns["combination_sum"](a, t)))
        want = set()

        def go(i, rem, cur):
            if rem == 0:
                want.add(tuple(cur)); return
            for j in range(i, len(a)):
                if a[j] <= rem:
                    go(j, rem - a[j], cur + [a[j]])
        go(0, t, [])
        assert got == sorted(want), (a, t)
    for _ in range(200):
        nums = [random.randint(0, 3) for _ in range(random.randint(0, 5))]
        got = sorted(map(tuple, ns["permute_unique"](nums[:])))
        want = sorted(set(permutations(nums)))
        assert got == want, nums


@case("W08", "N 皇后解数 = 已知值（n=1..9）")
def _():
    f = load("W08", "def solve_n_queens(n)")["solve_n_queens"]
    known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}
    for n, cnt in known.items():
        sols = f(n)
        assert len(sols) == cnt, (n, len(sols), cnt)
        for cols in sols:            # 每个解都要真的合法
            assert len(set(cols)) == n
            assert len({c - r for r, c in enumerate(cols)}) == n
            assert len({c + r for r, c in enumerate(cols)}) == n


@case("W08", "马走日 count_tours vs 暴力枚举")
def _():
    f = load("W08", "def count_tours(n, m, x, y)")["count_tours"]
    MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    def brute(n, m, x, y):
        seen = {(x, y)}

        def go(i, j, c):
            if c == n * m:
                return 1
            t = 0
            for di, dj in MOVES:
                a, b = i + di, j + dj
                if 0 <= a < n and 0 <= b < m and (a, b) not in seen:
                    seen.add((a, b)); t += go(a, b, c + 1); seen.discard((a, b))
            return t
        return go(x, y, 1)

    for n, m in [(1, 1), (2, 3), (3, 3), (3, 4), (4, 4)]:
        for x in range(n):
            for y in range(m):
                assert f(n, m, x, y) == brute(n, m, x, y), (n, m, x, y)


@case("W08", "多源 BFS update_matrix vs 逐点最短距离")
def _():
    # update_matrix 所在块依赖前文块里的 deque 与 DIRS4，一并载入
    ns = load("W08", "DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]",
              "from collections import deque", "def update_matrix(mat)")
    f = ns["update_matrix"]
    for _ in range(200):
        r, c = random.randint(1, 6), random.randint(1, 6)
        mat = [[random.randint(0, 1) for _ in range(c)] for _ in range(r)]
        if all(v for row in mat for v in row):
            mat[random.randrange(r)][random.randrange(c)] = 0
        zeros = [(i, j) for i in range(r) for j in range(c) if mat[i][j] == 0]
        want = [[min(abs(i - a) + abs(j - b) for a, b in zeros)
                 for j in range(c)] for i in range(r)]
        assert f([row[:] for row in mat]) == want, mat


# ===================================================== W09 树
def _rand_tree(TreeNode, n, vals=None):
    """随机二叉树，结点值互不相同。"""
    vals = vals or random.sample(range(1000), n)
    if not vals:
        return None
    nodes = [TreeNode(v) for v in vals]
    root = nodes[0]
    for nd in nodes[1:]:
        cur = root
        while True:
            side = random.choice(("left", "right"))
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, nd); break
            cur = nxt
    return root


@case("W09", "前/中/后序：递归 vs 迭代 vs 双色标记法 三者一致")
def _():
    ns = load("W09", "class TreeNode:", "def preorder(node, res)",
              "def preorder_iter(root)", "def inorder_iter(root)",
              "def postorder_iter(root)", "def traverse(root, order=")
    T = ns["TreeNode"]
    for _ in range(300):
        root = _rand_tree(T, random.randint(0, 12))
        for kind, it in (("pre", ns["preorder_iter"]), ("in", ns["inorder_iter"]),
                         ("post", ns["postorder_iter"])):
            res = []
            {"pre": ns["preorder"], "in": ns["inorder"], "post": ns["postorder"]}[kind](root, res)
            assert it(root) == res, kind
            assert ns["traverse"](root, kind) == res, kind


@case("W09", "前序+中序 / 后序+中序 建树，与原树遍历一致")
def _():
    ns = load("W09", "class TreeNode:", "def preorder(node, res)",
              "def build_from_pre_in(preorder, inorder)",
              "def build_from_post_in(inorder, postorder)")
    T = ns["TreeNode"]
    for _ in range(300):
        root = _rand_tree(T, random.randint(1, 12))
        pre, ino, post = [], [], []
        ns["preorder"](root, pre); ns["inorder"](root, ino); ns["postorder"](root, post)
        for rebuilt in (ns["build_from_pre_in"](pre, ino),
                        ns["build_from_post_in"](ino, post)):
            a, b = [], []
            ns["preorder"](rebuilt, a); ns["inorder"](rebuilt, b)
            assert (a, b) == (pre, ino)


@case("W09", "序列化 / 反序列化 往返")
def _():
    ns = load("W09", "class TreeNode:", "def preorder(node, res)",
              "def serialize(root)", "def deserialize(data)")
    T = ns["TreeNode"]
    for _ in range(300):
        root = _rand_tree(T, random.randint(0, 12), random.sample(range(1, 500), random.randint(0, 12)))
        back = ns["deserialize"](ns["serialize"](root))
        a, b = [], []
        ns["preorder"](root, a); ns["preorder"](back, b)
        assert a == b
        assert ns["serialize"](back) == ns["serialize"](root)


@case("W09", "深度 / 叶子数 / 直径 / 对称 / 平衡 / LCA vs 暴力")
def _():
    ns = load("W09", "class TreeNode:", "def max_depth(root)",
              "def diameter_of_binary_tree(root)", "def is_symmetric(root)",
              "def is_balanced(root)", "def lowest_common_ancestor(root, p, q)")
    T = ns["TreeNode"]

    def depth(n):
        return 0 if n is None else 1 + max(depth(n.left), depth(n.right))

    def leaves(n):
        if n is None:
            return 0
        return 1 if not n.left and not n.right else leaves(n.left) + leaves(n.right)

    def diam(n):
        if n is None:
            return 0
        return max(depth(n.left) + depth(n.right), diam(n.left), diam(n.right))

    def bal(n):
        if n is None:
            return True
        return abs(depth(n.left) - depth(n.right)) <= 1 and bal(n.left) and bal(n.right)

    def path(root, tgt):
        if root is None:
            return None
        if root is tgt:
            return [root]
        for side in (root.left, root.right):
            p = path(side, tgt)
            if p:
                return [root] + p
        return None

    for _ in range(300):
        n = random.randint(1, 12)
        root = _rand_tree(T, n)
        assert ns["max_depth"](root) == depth(root)
        assert ns["count_leaves"](root) == leaves(root)
        assert ns["diameter_of_binary_tree"](root) == diam(root)
        assert ns["is_balanced"](root) == bal(root)
        # 与暴力镜像判定对拍；并额外构造一棵真对称树，确保这条断言不是恒真
        def ref_sym(a, b):
            if a is None and b is None:
                return True
            if a is None or b is None or a.val != b.val:
                return False
            return ref_sym(a.left, b.right) and ref_sym(a.right, b.left)
        assert ns["is_symmetric"](root) == ref_sym(root, root)
        nodes = []
        st = [root]
        while st:
            x = st.pop()
            if x:
                nodes.append(x); st += [x.left, x.right]
        p, q = random.choice(nodes), random.choice(nodes)
        pa, qa = path(root, p), path(root, q)
        want = [a for a, b in zip(pa, qa) if a is b][-1]
        assert ns["lowest_common_ancestor"](root, p, q) is want
    # 正例：手工造一棵对称树，is_symmetric 必须为 True（否则上面的对拍可能恒 False）
    sym = T(1); sym.left = T(2); sym.right = T(2)
    sym.left.left = T(3); sym.right.right = T(3)
    assert ns["is_symmetric"](sym) is True
    sym.right.right.val = 4
    assert ns["is_symmetric"](sym) is False


# ===================================================== W10 BST
@case("W10", "BST 插入 / 查找 / 删除 vs 有序列表模型")
def _():
    # W10 的 BST 代码沿用第 9 周定义的 TreeNode（讲义里是跨周复用），这里跨周载入
    ns = load("W09", "class TreeNode:")
    load("W10", "def insert(root, key)", "def search(root, key)", "def delete(root, key)",
         "def is_valid_bst(root)", "def kth_smallest(root, k)", ns=ns)
    for _ in range(200):
        root, model = None, []
        for _ in range(40):
            r, v = random.random(), random.randint(0, 40)
            if r < 0.55:
                root = ns["insert"](root, v)
                if v not in model:
                    model.append(v); model.sort()
            elif r < 0.75:
                assert (ns["search"](root, v) is not None) == (v in model)
            else:
                root = ns["delete"](root, v)
                if v in model:
                    model.remove(v)
            assert ns["is_valid_bst"](root), model
            got = []
            st, cur = [], root
            while cur or st:
                while cur:
                    st.append(cur); cur = cur.left
                cur = st.pop(); got.append(cur.val); cur = cur.right
            assert got == model
        for k in range(1, len(model) + 1):
            assert ns["kth_smallest"](root, k) == model[k - 1]


# ===================================================== W11 并查集
@case("W11", "DSU vs 朴素并查集模型")
def _():
    DSU = load("W11", "class DSU:")["DSU"]
    for _ in range(300):
        n = random.randint(1, 12)
        d, groups = DSU(n), [{i} for i in range(n)]

        def find_model(x):
            return next(i for i, g in enumerate(groups) if x in g)

        for _ in range(30):
            a, b = random.randrange(n), random.randrange(n)
            ga, gb = find_model(a), find_model(b)
            merged = ga != gb
            assert d.union(a, b) == merged, (a, b)
            if merged:
                groups[ga] |= groups[gb]; groups[gb] = set()
            assert d.connected(a, b) is True
            x, y = random.randrange(n), random.randrange(n)
            assert d.connected(x, y) == (find_model(x) == find_model(y))
            assert d.count == sum(1 for g in groups if g)
            assert d.group_size(a) == len(groups[find_model(a)])


@case("W11", "带权并查集 WeightedDSU 的奇偶关系一致性")
def _():
    W = load("W11", "class WeightedDSU:")["WeightedDSU"]
    for _ in range(300):
        n = random.randint(2, 10)
        truth = [random.randrange(2) for _ in range(n)]   # 每个点的真实"类别"
        w = W(n)
        for _ in range(25):
            a, b = random.randrange(n), random.randrange(n)
            d = truth[a] ^ truth[b]
            assert w.union(a, b, d) is True, (a, b, d)    # 与真值一致，不应矛盾
        # 再断言一个错误关系，必须被判为矛盾
        a, b = random.randrange(n), random.randrange(n)
        if w.find(a) == w.find(b):
            assert w.union(a, b, 1 - (truth[a] ^ truth[b])) is False


# ===================================================== W12 图
def _rand_graph(n, p, directed=False):
    g = [[] for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < p:
                if directed or u < v:
                    g[u].append(v)
                    if not directed:
                        g[v].append(u)
    return g


@case("W12", "DFS 递归 / DFS 迭代 / BFS 可达集一致，dist 为最短步数")
def _():
    ns = load("W12", "def dfs_recursive(graph, u, visited, order)",
              "def dfs_iterative(graph, start, n)", "def bfs(graph, start, n)")
    for _ in range(300):
        n = random.randint(1, 10)
        g = _rand_graph(n, 0.3)
        s = random.randrange(n)
        vis, order = [False] * n, []
        ns["dfs_recursive"](g, s, vis, order)
        it = ns["dfs_iterative"](g, s, n)
        border, dist, parent = ns["bfs"](g, s, n)
        assert set(order) == set(it) == set(border)
        assert set(order) == {i for i in range(n) if dist[i] >= 0}
        # dist 与 BFS 参考一致
        from collections import deque
        ref = [-1] * n; ref[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if ref[v] < 0:
                    ref[v] = ref[u] + 1; q.append(v)
        assert dist == ref


@case("W12", "连通分量 / 二分图 / 无向判环 / 有向判环 vs 暴力")
def _():
    ns = load("W12", "def count_components(graph, n)", "def is_bipartite(graph)",
              "def has_cycle_undirected(graph, n)", "def has_cycle_directed(graph, n)")
    from itertools import product
    for _ in range(300):
        n = random.randint(1, 7)
        g = _rand_graph(n, 0.3)
        comps = ns["count_components"](g, n)
        seen = set()
        cnt = 0
        for s in range(n):
            if s in seen:
                continue
            cnt += 1
            st = [s]; seen.add(s)
            while st:
                u = st.pop()
                for v in g[u]:
                    if v not in seen:
                        seen.add(v); st.append(v)
        assert len(comps) == cnt
        # 二分图：暴力枚举 2 染色
        ok = any(all(col[u] != col[v] for u in range(n) for v in g[u])
                 for col in product((0, 1), repeat=n))
        assert ns["is_bipartite"](g) == ok, g
        # 无向图有环 <=> 边数 >= 结点数 - 连通分量数
        edges = sum(len(x) for x in g) // 2
        assert ns["has_cycle_undirected"](g, n) == (edges > n - cnt), g
        dg = _rand_graph(n, 0.25, directed=True)
        # 有向图判环：暴力找回边
        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * n
        found = [False]

        def go(u):
            color[u] = GRAY
            for v in dg[u]:
                if color[v] == GRAY:
                    found[0] = True
                elif color[v] == WHITE:
                    go(v)
            color[u] = BLACK
        for u in range(n):
            if color[u] == WHITE:
                go(u)
        assert ns["has_cycle_directed"](dg, n) == found[0], dg


@case("W12", "倒水问题 pour_water vs BFS 参考")
def _():
    f = load("W12", "def pour_water(cap_a, cap_b, target)")["pour_water"]
    from collections import deque
    for ca in range(1, 8):
        for cb in range(1, 8):
            for t in range(0, max(ca, cb) + 1):
                q, seen = deque([((0, 0), 0)]), {(0, 0)}
                ref = -1
                while q:
                    (a, b), d = q.popleft()
                    if a == t or b == t:
                        ref = d; break
                    for s in [(ca, b), (a, cb), (0, b), (a, 0),
                              (a - min(a, cb - b), b + min(a, cb - b)),
                              (a + min(b, ca - a), b - min(b, ca - a))]:
                        if s not in seen:
                            seen.add(s); q.append((s, d + 1))
                assert f(ca, cb, t) == ref, (ca, cb, t)


def main(argv):
    want = {a.upper() for a in argv}
    rows = [c for c in CASES if not want or c[0] in want]
    print(f"── check_note_code · {len(rows)} 项 ──")
    bad, by_week = 0, {}
    for week, name, fn in rows:
        try:
            fn()
            by_week.setdefault(week, []).append(f"  ✅ {name}")
        except Exception:
            bad += 1
            by_week.setdefault(week, []).append(
                f"  ❌ {name}\n{traceback.format_exc(limit=3)}")
    for week in sorted(by_week):
        print(f"\n{week}")
        for line in by_week[week]:
            print(line)
    print(f"\n{'全部通过。' if not bad else f'{bad} 项失败。'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
