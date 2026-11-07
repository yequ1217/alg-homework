# HW3 - 列舉真值表解決 SAT 問題

- 題目: [作業.md](作業.md)
- 原始 issue: https://github.com/ccc115a/_alg/issues/5
- 程式: [sat.py](sat.py)
- 狀態: 已完成

## 題目重點

寫一個程式，系統性地列舉真值表來解決 SAT（布林可滿足性）問題。

## 原理

SAT 問題是問：是否存在一組變數的 `True / False` 指派，讓整個布林表示式為真。

暴力法的做法：

1. 從表示式中找出所有變數，假設有 `n` 個。
2. 用 `itertools.product([False, True], repeat=n)` 列舉全部 `2^n` 種指派。
3. 每種指派都代入表示式求值。
4. 收集所有使結果為 `True` 的指派；若一組都沒有，就是 UNSAT。

為了安全與正確性，程式用 Python 的 `ast` 模組先檢查語法，只允許：

- 變數（`Name`）
- 布林常數（`True` / `False`）
- `and`、`or`、`not`

不允許函式呼叫、算術或其他語法。

## 複雜度

- 時間：`O(2^n * m)`，其中 `n` 是變數個數、`m` 是表示式大小
- 空間：`O(n + m)`（不計輸出）

這是指數演算法，變數一多就會爆掉；實務上會用 DPLL、CDCL 等更聰明的方法。

## 執行方式

```powershell
python sat.py
```

## 執行結果（節錄）

第一個表示式 `(a or b) and (not a or c) and (not b or not c)`：

```text
a | b | c | 結果
--------------
F | F | F | F
F | F | T | F
F | T | F | T
F | T | T | F
T | F | F | F
T | F | T | T
T | T | F | F
T | T | T | F

變數個數 3，暴力列舉 8 種組合
可滿足，共 2 組解：
  a=F, b=T, c=F
  a=T, b=F, c=T
```

`a and not a`：

```text
不可滿足 (UNSAT)
```

`(a or not a) and (b or not b)`：

```text
可滿足，共 4 組解
```

## 結論

- 真值表列舉可以完整判斷 SAT，不會漏解，也保證能找到所有解。
- 代價是指數時間 `O(2^n)`；本題的三個例子分別用了 8、2、4 種組合。
- 若變數數量很大，需要改用 DPLL 或 CDCL 等演算法。
