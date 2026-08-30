# 课件 PPTX（第 2–17 周）

*Updated 2026-08-30 16:20 GMT+8*
 *Compiled by Hongfei Yan (2026 Fall)*

本目录存放《数据结构与算法》第 2–17 周的 **PowerPoint 课件**，与仓库根目录的
Markdown 讲义一一对应（同名，仅扩展名不同），内容依据
《重庆人工智能学院课程教学大纲-闫宏飞.docx》"四、教学内容、要求及进度安排"编写。

> 本目录**自成一体**，不与根目录既有材料混放。根目录的 `.md` 是**讲义**（供学生阅读、
> 含完整题解）；本目录的 `.pptx` 是**课件**（供课堂放映，只保留主干与关键代码）。

---

## 1 文件清单

| 周次 | 文件 | 页数 | 主题 |
| ---- | ---- | ---- | ---- |
| 2 | `202609_DSA_W02_Intro_ADT_OOP.pptx` | 33 | 导论、ADT 与 OOP、Python 基础回顾 |
| 3 | `202609_DSA_W03_Algorithm_Analysis.pptx` | 31 | 大 O、复杂度级别、内建结构性能 |
| 4 | `202609_DSA_W04_Stack.pptx` | 30 | 栈、括号匹配、进制转换、调度场算法 |
| 5 | `202609_DSA_W05_Queue_Deque_LinkedList.pptx` | 32 | 队列、双端队列、顺序表与链表 |
| 6 | `202610_DSA_W06_Recursion_Divide_Sorting.pptx` | 30 | 递归与分治、五大排序与性能对比 |
| 7 | `202610_DSA_W07_Greedy_DP.pptx` | 30 | 贪心与动态规划 |
| 8 | `202610_DSA_W08_Search_DFS_BFS_Backtracking.pptx` | 27 | DFS/BFS、回溯与剪枝 |
| 9 | `202610_DSA_W09_Tree_Traversal.pptx` | 32 | 树的概念与二叉树遍历 |
| 10 | `202611_DSA_W10_Heap_BST.pptx` | 29 | 堆、堆排序、二叉搜索树 |
| 11 | `202611_DSA_W11_AVL_DisjointSet.pptx` | 31 | AVL 树、并查集 |
| 12 | `202611_DSA_W12_Graph_Representation_Traversal.pptx` | 26 | 图的表示与遍历 |
| 13 | `202611_DSA_W13_ShortestPath.pptx` | 28 | Dijkstra、Bellman-Ford、Floyd |
| 14 | `202612_DSA_W14_MST_TopoSort.pptx` | 31 | 最小生成树、拓扑排序、DAG 应用 |
| 15 | `202612_DSA_W15_Hash_KMP_InvertedIndex_RAG.pptx` | 32 | 散列表、KMP、倒排索引 → RAG |
| 16 | `202612_DSA_W16_Review.pptx` | 32 | 总结复习、模板代码库、考试要点 |
| 17 | `202612_DSA_W17_Final_Machine_Exam.pptx` | 34 | 上机考试命题方案与样卷 |

合计 **488 页**。版面 16:9，中文字体 **微软雅黑**，代码字体 **Consolas**。

---

## 2 源码与再生成

课件**不是手工排版的**，而是由脚本从结构化内容生成，便于批量修改样式与逐年复用。

```
slides/
├── deck.py            # 排版引擎：主题配色、版面构件、自适应字号
├── build_all.py       # 生成入口
├── content/
│   ├── w02.py         # 第 2 周的内容（META + SLIDES）
│   ├── ...
│   └── w17.py
└── *.pptx             # 生成结果
```

**环境**：

```bash
pip install python-pptx
```

**生成**：

```bash
cd slides
python3 build_all.py           # 生成全部 16 个 pptx
python3 build_all.py 07 12     # 只重新生成第 7、12 周
```

---

## 3 修改内容

编辑 `content/wNN.py` 中的 `SLIDES` 列表即可，无需碰排版代码。每张幻灯片是一个元组：

| 写法 | 说明 |
| ---- | ---- |
| `('section', '第 1 节', '标题', '副标题?')` | 章节分隔页 |
| `('bullets', '标题', [条目, ...])` | 要点页；条目以 `- ` 开头表示次级 |
| `('code', '标题', '代码', '说明?')` | 代码页，字号按行数与最长行自动缩放 |
| `('ascii', '标题', '示意图', '说明?')` | 等宽示意图，居中 |
| `('table', '标题', [[表头...], [行...]], '说明?')` | 表格，列宽按内容自动分配 |
| `('two', '标题', '左标题', [...], '右标题', [...])` | 左右两栏 |
| `('key', '标题', '要点正文')` | 整页强调一句话 |

正文中可用 `**强调**`（渲染为深蓝加粗）与 `` `等宽` ``。
**代码页与示意图页原样输出**，不解析这些标记 —— 所以 Python 的 `**` 幂运算符是安全的。

字号、行高、列宽全部**按内容自动计算**，不需要手工调整；新增内容后直接重新生成即可。

---

## 4 质量检查

生成后可用 LibreOffice 渲染为 PDF，再机器检查排版：

```bash
libreoffice --headless --convert-to pdf --outdir /tmp/render slides/*.pptx
```

本次交付前已完成的检查：

- **488 页全部渲染通过**，无文字越出版心（右边界 / 底部页脚区）；
- 代码块均完整落在灰底框内，说明文字不与表格、代码重叠；
- 表格行高按 LibreOffice 实测行距（约 34pt）校准；
- 无 `**` / 反引号等标记泄漏到渲染结果中。

> ⚠️ 字体以放映机器为准：Windows + Office 下"微软雅黑 + Consolas"可直接使用；
> macOS 若无微软雅黑会回退到系统中文字体，版面基本不受影响。
