from grammar import Grammar

class Situation:
    _rule: tuple[str, str]
    _index: int
    _dot_pos: int

    def __init__(self, rule, i, dot_pos):
        self._rule = rule
        self._index = i
        self._dot_pos = dot_pos

    def __eq__(self, other):
        return self._rule[0] == other._rule[0] and self._rule[1] == other._rule[1] and self._index == other._index and self._dot_pos == other._dot_pos

    def __repr__(self):
        return f"Situation[{self._rule=}, {self._index=}, {self._dot_pos=}]"

    def __hash__(self):
        return hash(self._rule[0] + "->" + self._rule[1] + "$" + str(self._index) + "$" + str(self._dot_pos)) 

class Earley:
    _grammar: Grammar
    _prev_start: str

    def __init__(self):
        pass

    def fit(self, grammar: Grammar):
        # Making new grammar with $ as start
        # And new rule $ -> S
        self._grammar = Grammar.from_other(grammar, ["$"], [], [("$", grammar._start)], "$") 
        self._prev_start = grammar._start

    def _scan(self, states: list[Situation], j: int, word: str):
        if j == 0:
            return
        for situation in states[j-1]:
            if len(situation._rule[1]) <= situation._dot_pos:
                continue
            if situation._rule[1][situation._dot_pos] == word[j-1]:
                states[j].add(Situation(situation._rule, situation._index, situation._dot_pos+1))

    def _complete(self, states: list[Situation], j: int, word: str) -> bool:
        update = set() 
        for situation in states[j]:
            if len(situation._rule[1]) != situation._dot_pos:
                continue
            for upper_situation in states[situation._index]:
                if len(upper_situation._rule[1]) <= upper_situation._dot_pos:
                    continue
                if upper_situation._rule[1][upper_situation._dot_pos] == situation._rule[0]:
                    update.add(Situation(upper_situation._rule, upper_situation._index, upper_situation._dot_pos+1))
        prev_len = len(states[j])
        states[j] |= update
        return len(states[j]) > prev_len
   
    def _predict(self, states: list[Situation], j: int, word: str) -> bool:
        update = set()
        for situation in states[j]:
            if len(situation._rule[1]) <= situation._dot_pos:
                continue
            b = situation._rule[1][situation._dot_pos] 
            if b not in self._grammar._not_terminals or b not in self._grammar._rules.keys():
                continue
            for right in self._grammar._rules[b]:
                update.add(Situation((b, right), j, 0))
        prev_len = len(states[j])
        states[j] |= update
        return len(states[j]) > prev_len
   
    def predict(self, word: str) -> bool:
        states = [set() for _ in range(len(word)+1)]
        states[0] = {Situation(("$", self._prev_start), 0, 0)}
        
        for j in range(len(word)+1):
            self._scan(states, j, word)
            while True:
                changed = False  
                changed = changed or self._complete(states, j, word)
                changed = changed or self._predict(states, j, word)
                if not changed:
                    break

        for situation in states[len(word)]:
            if situation == Situation(("$", self._prev_start), 0, 1):
                return True
        return False
