__author__ = 'aaron'

from re import split
from collections import defaultdict

def compile(grammar):
    '''
    Compile the specified grammar into a dict of rule name -> abstract syntax tree.
    :param grammar: string input, with rules delimited by new lines
    :return: { str : (nested tuples) )
    '''
    lines = grammar.split("\n")
    rules = {}
    for line in lines:
        line = grammar.split(":=")
        name = line[0].lstrip().rstrip()
        body = line[1].lstrip().rstrip()
        rules[name] = ast(body)
    return rules

def transform(str):
    '''
    Transform string representation of primitive compositions into the representation
    used internally by the AST. E.g.: "|" --> "OR"
    :param str: string to transform
    :return: string
    '''
    if str == "|": return "OR"
    elif str.startswith('"') and str.endswith('"'):
        return "LITER " + str[1:-1]
    else: return str

def infix2postfix(infix):
    '''
    Transform infix representation of a rule to its postfix representation.
    :param infix: s-expression (list of string tokens)
    :return: list of string tokens
    '''

    # Establish precedence of operators.
    opers = { "AND" : 3, "OR" : 2 }

    # Set up stack and infix/postfix strings.
    infix.reverse()
    infix.append("(")
    stack = [")"]
    postfix = []

    for token in infix:

        if token == ")":
            stack.append(token)

        elif token in opers:
            prez = opers[token]
            while len(stack) > 0 and stack[-1] in opers and opers[stack[-1]] >= prez:
                postfix.append(stack.pop())
            stack.append(token)

        elif token == "(":
            while len(stack) > 0 and stack[-1] in opers:
                postfix.append(stack.pop())
            stack.pop()

        else: postfix.append(token)

    return postfix

def ast(body):
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

    # Turn infix string representation to postfix string representation.
    postfix = infix2postfix(newbody)
    astuple = lambda x : tuple(x.split(" "))
    postfix = [astuple(x) for x in postfix]

    # Turn the tuples into an abstract syntax tree.
    stack = []
    for rule in postfix:
        if rule not in [("AND",), ("OR",)]:
            stack.append(rule)
        else:
            arg1 = stack.pop()
            arg2 = stack.pop()
            tree = (rule[0], arg1, arg2)
            stack.append(tree)

    if len(stack) != 1: raise ValueError("Final AST should only have one thing in it :(")
    return stack[0]