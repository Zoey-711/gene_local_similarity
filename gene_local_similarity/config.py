"""项目全局配置。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringConfig:
    """Smith-Waterman 计分参数。"""

    match: int = 2
    mismatch: int = -1
    gap: int = -2


# 默认计分参数
DEFAULT_SCORING = ScoringConfig()

# 合法碱基字符集合
VALID_BASES = {"A", "C", "G", "T", "N"}
