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
import importlib.util
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
    real_run = subprocess.run
    vc.subprocess.run = lambda *a, **k: fake
    vc.shutil.which = lambda name: "/bin/true"
    try:
        vc.check_render()
    finally:
        vc.subprocess.run = real_run
    expect("渲染失败报出退出码", any("退出码 1" in f for f in vc.failures), str(vc.failures))
    expect("渲染失败不再自称通过",
           not any("渲染" in n and "全部渲染通过" in n for n in vc.notes), str(vc.notes))


def t_oj_allowlist_is_per_alias():
    """① 白名单必须"按别名"放行，不能"按题号"整体豁免。"""
    time.sleep = lambda *_: None                     # 测试里不必对题库限速
    plat = {"03704": "扩号匹配问题"}                  # 只桩这一个号

    def run(allow):
        vc = fresh()
        vc.OJ_TITLE_ALLOW = allow
        vc._oj_title = lambda num: plat.get(num)     # 其余号返回 None -> 记为取不到
        vc.check_oj_titles(vc.decks())
        return hits(vc, "03704")

    expect("无白名单时不符会失败", run({}), "空白名单下 03704 应当失败")
    expect("登记了正确别名则放行",
           not run({"03704": {"括号匹配问题": "平台笔误"}}), "登记别名后不该失败")
    expect("登记了别的别名仍拒绝（Codex 的收紧）",
           run({"03704": {"汉诺塔": "无关别名"}}), "换个别名就该继续失败")


def t_positive_control():
    """反向对照：不喂错误输入时，这些检查必须一条失败都没有。

    没有这条，上面任何一个用例即便恒真也看不出来。
    """
    vc = fresh()
    vc.check_syllabus(vc.decks())
    vc.check_links()
    expect("正常输入下大纲/链接零失败", not vc.failures, str(vc.failures))


def main():
    for fn in (t_missing_week_does_not_crash, t_deck_meta_drift_caught,
               t_render_failure_reports_exit_code, t_oj_allowlist_is_per_alias,
               t_positive_control):
        try:
            fn()
        except Exception as e:
            expect(fn.__name__, False, f"用例自身出错 {type(e).__name__}: {e}")
    print("── test_gate · 闸门失败路径 ──")
    bad = 0
    for ok, name, detail in RESULTS:
        print(f"  {'✅' if ok else '❌'} {name}" + (f"\n       {detail}" if not ok else ""))
        bad += not ok
    print(f"\n{'全部通过。' if not bad else f'{bad} 项失败。'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
