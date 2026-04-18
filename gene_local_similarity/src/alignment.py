"""Smith-Waterman 局部比对动态规划实现。"""

from typing import List, Tuple

from config import ScoringConfig


# traceback 方向编码
STOP = 0
DIAG = 1
UP = 2
LEFT = 3


def smith_waterman(
    seq1: str,
    seq2: str,
    scoring: ScoringConfig,
) -> Tuple[List[List[int]], List[List[int]], Tuple[int, int], int]:
    """计算局部比对得分矩阵与回溯方向矩阵。"""
    # 多开一行一列，便于处理边界（第0行/列恒为0）
    rows = len(seq1) + 1
    cols = len(seq2) + 1

    score_matrix = [[0] * cols for _ in range(rows)]
    trace_matrix = [[STOP] * cols for _ in range(rows)]

    max_score = 0
    max_pos = (0, 0)

    for i in range(1, rows):
        for j in range(1, cols):
            # 三个候选转移：对角（匹配/错配）、上（删除）、左（插入）
            match_or_mismatch = (
                score_matrix[i - 1][j - 1] + (scoring.match if seq1[i - 1] == seq2[j - 1] else scoring.mismatch)
            )
            delete = score_matrix[i - 1][j] + scoring.gap
            insert = score_matrix[i][j - 1] + scoring.gap

            # Smith-Waterman 的关键：与0比较，允许“局部重启”
            best = max(0, match_or_mismatch, delete, insert)
            score_matrix[i][j] = best

            # 记录回溯方向，后续用于恢复最优局部对齐路径
            if best == 0:
                trace_matrix[i][j] = STOP
            elif best == match_or_mismatch:
                trace_matrix[i][j] = DIAG
            elif best == delete:
                trace_matrix[i][j] = UP
            else:
                trace_matrix[i][j] = LEFT

            # 全局最大得分点作为回溯起点
            if best > max_score:
                max_score = best
                max_pos = (i, j)

    return score_matrix, trace_matrix, max_pos, max_score
