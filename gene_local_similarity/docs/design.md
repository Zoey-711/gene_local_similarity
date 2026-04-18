# 课程设计说明书草稿

## 1. 课题背景
基因序列比对是生物信息学中的核心问题之一，可用于同源分析、功能预测、变异检测等。

## 2. 功能需求
- 读取并校验 DNA 序列（A/C/G/T/N）
- 计算局部最优比对（Smith-Waterman）
- 输出比对结果与相似度指标
- 分析 SNP / INS / DEL 变异位点
- 导出得分矩阵用于展示与答辩说明

## 3. 数据结构设计
- 二维数组：保存动态规划得分矩阵 `score_matrix`
- 二维数组：保存回溯方向矩阵 `trace_matrix`
- 数据类：`AlignmentResult` 保存比对结果，`Variation` 保存变异信息

## 4. 算法复杂度
- 时间复杂度：`O(mn)`
- 空间复杂度：`O(mn)`
其中 `m`、`n` 分别为两条序列长度。

## 5. 模块划分
- `preprocess.py`：清洗与合法性校验
- `alignment.py`：动态规划求解
- `traceback.py`：最优路径回溯
- `similarity.py`：相似度统计
- `variation.py`：变异检测
- `visualization.py`：可视化输出

## 6. 可扩展方向
- 支持 FASTA 文件解析
- 支持 affine gap penalty
- 支持多条序列批处理比对
