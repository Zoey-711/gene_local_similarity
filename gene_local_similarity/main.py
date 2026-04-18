"""程序入口：基因序列局部相似度检测与变异位点分析。"""

import argparse
from pathlib import Path

from config import DEFAULT_SCORING
from src.alignment import smith_waterman
from src.io_utils import ensure_dir, load_sequence, save_matrix_csv, save_text
from src.preprocess import clean_sequence, validate_sequence
from src.similarity import calculate_similarity
from src.traceback import traceback_local
from src.variation import detect_variations, format_variations
from src.visualization import plot_score_matrix


def format_alignment_result(aln, similarity: dict) -> str:
    lines = [
        "=== 局部比对结果（Smith-Waterman）===",
        f"最佳得分: {aln.score}",
        f"序列1局部区间: [{aln.start_idx_seq1}, {aln.end_idx_seq1}]",
        f"序列2局部区间: [{aln.start_idx_seq2}, {aln.end_idx_seq2}]",
        "",
        aln.aligned_seq1,
        aln.match_line,
        aln.aligned_seq2,
        "",
        "=== 相似度统计 ===",
        f"比对长度: {similarity['alignment_length']}",
        f"匹配数: {similarity['matches']}",
        f"错配数: {similarity['mismatches']}",
        f"Gap数: {similarity['gaps']}",
        f"Identity: {similarity['identity']:.2f}%",
        f"Gap Ratio: {similarity['gap_ratio']:.2f}%",
    ]
    return "\n".join(lines)


def resolve_sequences(args: argparse.Namespace) -> tuple[str, str]:
    """根据参数解析输入序列：支持文件、命令行直传、交互输入。"""
    if args.interactive:
        seq1 = clean_sequence(input("请输入序列1: ").strip())
        seq2 = clean_sequence(input("请输入序列2: ").strip())
        validate_sequence(seq1)
        validate_sequence(seq2)
        return seq1, seq2

    if args.seq1_str or args.seq2_str:
        if not (args.seq1_str and args.seq2_str):
            raise ValueError("使用命令行直传序列时，--seq1-str 和 --seq2-str 需要同时提供。")
        seq1 = clean_sequence(args.seq1_str)
        seq2 = clean_sequence(args.seq2_str)
        validate_sequence(seq1)
        validate_sequence(seq2)
        return seq1, seq2

    return load_sequence(args.seq1), load_sequence(args.seq2)


def main() -> None:
    parser = argparse.ArgumentParser(description="基因序列局部相似度检测与变异位点分析")
    parser.add_argument("--seq1", default="data/sample_seq1.txt", help="序列1文件路径")
    parser.add_argument("--seq2", default="data/sample_seq2.txt", help="序列2文件路径")
    parser.add_argument("--seq1-str", default="", help="直接输入序列1（如 ACGTACGT）")
    parser.add_argument("--seq2-str", default="", help="直接输入序列2（如 ACGTACGT）")
    parser.add_argument("--interactive", action="store_true", help="交互式手动输入两条序列")
    parser.add_argument("--out", default="output", help="输出目录")
    args = parser.parse_args()

    seq1, seq2 = resolve_sequences(args)

    score_matrix, trace_matrix, max_pos, max_score = smith_waterman(seq1, seq2, DEFAULT_SCORING)
    aln_result = traceback_local(seq1, seq2, score_matrix, trace_matrix, max_pos, max_score)
    sim_result = calculate_similarity(aln_result)
    var_result = detect_variations(aln_result)

    out_dir = Path(args.out)
    ensure_dir(out_dir)

    alignment_text = format_alignment_result(aln_result, sim_result)
    variation_text = format_variations(var_result)

    save_text(out_dir / "alignment_result.txt", alignment_text)
    save_text(out_dir / "variation_result.txt", variation_text)
    save_matrix_csv(out_dir / "score_matrix.csv", score_matrix)

    heatmap_ok = plot_score_matrix(score_matrix, str(out_dir / "score_matrix.png"))

    print(alignment_text)
    print("\n" + "=" * 40 + "\n")
    print(variation_text)

    print("\n输出文件已生成：")
    print(f"- {out_dir / 'alignment_result.txt'}")
    print(f"- {out_dir / 'variation_result.txt'}")
    print(f"- {out_dir / 'score_matrix.csv'}")
    if heatmap_ok:
        print(f"- {out_dir / 'score_matrix.png'}")


if __name__ == "__main__":
    main()
