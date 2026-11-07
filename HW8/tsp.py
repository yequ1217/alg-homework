import math
import random
import time


def distance_matrix(points):
    return [[math.dist(p, q) for q in points] for p in points]


def tour_length(tour, dist):
    n = len(tour)
    return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))


def two_opt(tour, i, j):
    return tour[:i + 1] + list(reversed(tour[i + 1:j + 1])) + tour[j + 1:]


def delta_two_opt(tour, i, j, dist):
    n = len(tour)
    a, b = tour[i], tour[(i + 1) % n]
    c, d = tour[j], tour[(j + 1) % n]
    return dist[a][c] + dist[b][d] - dist[a][b] - dist[c][d]


def greedy(dist, start=0):
    n = len(dist)
    unvisited = set(range(n)) - {start}
    tour = [start]
    current = start
    while unvisited:
        nxt = min(unvisited, key=lambda city: dist[current][city])
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    return tour


def improvement(dist, start=0, max_rounds=100):
    tour = greedy(dist, start)
    n = len(tour)
    for _ in range(max_rounds):
        best_delta, best_move = 0.0, None
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                delta = delta_two_opt(tour, i, j, dist)
                if delta < best_delta:
                    best_delta, best_move = delta, (i, j)
        if best_move is None:
            break
        tour = two_opt(tour, *best_move)
    return tour


def hill_climbing(dist, seed=1, max_iter=5000, max_stall=500):
    rng = random.Random(seed)
    n = len(dist)
    tour = list(range(n))
    rng.shuffle(tour)
    best = tour_length(tour, dist)
    stall = 0
    for _ in range(max_iter):
        i = rng.randint(0, n - 2)
        j = rng.randint(i + 1, n - 1)
        candidate = two_opt(tour, i, j)
        length = tour_length(candidate, dist)
        if length < best:
            tour, best, stall = candidate, length, 0
        else:
            stall += 1
            if stall >= max_stall:
                break
    return tour


def simulated_annealing(dist, seed=1, max_iter=20000, t0=100.0, alpha=0.9995):
    rng = random.Random(seed)
    n = len(dist)
    tour = list(range(n))
    rng.shuffle(tour)
    current = tour_length(tour, dist)
    best_tour, best = tour[:], current
    temp = t0
    for _ in range(max_iter):
        i = rng.randint(0, n - 2)
        j = rng.randint(i + 1, n - 1)
        delta = delta_two_opt(tour, i, j, dist)
        if delta < 0 or rng.random() < math.exp(-delta / temp):
            tour = two_opt(tour, i, j)
            current += delta
            if current < best:
                best_tour, best = tour[:], current
        temp *= alpha
        if temp < 1e-3:
            break
    return best_tour


def gradient_descent(dist, seed=1, max_iter=1000):
    rng = random.Random(seed)
    n = len(dist)
    tour = list(range(n))
    rng.shuffle(tour)
    for _ in range(max_iter):
        best_delta, best_move = 0.0, None
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                delta = delta_two_opt(tour, i, j, dist)
                if delta < best_delta:
                    best_delta, best_move = delta, (i, j)
        if best_move is None:
            break
        tour = two_opt(tour, *best_move)
    return tour


def run(name, func, dist, **kwargs):
    start = time.perf_counter()
    tour = func(dist, **kwargs) if kwargs else func(dist)
    elapsed = time.perf_counter() - start
    return name, tour, tour_length(tour, dist), elapsed


def main():
    random.seed(42)
    n = 15
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
    dist = distance_matrix(points)

    print(f"城市數: {n}")
    print("座標:", [(round(x, 1), round(y, 1)) for x, y in points])
    print()

    results = [
        run("貪婪法 (Nearest Neighbor)", greedy, dist),
        run("改良法 (Greedy + 2-opt)", improvement, dist),
        run("爬山演算法", hill_climbing, dist, seed=1),
        run("模擬退火法", simulated_annealing, dist, seed=1),
        run("梯度下降法 (最陡 2-opt)", gradient_descent, dist, seed=1),
    ]

    print(f"{'方法':<28} | {'路徑長度':>12} | {'耗時(秒)':>10}")
    print("-" * 60)
    best = min(results, key=lambda r: r[2])
    for name, tour, length, elapsed in results:
        mark = "  <-- 最佳" if (name, tour, length, elapsed) == best else ""
        print(f"{name:<28} | {length:>12.4f} | {elapsed:>10.6f}{mark}")

    print("\n最佳路徑:", best[1])
    print("最佳長度:", round(best[2], 4))


if __name__ == "__main__":
    main()
