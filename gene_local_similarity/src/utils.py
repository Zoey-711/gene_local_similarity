"""通用数据结构与工具函数。"""

from dataclasses import dataclass
from typing import List


@dataclass
class AlignmentResult:
    """一次局部比对的结果。"""

    aligned_seq1: str
    aligned_seq2: str
    match_line: str
    score: int
    start_idx_seq1: int
    end_idx_seq1: int
    start_idx_seq2: int
    end_idx_seq2: int


@dataclass
class Variation:
    """变异位点信息。"""

    var_type: str
    pos_seq1: int
    pos_seq2: int
    ref: str
    alt: str


def build_match_line(aligned_seq1: str, aligned_seq2: str) -> str:
    """构造比对中间标记行：匹配用 |，错配用 .，gap 用空格。"""
    chars: List[str] = []
    for a, b in zip(aligned_seq1, aligned_seq2):
        # 完全匹配
        if a == b and a != "-":
            chars.append("|")
        # 任一位置是 gap
        elif a == "-" or b == "-":
            chars.append(" ")
        # 非 gap 的错配
        else:
            chars.append(".")
    return "".join(chars)
