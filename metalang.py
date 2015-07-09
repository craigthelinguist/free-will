__author__ = 'aaron'

TEXT = None
from copy import deepcopy
import grammar

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

def parse(input_txt, input_grammar):
    '''
    Return all possible parses of the text given
    :param input: text to be parsed.
    :return: list of all possible parse trees.
             each parse represented by s-expressions in a list.
    '''

    # Compile grammar.
    global composite_rules
    composite_rules = grammar.compile(input_grammar)

    # set current text to be parsed.
    if not type(input_txt) == str:
        raise TypeError("Can only parse strings.")
    global TEXT
    TEXT = input_txt

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
            for rule in composite_rules:
                if rule == "LITER": continue
                new_trees = match_rule(i, tree, rule)
                next_iter_parses += new_trees

            # next generation is now current generation.

        possible_parses = uniques(next_iter_parses)

    return [tree for i,tree in possible_parses]

def match_LITERAL(indx, parse_tree, literal):
    global TEXT
    if not TEXT[indx:indx+len(literal)] == literal: return None
    tree = deepcopy(parse_tree)
    tree.append(literal)
    return [(indx + len(literal), tree)]

def match_NUM(indx, parse_tree):
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

def match_STR(indx, parse_tree):
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

def match_COMPOSITE(indx, parse_tree, body):

    trees = []

    for clause in body:

        # Match rule at head of body.
        name = clause[0]
        if name == "LITER":
            literal = clause[1]
            pts = match_LITERAL(indx, parse_tree, literal)
        elif name == "NUM":
            pts = match_NUM(indx, parse_tree)
        elif name == "STR":
            pts = match_STR(indx, parse_tree)
        else:
            raise SyntaxError("Composite rules in body of composite rules not yet implemented")

        # For every possible match, match rest of the body.
        for next_index, pt in pts:
            pts_rest = match_COMPOSITE(next_index, pt, body[1:])
            trees.append(pts_rest)

    return trees



def match_rule(indx, parse_tree, rule):
    if rule in primitive_rules:
        func = primitive_rules[rule]
        return func(indx, parse_tree)
    else:
        if rule not in composite_rules:
            raise ValueError("Unknown rule: {}".format(rule))
        else:
            body = composite_rules[rule]
            return match_COMPOSITE(indx, parse_tree, body)

rules = ["NUM", "STR"]
composite_rules = { "LITER" : () }
primitive_rules = { "NUM" : match_NUM, "STR" : match_STR }

def main():
    gr = 'GEO := "billy" NUM'
    print parse("billy13", gr)

if __name__ == "__main__":
    main()