import math


def generic_iterator(transition, is_converged, initial_state, max_iter=1000):
    state = initial_state
    for iteration in range(max_iter):
        next_state = transition(state)
        if is_converged(state, next_state, iteration):
            return next_state, iteration + 1
        state = next_state
    print("  [警告] 達到最大迭代次數仍未收斂")
    return state, max_iter


def mat_vec(A, v):
    return [sum(a * b for a, b in zip(row, v)) for row in A]


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def demo_fixed_point():
    print("--- 1. 不動點迭代：x = cos(x) ---")
    result, iters = generic_iterator(
        math.cos,
        lambda old, new, i: abs(new - old) < 1e-12,
        1.0,
    )
    print(f"x = {result:.12f}，迭代 {iters} 次")
    print(f"驗證 cos(x) = {math.cos(result):.12f}\n")


def demo_newton():
    print("--- 2. 牛頓法：求 x^2 - 2 = 0 ---")
    result, iters = generic_iterator(
        lambda x: (x + 2 / x) / 2,
        lambda old, new, i: abs(new - old) < 1e-15,
        1.0,
    )
    print(f"x = {result:.15f}，迭代 {iters} 次")
    print(f"驗證 x^2 = {result ** 2:.15f}\n")


def demo_gauss_seidel():
    print("--- 3. 高斯-賽得爾法：解線性方程組 ---")
    A = [[4.0, -1.0, 0.0], [-1.0, 4.0, -1.0], [0.0, -1.0, 4.0]]
    b = [7.0, 2.0, 13.0]
    n = len(b)

    def transition(x):
        x_new = x[:]
        for i in range(n):
            s = sum(A[i][j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        return x_new

    result, iters = generic_iterator(
        transition,
        lambda old, new, i: max(abs(a - c) for a, c in zip(new, old)) < 1e-10,
        [0.0] * n,
    )
    print(f"x = {[round(v, 6) for v in result]}，迭代 {iters} 次")
    print(f"驗證 Ax = {[round(v, 6) for v in mat_vec(A, result)]}\n")


def demo_power_iteration():
    print("--- 4. 冪次迭代：最大特徵值 ---")
    A = [[4.0, 1.0, 0.5], [1.0, 3.0, 0.2], [0.5, 0.2, 2.0]]
    v0 = [1.0, 1.0, 1.0]
    v0 = [x / norm(v0) for x in v0]

    def transition(v):
        w = mat_vec(A, v)
        return [x / norm(w) for x in w]

    result, iters = generic_iterator(
        transition,
        lambda old, new, i: norm([a - c for a, c in zip(new, old)]) < 1e-12,
        v0,
    )
    eigenvalue = sum(a * b for a, b in zip(result, mat_vec(A, result)))
    print(f"主特徵向量 = {[round(x, 6) for x in result]}")
    print(f"最大特徵值 = {eigenvalue:.6f}，迭代 {iters} 次\n")


def demo_pagerank():
    print("--- 5. PageRank：隨機衝浪者模型 ---")
    M = [
        [0.0, 0.0, 1.0, 0.5],
        [1 / 3, 0.0, 0.0, 0.5],
        [1 / 3, 0.5, 0.0, 0.0],
        [1 / 3, 0.5, 0.0, 0.0],
    ]
    d = 0.85
    n = len(M)
    G = [[d * M[i][j] + (1 - d) / n for j in range(n)] for i in range(n)]
    r0 = [1 / n] * n

    result, iters = generic_iterator(
        lambda r: mat_vec(G, r),
        lambda old, new, i: norm([a - c for a, c in zip(new, old)]) < 1e-12,
        r0,
    )
    total = sum(result)
    result = [x / total for x in result]
    print(f"PageRank = {[round(x, 6) for x in result]}，迭代 {iters} 次\n")


def main():
    print("== 通用迭代框架示範 ==")
    print("generic_iterator(transition, is_converged, initial_state)\n")
    demo_fixed_point()
    demo_newton()
    demo_gauss_seidel()
    demo_power_iteration()
    demo_pagerank()


if __name__ == "__main__":
    main()
