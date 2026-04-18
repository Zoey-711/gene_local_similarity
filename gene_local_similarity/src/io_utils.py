"""文件读写与序列加载。"""

from pathlib import Path
from typing import List

from .preprocess import clean_sequence, validate_sequence


def ensure_dir(path: str | Path) -> None:
    """确保目录存在，不存在则递归创建。"""
    Path(path).mkdir(parents=True, exist_ok=True)


def load_sequence(file_path: str | Path) -> str:
    """从文件读取序列，并完成清洗与合法性校验。"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"找不到序列文件: {path}")

    # utf-8-sig 可自动兼容带 BOM 的 UTF-8 文本
    raw_text = path.read_text(encoding="utf-8-sig")
    seq = clean_sequence(raw_text)
    validate_sequence(seq)
    return seq


def save_text(file_path: str | Path, text: str) -> None:
    """保存普通文本结果。"""
    Path(file_path).write_text(text, encoding="utf-8")


def save_matrix_csv(file_path: str | Path, matrix: List[List[int]]) -> None:
    """将动态规划矩阵按 CSV 形式写出，便于表格软件查看。"""
    lines = [",".join(map(str, row)) for row in matrix]
    Path(file_path).write_text("\n".join(lines), encoding="utf-8")
