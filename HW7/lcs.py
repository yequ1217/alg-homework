import time
from functools import lru_cache


def lcs_recursive(a, b):
    if not a or not b:
        return 0
    if a[-1] == b[-1]:
        return 1 + lcs_recursive(a[:-1], b[:-1])
    return max(lcs_recursive(a[:-1], b), lcs_recursive(a, b[:-1]))


@lru_cache(maxsize=None)
def _lcs_memo(a, b, i, j):
    if i == 0 or j == 0:
        return 0
    if a[i - 1] == b[j - 1]:
        return 1 + _lcs_memo(a, b, i - 1, j - 1)
    return max(_lcs_memo(a, b, i - 1, j), _lcs_memo(a, b, i, j - 1))


def lcs_memo(a, b):
    return _lcs_memo(a, b, len(a), len(b))


def lcs_dp(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i, j, chars = m, n, []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], "".join(reversed(chars)), dp


def diff_marks(a, b):
    _, common, _ = lcs_dp(a, b)
    marks = [" "] * len(a)
    pos = 0
    for index, ch in enumerate(a):
        if pos < len(common) and ch == common[pos]:
            marks[index] = "="
            pos += 1
        else:
            marks[index] = "-"
    return "".join(marks), common


def show_table(a, b, dp):
    print("    " + "  ".join([""] + list(b)))
    for i in range(len(a) + 1):
        row = " ".join(f"{v:>2}" for v in dp[i])
        left = " " if i == 0 else a[i - 1]
        print(f"{left:>2}  {row}")


def timed(name, func, *args):
    start = time.perf_counter()
    value = func(*args)
    elapsed = time.perf_counter() - start
    print(f"{name:<22} 耗時 {elapsed:>9.6f} 秒")
    return value


def main():
    a, b = "AGGTAB", "GXTXAYB"
    print("== 文字差異比對：以 LCS 為基礎 ==")
    print(f"A = {a}")
    print(f"B = {b}\n")

    print("LCS 長度:")
    print("  暴力遞迴   :", lcs_recursive(a, b))
    print("  記憶化遞迴 :", lcs_memo(a, b))
    length, common, dp = lcs_dp(a, b)
    print("  動態規劃   :", length)
    print(f"  其中一組 LCS = {common!r}\n")

    print("DP 表格:")
    show_table(a, b, dp)
    print()
    marks, common = diff_marks(a, b)
    print("A :", a)
    print("    ", marks)
    print("B :", b)
    print(f"相同字元: {common!r}\n")

    print("== 效能比較 ==")
    small_a = "abcdefghij" + "k" * 2
    small_b = "jihgfedcba" + "k" * 2
    timed("暴力遞迴 (n=12)", lcs_recursive, small_a, small_b)
    timed("記憶化遞迴 (n=12)", lcs_memo, small_a, small_b)
    timed("動態規劃 (n=12)", lambda x, y: lcs_dp(x, y)[0], small_a, small_b)

    big_a = "ACGT" * 250
    big_b = "TGCA" * 250
    timed("動態規劃 (n=1000)", lambda x, y: lcs_dp(x, y)[0], big_a, big_b)
    print("暴力遞迴在 n=1000 時需要指數時間，無法實際執行。")


if __name__ == "__main__":
    main()
