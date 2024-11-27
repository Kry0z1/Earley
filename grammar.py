class Grammar:
    _terminals: list[str] 
    _not_terminals: list[str]
    _rules: dict[str, set[str]]
    _start: str

    def __init__(self, not_terminals: list[str], terminals: list[str], rules: list[tuple[str, str]], start: str):
        self._terminals = terminals
        self._not_terminals = not_terminals
        self._rules = dict()
        for rule in rules:
            self.add_rule(rule)
        if start not in not_terminals:
            raise ValueError(f"Grammar is invalud: unknown start char: {start}")
        self._start = start

    @staticmethod
    def from_other(other, not_terminals: list[str], terminals: list[str], rules: list[tuple[str, str]], start: str):
        result = Grammar([""], [], [], "")
        result._terminals = list(set(other._terminals) | set(terminals))
        result._not_terminals = list(set(other._not_terminals) | set(not_terminals))
        for left, lst_right in other._rules.items():
            for right in lst_right:
                result.add_rule((left, right))
        for rule in rules:
            result.add_rule(rule)
        result.start = start
        return result

    def add_rule(self, rule: tuple[str, str]):
        left_side, right_side = rule[0], rule[1]
        if len(left_side) != 1:
            raise ValueError(f"Grammar is not context-free: left side is too long: {left_side}->{right_side}")
        if left_side[0] not in self._not_terminals:
            raise ValueError(f"Grammar is invalid: invalid char in left side: {left_side}->{right_side}")
        for c in left_side:
            if c not in self._not_terminals and c not in self._terminals:
                raise ValueError(f"Grammar is invalid: unknown char in left side: {left_side}->{right_side}: {c}")
        for c in right_side:
            if c not in self._not_terminals and c not in self._terminals:
                raise ValueError(f"Grammar is invalud: unknown char in right side: {left_side}->{right_side}: {c}")
        if left_side in self._rules.keys():
            self._rules[left_side].add(right_side)
        else:
            self._rules[left_side] = {right_side}
