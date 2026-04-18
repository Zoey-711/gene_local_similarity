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
    rows = len(seq1) + 1
    cols = len(seq2) + 1

    score_matrix = [[0] * cols for _ in range(rows)]
    trace_matrix = [[STOP] * cols for _ in range(rows)]

    max_score = 0
    max_pos = (0, 0)

    for i in range(1, rows):
        for j in range(1, cols):
            match_or_mismatch = (
                score_matrix[i - 1][j - 1] + (scoring.match if seq1[i - 1] == seq2[j - 1] else scoring.mismatch)
            )
            delete = score_matrix[i - 1][j] + scoring.gap
            insert = score_matrix[i][j - 1] + scoring.gap

            best = max(0, match_or_mismatch, delete, insert)
            score_matrix[i][j] = best

            if best == 0:
                trace_matrix[i][j] = STOP
            elif best == match_or_mismatch:
                trace_matrix[i][j] = DIAG
            elif best == delete:
                trace_matrix[i][j] = UP
            else:
                trace_matrix[i][j] = LEFT

            if best > max_score:
                max_score = best
                max_pos = (i, j)

    return score_matrix, trace_matrix, max_pos, max_score
