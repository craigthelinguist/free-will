__author__ = 'aaron'

TEXT = None
from copy import deepcopy

def uniques(parses):
    '''
    Return only the unique parses (the usual list(set(parses)) doesn't
    work as lists are not hashable.
    :param parses: list of (indx, parse-tree)
    :return: unique parses
    '''
    parses2 = []
    for p in parses:
        if p not in parses2:
            parses2.append(p)
    return parses2

def last_rule(tree):
    if len(tree) == 0: return None
    else: return tree[-1][0]

def parse(input):
    '''
    Return all possible parses of the text given
    :param input: text to be parsed.
    :return: list of all possible parse trees.
             each parse represented by s-expressions in a list.
    '''

    # set current text to be parsed.
    if not type(input) == str:
        raise TypeError("Can only parse strings.")
    global TEXT
    TEXT = input

    # you've finished parsing when every branch has been exhausted.
    def done(parses):
        if len(parses) == 0: return True
        for i, parse in parses:
            if i < len(TEXT): return False
        return True

    # a "possible_parse" is
    possible_parses = [(0,[])]
    while not done(possible_parses):
        next_iter_parses = []
        for i, tree in possible_parses:

            # if a parse tree has exhausted input it
            # constitutes a complete parse.
            if i >= len(TEXT):
                next_iter_parses.append((i,tree))
                continue

            # try to extend tree by every possible rule
            # add the new trees to the next generation.
            for rule in rules:
                new_trees = parse_rule(i, tree, rule)
                next_iter_parses += new_trees

            # next generation is now current generation.

        possible_parses = uniques(next_iter_parses)

    return [tree for i,tree in possible_parses]

def parse_LITERAL(indx, parse_tree, literal):
    global TEXT
    if not TEXT[indx:indx+len(literal)] == literal: return None
    tree = deepcopy(parse_tree)
    tree.append(literal)
    return [(indx + len(literal), tree)]

def parse_NUM(indx, parse_tree):
    global TEXT

    # count size of maximal string
    strlen = 0
    for char in TEXT[indx:]:
        if char.isdigit(): strlen += 1
        else: break


    if parse_tree == [["STR", "ab"], ('NUM', '3')]:
        print "hi"
    # all possible substrings of maximal number represent a
    # potential parse.
    parse_trees = []
    for i in range(1, strlen+1):
        substr = TEXT[indx:indx+i]
        tree = deepcopy(parse_tree)
        # combine with previous NUM if possible
        if last_rule(tree) == "NUM":
            tree[-1] = ("NUM", tree[-1][1] + substr)
        # otherwise add to list
        else:
            tree.append(("NUM", substr))
        parse_trees.append((indx+i, tree))

    return parse_trees

def parse_STR(indx, parse_tree):
    global TEXT

    # count size of maximal string
    strlen = 0
    for char in TEXT[indx:]:
        if char.isalpha(): strlen += 1
        else: break

    # all possible substrings of maximal string represent a
    # potential parse
    parse_trees = []
    for i in range(1, strlen+1):
        substr = TEXT[indx:indx+i]
        tree = deepcopy(parse_tree)
        if last_rule(tree) == "STR":
            tree[-1] = ("STR", tree[-1][1] + substr)
        else:
            tree.append(("STR", substr))
        parse_trees.append((indx+i, tree))

    return parse_trees

def parse_rule(indx, parse_tree, rule):
    if rule in primitive_rules:
        func = primitive_rules[rule]
        return func(indx, parse_tree)
    else:
        raise ValueError("Composite rules not yet implemented.")

rules = ["NUM", "STR"]
composite_rules = {}
primitive_rules = { "NUM" : parse_NUM, "STR" : parse_STR }