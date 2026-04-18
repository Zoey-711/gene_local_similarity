"""比对结果可视化。"""

from pathlib import Path


def plot_score_matrix(score_matrix: list[list[int]], save_path: str) -> bool:
    """保存得分矩阵热力图；若 matplotlib 不可用则返回 False。"""
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return False

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.imshow(score_matrix, aspect="auto")
    plt.colorbar(label="Score")
    plt.title("Smith-Waterman Score Matrix")
    plt.xlabel("Sequence 2 Index")
    plt.ylabel("Sequence 1 Index")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    return True
