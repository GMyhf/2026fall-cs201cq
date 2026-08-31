#!/usr/bin/env python3
"""test_gate.py — 测闸门自己的失败路径。

Codex 已经在 `verify_courseware.py` 里连着找出三个缺陷，**三个都在失败路径上**：
  ① OJ 白名单按题号整体豁免，该号的任何错名都能过（`32757c2` 修）
  ② LibreOffice 失败时仍打印 `✅ 渲染：0 页全部渲染通过`，与 ❌ 自相矛盾（`6150670` 修）
  ③ 大纲少一周时 META 循环 KeyError 崩溃，后续检查全部不执行（本轮修）

共同点：正常绿跑时这些分支一行都不会执行，所以"闸门天天全绿"给不了任何保证。
这个文件专门喂错误输入，检查闸门**报错报得对不对**。

用法:
  python3 tools/test_gate.py
"""
import contextlib
import importlib.util
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS: list[tuple[bool, str, str]] = []



def fresh():
    """每个用例拿一份干净的模块实例，避免 failures/notes 互相污染。"""
    spec = importlib.util.spec_from_file_location("vc", ROOT / "tools" / "verify_courseware.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@contextlib.contextmanager
def patched(*targets):
    """临时替换若干 (对象, 属性名, 新值)，退出时一律还原。

    Codex 指出 OJ 用例替换了全局 `time.sleep` 却不还原。自查后发现同类问题
    还有一处且更严重：渲染用例把全局 `shutil.which` 桩成恒返回 "/bin/true"，
    之后进程内任何命令探测都会误判为"存在"。统一走这个上下文，避免再犯。
    """
    saved = [(obj, attr, getattr(obj, attr)) for obj, attr, _ in targets]
    try:
        for obj, attr, new in targets:
            setattr(obj, attr, new)
        yield
    finally:
        for obj, attr, old in saved:
            setattr(obj, attr, old)


def expect(name, cond, detail=""):
    RESULTS.append((bool(cond), name, detail))


def hits(vc, keyword):
    return [f for f in vc.failures if keyword in f]


# ---------------------------------------------------------------- 用例
def t_missing_week_does_not_crash():
    """③ 大纲缺一周：必须干净失败，不能抛异常中断后续检查。"""
    vc = fresh()
    orig = vc.syllabus_rows
    vc.syllabus_rows = lambda: {k: v for k, v in orig().items() if k != "05"}
    try:
        vc.check_syllabus(vc.decks())
    except Exception as e:
        expect("大纲缺周不崩溃", False, f"抛了 {type(e).__name__}: {e}")
        return
    expect("大纲缺周不崩溃", True)
    expect("大纲缺周有报错", any("没有第 05 周" in f for f in vc.failures),
           str(vc.failures))
    # 关键：崩了就等于后面的链接/语法/题号全都没跑
    vc.check_links()
    expect("缺周后其余检查仍可执行", any("链接" in n for n in vc.notes))


def t_deck_meta_drift_caught():
    """课件 META 的教学要求与大纲不符必须被抓。"""
    vc = fresh()
    orig = vc.syllabus_rows
    vc.syllabus_rows = lambda: {k: (v[0], v[1] + "；另加一句大纲要求")
                                for k, v in orig().items()}
    vc.check_syllabus(vc.decks())
    expect("课件 META 漂移被抓", len(hits(vc, "课件 META")) == 16,
           f"命中 {len(hits(vc, '课件 META'))} 条，预期 16")


def t_render_failure_reports_exit_code():
    """② LibreOffice 失败：要报退出码，且不能同时说"渲染通过"。"""
    vc = fresh()
    fake = subprocess.CompletedProcess([], returncode=1, stdout="",
                                       stderr="Error: source file could not be loaded")
    with patched((subprocess, "run", lambda *a, **k: fake),
                 (shutil, "which", lambda name: "/bin/true")):
        vc.check_render()
    expect("渲染失败报出退出码", any("退出码 1" in f for f in vc.failures), str(vc.failures))
    expect("渲染失败不再自称通过",
           not any("渲染" in n and "全部渲染通过" in n for n in vc.notes), str(vc.notes))


def t_oj_allowlist_is_per_alias():
    """① 白名单必须"按别名"放行，不能"按题号"整体豁免。"""
    plat = {"03704": "扩号匹配问题"}                  # 只桩这一个号

    def run(allow):
        vc = fresh()
        vc.OJ_TITLE_ALLOW = allow
        vc._oj_title = lambda num: plat.get(num)     # 其余号返回 None -> 记为取不到
        with patched((time, "sleep", lambda *_: None)):   # 测试里不必对题库限速
            vc.check_oj_titles(vc.decks())
        return hits(vc, "03704")

    expect("无白名单时不符会失败", run({}), "空白名单下 03704 应当失败")
    expect("登记了正确别名则放行",
           not run({"03704": {"括号匹配问题": "平台笔误"}}), "登记别名后不该失败")
    expect("登记了别的别名仍拒绝（Codex 的收紧）",
           run({"03704": {"汉诺塔": "无关别名"}}), "换个别名就该继续失败")


def t_cjk_font_detection():
    """渲染产物必须真嵌入中文字体 —— 缺字体时会画方框，而越界检查照样通过。

    Codex 在 macOS 上发现：LibreOffice 缺中文字体会把汉字导成方框，
    但 PDF 里的 Unicode 文本仍然正确，`pdftotext` 抽得出、越界也测不出。
    所以"文字未越界"不能当作可读性证据。
    """
    vc = fresh()
    hdr = ("name  type  encoding  emb sub uni object ID\n"
           "---   ---   ---       --- --- --- ---\n")
    cases = {
        "有 CJK 且嵌入（Type 1）":
            (hdr + "BAAAAA+NotoSansCJKsc-Bold  Type 1  Builtin  yes yes yes 1024 0", True),
        "有 CJK 且嵌入（TrueType）":
            (hdr + "X+SourceHanSansSC  TrueType  Identity-H  yes yes yes 20 0", True),
        "只有拉丁字体（缺中文字体的典型产物）":
            (hdr + "CAAAAA+NotoSans-Bold  TrueType  WinAnsi  yes yes yes 1014 0", False),
        "有 CJK 但未嵌入":
            (hdr + "BAAAAA+NotoSansCJKsc-Bold  Type 1  Builtin  no  no  yes 1024 0", False),
        "空输出": ("", False),
    }
    for label, (text, want) in cases.items():
        expect(f"CJK 字体判定：{label}", vc.has_cjk_font(text) is want)


def t_positive_control():
    """反向对照：不喂错误输入时，这些检查必须一条失败都没有。

    没有这条，上面任何一个用例即便恒真也看不出来。
    """
    vc = fresh()
    vc.check_syllabus(vc.decks())
    vc.check_links()
    expect("正常输入下大纲/链接零失败", not vc.failures, str(vc.failures))


# ---------------------------------------------------------------- LC 侧
def _lc_corpus(tmp: Path, text: str):
    """造一份只含指定引用的合成语料，并把模块的 CW 指过去。

    `check_lc_titles` 会扫 `found` 里的讲义与 `CW/content/*.py`；
    指向空的临时 content 目录，就能精确控制被检查的内容。
    """
    (tmp / "content").mkdir(parents=True, exist_ok=True)
    md = tmp / "fake.md"
    md.write_text(text, encoding="utf-8")
    return {"99": md}


def t_lc_per_occurrence_not_masked():
    """同一 slug 在别处被正确引用，不得掩盖这一处的错号。

    这正是 Claude 第 4 轮栽过的跟头：按 slug 汇总各处题号再比对，
    house-robber 在别处的正确号 198 把误标成 70 的那一处放过去了。
    """
    import tempfile
    vc = fresh()
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        found = _lc_corpus(tmp,
            "**LeetCode 198. 打家劫舍**，https://leetcode.cn/problems/house-robber/\n"
            "**LeetCode 70**，https://leetcode.cn/problems/house-robber/\n")
        with patched((vc, "CW", tmp), (time, "sleep", lambda *_: None)):
            vc._lc_meta = lambda slug: ("198", "打家劫舍")
            vc.check_lc_titles(found)
    expect("LC 逐处比对：错号不被同 slug 的正确引用掩盖",
           any("标成 70" in f for f in vc.failures), str(vc.failures))


def t_lc_allowlist_is_per_alias():
    """LC 白名单同样必须"按别名"放行，不能按题号整体豁免。"""
    import tempfile

    def run(allow):
        vc = fresh()
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            found = _lc_corpus(tmp,
                "**LeetCode 198. 打劫民宅**，https://leetcode.cn/problems/house-robber/\n")
            vc.LC_TITLE_ALLOW = allow
            with patched((vc, "CW", tmp), (time, "sleep", lambda *_: None)):
                vc._lc_meta = lambda slug: ("198", "打家劫舍")
                vc.check_lc_titles(found)
        return [f for f in vc.failures if "198" in f]

    expect("LC 无白名单时题名不符会失败", run({}), "空白名单下应当失败")
    expect("LC 登记了正确别名则放行",
           not run({"198": {"打劫民宅": "教学用简称"}}), "登记别名后不该失败")
    expect("LC 登记了别的别名仍拒绝",
           run({"198": {"无关别名": "无关理由"}}), "换个别名就该继续失败")


GLOBAL_WATCH = ((shutil, "which"), (time, "sleep"), (subprocess, "run"))


def snapshot():
    return {(id(o), a): getattr(o, a) for o, a in GLOBAL_WATCH}


def main():
    cases = (t_missing_week_does_not_crash, t_deck_meta_drift_caught,
             t_render_failure_reports_exit_code, t_oj_allowlist_is_per_alias,
             t_lc_per_occurrence_not_masked, t_lc_allowlist_is_per_alias,
             t_cjk_font_detection, t_positive_control)
    # 泄漏检查逐用例执行，而不是只在最后跑一次。
    # 只在最后查，既依赖用例顺序（有人往后插一个用例就失效），
    # 也说不出是哪个用例漏的 —— Codex 的建议。
    baseline = snapshot()
    leaked = 0
    for fn in cases:
        try:
            fn()
        except Exception as e:
            expect(fn.__name__, False, f"用例自身出错 {type(e).__name__}: {e}")
        after = snapshot()
        bad = [a for (_, a), v in after.items() if v is not baseline[(_, a)]]
        if bad:
            leaked += 1
            expect(f"{fn.__name__} 未泄漏全局补丁", False,
                   f"未还原：{', '.join(sorted(bad))}")
            for o, a in GLOBAL_WATCH:      # 复原后继续，避免污染后续用例
                setattr(o, a, baseline[(id(o), a)])
    if not leaked:
        expect(f"逐用例检查：{len(cases)} 个用例均未泄漏全局补丁", True)

    print("── test_gate · 闸门失败路径 ──")
    bad = 0
    for ok, name, detail in RESULTS:
        print(f"  {'✅' if ok else '❌'} {name}" + (f"\n       {detail}" if not ok else ""))
        bad += not ok
    print(f"\n{'全部通过。' if not bad else f'{bad} 项失败。'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
