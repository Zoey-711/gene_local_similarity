# 基因序列局部相似度检测与变异位点分析

本项目用于数据结构与算法课程设计，核心算法采用 **Smith-Waterman** 动态规划进行局部序列比对，并支持：

- 局部最优片段检测
- 相似度统计（Identity、Gap Ratio）
- 变异位点分析（SNP、插入 INS、缺失 DEL）
- 得分矩阵导出（CSV）与热力图可视化（PNG）

## 项目结构

```text
gene_local_similarity/
├── main.py
├── config.py
├── README.md
├── requirements.txt
├── data/
├── src/
├── output/
└── docs/
```

## 运行方式

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 进入项目目录并运行：

```bash
python main.py
```

或指定输入输出路径：

```bash
python main.py --seq1 data/sample_seq1.txt --seq2 data/sample_seq2.txt --out output

或直接在命令行输入序列：

```bash
python main.py --seq1-str ACCGTATGCTAG --seq2-str TTTGTATGATAG
```

或使用交互模式手动输入：

```bash
python main.py --interactive
```
```

## 输出结果

- `output/alignment_result.txt`：局部比对结果与相似度统计
- `output/variation_result.txt`：变异位点分析结果
- `output/score_matrix.csv`：动态规划得分矩阵
- `output/score_matrix.png`：得分矩阵热力图（可选）

## 算法说明（简要）

- 状态定义：`dp[i][j]` 表示以 `seq1[i]` 与 `seq2[j]` 结尾的局部比对最优得分。
- 转移方程：

```text
dp[i][j] = max(
    0,
    dp[i-1][j-1] + (match / mismatch),
    dp[i-1][j] + gap,
    dp[i][j-1] + gap
)
```

- 当得分为 0 时停止回溯，得到一条局部最优对齐路径。
