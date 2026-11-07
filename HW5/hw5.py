import ast


def hanoi_rec(n, src="A", aux="B", dst="C", moves=None):
    if moves is None:
        moves = []
    if n == 1:
        moves.append((src, dst))
    else:
        hanoi_rec(n - 1, src, dst, aux, moves)
        moves.append((src, dst))
        hanoi_rec(n - 1, aux, src, dst, moves)
    return moves


def hanoi_iter(n, src="A", aux="B", dst="C"):
    moves = []
    stack = [(n, src, aux, dst, False)]
    while stack:
        size, a, b, c, expanded = stack.pop()
        if size == 0:
            continue
        if expanded:
            moves.append((a, c))
        else:
            stack.append((size - 1, b, a, c, False))
            stack.append((size, a, b, c, True))
            stack.append((size - 1, a, c, b, False))
    return moves


def conv(node):
    if isinstance(node, ast.Constant):
        return ("num", node.value)
    if isinstance(node, ast.Name):
        return ("var", node.id)
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return ("neg", conv(node.operand))
        if isinstance(node.op, ast.UAdd):
            return conv(node.operand)
    if isinstance(node, ast.BinOp):
        left, right = conv(node.left), conv(node.right)
        if isinstance(node.op, ast.Add):
            return ("add", left, right)
        if isinstance(node.op, ast.Sub):
            return ("sub", left, right)
        if isinstance(node.op, ast.Mult):
            return ("mul", left, right)
        if isinstance(node.op, ast.Div):
            return ("div", left, right)
        if isinstance(node.op, ast.Pow):
            return ("pow", left, right)
    raise ValueError(f"不支援的語法: {ast.dump(node)}")


def diff(node, var):
    if isinstance(node, ast.Constant):
        return ("num", 0)
    if isinstance(node, ast.Name):
        return ("num", 1) if node.id == var else ("num", 0)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return simplify(("neg", diff(node.operand, var)))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
        return diff(node.operand, var)
    if isinstance(node, ast.BinOp):
        a, b = node.left, node.right
        da, db = diff(a, var), diff(b, var)
        if isinstance(node.op, ast.Add):
            return simplify(("add", da, db))
        if isinstance(node.op, ast.Sub):
            return simplify(("sub", da, db))
        if isinstance(node.op, ast.Mult):
            return simplify(("add", ("mul", da, conv(b)), ("mul", conv(a), db)))
        if isinstance(node.op, ast.Div):
            numerator = ("sub", ("mul", da, conv(b)), ("mul", conv(a), db))
            denominator = ("pow", conv(b), ("num", 2))
            return simplify(("div", numerator, denominator))
        if isinstance(node.op, ast.Pow):
            if not isinstance(b, ast.Constant):
                raise ValueError("指數必須是常數")
            n = b.value
            if n == 0:
                return ("num", 0)
            base = ("pow", conv(a), ("num", n - 1))
            return simplify(("mul", ("mul", ("num", n), base), da))
    raise ValueError(f"不支援的語法: {ast.dump(node)}")


def flatten(e, tag):
    if e[0] == tag:
        return flatten(e[1], tag) + flatten(e[2], tag)
    return [e]


def simplify(e):
    tag = e[0]
    if tag in ("num", "var"):
        return e
    if tag == "neg":
        a = simplify(e[1])
        if a[0] == "num":
            return ("num", -a[1])
        if a[0] == "neg":
            return a[1]
        return ("neg", a)
    if tag in ("add", "sub"):
        a, b = simplify(e[1]), simplify(e[2])
        if tag == "sub":
            if b == ("num", 0):
                return a
            if a == b:
                return ("num", 0)
            b = ("neg", b)
        terms = flatten(a, "add") + flatten(b, "add")
        num = sum(t[1] for t in terms if t[0] == "num")
        rest = [t for t in terms if t[0] != "num"]
        if num != 0:
            rest = [("num", num)] + rest
        if not rest:
            return ("num", 0)
        result = rest[0]
        for t in rest[1:]:
            result = ("add", result, t)
        return result
    if tag == "mul":
        factors = flatten(simplify(e[1]), "mul") + flatten(simplify(e[2]), "mul")
        num, rest = 1, []
        for f in factors:
            if f[0] == "num":
                num *= f[1]
            else:
                rest.append(f)
        if num == 0:
            return ("num", 0)
        if rest and num != 1:
            rest = [("num", num)] + rest
        if not rest:
            return ("num", num)
        result = rest[0]
        for f in rest[1:]:
            result = ("mul", result, f)
        return result
    if tag == "div":
        a, b = simplify(e[1]), simplify(e[2])
        if b == ("num", 0):
            raise ZeroDivisionError
        if b == ("num", 1):
            return a
        if a == ("num", 0):
            return ("num", 0)
        return ("div", a, b)
    if tag == "pow":
        a, b = simplify(e[1]), simplify(e[2])
        if b == ("num", 0):
            return ("num", 1)
        if b == ("num", 1):
            return a
        if a[0] == "num" and b[0] == "num":
            return ("num", a[1] ** b[1])
        return ("pow", a, b)
    return e


def to_str(e, parent=0):
    tag = e[0]
    if tag == "num":
        return str(e[1])
    if tag == "var":
        return e[1]
    if tag == "neg":
        prec, s = 4, "-" + to_str(e[1], 4)
    elif tag in ("add", "sub"):
        prec = 1
        op = " + " if tag == "add" else " - "
        s = to_str(e[1], 1) + op + to_str(e[2], 2)
    elif tag in ("mul", "div"):
        prec = 2
        op = " * " if tag == "mul" else " / "
        s = to_str(e[1], 2) + op + to_str(e[2], 3)
    elif tag == "pow":
        prec, s = 3, to_str(e[1], 4) + "**" + to_str(e[2], 4)
    else:
        raise ValueError(tag)
    return f"({s})" if prec < parent else s


def sym_diff(expr, var="x"):
    tree = ast.parse(expr, mode="eval")
    return to_str(simplify(diff(tree.body, var)))


def my_map(f, xs):
    if not xs:
        return []
    return [f(xs[0])] + my_map(f, xs[1:])


def my_filter(pred, xs):
    if not xs:
        return []
    head = [xs[0]] if pred(xs[0]) else []
    return head + my_filter(pred, xs[1:])


def my_reduce(f, xs, init):
    if not xs:
        return init
    return my_reduce(f, xs[1:], f(init, xs[0]))


def bubble_pass(xs):
    if len(xs) <= 1:
        return xs

    def step(state, x):
        out, carry = state
        if carry <= x:
            return out + [carry], x
        return out + [x], carry

    out, last = my_reduce(step, xs[1:], ([], xs[0]))
    return out + [last]


def bubble_sort(xs):
    if len(xs) <= 1:
        return xs
    ys = bubble_pass(xs)
    return bubble_sort(ys[:-1]) + [ys[-1]]


def main():
    print("== 1. 河內塔 ==")
    for n in (1, 2, 3, 4):
        rec = hanoi_rec(n)
        it = hanoi_iter(n)
        print(f"n={n}: 遞迴 {len(rec)} 步，迭代 {len(it)} 步，結果相同 {rec == it}")
    print("n=3 的移動順序:", hanoi_rec(3), "\n")

    print("== 2. 符號微分 ==")
    expressions = [
        "x**3 + 2*x**2 - 5*x + 7",
        "(x**2 + 1)*(x - 3)",
        "1/x",
        "x**10",
        "3*x**2 + 4*x - 5",
    ]
    for expr in expressions:
        print(f"d/dx ({expr}) = {sym_diff(expr)}")
    print()

    print("== 3. 自製 map / filter / reduce 與無迴圈泡沫排序 ==")
    data = [5, 2, 9, 1, 5, 6]
    print("原始資料:", data)
    print("map 平方:", my_map(lambda x: x * x, data))
    print("filter 偶數:", my_filter(lambda x: x % 2 == 0, data))
    print("reduce 總和:", my_reduce(lambda a, x: a + x, data, 0))
    print("泡沫排序:", bubble_sort(data))
    print("較大資料:", bubble_sort([9, 8, 7, 6, 5, 4, 3, 2, 1]))


if __name__ == "__main__":
    main()
