"""局部比对最优路径回溯。"""

from .alignment import DIAG, LEFT, STOP, UP
from .utils import AlignmentResult, build_match_line


def traceback_local(
    seq1: str,
    seq2: str,
    score_matrix: list[list[int]],
    trace_matrix: list[list[int]],
    start_pos: tuple[int, int],
    final_score: int,
) -> AlignmentResult:
    """从最大得分点回溯，得到一条局部最优比对。"""
    i, j = start_pos
    aligned1: list[str] = []
    aligned2: list[str] = []

    # 记录回溯起点，对应局部最优片段的结束位置
    end_i = i
    end_j = j

    while i > 0 and j > 0:
        direction = trace_matrix[i][j]
        # 到达 STOP 或得分为0，说明局部比对片段起点已找到
        if direction == STOP or score_matrix[i][j] == 0:
            break

        if direction == DIAG:
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif direction == UP:
            aligned1.append(seq1[i - 1])
            aligned2.append("-")
            i -= 1
        elif direction == LEFT:
            aligned1.append("-")
            aligned2.append(seq2[j - 1])
            j -= 1

    aligned_seq1 = "".join(reversed(aligned1))
    aligned_seq2 = "".join(reversed(aligned2))

    # 回溯停止时 i/j 停在片段起点前一个位置，因此 +1
    start_i = i + 1
    start_j = j + 1

    return AlignmentResult(
        aligned_seq1=aligned_seq1,
        aligned_seq2=aligned_seq2,
        match_line=build_match_line(aligned_seq1, aligned_seq2),
        score=final_score,
        start_idx_seq1=start_i,
        end_idx_seq1=end_i,
        start_idx_seq2=start_j,
        end_idx_seq2=end_j,
    )
