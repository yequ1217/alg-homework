import math


def rec1(n):
    if n == 1:
        return 1
    return rec1(n - 1) + 8


def closed1(n):
    return 8 * n - 7


def rec2(n):
    if n == 1:
        return 1
    return 2 * rec2(n - 1) + 9


def closed2(n):
    return 5 * (2 ** n) - 9


def rec3(n):
    if n == 1:
        return 1
    return 2 * rec3(n // 2) + 1


def closed3(n):
    return 2 * n - 1


def rec4(n):
    if n == 1:
        return 1
    return rec4(n // 2) + 1


def closed4(n):
    return int(1 + math.log2(n))


def check(label, rec, closed, ns):
    print(f"\n{label}")
    print(f"{'n':>8} | {'遞迴值':>12} | {'公式值':>12} | {'一致':>4}")
    print("-" * 46)
    ok = True
    for n in ns:
        r, c = rec(n), closed(n)
        same = r == c
        ok = ok and same
        print(f"{n:>8} | {r:>12} | {c:>12} | {'是' if same else '否':>4}")
    return ok


def main():
    print("== 四條遞迴方程式的精確解與 Big O ==")

    check("1. T(n) = T(n-1) + 8, T(1) = 1",
          rec1, closed1, [1, 2, 5, 10, 20])
    print("   解：T(n) = 1 + 8(n-1) = 8n - 7  =>  Θ(n)")

    check("2. T(n) = 2T(n-1) + 9, T(1) = 1",
          rec2, closed2, [1, 2, 5, 10, 20])
    print("   解：T(n) = 5 * 2^n - 9  =>  Θ(2^n)")

    check("3. T(n) = 2T(n/2) + 1, T(1) = 1",
          rec3, closed3, [1, 2, 4, 8, 16, 32])
    print("   解：T(n) = 2n - 1  =>  Θ(n)")

    check("4. T(n) = T(n/2) + 1, T(1) = 1",
          rec4, closed4, [1, 2, 4, 8, 16, 32])
    print("   解：T(n) = 1 + log2(n)  =>  Θ(log n)")


if __name__ == "__main__":
    main()
