# -*- coding: utf-8 -*-
"""生成第 2–17 周的课件 PPTX。

用法：
    python3 build_all.py           # 生成全部
    python3 build_all.py 02 07     # 只生成指定周次
"""

import importlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'content'))

import deck  # noqa: E402

# 周次 -> 输出文件名（与 Markdown 讲义同名，便于对照）
WEEKS = {
    '02': '202609_DSA_W02_Intro_ADT_OOP',
    '03': '202609_DSA_W03_Algorithm_Analysis',
    '04': '202609_DSA_W04_Stack',
    '05': '202609_DSA_W05_Queue_Deque_LinkedList',
    '06': '202610_DSA_W06_Recursion_Divide_Sorting',
    '07': '202610_DSA_W07_Greedy_DP',
    '08': '202610_DSA_W08_Search_DFS_BFS_Backtracking',
    '09': '202610_DSA_W09_Tree_Traversal',
    '10': '202611_DSA_W10_Heap_BST',
    '11': '202611_DSA_W11_AVL_DisjointSet',
    '12': '202611_DSA_W12_Graph_Representation_Traversal',
    '13': '202611_DSA_W13_ShortestPath',
    '14': '202612_DSA_W14_MST_TopoSort',
    '15': '202612_DSA_W15_Hash_KMP_InvertedIndex_RAG',
    '16': '202612_DSA_W16_Review',
    '17': '202612_DSA_W17_Final_Machine_Exam',
}


def main(argv):
    wanted = argv or sorted(WEEKS)
    for wk in wanted:
        mod = importlib.import_module(f'w{wk}')
        out = HERE / (WEEKS[wk] + '.pptx')
        pages = deck.build(mod.META, mod.SLIDES, str(out))
        print(f"{out.name}  ({pages} slides)")


if __name__ == '__main__':
    main(sys.argv[1:])
