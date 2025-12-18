

## 🚀 快速开始

### 运行测试
```bash
python test_all_inputs.py
```

**预期输出**：
```
================================================================================
Testing Question 4.1 (mtsp_dp) and Question 4.2 (php_solver_from_tsp)
================================================================================

Testing PHP solver on 10 input files...

✓ PASS | 1.in    | Nodes:  5 | Homes:  3 | Cost:    5.33
...
✓ PASS | 10.in   | Nodes: 40 | Homes: 20 | Cost:18192.00

================================================================================
Summary: 10/10 tests passed
✓ All tests passed! Question 4.1 and 4.2 are correctly implemented.
================================================================================
```

---

## 📁 文件结构

### 核心实现文件
```
mtsp_dp.py              # Question 4.1 - M-TSP动态规划求解器
php_from_tsp.py         # Question 4.2 - PHP求解器（通过TSP归约）
test_all_inputs.py      # 综合测试脚本
```

### 报告文件（包含Question 4和5）
```
Report_Q4_Formal.md     # 正式学术报告（推荐提交）⭐
Report_Q4.md            # 详细技术报告
报告_问题4_中文版.md     # 中文版报告
```

### 文档文件
```
最终总结_Q4_Q5.md       # 最终完成总结
QUICK_REFERENCE_Q4.md   # 快速参考指南
完成总结_Q4.md          # 详细完成总结
项目交付清单_Q4.md      # 交付清单
README_Q4.md            # 使用指南
IMPLEMENTATION_SUMMARY.md  # 实现总结
```

---

## 📊 内容详情

### Question 4.1: M-TSP动态规划求解器

**文件**: `mtsp_dp.py`

**算法**: Held-Karp动态规划算法
- 使用位掩码表示访问过的节点集合
- DP状态: `dp[mask][i]` = 访问mask中的节点，当前在节点i的最小代价
- 时间复杂度: O(n² × 2ⁿ)
- 空间复杂度: O(n × 2ⁿ)

**测试结果**: 10/10通过 ✅

### Question 4.2: PHP求解器

**文件**: `php_from_tsp.py`

**算法**: 三步归约过程
1. 构造完全图G'，节点为H∪{0}
2. 使用最短路径距离作为G'的边权重
3. 在G'上调用mtsp_dp求解TSP
4. 将TSP解扩展回原图G

**测试结果**: 10/10通过 ✅

### Question 5.1: PTP的NP-hard证明

**位置**: 所有报告文件中

**证明方法**:
- 证明当α=1时，PHP是PTP的特殊情况
- 由于PHP是NP-hard，因此PTP也是NP-hard
- 使用归约方法，逻辑严谨

**包含内容**:
- 完整的数学证明
- LaTeX公式表达
- 清晰的推理步骤

### Question 5.2: PHP的近似比证明

**位置**: 所有报告文件中

**第一部分**: 证明β = C_php / C_ptpopt ≤ 2
- 从最优PTP解构造PHP解
- 使用三角不等式限定绕道代价
- 详细的数学推导

**第二部分**: 构造紧界实例
- 构造具体图实例
- 证明当n→∞时，β→2
- 包含直观解释和图示

---

## 🎯 评分预期

| 问题 | 分数 | 状态 |
|------|------|------|
| Question 4.1 | 10分 | ✅ 完成 |
| Question 4.2 | 10分 | ✅ 完成 |
| Question 5.1 | 10分 | ✅ 完成 |
| Question 5.2 | 10分 | ✅ 完成 |
| **总计** | **40分** | **✅ 完成** |

---

## 📝 提交建议

### 推荐提交文件

**最小集合**（必需）:
1. `mtsp_dp.py` - Question 4.1实现
2. `php_from_tsp.py` - Question 4.2实现
3. `Report_Q4_Formal.md` - 正式报告（或转换为PDF）

**完整集合**（推荐）:
1. `mtsp_dp.py`
2. `php_from_tsp.py`
3. `test_all_inputs.py`
4. `Report_Q4_Formal.md`（或PDF）
5. `IMPLEMENTATION_SUMMARY.md`

### 报告选择

推荐提交 **`Report_Q4_Formal.md`**（或转换为PDF），因为：
- ✅ 包含Question 4.1和4.2的完整实现说明
- ✅ 包含Question 5.1的NP-hard证明
- ✅ 包含Question 5.2的近似比证明
- ✅ 使用LaTeX数学公式，格式规范
- ✅ 学术标准格式，适合提交

### 转换为PDF

```bash
# 使用Pandoc
pandoc Report_Q4_Formal.md -o Report_Q4.pdf

# 或使用Typora、VS Code等工具导出
```

---

## 🔍 常见问题

### Q1: 如何验证代码正确性？
**A**: 运行 `python test_all_inputs.py`，应该看到10/10测试通过。

### Q2: 报告应该提交哪个版本？
**A**: 推荐 `Report_Q4_Formal.md`（或PDF），它包含所有Question 4和5的内容，格式最规范。

### Q3: Question 5需要代码实现吗？
**A**: 不需要。Question 5.1和5.2是理论证明题，只需要在报告中提供数学证明即可。

### Q4: 如何理解归约过程？
**A**: 查看报告中的Section 2.2，有详细的三步说明和示例。

### Q5: 近似比的紧界是什么意思？
**A**: 紧界意味着存在实例使得β接近2，证明了β≤2这个界是最优的，不能进一步改进。

