"""序列清洗与合法性校验。"""

from config import VALID_BASES


def clean_sequence(raw_text: str) -> str:
    """清洗原始序列文本：去空白、转大写。"""
    # 移除 UTF-8 BOM，避免被识别为非法碱基字符
    raw_text = raw_text.replace("\ufeff", "")
    return "".join(raw_text.split()).upper()


def validate_sequence(sequence: str) -> None:
    """校验序列仅包含合法碱基字符。"""
    if not sequence:
        raise ValueError("序列为空，请检查输入文件。")

    illegal = sorted(set(sequence) - VALID_BASES)
    if illegal:
        raise ValueError(f"发现非法字符: {illegal}，仅允许 {sorted(VALID_BASES)}")
