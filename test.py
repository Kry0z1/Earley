from .grammar import Grammar
from .earley import Earley
from itertools import product
from collections import deque

def construct_grammar(not_terminals, terminals, rules, start):
    return Grammar(not_terminals, terminals, list(map(tuple, [rule.split("->") for rule in rules])), start)

def in_grammar(grammar, word):
    e = Earley()
    e.fit(grammar)
    return e.predict(word)

def is_RBS(word, brackets=None):
    if brackets == None:
        brackets = ["()"]
    table = {br[0]: br[1] for br in brackets}
    table_rv = {br[1]: br[0] for br in brackets}
    stack = deque()
    for c in word:
        if c in table.keys():
            stack.append(c)
            continue
        if c not in table_rv.keys() or len(stack) == 0:
            return False
        if stack.pop() != table_rv[c]:
            return False
    return len(stack) == 0

## Тест ПСП
def test_RBS():
    rules = [
        "S->",
        "S->(S)S"
    ]
    g = construct_grammar(["S"], "()", rules, "S")
   
    for rep in range(11):
        for seq in product("()", repeat=rep):
            result_gr = in_grammar(g, "".join(seq))
            result = is_RBS("".join(seq))
            assert (result_gr and result) or (not result_gr and not result)
    assert in_grammar(g, "")

## Тест ПСП при неоднозначности разбора
def test_RBS_quirky():
    rules = [
        "S->",
        "S->S(S)S",
        "S->()"
    ]

    g = construct_grammar(["S"], "()", rules, "S")
    for rep in range(11): 
        for seq in product("()", repeat=8):
            result_gr = in_grammar(g, "".join(seq))
            result = is_RBS("".join(seq))
            assert (result_gr and result) or (not result_gr and not result)
    assert in_grammar(g, "")

## Тест ПСП с разными скобками
def test_RBS_different():
    rules = [
        "S->",
        "S->S(S)S",
        "S->S[S]S",
    ]

    g = construct_grammar(["S"], "([]){}", rules, "S")
   
    for rep in range(11):
        for seq in product("()", repeat=12):
            result_gr = in_grammar(g, "".join(seq))
            result = is_RBS("".join(seq), brackets=["()", "[]", "{}"])
            assert (result_gr and result) or (not result_gr and not result)
    assert in_grammar(g, "")

## Тест праволинейной грамматики
def test_right():
    rules = [
        "S->A",
        "S->B",
        "A->aA",
        "B->bB",
        "A->a",
        "B->b"
    ]
    g = construct_grammar("SAB", "ab", rules, "S")
    for seq in product("ab", repeat=5):
        result = in_grammar(g, "".join(seq))
        assert (result and (seq.count("a") == 5 or seq.count("b") == 5)) or (not result and seq.count("a") != 5 and seq.count("b") != 5)

    assert not in_grammar(g, "")

## Тест пустой грамматики
def test_empty():
    rules = [
        "S->S",
        "S->AB",
        "A->a",
        "B->bAB"
    ]
    g = construct_grammar("SAB", "ab", rules, "S")
    for seq in product("ab", repeat=8):
        assert not in_grammar(g, "".join(seq))

    assert not in_grammar(g, "")
