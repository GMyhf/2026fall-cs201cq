# 更新日志 / Changelog

本文档记录课件（Markdown 笔记）的重要修订。时间为 GMT+8（北京时间）。

---

## 2026-06-18 ~ 2026-06-19 — 课件校对（Proofreading pass）

对课程讲义、写作题库等 Markdown 笔记进行了一轮系统性校对。本轮改动以排版规范化与错别字订正为主，**不改变任何技术内容与题解结论**。主要类别如下：

- **中英文/数字间距**：在中文与英文单词、数字之间统一补加空格，例如
  `Python是` → `Python 是`、`2026spring` → `2026 spring`、`OOP及` → `OOP 及`、
  `入度为0` → `入度为 0`、`DFS或BFS` → `DFS 或 BFS`。
- **错别字与拼写订正**：
  - 英文：`Complied` → `Compiled`、`Karn` → `Kahn`、`Intialize` → `Initialize`、
    `Thmos.H.Cormen` → `Thomas H. Cormen`。
  - 中文：`其它` → `其他`、`储存` → `存储`、`邻接列表` → `邻接表`、
    `宽度优先搜索` → `广度优先搜索`、`树节无树` → `树结无树`、`多家练习` → `多加练习`、
    `加人该棵树` → `加入该棵树`、`写的比较随意` → `写得比较随意`。
- **标点规范化**：全角句点 `．` → `。`，省略号 `。。。` → `……`，
  以及全角拉丁字母（`Ｌ`、`Ｑ` 等）改为半角。
- **数学公式修复**：将失效的 GIF/base64 内联图片公式改为 LaTeX 记法，例如
  `{0,11,45,81}![...]` → `$\{0,11,45,81\}$`、`𝑂(𝑛×𝑘)` → `$O(n \times k)$`。
- **代码格式**：修正行末反斜杠续行为括号换行（`knight_tour` 示例），
  统一行内代码反引号与 `stack + DFS` 类术语间距。
- **文字清理**：删除个别已废弃的删除线编辑批注；对少数表述补充说明
  （如满 m 叉树题目补充“根为第一层”前提）。

### 涉及文件

| 文件 | 说明 |
| ---- | ---- |
| `202603_DSA_W01_OOP.md` | 第 1 周 OOP 与 Python 基础 |
| `202603_DSA_W02_BIT_Fenwick.md` | 第 2 周 树状数组（Fenwick / BIT） |
| `202603_DSA_W03_KMP_InvertedIndex_BitOpt.md` | 第 3 周 KMP、倒排索引、位运算优化 |
| `202603_DSA_W04-5.5_Complexity_LinearStructures.md` | 第 4–5.5 周 复杂度与线性结构 |
| `202603_DSA_W5.5_VM_Shell_LLMs.md` | 第 5.5 周 虚拟机、Shell、LLM |
| `202603_DSA_AI_literacy.md` | AI 素养 |
| `202604_DSA_W06-08_Tree.md` | 第 6–8 周 树 |
| `202604_DSA_W09-12_Graph.md` | 第 9–12 周 图论 |
| `202606_DSA_W14_Final_Exam_Review.md` | 第 14 周 期末复习 |
| `20250520_HashTable.md` | 哈希表 |
| `DSA_MOOC_solution.md` | MOOC 题解 |
| `DSA_problem_list_at_2026spring.md` | 每日选作题目列表 |
| `LC_top-100-liked.md` | LeetCode 热题 100 |
| `written_exam_DSA-B.md` | 笔试题（含解答） |
| `written_exam_DSA-B_nosolution.md` | 笔试题（无解答） |

### 相关提交

- `c8266fd` Proofread week 1 OOP notes
- `4682a4e` Proofread remaining root markdown notes
- `cc4d2a7` Proofread tree data structure notes
- `686b022` Proofread graph theory notes
- `3164610` / `775330f` Proofread DSA written exam materials
- `7a8d6ec` Proofread DSA written exam without solutions

---

## 2026-08-30 — 新增第 2–17 周课件（2026 Fall / 重庆人工智能学院）

依据《重庆人工智能学院课程教学大纲-闫宏飞.docx》"四、教学内容、要求及进度安排"，
新建覆盖第 2–17 周的全套课件，共 16 个文件。每份课件包含：大纲对应的教学内容与要求、
知识点清单、完整可运行的 Python 实现（非伪代码）、OpenJudge / LeetCode 例题与题解、
本周作业、实验安排、思考题与小结。

### 新增文件

| 文件 | 周次 / 内容 |
| ---- | ---- |
| `202609_DSA_W02_Intro_ADT_OOP.md` | 第 2 周 导论、ADT 与 OOP、Python 基础回顾 |
| `202609_DSA_W03_Algorithm_Analysis.md` | 第 3 周 算法分析：大 O、复杂度级别、内建结构性能 |
| `202609_DSA_W04_Stack.md` | 第 4 周 栈：括号匹配、进制转换、调度场算法 |
| `202609_DSA_W05_Queue_Deque_LinkedList.md` | 第 5 周 队列、双端队列；顺序表与链表 |
| `202610_DSA_W06_Recursion_Divide_Sorting.md` | 第 6 周 递归与分治；五大排序与性能对比 |
| `202610_DSA_W07_Greedy_DP.md` | 第 7 周 贪心与动态规划 |
| `202610_DSA_W08_Search_DFS_BFS_Backtracking.md` | 第 8 周 搜索专题：DFS/BFS、回溯与剪枝 |
| `202610_DSA_W09_Tree_Traversal.md` | 第 9 周 树的概念与二叉树遍历 |
| `202611_DSA_W10_Heap_BST.md` | 第 10 周 堆、堆排序、二叉搜索树 |
| `202611_DSA_W11_AVL_DisjointSet.md` | 第 11 周 AVL 树；并查集 |
| `202611_DSA_W12_Graph_Representation_Traversal.md` | 第 12 周 图的表示与遍历 |
| `202611_DSA_W13_ShortestPath.md` | 第 13 周 Dijkstra、Bellman-Ford、Floyd-Warshall |
| `202612_DSA_W14_MST_TopoSort.md` | 第 14 周 最小生成树；拓扑排序；DAG 应用 |
| `202612_DSA_W15_Hash_KMP_InvertedIndex_RAG.md` | 第 15 周 散列表、KMP、倒排索引 → RAG |
| `202612_DSA_W16_Review.md` | 第 16 周 总结与复习：知识体系、模板代码库、考试要点 |
| `202612_DSA_W17_Final_Machine_Exam.md` | 第 17 周 期末上机考试命题方案与样卷 |

### 说明

- 文件名中的 `YYYYMM` 按秋季学期周次对应月份编排（第 2–5 周 → 09，第 6–9 周 → 10，
  第 10–13 周 → 11，第 14–17 周 → 12）。
- 第 15 周把散列表与倒排索引延伸到 TF-IDF / BM25 与 RAG，落实大纲"创新与前沿目标"中
  "AI 大模型实践内容"的要求，并给出 AI 辅助算法实践小项目（占总评 10%）的选题建议。
- 第 17 周为面向教师的命题方案：知识点覆盖矩阵、6 题样卷（题面 + 样例 + 参考解答 +
  数据构造建议 + 评分标准）、分类备选题库，以及命题/阅卷检查清单。
  6 份参考解答均已在本地运行，输出与题面样例逐一核对一致。
- `README.md` 新增"课件目录"一节，链接全部 16 份课件并列出考核方式。

---

## 2026-08-30 — 新增第 2–17 周课件 PPTX（`slides/`）

为第 2–17 周的 Markdown 讲义配套制作了课堂放映用的 PowerPoint 课件，共 16 个文件、
**488 页**，统一放在新建的 `slides/` 目录，不与根目录既有材料混放。

### 目录结构

| 文件 | 说明 |
| ---- | ---- |
| `slides/*.pptx` | 16 份课件，与根目录同名 `.md` 讲义一一对应 |
| `slides/deck.py` | 排版引擎：主题配色、版面构件、自适应字号与列宽 |
| `slides/build_all.py` | 生成入口，`python3 build_all.py [周次...]` |
| `slides/content/wNN.py` | 各周内容（`META` + `SLIDES`），与排版代码解耦 |
| `slides/README.md` | 使用与二次编辑说明 |

### 说明

- 课件**由脚本生成**而非手工排版：编辑 `content/wNN.py` 后重新运行 `build_all.py` 即可，
  字号、行高、表格列宽全部按内容自动计算。
- 版面 16:9，中文字体微软雅黑、代码字体 Consolas；支持要点页、代码页、等宽示意图页、
  表格页、双栏页、强调页六种版式。
- **质量检查**：用 LibreOffice 将全部 488 页渲染为 PDF 后逐页机器校验 ——
  无文字越出版心、代码块完整落在框内、说明文字不与表格重叠、无 Markdown 标记泄漏；
  表格行高按实测渲染行距（约 34pt）校准。
- 分工：根目录 `.md` 是**讲义**（含完整题解，供学生阅读），`slides/*.pptx` 是**课件**
  （只保留主干与关键代码，供课堂放映）。
- `README.md` 的“课件目录”一节新增指向 `slides/` 的链接。

---

## 2026-08-30 — 讲义与课件合并到 `slides/` 目录

第 2–17 周的讲义（`.md`）与课件（`.pptx`）是一套材料，现统一放在 `slides/` 目录成对维护，
不再分散在根目录与子目录两处。

### 改动

- 用 `git mv` 把 16 份讲义从根目录移入 `slides/`（保留文件历史）：
  `202609_DSA_W02_*` … `202612_DSA_W17_*`。根目录的 2026 spring 讲义
  （`202603_`–`202606_`）保持原位不动。
- 修正移动后受影响的相对链接：
  - W02 讲义引用的 `Python_Development_Setup_Mac_Windows.md` → `../Python_Development_Setup_Mac_Windows.md`
  - W16 讲义对 W17 的引用改为同目录相对链接
- `README.md` 的课件目录表改为每周一行、**同时给出讲义与课件两个链接**。
- `slides/README.md` 更名为“讲义与课件”，说明两者分工，并强调
  **`.pptx` 由脚本生成、不要手工编辑**，`.md` 为手写维护。
- `CLAUDE.md` 的目录约定同步更新，注明 2026 fall 讲义位于 `slides/`。

---

## 2026-08-30 — 目录 `slides/` 更名为 `courseware/`

该目录同时存放讲义（`.md`）与课件（`.pptx`），"slides"（幻灯片）只描述了其中一半，
故更名为 `courseware/`（课件资料），语义更贴切。

- 用 `git mv` 整目录重命名，51 个文件全部识别为 rename，**内容零改动**。
- 同步更新引用：`README.md` 的目录表与生成命令、`courseware/README.md` 的目录树与
  渲染命令、`CLAUDE.md` 的目录约定。
- 新增 `courseware/.gitignore`，忽略 `__pycache__/` 与 `*.pyc`。
- 本文件中 2026-08-30 早先两条记录仍写作 `slides/`，为当时的真实路径，按变更日志惯例保留。

---

## 2026-08-31 — 新增回归闸门与 Claude⇄Codex 协作脚手架

为让另一个 AI（Codex）能接手审查这批课件，补上「可验证」与「可交接」两层基础设施。

### 新增文件

| 文件 | 作用 |
| ---- | ---- |
| `tools/verify_courseware.py` | 课件回归闸门，7 项检查 |
| `tools/handoff.py` | 把一个 git range 打包成给对方 AI 的 review 输入包 |
| `collab/README.md` | 协作脚手架说明 + 本项目红线清单 |
| `collab/PLAN.md` | 唯一任务清单（T-001…T-006）、未决项、决策记录 |
| `collab/HANDOFF.md` | 交接日志（含本轮 Claude → Codex 记录与模板） |
| `collab/NOTES-claude.md` | Claude 留给 Codex 的话：实跑过什么、**哪里没把握** |
| `collab/NOTES-codex.md` | Codex 回写位（占位） |

### 闸门检查项

配对（每周 `.md` + 同名 `.pptx` + `content/wNN.py`）、元数据（标题与 GMT+8 时间戳）、
**大纲对齐**（直接解析教学大纲 `.docx` 第四节，与讲义头部逐字比对）、本地链接可达、
Python 语法（讲义代码块 + `courseware/*.py`）、可重新生成（页数与 README 声明一致），
以及可选的渲染越界检查（`--render`）。

闸门做过**变异自检**：7 处人为破坏全部被抓（7/7），复原后全绿。

### 顺带修正

- `courseware/deck.py` 原用 python-pptx 私有 API `prs.slides.__iter__.__self__._sldIdLst`
  数页数，改为公共的 `len(prs.slides)`。
- `courseware/build_all.py` 改为打印**实际生成页数**（来自 `deck.build` 的返回值）
  而不是 `len(SLIDES) + 1`；两者恰好相等，但前者才是事实，也让闸门的页数比对有据可依。
- 新增根 `.gitignore` 与 `collab/.gitignore`（忽略 `__pycache__` 与生成的 `review-input.md`）。
- `README.md` 与 `CLAUDE.md` 补充闸门用法与 `collab/` 指引。
