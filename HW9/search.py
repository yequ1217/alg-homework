import heapq
import itertools
from collections import deque

DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def reconstruct(parent, start, goal):
    if goal not in parent:
        return None
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def neighbors(grid, node):
    r, c = node
    for dr, dc in DIRS4:
        nr, nc = r + dr, c + dc
        if in_bounds(grid, nr, nc) and grid[nr][nc] == 0:
            yield nr, nc


def dfs_path(grid, start, goal):
    stack = [start]
    parent = {start: None}
    while stack:
        current = stack.pop()
        if current == goal:
            return reconstruct(parent, start, goal)
        for nxt in neighbors(grid, current):
            if nxt not in parent:
                parent[nxt] = current
                stack.append(nxt)
    return None


def bfs_path(grid, start, goal):
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct(parent, start, goal)
        for nxt in neighbors(grid, current):
            if nxt not in parent:
                parent[nxt] = current
                queue.append(nxt)
    return None


def astar_path(grid, start, goal):
    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    counter = itertools.count()
    open_heap = [(heuristic(start), 0, next(counter), start)]
    parent = {start: None}
    g_score = {start: 0}
    while open_heap:
        _, g, _, current = heapq.heappop(open_heap)
        if current == goal:
            return reconstruct(parent, start, goal)
        if g > g_score.get(current, float("inf")):
            continue
        for nxt in neighbors(grid, current):
            new_g = g + 1
            if new_g < g_score.get(nxt, float("inf")):
                g_score[nxt] = new_g
                parent[nxt] = current
                f = new_g + heuristic(nxt)
                heapq.heappush(open_heap, (f, new_g, next(counter), nxt))
    return None


def render(grid, marks):
    lines = []
    for r, row in enumerate(grid):
        cells = []
        for c, value in enumerate(row):
            if (r, c) in marks:
                cells.append(marks[(r, c)])
            elif value == 1:
                cells.append("#")
            else:
                cells.append(".")
        lines.append("".join(cells))
    return "\n".join(lines)


def path_marks(path, grid, start, goal, path_char="*"):
    marks = {node: path_char for node in path if node not in (start, goal)}
    marks[start] = "S"
    marks[goal] = "G"
    return marks


def demo_maze():
    print("=" * 60)
    print("1. 老鼠走迷宮 (DFS)")
    grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
    ]
    start, goal = (0, 0), (4, 4)
    path = dfs_path(grid, start, goal)
    print(f"路徑長度: {len(path) if path else 0}，路徑: {path}")
    print(render(grid, path_marks(path, grid, start, goal)))
    print()


def demo_wolf_goat_cabbage():
    print("=" * 60)
    print("2. 狼、羊、甘藍菜過河 (BFS)")
    start = (0, 0, 0, 0)
    goal = (1, 1, 1, 1)
    names = {1: "狼", 2: "羊", 3: "甘藍菜"}

    def safe(state):
        farmer, wolf, goat, cabbage = state
        if wolf == goat and farmer != wolf:
            return False
        if goat == cabbage and farmer != goat:
            return False
        return True

    queue = deque([start])
    parent = {start: None}
    action = {}
    while queue:
        state = queue.popleft()
        if state == goal:
            break
        farmer = state[0]
        moves = [(None, None)]
        for index, name in names.items():
            if state[index] == farmer:
                moves.append((index, name))
        for index, name in moves:
            nxt = list(state)
            nxt[0] ^= 1
            if index is not None:
                nxt[index] ^= 1
            nxt = tuple(nxt)
            if nxt in parent or not safe(nxt):
                continue
            parent[nxt] = state
            action[nxt] = (name, farmer)
            queue.append(nxt)

    if goal not in parent:
        print("無解")
        return
    path = reconstruct(parent, start, goal)
    print(f"最少 {len(path) - 1} 趟")
    for step, state in enumerate(path):
        free = ["左岸", "右岸"]
        left = [names[i] for i in names if state[i] == 0]
        right = [names[i] for i in names if state[i] == 1]
        line = f"{step:>2}: 左岸={left or ['空']} 右岸={right or ['空']}"
        if step > 0:
            name, side = action[state]
            what = f"帶{name}" if name else "獨自"
            line += f"   ({what}從{free[side]}到{free[side ^ 1]})"
        print(line)
    print()


def demo_eight_queens():
    print("=" * 60)
    print("3. 八皇后問題 (DFS)")

    def solve(n, find_all=False):
        solutions, cols = [], []

        def safe(row, col):
            for r, c in enumerate(cols):
                if c == col or abs(c - col) == abs(r - row):
                    return False
            return True

        def dfs(row):
            if row == n:
                solutions.append(cols[:])
                return
            for col in range(n):
                if safe(row, col):
                    cols.append(col)
                    dfs(row + 1)
                    cols.pop()
                    if solutions and not find_all:
                        return

        dfs(0)
        return solutions

    first = solve(8)[0]
    board = []
    for r in range(8):
        board.append(" ".join("Q" if first[r] == c else "." for c in range(8)))
    print("第一組解（row -> col）:", first)
    print("\n".join(board))
    print("八皇后總解數:", len(solve(8, find_all=True)))
    print()


def demo_npc_astar():
    print("=" * 60)
    print("4. NPC 搜尋玩家 (A*)")
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 0],
    ]
    start, goal = (0, 0), (7, 7)
    path = astar_path(grid, start, goal)
    print(f"NPC 到玩家的步數: {len(path) - 1 if path else '無路可走'}")
    marks = path_marks(path, grid, start, goal)
    marks[start] = "N"
    marks[goal] = "P"
    print(render(grid, marks))
    print()


def demo_ic_routing():
    print("=" * 60)
    print("5. IC 電路繞線 (BFS / Lee 演算法)")
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    ]
    start, goal = (0, 0), (6, 9)
    path = bfs_path(grid, start, goal)
    print(f"繞線長度: {len(path) - 1 if path else '無法繞線'}")
    marks = path_marks(path, grid, start, goal)
    marks[start] = "A"
    marks[goal] = "B"
    print(render(grid, marks))
    print()


def main():
    demo_maze()
    demo_wolf_goat_cabbage()
    demo_eight_queens()
    demo_npc_astar()
    demo_ic_routing()


if __name__ == "__main__":
    main()
