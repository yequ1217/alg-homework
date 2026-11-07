# HW4 - 迭代法與通用迭代框架

- 題目: [作業.md](作業.md)
- 原始 issue: https://github.com/ccc115a/_alg/issues/6
- 程式: [iterative.py](iterative.py)
- 狀態: 已完成

## 題目重點

1. 用迭代法求解一個自訂問題。
2. 讀懂課程的 `iter_framework.py`，並寫一篇說明文件。

## 核心：通用迭代框架

課程的 `iter_framework.py` 把「迭代法」抽象成同一個函式：

```python
def generic_iterator(transition_func, is_converged, initial_state, max_iter=1000):
    state = initial_state
    for iteration in range(max_iter):
        next_state = transition_func(state)
        if is_converged(state, next_state, iteration):
            return next_state, iteration + 1
        state = next_state
    return state, max_iter
```

三個關鍵輸入：

| 參數 | 意義 |
| --- | --- |
| `transition_func(state)` | 如何從目前狀態算出下一個狀態 |
| `is_converged(old, new, iteration)` | 何時停止（收斂條件） |
| `initial_state` | 起始值 |

只要換掉這三個函式，就能描述各種不同的迭代法：

| 迭代法 | transition | 收斂條件 |
| --- | --- | --- |
| 不動點迭代 | `x -> g(x)` | `abs(new-old) < eps` |
| 牛頓法 | `x -> x - f(x)/f'(x)` | `abs(new-old) < eps` |
| 高斯-賽得爾法 | 逐條更新線性方程組 | 最大誤差 `< eps` |
| 冪次迭代 | `v -> A v / ||A v||` | 向量變化量 `< eps` |
| QR 演算法 | `A -> RQ` | 非對角線元素趨近 0 |
| RK4（解 ODE） | 用四個斜率推進 | 抵達終點時間 |
| PageRank | `r -> G r` | 向量變化量 `< eps` |
| K-means | E-step + M-step | 中心點不再移動 |
| EM 演算法 | E-step + M-step | 參數變化量 `< eps` |

課程版本使用 NumPy，本作業的 `iterative.py` 則用純 Python 實作同樣框架，並示範其中五種：

1. 不動點迭代：解 `x = cos(x)`
2. 牛頓法：解 `x^2 - 2 = 0`
3. 高斯-賽得爾法：解 3×3 線性方程組
4. 冪次迭代：求最大特徵值
5. PageRank：求網頁權重

## 迭代法 v.s. 遞迴

- **迭代法**：用迴圈反覆更新狀態，通常空間固定，不會有遞迴堆疊過深的問題。
- **遞迴**：把大問題拆成小問題，程式碼直觀，但可能重複計算、佔用堆疊。
- 兩者可以互相轉換；本質差別在於「狀態如何前進」與「何時停止」。

## 執行方式

```powershell
python iterative.py
```

## 執行結果

```text
--- 1. 不動點迭代：x = cos(x) ---
x = 0.739085133215，迭代 69 次
驗證 cos(x) = 0.739085133215

--- 2. 牛頓法：求 x^2 - 2 = 0 ---
x = 1.414213562373095，迭代 6 次
驗證 x^2 = 2.000000000000000

--- 3. 高斯-賽得爾法：解線性方程組 ---
x = [2.25, 2.0, 3.75]，迭代 14 次
驗證 Ax = [7.0, 2.0, 13.0]

--- 4. 冪次迭代：最大特徵值 ---
主特徵向量 = [0.838865, 0.509521, 0.191557]
最大特徵值 = 4.721570，迭代 38 次

--- 5. PageRank：隨機衝浪者模型 ---
PageRank = [0.324561, 0.225146, 0.225146, 0.225146]，迭代 31 次
```

## 心得

- 迭代法的重點是「收斂」：初始值、步進函式、停止條件都會影響結果與速度。
- 牛頓法收斂很快（6 次），不動點迭代較慢（69 次），但兩者用同一個框架就能表達。
- 把流程抽象成 `generic_iterator` 後，程式重複度大幅降低，也更容易比較不同演算法。
