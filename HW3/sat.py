import ast
import itertools

ALLOWED_NODES = (
    ast.Expression, ast.BoolOp, ast.And, ast.Or,
    ast.UnaryOp, ast.Not, ast.Name, ast.Load, ast.Constant,
)


def parse(expr):
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"不支援的語法: {type(node).__name__}")
        if isinstance(node, ast.Constant) and not isinstance(node.value, bool):
            raise ValueError(f"只接受布林常數，收到: {node.value!r}")
    return tree


def variables(tree):
    return sorted({n.id for n in ast.walk(tree) if isinstance(n, ast.Name)})


def evaluate(tree, env):
    return bool(eval(compile(tree, "<sat>", "eval"), {"__builtins__": {}}, env))


def truth_table(expr):
    tree = parse(expr)
    names = variables(tree)
    header = " | ".join(names + ["結果"])
    print(header)
    print("-" * len(header))
    rows = []
    for values in itertools.product([False, True], repeat=len(names)):
        env = dict(zip(names, values))
        result = evaluate(tree, env)
        rows.append((env, result))
        cells = ["T" if v else "F" for v in values]
        print(" | ".join(cells + ["T" if result else "F"]))
    return names, rows


def sat_solve(expr):
    tree = parse(expr)
    names = variables(tree)
    return names, [env for env, ok in
                   ((dict(zip(names, vs)), evaluate(tree, dict(zip(names, vs))))
                    for vs in itertools.product([False, True], repeat=len(names)))
                   if ok]


def show(expr):
    print("=" * 60)
    print("表示式:", expr)
    names, solutions = sat_solve(expr)
    truth_table(expr)
    print(f"\n變數個數 {len(names)}，暴力列舉 {2 ** len(names)} 種組合")
    if solutions:
        print(f"可滿足，共 {len(solutions)} 組解：")
        for env in solutions:
            print("  " + ", ".join(f"{k}={'T' if v else 'F'}" for k, v in env.items()))
    else:
        print("不可滿足 (UNSAT)")
    print()


def main():
    show("(a or b) and (not a or c) and (not b or not c)")
    show("a and not a")
    show("(a or not a) and (b or not b)")


if __name__ == "__main__":
    main()
