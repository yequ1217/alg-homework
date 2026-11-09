# ccc115a/_alg 週次習題

來源：https://github.com/ccc115a/_alg/issues （只取 `ccckmit` 發佈的週次習題）

每個資料夾都包含：

- `作業.md`：ccckmit 的原始題目
- `README.md`：解題過程（原理、方法、推導與複雜度）
- `.py`：Python 實作

| 資料夾 | 週次 | 主題 | 程式 | 說明 |
| --- | --- | --- | --- | --- |
| [HW1](HW1/) | 習題1 | 四種 power2n 與效能比較 | [power2n.py](HW1/power2n.py) | [README](HW1/README.md) |
| [HW2](HW2/) | 習題2 | 遞迴方程式求解 | [recurrences.py](HW2/recurrences.py) | [README](HW2/README.md) |
| [HW3](HW3/) | 第三週 | SAT 真值表列舉 | [sat.py](HW3/sat.py) | [README](HW3/README.md) |
| [HW4](HW4/) | 第四週 | 迭代法與通用框架 | [iterative.py](HW4/iterative.py) | [README](HW4/README.md) |
| [HW5](HW5/) | 第五週 | 河內塔、符號微分、無迴圈泡沫排序 | [hw5.py](HW5/hw5.py) | [README](HW5/README.md) |
| [HW6](HW6/) | 第六週 | Lambda Calculus 解譯器 | [lambda_calc.py](HW6/lambda_calc.py) | [README](HW6/README.md) |
| [HW7](HW7/) | 第七週 | LCS 動態規劃 v.s. 遞迴 | [lcs.py](HW7/lcs.py) | [README](HW7/README.md) |
| [HW8](HW8/) | 第8週 | TSP 五種優化方法 | [tsp.py](HW8/tsp.py) | [README](HW8/README.md) |
| [HW9](HW9/) | 第9週 | 五個搜尋演算法問題 | [search.py](HW9/search.py) | [README](HW9/README.md) |

## 執行方式

在根目錄執行任一程式，例如：

```powershell
python HW1\power2n.py
python HW9\search.py
```

## 重新抓取題目

```powershell
python fetch_issues.py
```

`fetch_issues.py` 只會更新各資料夾的 `作業.md`，已存在的 `README.md` 不會被覆蓋。
