#!/usr/bin/env python3
"""verify_courseware.py — 第 2–17 周讲义与课件的回归闸门。

这是一个内容仓库，没有单元测试；能当仲裁的是"文档之间、文档与大纲之间是否自洽"。
本脚本把这些不变量固化下来，交接前必须跑通。

检查项：
  1. 配对     每周恰好一份 .md 讲义 + 一份同名 .pptx 课件，W02–W17 无缺漏
  2. 元数据   讲义有标题、`*Updated ...*` 时间戳（GMT+8）、`*Compiled by ...*`
  3. 大纲     讲义声明的"教学内容/教学要求"与教学大纲 .docx 原文逐字一致
  4. 链接     所有本地 .md/.pptx/.py 链接可达
  5. 语法     讲义里的 ```python 代码块、以及 courseware/*.py 全部能被解析
  6. 可重生成 课件能从 content/wNN.py 重新生成，页数与 README 表格声明一致
  7. OJ题号   （可选，需联网）抓 cs101.openjudge.cn 的题目标题，与讲义里的叫法比对
  8. 渲染     （可选，需 libreoffice + pdftotext）渲染全部页面，检查文字未越出版心

用法:
  python3 tools/verify_courseware.py              # 1–6，秒级
  python3 tools/verify_courseware.py --check-oj   # 加第 7 项，约 30 秒（需联网）
  python3 tools/verify_courseware.py --render     # 加第 8 项，约 2–4 分钟
"""
import argparse
import ast
import html
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CW = ROOT / "courseware"
SYLLABUS = ROOT / "重庆人工智能学院课程教学大纲-闫宏飞.docx"
WEEKS = [f"{i:02d}" for i in range(2, 18)]

failures: list[str] = []
notes: list[str] = []


def fail(check: str, msg: str) -> None:
    failures.append(f"[{check}] {msg}")


def decks() -> dict[str, Path]:
    """周次 -> 讲义路径。"""
    out = {}
    for md in sorted(CW.glob("2026*_DSA_W*.md")):
        m = re.match(r"2026\d\d_DSA_W(\d\d)_", md.name)
        if m:
            out[m.group(1)] = md
    return out


# ---------------------------------------------------------------- 1 配对
def check_pairing(found: dict[str, Path]) -> None:
    missing = [w for w in WEEKS if w not in found]
    if missing:
        fail("配对", f"缺少讲义：第 {', '.join(missing)} 周")
    for wk, md in found.items():
        if not md.with_suffix(".pptx").is_file():
            fail("配对", f"{md.name} 没有同名 .pptx")
        if not (CW / "content" / f"w{wk}.py").is_file():
            fail("配对", f"第 {wk} 周缺少课件内容模块 content/w{wk}.py")
    for pptx in CW.glob("*.pptx"):
        if not pptx.with_suffix(".md").is_file():
            fail("配对", f"{pptx.name} 没有同名 .md")
    notes.append(f"配对：{len(found)} 周，讲义/课件/内容模块三者齐备")


# ---------------------------------------------------------------- 2 元数据
META_UPDATED = re.compile(r"^\*Updated \d{4}-\d\d-\d\d \d\d:\d\d GMT\+8\*", re.M)
META_AUTHOR = re.compile(r"^\s*\*Compiled by Hongfei Yan \(2026 Fall\)\*", re.M)


def check_metadata(found: dict[str, Path]) -> None:
    for wk, md in sorted(found.items()):
        text = md.read_text(encoding="utf-8")
        head = "\n".join(text.splitlines()[:8])
        if not head.lstrip().startswith("# "):
            fail("元数据", f"{md.name} 首行不是一级标题")
        if not META_UPDATED.search(head):
            fail("元数据", f"{md.name} 缺少 `*Updated YYYY-MM-DD HH:MM GMT+8*`")
        if not META_AUTHOR.search(head):
            fail("元数据", f"{md.name} 缺少 `*Compiled by Hongfei Yan (2026 Fall)*`")
    notes.append(f"元数据：{len(found)} 份讲义头部齐全")


# ---------------------------------------------------------------- 3 大纲对齐
def syllabus_rows() -> dict[str, tuple[str, str]]:
    """从教学大纲 .docx 解析 周次 -> (教学内容, 教学要求)。"""
    with zipfile.ZipFile(SYLLABUS) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = xml.replace("</w:p>", "\n").replace("</w:tr>", "\x1e").replace("</w:tc>", "\x1f")
    text = html.unescape(re.sub(r"<[^>]+>", "", xml))
    rows = {}
    for row in text.split("\x1e"):
        cells = [c.replace("\n", "").strip() for c in row.split("\x1f")]
        cells = [c for c in cells if c]
        m = re.match(r"^第(\d+)周$", cells[0]) if cells else None
        if m and len(cells) >= 4:
            rows[f"{int(m.group(1)):02d}"] = (cells[2], cells[3])
    return rows


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def check_syllabus(found: dict[str, Path]) -> None:
    if not SYLLABUS.is_file():
        fail("大纲", f"找不到教学大纲：{SYLLABUS.name}")
        return
    rows = syllabus_rows()
    if len(rows) != 16:
        fail("大纲", f"从 docx 解析出 {len(rows)} 行周次，预期 16 行")
    for wk, md in sorted(found.items()):
        if wk not in rows:
            fail("大纲", f"大纲里没有第 {wk} 周")
            continue
        want_content, want_req = rows[wk]
        text = md.read_text(encoding="utf-8")
        got_content = re.search(r"^> \*\*教学内容\*\*：(.+)$", text, re.M)
        got_req = re.search(r"^> \*\*教学要求\*\*：(.+)$", text, re.M)
        if not got_content or not got_req:
            fail("大纲", f"{md.name} 缺少 `> **教学内容**：` 或 `> **教学要求**：` 行")
            continue
        if norm(got_content.group(1)) != norm(want_content):
            fail("大纲", f"第 {wk} 周教学内容与大纲不一致\n"
                         f"        大纲: {want_content}\n"
                         f"        讲义: {got_content.group(1)}")
        if norm(got_req.group(1)) != norm(want_req):
            fail("大纲", f"第 {wk} 周教学要求与大纲不一致\n"
                         f"        大纲: {want_req}\n"
                         f"        讲义: {got_req.group(1)}")
    notes.append(f"大纲：{len(rows)} 周教学内容/要求与 docx 逐字一致")


# ---------------------------------------------------------------- 4 链接
LINK = re.compile(r"\]\((?!https?:|#|mailto:)([^)]+\.(?:md|pptx|py))\)")


def check_links() -> None:
    total = 0
    scan = sorted(ROOT.glob("*.md")) + sorted(CW.glob("*.md")) + sorted((ROOT / "homework").glob("*.md"))
    for md in scan:
        for m in LINK.finditer(md.read_text(encoding="utf-8")):
            total += 1
            target = (md.parent / m.group(1)).resolve()
            if not target.exists():
                fail("链接", f"{md.relative_to(ROOT)} -> {m.group(1)} 不存在")
    notes.append(f"链接：{total} 个本地链接全部可达")


# ---------------------------------------------------------------- 5 语法
FENCE = re.compile(r"```python\n(.*?)```", re.S)


def check_python(found: dict[str, Path]) -> None:
    blocks = 0
    for md in sorted(found.values()):
        for i, code in enumerate(FENCE.findall(md.read_text(encoding="utf-8"))):
            # 引用块里的嵌套围栏，每行带 "> " 前缀，先剥掉
            lines = code.split("\n")
            if all(l.startswith(("> ", ">")) or not l.strip() for l in lines):
                code = "\n".join(re.sub(r"^> ?", "", l) for l in lines)
            # 讲义里允许出现片段式代码（缩进的续写、省略号），只报真正的语法错
            if re.match(r"^\s+\S", code) or "..." in code.split("\n")[0]:
                continue
            blocks += 1
            try:
                ast.parse(code)
            except SyntaxError as e:
                fail("语法", f"{md.name} 第 {i} 个 python 块: {e}")
    py = sorted(CW.glob("*.py")) + sorted((CW / "content").glob("*.py")) + sorted((ROOT / "tools").glob("*.py"))
    proc = subprocess.run([sys.executable, "-m", "py_compile", *map(str, py)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        fail("语法", f"py_compile 失败:\n{proc.stdout}{proc.stderr}")
    notes.append(f"语法：{blocks} 个讲义代码块 + {len(py)} 个 .py 文件均通过解析")


# ---------------------------------------------------------------- 6 可重新生成
README_ROW = re.compile(r"^\| (\d+) \| `(2026\d\d_DSA_W\d\d_[^`]+)` \| (\d+) \|", re.M)


def check_regenerate() -> None:
    # Codex 第 1 轮的教训：缺依赖时这一项抛的是 build_all.py 的原始 traceback，
    # 看不出"装个包就行"。先探测，给一句能照做的话。
    probe = subprocess.run([sys.executable, "-c", "import pptx"], capture_output=True)
    if probe.returncode != 0:
        fail("可重生成", "缺少 python-pptx，无法重新生成课件；请先 `pip install python-pptx`"
                         f"（当前解释器：{sys.executable}）")
        return

    declared = {m.group(2): int(m.group(3))
                for m in README_ROW.finditer((CW / "README.md").read_text(encoding="utf-8"))}
    if len(declared) != 16:
        fail("可重生成", f"courseware/README.md 文件清单解析出 {len(declared)} 行，预期 16 行")

    with tempfile.TemporaryDirectory() as tmp:
        # 在临时副本里生成，避免污染工作区（pptx 每次生成字节都不同）
        work = Path(tmp) / "courseware"
        shutil.copytree(CW, work, ignore=shutil.ignore_patterns("*.pptx", "__pycache__"))
        proc = subprocess.run([sys.executable, "build_all.py"], cwd=work,
                              capture_output=True, text=True)
        if proc.returncode != 0:
            fail("可重生成", f"build_all.py 失败:\n{proc.stdout}{proc.stderr}")
            return
        built = {}
        for line in proc.stdout.splitlines():
            m = re.match(r"(\S+)\.pptx\s+\((\d+) slides\)", line.strip())
            if m:
                built[m.group(1)] = int(m.group(2))
        if len(built) != 16:
            fail("可重生成", f"只生成了 {len(built)} 份课件，预期 16 份")
        for base, pages in sorted(declared.items()):
            if base not in built:
                fail("可重生成", f"README 声明的 {base} 未被生成")
            elif built[base] != pages:
                fail("可重生成", f"{base} 实际 {built[base]} 页，README 声明 {pages} 页")
        total = sum(built.values())
        if f"{total} 页" not in (CW / "README.md").read_text(encoding="utf-8"):
            fail("可重生成", f"courseware/README.md 未声明总页数 {total}")
        notes.append(f"可重生成：16 份课件重新生成成功，共 {total} 页，页数与 README 一致")


# ------------------------------------------------------- 7 OJ 题号（需联网）
# 上一轮我判定"题号↔题名离线检不出来"——对，但那只说明它不能进默认闸门。
# cs101.openjudge.cn 走明文 HTTP 可达（WebFetch 强制 https 才连不上），
# 于是把它做成一项显式的联网检查：抓平台标题，与讲义/课件里的叫法比对。
OJ_URL = "http://cs101.openjudge.cn/practice/{}/"
OJ_NUM = re.compile(r"OJ\s*(\d{5})")
OJ_NAMED = [
    re.compile(r"\*\*OJ (\d{5})[:：]\s*([^*]+?)\*\*"),        # **OJ 03704: 括号匹配问题**
    re.compile(r"\|\s*([^|]{2,30}?)\s*\|\s*OJ (\d{5})\s*\|"),  # | 括号匹配问题 | OJ 03704 |
]


def _oj_title(num: str) -> str | None:
    import urllib.error
    import urllib.request
    try:
        with urllib.request.urlopen(OJ_URL.format(num), timeout=20) as r:
            body = r.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError):
        return None
    m = re.search(r"<title>([^<]*)</title>", body)
    if not m:
        return None
    t = m.group(1).replace("OpenJudge - ", "").strip()
    return t.split(":", 1)[1].strip() if ":" in t else t


# 有意偏离平台标题的，登记在这里并写明理由——不写理由不许加
OJ_TITLE_ALLOW = {
    "03704": "平台标题把「括号」误写成「扩号」，讲义用正确写法",
    "27653": "平台写「Fraction类」，讲义按仓库规范在中英文间加空格",
    "22158": "备选题库表格列宽有限，简称「前中序建树」",
    "24591": "备选题库表格列宽有限，简称「中序转后序」",
}


def check_oj_titles(found: dict[str, Path]) -> None:
    import time

    files = sorted(found.values()) + sorted((CW / "content").glob("*.py"))
    nums, used = set(), {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        nums |= set(OJ_NUM.findall(text))
        for m in OJ_NAMED[0].finditer(text):
            used.setdefault(m.group(1), set()).add(m.group(2).strip())
        for m in OJ_NAMED[1].finditer(text):
            used.setdefault(m.group(2), set()).add(m.group(1).strip())

    unreachable, mismatched, checked, allowed = [], 0, 0, []
    for num in sorted(nums):
        title = _oj_title(num)
        time.sleep(0.3)                      # 对题库客气一点
        if title is None:
            unreachable.append(num)
            continue
        checked += 1
        mine = used.get(num)
        if not mine:
            continue                          # 只在正文提过，没有可提取的"号: 名"
        norm = lambda x: re.sub(r"[\s（(].*$", "", x).strip()
        # 必须【每一处】叫法都对得上：只要有一处写错就得报。
        # 早先写成 any() —— 同一个号在别处的正确叫法会把错的那处盖掉，变异自检没抓到。
        wrong = [m for m in sorted(mine)
                 if not (norm(m) == norm(title) or norm(title) in m or m in title)]
        if wrong:
            if num in OJ_TITLE_ALLOW:
                allowed.append(f"{num}（{OJ_TITLE_ALLOW[num]}）")
                continue
            mismatched += 1
            fail("OJ题号", f"{num} 平台标题「{title}」，讲义里写作「{' / '.join(wrong)}」")
    if unreachable:
        fail("OJ题号", f"{len(unreachable)} 个题号取不到平台标题（网络不通？）：{', '.join(unreachable)}")
    extra = f"，另有 {len(allowed)} 处已登记的有意偏离" if allowed else ""
    notes.append(f"OJ题号：{checked}/{len(nums)} 个题号已联网核对平台标题，"
                 f"不一致 {mismatched} 处{extra}")
    for a in allowed:
        notes.append(f"  ↳ 有意偏离：{a}")


# ---------------------------------------------------------------- 8 渲染
def check_render() -> None:
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    if not soffice or not shutil.which("pdftotext"):
        fail("渲染", "需要 libreoffice 与 pdftotext（poppler-utils）")
        return
    from xml.etree import ElementTree as ET
    NS = "{http://www.w3.org/1999/xhtml}"
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp,
               *map(str, sorted(CW.glob("*.pptx")))]
        subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        pdfs = sorted(Path(tmp).glob("*.pdf"))
        if len(pdfs) != 16:
            fail("渲染", f"只渲染出 {len(pdfs)} 个 PDF，预期 16 个")
        pages = bad = 0
        for pdf in pdfs:
            out = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"],
                                 capture_output=True, text=True).stdout
            for pno, page in enumerate(ET.fromstring(out).iter(NS + "page"), 1):
                pages += 1
                sx = 960.0 / float(page.get("width"))
                sy = 540.0 / float(page.get("height"))
                for w in page.iter(NS + "word"):
                    if not (w.text or "").strip():
                        continue
                    x1 = float(w.get("xMax")) * sx
                    y0 = float(w.get("yMin")) * sy
                    y1 = float(w.get("yMax")) * sy
                    # 右边界 930pt；页脚带 518pt 以下只允许页脚自身（y0>=488）
                    if x1 > 930 or (y1 > 518 and y0 < 488):
                        bad += 1
                        fail("渲染", f"{pdf.stem} 第 {pno} 页文字越界: {w.text!r}")
        notes.append(f"渲染：{pages} 页全部渲染通过，越界 {bad} 处")


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--render", action="store_true", help="附加渲染与排版越界检查（慢）")
    ap.add_argument("--check-oj", action="store_true",
                    help="附加 OJ 题号联网核对（需能访问 cs101.openjudge.cn）")
    opts = ap.parse_args()

    found = decks()
    check_pairing(found)
    check_metadata(found)
    check_syllabus(found)
    check_links()
    check_python(found)
    check_regenerate()
    if opts.check_oj:
        check_oj_titles(found)
    if opts.render:
        check_render()

    print("── verify_courseware ──")
    for n in notes:
        print(f"  ✅ {n}")
    if failures:
        print(f"\n  ❌ {len(failures)} 项不通过：")
        for f in failures:
            print(f"     {f}")
        return 1
    print("\n  全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
