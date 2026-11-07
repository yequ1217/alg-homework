# HW7 - 動態規劃與文字算法：LCS / diff

- 題目: [作業.md](作業.md)
- 原始 issue: https://github.com/ccc115a/_alg/issues/11
- 程式: [lcs.py](lcs.py)
- 狀態: 已完成

## 題目重點

找一個文字類型的問題，分別用「動態規劃」與「非動態規劃」解決，並說明兩者的原理、複雜度與比較。

本作業選擇 **最長共同子序列（Longest Common Subsequence, LCS）**，它是 `diff` 檔案比對的核心。

## 問題定義

給兩個字串 `A`、`B`，找出最長的子序列（不要求連續），使其同時出現在兩者中。

例如：

```text
A = AGGTAB
B = GXTXAYB
LCS = GTAB（長度 4）
```

## 方法一：暴力遞迴（非動態規劃）

比較兩字串最後一個字元：

- 若相同：`1 + LCS(A[:-1], B[:-1])`
- 若不同：`max(LCS(A[:-1], B), LCS(A, B[:-1]))`
- 任一字串為空：回傳 0

```python
def lcs_recursive(a, b):
    if not a or not b:
        return 0
    if a[-1] == b[-1]:
        return 1 + lcs_recursive(a[:-1], b[:-1])
    return max(lcs_recursive(a[:-1], b), lcs_recursive(a, b[:-1]))
```

問題是同樣的子問題會被重複計算，時間複雜度為指數 `O(2^(m+n))`。

## 方法二：記憶化遞迴（top-down DP）

把算過的 `(i, j)` 存進快取，避免重複計算：

```python
@lru_cache(maxsize=None)
def _lcs_memo(a, b, i, j):
    ...
```

時間降為 `O(mn)`，空間為 `O(mn)`。

## 方法三：動態規劃（bottom-up DP）

定義 `dp[i][j]` 為 `A[:i]` 與 `B[:j]` 的 LCS 長度：

```text
dp[0][j] = dp[i][0] = 0
若 A[i-1] == B[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
否則:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

再從 `dp[m][n]` 往回追蹤，就能还原出一組 LCS。

- 時間：`O(mn)`
- 空間：`O(mn)`（可再優化成 `O(n)`，但無法輕易还原字串）

## 執行方式

```powershell
python lcs.py
```

## 執行結果

```text
A = AGGTAB
B = GXTXAYB

LCS 長度:
  暴力遞迴   : 4
  記憶化遞迴 : 4
  動態規劃   : 4
  其中一組 LCS = 'GTAB'

DP 表格:
      G  X  T  X  A  Y  B
     0  0  0  0  0  0  0  0
 A   0  0  0  0  0  1  1  1
 G   0  1  1  1  1  1  1  1
 G   0  1  1  1  1  1  1  1
 T   0  1  1  2  2  2  2  2
 A   0  1  1  2  2  3  3  3
 B   0  1  1  2  2  3  3  4

A : AGGTAB
     -=-===
B : GXTXAYB
相同字元: 'GTAB'
```

效能比較（n 為字串長度）：

```text
暴力遞迴 (n=12)            耗時  0.012577 秒
記憶化遞迴 (n=12)           耗時  0.000059 秒
動態規劃 (n=12)            耗時  0.000037 秒
動態規劃 (n=1000)          耗時  0.204151 秒
暴力遞迴在 n=1000 時需要指數時間，無法實際執行。
```

## 比較

| 方法 | 時間複雜度 | 空間複雜度 | 特點 |
| --- | --- | --- | --- |
| 暴力遞迴 | O(2^(m+n)) | O(m+n) | 寫法直觀，但大量重複計算 |
| 記憶化遞迴 | O(mn) | O(mn) | top-down，只算需要的子問題 |
| 動態規劃 | O(mn) | O(mn) | bottom-up，可用表格追溯解答 |

## 與 diff 的關係

`diff` 想找出兩個檔案「哪些地方相同、哪些地方不同」。常見做法是先用 LCS 找出共同部分，沒被對上的字元就標成刪除或新增。本程式用 `diff_marks` 示範：`=` 代表在 LCS 中，`-` 代表沒有對上。

## 心得

- 動態規劃的關鍵是「定義狀態」與「轉移式」；LCS 的狀態就是兩個前綴的長度。
- 記憶化與 bottom-up DP 都是同一個遞迴式的實作，只是一個由需求驅動、一個由小到大填表。
- 能把 `O(2^(m+n))` 降到 `O(mn)`，是動態規劃最明顯的價值。
