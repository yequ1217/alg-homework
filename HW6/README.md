# HW6 - Lambda Calculus 解譯器

## Lambda Calculus 簡介

語法只有三種形式：

```text
e ::= x           變數
    | λx. e       函數抽象（lambda）
    | e1 e2       函數應用（application）
```

計算規則只有 beta 化簡：

```text
(λx. e) a  ->  e[x := a]
```

也就是把函數 body 中的 `x` 全部換成參數 `a`。

## 解譯器結構

`lambda_calc.py` 包含以下部分：

| 元件 | 功能 |
| --- | --- |
| `tokenize` / `Parser` | 解析 `\x.x`、`λx.x`、`f x`、括號等語法 |
| `Var` / `Lam` / `App` | 用 dataclass 表示三種 term |
| `free_vars` | 計算自由變數 |
| `substitute` | 捕獲避免（capture-avoiding）的代換 |
| `reduce_step` | 做一次 beta 化簡 |
| `normalize` | 反覆化簡直到正規形式，並保留每一步 |
| `show` | 將 term 印成可讀的 lambda 語法 |

### 捕獲避免的代換

直接代換可能發生變數被捕獲的問題，例如：

```text
(λx. λy. x) y  ->  λy. y   （錯誤）
```

正確結果應該保留自由變數 `y`。程式在遇到參數名稱和傳入值的自由變數衝突時，會先把內層參數改名（alpha 轉換），再做代換。

### 化簡策略

採用 **normal order**（最左最外優先）：

1. 若目前是 application 且函數部分是 lambda，直接 beta 化簡。
2. 否則先化簡函數部分，再化簡參數部分。
3. lambda body 內部也遞迴化簡。

每一步都會存進 trace，因此可以完整顯示計算過程。

## 內建範例

| 範例 | 內容 |
| --- | --- |
| Identity | `(λx.x) y` |
| K | `(λx.λy.x) a b` |
| Church 後繼 | `succ 1`、`succ 2` |
| Church 加法 | `plus 2 3` |
| 布林 AND | `and true false`、`and true true` |

Church numerals 的定義：

```text
0 = λf.λx.x
1 = λf.λx.f x
2 = λf.λx.f (f x)
succ = λn.λf.λx.f (n f x)
plus = λm.λn.λf.λx.m f (n f x)
true  = λx.λy.x
false = λx.λy.y
and   = λp.λq.p q p
```

## 限制

- 只實作 beta 化簡，沒有實作 eta 化簡。
- 使用具名變數，代換時以 alpha 改名避免捕獲；沒有使用 de Bruijn index。
- 有最大步數限制（預設 500 步），避免某些 term 無限展開。
- 沒有型別系統，是非型別（untyped）lambda calculus。
