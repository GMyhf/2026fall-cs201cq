#!/usr/bin/env python3
"""handoff.py — 把一方的 git 改动整理成给另一方 AI 的 review 输入包。

用法:
  python3 tools/handoff.py --from claude --to codex
  python3 tools/handoff.py --from claude --to codex --base main
  python3 tools/handoff.py --from codex --to claude --range HEAD~3..HEAD --verify
  python3 tools/handoff.py --from claude --stdout        # 打印而不写文件
  python3 tools/handoff.py --verify                      # 只跑验证（verify_courseware 闸门）

参数:
  --from <name>   交接方（claude|codex），默认 claude
  --to <name>     接收方，默认取另一方
  --base <ref>    审查 <ref>..HEAD 的全部改动
  --range <a..b>  显式 git range，优先级高于 --base
  --out <path>    输出路径，默认 collab/review-input.md
  --verify        附带运行语法验证并写进包里；单独使用（无生成动作时也会生成）
  --stdout        打印到 stdout，不写文件

无 --base/--range 时自动推断：工作区有未提交改动 → 对比 HEAD；否则 → HEAD~1..HEAD。
只用 Python 标准库 + git，无第三方依赖。移植自 cs101.openjudge.cn/tools/handoff.py。
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COLLAB = ROOT / "collab"
OTHER = {"claude": "codex", "codex": "claude"}
MAX_DIFF_BYTES = 200_000  # 超过则截断，避免生成一个没法读的巨文件

CHECKLIST = """## Review 检查清单（本项目红线）

- [ ] **对齐大纲**：讲义头部的 `> **教学内容**：` / `> **教学要求**：` 是否与
      `重庆人工智能学院课程教学大纲-闫宏飞.docx` 第四节表格**逐字一致**？改主题必须先改大纲或说明偏离理由。
- [ ] **讲义 ⇄ 课件一致**：同名 `.md` 与 `.pptx` 讲的是不是同一件事？讲义改了知识点、
      例题或复杂度结论，同名 `content/wNN.py` 有没有跟着改？
- [ ] **`.pptx` 不可手编**：课件由 `courseware/content/wNN.py` 生成。diff 里若只有 `.pptx`
      变化而 `content/` 没动，说明有人手工改了幻灯片，下次生成会被覆盖 —— 必须打回。
- [ ] **代码要真能跑**：讲义与样卷里的 Python 是给学生照抄的。复杂度声明、边界条件、
      样例输出是否与代码实际行为一致？（本轮已实跑的见 NOTES；未跑的要标出来）
- [ ] **OJ / LeetCode 题号**：题号、题名、链接是否对得上？难度与考点标注是否合理？
      编号错会让学生找不到题 —— 这是本仓库最容易出错也最难自动检出的一类。
- [ ] **元数据与时间戳**：改动过的 `.md` 是否 bump 了 `*Updated ... GMT+8*`？
- [ ] **命名与位置**：新增讲义是否沿用 `YYYYMM_DSA_W<week>_<topic>.md`？
      2026 fall 材料是否都在 `courseware/`，没有散落回根目录？
- [ ] **中英文与术语**：是否保持了原文语言？术语是否与前后周一致
      （如"邻接表"不写成"邻接列表"、"广度优先搜索"不写成"宽度优先搜索"）？
- [ ] **排版不溢出**：课件内容加长后是否仍在版心内？
      （`python3 tools/verify_courseware.py --render` 会逐页检查）
- [ ] **闸门**：`python3 tools/handoff.py --verify` 是否通过？交接记录里有没有真实的验证输出？
"""


def git(args, soft=False):
    try:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.rstrip("\n")
    except subprocess.CalledProcessError:
        if soft:
            return ""
        raise


def resolve_range(opts):
    if opts.range:
        return opts.range, "range"
    if opts.base:
        return f"{opts.base}..HEAD", "range"
    dirty = git(["status", "--porcelain"], soft=True)
    if dirty:
        return "HEAD", "worktree"  # git diff HEAD == 未提交(已跟踪)改动
    has_parent = git(["rev-parse", "--verify", "--quiet", "HEAD~1"], soft=True)
    if not has_parent:
        return "HEAD", "worktree"
    return "HEAD~1..HEAD", "range"


def collect(opts):
    rng, mode = resolve_range(opts)
    diff_args = ["diff", "HEAD"] if mode == "worktree" else ["diff", rng]
    data = {
        "range": rng,
        "mode": mode,
        "diff_args": diff_args,
        "branch": git(["rev-parse", "--abbrev-ref", "HEAD"], soft=True),
        "head_sha": git(["rev-parse", "--short", "HEAD"], soft=True),
        "stat": git([*diff_args, "--stat"], soft=True),
        "name_status": git([*diff_args, "--name-status"], soft=True),
        "untracked": git(["ls-files", "--others", "--exclude-standard"], soft=True),
        "log": git(["log", "--oneline", "--no-decorate", rng], soft=True) if mode == "range" else "",
    }
    diff = git(diff_args, soft=True)
    data["truncated"] = len(diff.encode()) > MAX_DIFF_BYTES
    if data["truncated"]:
        diff = diff.encode()[:MAX_DIFF_BYTES].decode(errors="replace")
    data["diff"] = diff
    return data


def read_notes(who):
    path = COLLAB / f"NOTES-{who}.md"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def read_open_items():
    path = COLLAB / "PLAN.md"
    if not path.is_file():
        return ""
    # 抽出状态看板里非 Done 的任务行，给审查方一眼看到还在飞的任务
    rows = [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.lstrip().startswith("| T-") and "Done" not in line
    ]
    return "\n".join(rows)


def run_verify():
    """跑课件回归闸门。内容仓库没有单测，仲裁靠 tools/verify_courseware.py。"""
    steps = [[sys.executable, "tools/verify_courseware.py"]]
    # 渲染检查很慢（约 2–4 分钟）且依赖 libreoffice，默认不进闸门；
    # 改动 courseware/deck.py（排版引擎）时必须手工补跑一次 --render，
    # 因为版面溢出只有真渲染才看得见 —— 这一条写进了 NOTES 模板。
    if os.environ.get("VERIFY_RENDER") == "1":
        steps[0].append("--render")
    outputs, ok = [], True
    for step in steps:
        proc = subprocess.run(step, cwd=ROOT, capture_output=True, text=True)
        label = " ".join(str(x) for x in step)
        body = proc.stdout + proc.stderr
        outputs.append(f"$ {label}\n{body.rstrip()}")
        ok = ok and proc.returncode == 0
    return ok, "\n".join(outputs)


def build(opts, data, verify_result):
    to = opts.to or OTHER[opts.sender]
    lines = [f"# Review 输入包 · {opts.sender} → {to}", ""]
    lines += [
        "> 由 `tools/handoff.py` 自动生成，不入库。审查方读完请把意见写进 "
        f"`collab/NOTES-{to}.md`，并在 `collab/HANDOFF.md` 追加一条交接记录。",
        "",
        "## 概况",
        "",
        f"- 分支: `{data['branch']}` @ `{data['head_sha']}`",
        f"- 对比范围: `{data['range']}`（{'未提交改动 vs HEAD' if data['mode'] == 'worktree' else '提交区间'}）",
    ]
    if data["truncated"]:
        lines.append(
            f"- ⚠️ diff 超过 {MAX_DIFF_BYTES} 字节已截断，完整改动请用 `git {' '.join(data['diff_args'])}` 查看"
        )
    lines.append("")

    open_items = read_open_items()
    if open_items:
        lines += ["## PLAN 中未完成的任务", "", "```", open_items, "```", ""]
    if data["log"]:
        lines += ["## 本区间提交", "", "```", data["log"], "```", ""]

    lines += ["## 改动文件", "", "```", data["name_status"] or "(无跟踪改动)", "```"]
    if data["untracked"]:
        lines += ["", "未跟踪(新增未 add)文件：", "```", data["untracked"], "```"]
    lines.append("")

    if data["stat"]:
        lines += ["<details><summary>diffstat</summary>", "", "```", data["stat"], "```", "", "</details>", ""]

    notes = read_notes(opts.sender)
    if notes:
        lines += [f"## 交接方留言（NOTES-{opts.sender}.md）", "", notes, ""]

    if verify_result:
        ok, out = verify_result
        lines += [f"## 验证结果：{'✅ 通过' if ok else '❌ 失败'}", "", "```", out, "```", ""]

    lines += ["## 完整 Diff", "", "```diff", data["diff"] or "(空)", "```", "", CHECKLIST, ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(add_help=True, description="生成给另一方 AI 的 review 输入包")
    parser.add_argument("--from", dest="sender", default="claude", choices=["claude", "codex"])
    parser.add_argument("--to", choices=["claude", "codex"])
    parser.add_argument("--base")
    parser.add_argument("--range")
    parser.add_argument("--out")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--stdout", action="store_true")
    opts = parser.parse_args()

    # 只想跑验证时（无任何生成相关参数）快速返回
    only_verify = opts.verify and not any([opts.to, opts.base, opts.range, opts.out, opts.stdout]) and "--from" not in sys.argv
    verify_result = run_verify() if opts.verify else None
    if only_verify:
        ok, out = verify_result
        print(out)
        sys.exit(0 if ok else 1)

    data = collect(opts)
    markdown = build(opts, data, verify_result)
    if opts.stdout:
        print(markdown)
        return
    out_path = (ROOT / opts.out) if opts.out else (COLLAB / "review-input.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    rel = out_path.relative_to(ROOT)
    print(f"✅ 已生成 review 输入包: {rel}")
    print(f"   把它交给 {opts.to or OTHER[opts.sender]}，或让对方直接读这个文件。")
    if verify_result and not verify_result[0]:
        sys.exit(1)


if __name__ == "__main__":
    main()
