# 2026fall-cs201cq: DS Algo（数据结构与算法）

*Updated 2026-08-31 02:30 GMT+8*  
 *Compiled by Hongfei Yan (2026 Fall)*  
*项目仓库：[GMyhf/2026fall-cs201cq](https://github.com/GMyhf/2026fall-cs201cq/)*

------

## 1 题解 & 教材资源

- **题解**：[fuynaloft.github.io/sol101/](https://fuynaloft.github.io/sol101/)

- **核心教材**：以课件为主，辅以以下参考书目：

  - 《Python数据结构与算法分析（第3版）》 Miller, Ranum, College

  - 《算法笔记》 胡凡、曾磊

  - 《算法导论（第3版）》 Cormen, Leiserson 等


- **AI 拓展**：
  *   教材：*Build a Large Language Model (From Scratch)* (Sebastian Raschka)
  *   [配套代码库](https://github.com/rasbt/LLMs-from-scratch)
  *   重点掌握《Test Yourself On Build a Large Language Model》中的核心概念与问题。

------

## 2 课件目录（按教学大纲第 2–17 周）

依据《重庆人工智能学院课程教学大纲》"四、教学内容、要求及进度安排"编写，每周 3 学时，共 48 学时（理论 24 + 实验 12 + 实践 12）。

讲义（`.md`）与课件（`.pptx`）成对存放在 **[`courseware/`](courseware/)** 目录，同名对应：
**讲义**含完整题解，供课后阅读；**课件**只保留主干与关键代码，供课堂放映。

| 周次 | 主题 | 讲义 | 课件 | 教学内容 |
| ---- | ---- | ---- | ---- | ---- |
| 第 2 周 | 导论、ADT 与 OOP | [md](courseware/202609_DSA_W02_Intro_ADT_OOP.md) | [pptx](courseware/202609_DSA_W02_Intro_ADT_OOP.pptx) | 导论、ADT 与 OOP、Python 基础回顾 |
| 第 3 周 | 算法分析 | [md](courseware/202609_DSA_W03_Algorithm_Analysis.md) | [pptx](courseware/202609_DSA_W03_Algorithm_Analysis.pptx) | 大 O、复杂度级别、Python 内建结构性能 |
| 第 4 周 | 栈 | [md](courseware/202609_DSA_W04_Stack.md) | [pptx](courseware/202609_DSA_W04_Stack.pptx) | ADT、实现、括号匹配、进制转换、调度场算法 |
| 第 5 周 | 队列、双端队列与链表 | [md](courseware/202609_DSA_W05_Queue_Deque_LinkedList.md) | [pptx](courseware/202609_DSA_W05_Queue_Deque_LinkedList.pptx) | 队列/双端队列；顺序表与链表对比；无序表与有序表 |
| 第 6 周 | 递归、分治与排序 | [md](courseware/202610_DSA_W06_Recursion_Divide_Sorting.md) | [pptx](courseware/202610_DSA_W06_Recursion_Divide_Sorting.pptx) | 递归与分治；冒泡/选择/插入/归并/快排与性能对比 |
| 第 7 周 | 贪心与动态规划 | [md](courseware/202610_DSA_W07_Greedy_DP.md) | [pptx](courseware/202610_DSA_W07_Greedy_DP.pptx) | 贪心选择性质、最优子结构、状态转移方程 |
| 第 8 周 | 搜索专题 | [md](courseware/202610_DSA_W08_Search_DFS_BFS_Backtracking.md) | [pptx](courseware/202610_DSA_W08_Search_DFS_BFS_Backtracking.pptx) | DFS/BFS、回溯与剪枝 |
| 第 9 周 | 树与二叉树遍历 | [md](courseware/202610_DSA_W09_Tree_Traversal.md) | [pptx](courseware/202610_DSA_W09_Tree_Traversal.pptx) | 树的概念；前中后序与层序遍历；建树 |
| 第 10 周 | 堆与二叉搜索树 | [md](courseware/202611_DSA_W10_Heap_BST.md) | [pptx](courseware/202611_DSA_W10_Heap_BST.pptx) | 堆、堆排序、优先队列、BST |
| 第 11 周 | AVL 树与并查集 | [md](courseware/202611_DSA_W11_AVL_DisjointSet.md) | [pptx](courseware/202611_DSA_W11_AVL_DisjointSet.pptx) | 平衡因子与四种旋转；路径压缩与按秩合并 |
| 第 12 周 | 图的表示与遍历 | [md](courseware/202611_DSA_W12_Graph_Representation_Traversal.md) | [pptx](courseware/202611_DSA_W12_Graph_Representation_Traversal.pptx) | 邻接矩阵/邻接表；BFS 与 DFS；连通分量 |
| 第 13 周 | 最短路 | [md](courseware/202611_DSA_W13_ShortestPath.md) | [pptx](courseware/202611_DSA_W13_ShortestPath.pptx) | Dijkstra、Bellman-Ford、Floyd-Warshall |
| 第 14 周 | 最小生成树与拓扑排序 | [md](courseware/202612_DSA_W14_MST_TopoSort.md) | [pptx](courseware/202612_DSA_W14_MST_TopoSort.pptx) | Prim、Kruskal；Kahn 算法；DAG 应用 |
| 第 15 周 | 散列表、KMP、倒排索引 → RAG | [md](courseware/202612_DSA_W15_Hash_KMP_InvertedIndex_RAG.md) | [pptx](courseware/202612_DSA_W15_Hash_KMP_InvertedIndex_RAG.pptx) | 冲突解决；next 数组；TF-IDF/BM25 与 RAG |
| 第 16 周 | 课程总结与复习 | [md](courseware/202612_DSA_W16_Review.md) | [pptx](courseware/202612_DSA_W16_Review.pptx) | 知识体系梳理、模板代码库、考试要点 |
| 第 17 周 | 期末上机考试 | [md](courseware/202612_DSA_W17_Final_Machine_Exam.md) | [pptx](courseware/202612_DSA_W17_Final_Machine_Exam.pptx) | 命题方案、样卷 6 题与参考解答、备选题库 |

### 重新生成课件

课件由脚本从结构化内容生成（共 16 份、488 页），源码见 [`courseware/README.md`](courseware/README.md)：

```bash
pip install python-pptx
cd courseware && python3 build_all.py        # 重新生成全部课件
```

### 校验与协作

课件材料有一套回归闸门，改动 `courseware/` 后请跑一遍：

```bash
python3 tools/verify_courseware.py            # 配对/元数据/大纲对齐/链接/语法/可重生成
python3 tools/verify_courseware.py --render   # 追加：渲染 488 页并检查排版越界
```

多 AI 协作（Claude ⇄ Codex）的任务清单、交接日志与审查约定见 **[`collab/`](collab/)**。

### 考核方式

| 考核项目 | 占比 | 说明 |
| ---- | ---- | ---- |
| 平时作业 | 30% | OpenJudge / LeetCode 编程题；考查 PEP 8 代码规范与提交纪律 |
| AI 辅助算法实践小项目 | 10% | 完整项目一个；鼓励使用大模型但**须声明** |
| 期末上机考试 | 60% | 120 分钟 6 题，OJ 平台完成；**禁止使用任何 AI 工具** |

------

## 3 数算B-15班 课程安排

- **上课时间**：1–15 周，每周二 7–9 节（15:10–18:00）
- **上课地点**：理教 410（150 座位）
- **期末机考**：第14周 周三（2026年6月3日 15:08–17:00）
  - 地点：5号机房（71 台）、6号机房（90 台）
- **期末笔试**：2026年6月23日（周二）14:00–16:00
  - 地点：理教402、理教403
- **评分规则**：
  - 机考详情：时长 112 分钟（1小时52分），共 6 道题。
  - 总评参考指标：
    - 优秀：通常需 AC（通过）5 题或 6 题。
    - 优秀机会：AC 4 题者，若笔试表现优异且在优秀率名额内，仍有机会获评优秀。
    - 及格底线：若机考 AC 0 题，即使笔试满分，总评成绩最高不超过 84 分。

------

## 4 预习与环境搭建指南

> 课程主要使用 **Python**，如有同学坚持使用 **C++**，课程亦予以支持。

- **开发工具推荐**：
  
  - 编辑器/IDE：PyCharm, VS Code
  - 环境配置指南：
    *   [Python 开发环境搭建 (Mac & Windows)](https://github.com/GMyhf/2026spring-cs201/blob/main/Python_Development_Setup_Mac_Windows.md)
    *   [在 VS Code 中配置 C++ 编程环境](https://github.com/GMyhf/2026spring-cs201/blob/main/Writing_First_C%2B%2B_Program_in_VS-Code.md)


------

### 编程强化训练建议

为夯实基础并培养算法思维，建议在开课前按以下路径进行针对性练习：

1.  **LeetCode 热题 100 (Top 100 Liked)**
    *   [在线练习链接](https://leetcode.cn/studyplan/top-100-liked/)
    *   重点掌握基础数据结构与高频算法题。
2.  **课程组精选每日选作题**
    *   [题目列表链接](https://github.com/GMyhf/2026spring-cs201/blob/main/DSA_problem_list_at_2026spring.md)
    *   **练习建议**：题目分为 Easy、Medium (M)、Tough (T) 三个等级。要求熟练完成所有 Easy 和 Medium 题目，鼓励勇于挑战 Tough 题目。

------

## 5 重要注意事项

建议在开课前完成 **LeetCode 热题 100**。

*   **预习范围**：可暂不包含“链表”（14题）和“二叉树”（15题）。
*   **目标**：通过刷题消除编程语言隔阂，确保能跟上数算课程的教学节奏。

------



**总结**：
本课程在传统“数据结构与算法”的基础上，融入了 **AI 大模型原理** 元素。希望同学们通过“预习 + 算法实战 + AI 辅助”的复合模式，在掌握经典算法的同时，理解现代智能技术的基石。
