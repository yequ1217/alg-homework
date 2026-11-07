import time


def power2n_1(n):
    return 2 ** n


def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)


def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)


def power2n_3(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 0:
        return 1
    memo[n] = power2n_3(n - 1, memo) + power2n_3(n - 1, memo)
    return memo[n]


def timed(name, func, n):
    start = time.perf_counter()
    value = func(n)
    elapsed = time.perf_counter() - start
    print(f"{name:<28} n={n:<3} 耗時 {elapsed:>10.6f} 秒  位數 {len(str(value))}")
    return value, elapsed


def main():
    print("== 四種 power2n 實作比較 ==")
    print("1. 內建指數        2. 遞迴 T(n)=2T(n-1)    3. 遞迴 T(n)=2*T(n-1)    4. 遞迴+查表\n")

    small = 20
    print(f"-- n = {small}（全部方法都可跑）--")
    values = []
    values.append(timed("方法 1：2 ** n", power2n_1, small)[0])
    values.append(timed("方法 2a：T(n-1)+T(n-1)", power2n_2a, small)[0])
    values.append(timed("方法 2b：2*T(n-1)", power2n_2b, small)[0])
    values.append(timed("方法 3：遞迴+查表", power2n_3, small)[0])
    print("四種結果一致:", len(set(values)) == 1, "\n")

    large = 100
    print(f"-- n = {large}（題目要求的測試值）--")
    v1 = timed("方法 1：2 ** n", power2n_1, large)[0]
    v2 = timed("方法 2b：2*T(n-1)", power2n_2b, large)[0]
    v3 = timed("方法 3：遞迴+查表", power2n_3, large)[0]
    print("方法 2a 在 n = 100 時需要約 2^100 次呼叫，實際上跑不出來，故略過。")
    print("結果一致:", v1 == v2 == v3)


if __name__ == "__main__":
    main()
