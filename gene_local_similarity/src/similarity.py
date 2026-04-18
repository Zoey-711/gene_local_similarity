"""局部比对相似度计算。"""

from .utils import AlignmentResult


def calculate_similarity(result: AlignmentResult) -> dict:
    """计算 identity、gap ratio 等指标。"""
    a1 = result.aligned_seq1
    a2 = result.aligned_seq2

    if not a1:
        return {
            "alignment_length": 0,
            "matches": 0,
            "mismatches": 0,
            "gaps": 0,
            "identity": 0.0,
            "gap_ratio": 0.0,
        }

    matches = 0
    mismatches = 0
    gaps = 0

    for x, y in zip(a1, a2):
        if x == "-" or y == "-":
            gaps += 1
        elif x == y:
            matches += 1
        else:
            mismatches += 1

    length = len(a1)
    identity = matches / length * 100
    gap_ratio = gaps / length * 100

    return {
        "alignment_length": length,
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps,
        "identity": identity,
        "gap_ratio": gap_ratio,
    }
