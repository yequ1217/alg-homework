from dataclasses import dataclass


class Term:
    pass


@dataclass(frozen=True)
class Var(Term):
    name: str


@dataclass(frozen=True)
class Lam(Term):
    param: str
    body: Term


@dataclass(frozen=True)
class App(Term):
    func: Term
    arg: Term


def tokenize(text):
    tokens, i = [], 0
    while i < len(text):
        c = text[i]
        if c.isspace():
            i += 1
        elif c in "\\λ":
            tokens.append("LAMBDA")
            i += 1
        elif c == ".":
            tokens.append("DOT")
            i += 1
        elif c in "()":
            tokens.append(c)
            i += 1
        elif c.isalnum() or c == "_":
            j = i
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            tokens.append(text[i:j])
            i = j
        else:
            raise ValueError(f"無法辨識的字元: {c!r}")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self, expected=None):
        tok = self.peek()
        if expected is not None and tok != expected:
            raise ValueError(f"預期 {expected}，得到 {tok}")
        self.pos += 1
        return tok

    def parse(self):
        term = self.expr()
        if self.pos != len(self.tokens):
            raise ValueError(f"多餘的 token: {self.peek()}")
        return term

    def expr(self):
        if self.peek() == "LAMBDA":
            self.take()
            param = self.take()
            self.take("DOT")
            return Lam(param, self.expr())
        return self.application()

    def application(self):
        terms = [self.atom()]
        while self.peek() not in (None, ")", "DOT", "LAMBDA"):
            terms.append(self.atom())
        result = terms[0]
        for term in terms[1:]:
            result = App(result, term)
        return result

    def atom(self):
        tok = self.peek()
        if tok == "(":
            self.take()
            term = self.expr()
            self.take(")")
            return term
        if tok is None or tok in (")", "DOT", "LAMBDA"):
            raise ValueError(f"預期變數或括號，得到 {tok}")
        self.take()
        return Var(tok)


def parse(text):
    return Parser(tokenize(text)).parse()


def free_vars(term):
    if isinstance(term, Var):
        return {term.name}
    if isinstance(term, Lam):
        return free_vars(term.body) - {term.param}
    return free_vars(term.func) | free_vars(term.arg)


_fresh_counter = [0]


def fresh(base):
    _fresh_counter[0] += 1
    return f"{base}{_fresh_counter[0]}"


def substitute(term, var, value):
    if isinstance(term, Var):
        return value if term.name == var else term
    if isinstance(term, App):
        return App(substitute(term.func, var, value),
                   substitute(term.arg, var, value))
    if isinstance(term, Lam):
        if term.param == var:
            return term
        if term.param in free_vars(value):
            new_param = fresh(term.param)
            body = substitute(term.body, term.param, Var(new_param))
            return Lam(new_param, substitute(body, var, value))
        return Lam(term.param, substitute(term.body, var, value))
    raise TypeError(term)


def reduce_step(term):
    if isinstance(term, App):
        if isinstance(term.func, Lam):
            reduced = substitute(term.func.body, term.func.param, term.arg)
            return reduced, True
        new_func, changed = reduce_step(term.func)
        if changed:
            return App(new_func, term.arg), True
        new_arg, changed = reduce_step(term.arg)
        if changed:
            return App(term.func, new_arg), True
        return term, False
    if isinstance(term, Lam):
        new_body, changed = reduce_step(term.body)
        return Lam(term.param, new_body), changed
    return term, False


def normalize(term, max_steps=500):
    trace = [term]
    for _ in range(max_steps):
        reduced, changed = reduce_step(term)
        if not changed:
            return term, trace, True
        term = reduced
        trace.append(term)
    return term, trace, False


def show(term, parent=0):
    if isinstance(term, Var):
        return term.name
    if isinstance(term, Lam):
        text = f"λ{term.param}. {show(term.body)}"
        return f"({text})" if parent >= 1 else text
    if isinstance(term, App):
        text = f"{show(term.func, 1)} {show(term.arg, 2)}"
        return f"({text})" if parent >= 2 else text
    raise TypeError(term)


def run(name, source, max_steps=500, max_print=40):
    print("=" * 64)
    print(f"{name}")
    print(f"輸入: {source}")
    term = parse(source)
    final, trace, normal = normalize(term, max_steps)
    print(f"共 {len(trace) - 1} 步 beta 化簡：")
    for index, item in enumerate(trace):
        if index > max_print:
            print("  ...")
            break
        print(f"{index:>3}: {show(item)}")
    status = "已達正規形式" if normal else "未達正規形式（超過步數上限）"
    print(f"結果: {show(final)}  [{status}]\n")


def main():
    zero = r"\f.\x.x"
    one = r"\f.\x.f x"
    two = r"\f.\x.f (f x)"
    three = r"\f.\x.f (f (f x))"
    succ = r"\n.\f.\x.f (n f x)"
    plus = r"\m.\n.\f.\x.m f (n f x)"
    true = r"\x.\y.x"
    false = r"\x.\y.y"
    land = r"\p.\q.p q p"

    run("1. 恆等函數 (Identity)", r"(\x.x) y")
    run("2. 常數函數 (K)", r"(\x.\y.x) a b")
    run("3. Church 後繼函數：succ 1", f"({succ}) ({one})")
    run("4. Church 後繼函數：succ 2", f"({succ}) ({two})")
    run("5. Church 加法：plus 2 3", f"({plus}) ({two}) ({three})")
    run("6. 布林 AND：and true false", f"({land}) ({true}) ({false})")
    run("7. 布林 AND：and true true", f"({land}) ({true}) ({true})")


if __name__ == "__main__":
    main()
