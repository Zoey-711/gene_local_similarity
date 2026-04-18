"""变异位点分析（SNP、插入、缺失）。"""

from typing import List

from .utils import AlignmentResult, Variation


def detect_variations(result: AlignmentResult) -> List[Variation]:
    """根据局部比对结果识别 SNP / INS / DEL。"""
    vars_found: List[Variation] = []

    pos1 = result.start_idx_seq1
    pos2 = result.start_idx_seq2

    for b1, b2 in zip(result.aligned_seq1, result.aligned_seq2):
        if b1 == b2:
            if b1 != "-":
                pos1 += 1
                pos2 += 1
            continue

        if b1 == "-":
            vars_found.append(
                Variation(
                    var_type="INS",
                    pos_seq1=pos1 - 1,
                    pos_seq2=pos2,
                    ref="-",
                    alt=b2,
                )
            )
            pos2 += 1
        elif b2 == "-":
            vars_found.append(
                Variation(
                    var_type="DEL",
                    pos_seq1=pos1,
                    pos_seq2=pos2 - 1,
                    ref=b1,
                    alt="-",
                )
            )
            pos1 += 1
        else:
            vars_found.append(
                Variation(
                    var_type="SNP",
                    pos_seq1=pos1,
                    pos_seq2=pos2,
                    ref=b1,
                    alt=b2,
                )
            )
            pos1 += 1
            pos2 += 1

    return vars_found


def format_variations(variations: List[Variation]) -> str:
    if not variations:
        return "未检测到变异位点。"

    header = "类型\t序列1位置\t序列2位置\t参考碱基\t变异碱基"
    lines = [header]
    for v in variations:
        lines.append(f"{v.var_type}\t{v.pos_seq1}\t{v.pos_seq2}\t{v.ref}\t{v.alt}")
    return "\n".join(lines)
