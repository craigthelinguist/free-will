__author__ = 'aaron'

from re import split
from collections import defaultdict

def compile(grammar):
    lines = grammar.split("\n")
    rules = {}
    for line in lines:
        line = grammar.split(":=")
        name = line[0].lstrip().rstrip()
        body = line[1].lstrip().rstrip()
        rules[name] = sexpr(body)
    return rules

def transform(str):
    if str == "|": return "OR"
    elif str.startswith('"') and str.endswith('"'):
        return "LITER " + str[1:-1]
    else: return str

def infix2prefix(infix):
    '''
    Transform infix representation of a rule to its postfix representation.
    :param infix: s-expression (list of string tokens)
    :return: list of string tokens
    '''

    # Establish precedence of operators.
    precedence = defaultdict(lambda : 1)
    precedence["AND"] = 3
    precedence["OR"] = 2
    OPERS = ["AND", "OR"]

    # Set up stack and infix/postfix strings.
    stack = [")"]
    infix.append("(")
    prefix = []

    for token in infix:

        if token == ")":
            stack.push(token)

        elif token in OPERS:
            prec = precedence[token]
            while len(stack) > 0 and stack[-1] in OPERS and precedence[stack[-1]] <= prec:
                prefix.append(stack.pop())
            prefix.append(token)

        elif token == ")":
            while stack[-1] in OPERS:
                prefix.append(stack.pop())

        else: prefix.append(token)

    return prefix

def sexpr(body):
    '''
    Turn a rule-body into its corresponding s-expression.
    :param body: string
    :return: list of tuples
    '''
    body = split(" ", body)
    newbody = []
    prev = None
    for token in body:
        if token == "": continue
        if prev not in [None, "OR"] and token != "|":
            newbody.append("AND")
        token = transform(token)
        newbody.append(token)
        prev = token
    postfix = infix2postfix(newbody)
    astuple = lambda x : tuple(x.split(" "))
    return [astuple(x) for x in postfix]

def main():
    g = 'GEO := "wellington" NUM | "auckland" NUM'
    print compile(g)

if __name__ == "__main__":
    main()