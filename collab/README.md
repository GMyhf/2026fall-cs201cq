# 协作脚手架 · Claude ⇄ Codex

两个 AI（Claude Code 与 Codex）不能靠"记忆"协作，只能靠**共享事实源**交接。
这个目录就是那层事实源：谁都能读、谁都能写、每一轮都留下书面痕迹。

> 移植自 `cs101.openjudge.cn/collab`，闸门与红线按本项目（内容仓库）改写。

## 这个仓库是什么

《数据结构与算法》课程材料，**不是软件项目**：主体是 Markdown 讲义、课件与题解，
没有构建系统、没有 CI。2026 fall（重庆人工智能学院）第 2–17 周的材料在 `courseware/`，
每周一份 `.md` 讲义 + 一份同名 `.pptx` 课件。

**课件是生成的**：`.pptx` 由 `courseware/content/wNN.py` 经 `courseware/build_all.py`
产出（排版引擎在 `courseware/deck.py`）。**永远不要手工编辑 `.pptx`**，会被下次生成覆盖。
讲义 `.md` 则是手写维护的，两者内容需人工保持一致。

## 文件职责

| 文件 | 作用 | 谁写 |
| --- | --- | --- |
| `PLAN.md` | 唯一任务清单 + 决策记录（Decision Log） | 人拍板；两个 agent 更新状态 |
| `HANDOFF.md` | 交接日志：每一次「我做完了，轮到你」都追加一条 | 交接方 |
| `NOTES-claude.md` | Claude 留给 Codex 的话（改了什么、哪里没把握） | 只有 Claude |
| `NOTES-codex.md` | Codex 留给 Claude 的话（审查意见、发现的问题） | 只有 Codex |
| `review-input.md` | 脚本自动生成的 review 包（**不入库**） | `tools/handoff.py` |

> `git` 是最硬的桥梁。软件项目里测试是仲裁，内容仓库里**闸门是"文档之间、
> 文档与大纲之间是否自洽"**——`tools/verify_courseware.py` 把这些不变量固化了下来。
> 文档负责「为什么」和「接下来」，闸门负责「是不是还成立」。

## 闸门：`tools/verify_courseware.py`

```bash
python3 tools/verify_courseware.py            # 1–6 项，约 20 秒
python3 tools/verify_courseware.py --render   # 加第 7 项渲染检查，约 2–4 分钟
```

| # | 检查 | 抓什么 |
| --- | --- | --- |
| 1 | 配对 | 每周恰好一份 `.md` + 同名 `.pptx` + `content/wNN.py`，W02–W17 无缺漏 |
| 2 | 元数据 | 讲义有标题、`*Updated ... GMT+8*`、`*Compiled by ...*` |
| 3 | **大纲** | 讲义声明的教学内容/要求与教学大纲 `.docx` **逐字一致** |
| 4 | 链接 | 所有本地 `.md`/`.pptx`/`.py` 链接可达 |
| 5 | 语法 | 讲义里所有 ```python 代码块 + `courseware/*.py` 能被解析 |
| 6 | 可重生成 | 课件能从 `content/` 重新生成，页数与 README 声明一致 |
| 7 | 渲染 | （需 libreoffice + pdftotext）逐页检查文字未越出版心 |

第 3 项直接解析 `重庆人工智能学院课程教学大纲-闫宏飞.docx` 的第四节表格，
所以**大纲是唯一事实源**：改主题必须先改大纲，或在 PLAN 里写明偏离理由。

闸门做过变异自检：7 处人为破坏（改坏大纲对齐 / 断链 / 删时间戳 / 改错页数 /
挪走课件 / 代码块语法错 / 改坏内容模块）**7/7 全部变红**。

## 一轮标准循环

```
1. 人：把目标写进 collab/PLAN.md（Backlog 里加一条任务）
2. 实现方（如 Claude）：
     - 认领任务 → 改 PLAN.md 状态为 In progress，署名
     - 实现 → python3 tools/handoff.py --verify → git commit（小步、清晰 message）
     - 写 NOTES-claude.md：做了什么 / 哪里没把握 / 想让对方重点看哪里
     - 追加一条 HANDOFF.md 交接记录
     - 运行 python3 tools/handoff.py --from claude --to codex
3. 人：把生成的 collab/review-input.md 交给 Codex（或让 Codex 直接读仓库）
4. 审查方（Codex）：
     - 读 review-input.md → 审查 / 挑错 / 补闸门检查项
     - 把意见写进 NOTES-codex.md；能直接修的就修 + commit
     - 追加一条 HANDOFF.md 交接记录，轮回给 Claude
5. 实现方：git pull → 看对方 commit 与 NOTES → 继续迭代
6. 闸门全绿 + 双方无异议 → 在 PLAN.md 标 Done，写进 Decision Log（如有决策）
```

## 协作模式（按需选）

- **生成 ↔ 审查**：一方写讲义/课件，另一方交叉审查。不同模型盲点不同，
  尤其适合抓**题号错、复杂度结论错、术语前后不一致**这三类。
- **规划 ↔ 执行**：一方拆周次写 PLAN，另一方逐周实现，偏差写回 NOTES。
- **红队 / 对抗**：对样卷题目与参考解答专门找茬——构造能让参考程序 WA/TLE 的数据。
- **分工并行**：按周次切分（如 Claude 管 W02–W09、Codex 管 W10–W17），
  各用 git 分支或 `git worktree` 隔离。

## 硬约束（避免互相覆盖）

- 开工前先在 `PLAN.md` 认领任务并署名；**不要两个 agent 同时改同一周的材料**。
- 小步提交、清晰 commit message，审查方才看得懂 diff。
- **交回时必须附一次真正跑完的闸门输出**（`--verify` 的完整结果）。不接受「我觉得没问题」。
- 改了 `courseware/deck.py`（排版引擎）**必须补跑一次 `--render`**——
  版面溢出只有真渲染才看得见，前 6 项检查不出来。
- **交付后回来销账**：任务落地时，把它回答掉的「未决 / 待拍板 / TODO」逐条改成带出处的
  已决记录。保留原问题、注明最终取值与出处，不要删除，让来回可查。

## 本项目红线（审查时必查）

1. **大纲是唯一事实源**：教学内容与教学要求以
   `重庆人工智能学院课程教学大纲-闫宏飞.docx` 第四节为准，讲义头部逐字复述。
   闸门第 3 项会验；想改主题，先改大纲。
2. **`.pptx` 是产物，不是源**：只改 `content/wNN.py`，不改 `.pptx`。
   diff 里若只有 `.pptx` 动而 `content/` 没动 → 打回。
3. **讲义与课件成对维护**：改了讲义里的知识点/例题/复杂度结论，同名课件要跟着改
   （反之亦然）。这一条**闸门验不了**，是人工审查的重点。
4. **代码是给学生照抄的**：讲义与样卷里的 Python 要真能跑、复杂度声明要与实际行为一致。
   闸门只验语法，**语义正确性靠审查与实跑**。
5. **题号必须对得上**：OJ / LeetCode 的编号、题名、链接三者一致。
   编号错会让学生找不到题，且**没有任何自动化能发现**——审查时逐条核。
6. **上机考试的诚信条款不得放宽**：120 分钟 6 题、禁止任何 AI 工具、
   无法解释自己代码按学术不端处理。这是考核制度，不是可优化的文案。
7. **命名与位置**：`YYYYMM_DSA_W<week>_<topic>`；2026 fall 材料只在 `courseware/`，
   根目录留给 2026 spring（`202603_`–`202606_`）。
8. **保持原文语言**：中文讲义就用中文，术语与前后周一致。

## 生成 review 包

```bash
python3 tools/handoff.py --from claude --to codex                  # 未提交改动 or 最近一次提交
python3 tools/handoff.py --from claude --to codex --base main      # main..HEAD 全部改动
python3 tools/handoff.py --from claude --to codex --range 5e7538c~1..HEAD --verify
VERIFY_RENDER=1 python3 tools/handoff.py --verify                  # 闸门带上渲染检查
```

生成 `collab/review-input.md`：改动摘要、changed files、完整 diff、交接方 NOTES、
PLAN 未决项，以及上面那份 review 检查清单。把这个文件喂给另一方即可。
