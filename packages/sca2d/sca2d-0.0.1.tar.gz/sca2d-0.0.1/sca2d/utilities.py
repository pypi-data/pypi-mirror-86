"""
This contains a number of useful functions used by other modules.
"""

from lark.tree import Tree
from sca2d.scadclasses import Variable

def is_empty_arg(tree):
    """
    Checks if an argument is empty. This is needed becuse
    lark returns and empty arg tree when `foo()` is encountered.
    This function is trivial but makes code clearer.
    """
    return len(tree.children) == 0

def is_termination(tree_or_token):
    """
    Checks if the tree or token is a termination character. i.e ";".
    This is useful when deciding how to pass a module call scope as
    the module may be called with a scope following or terminated. It is
    Used for all module and control scopes as terminating them isntantly
    with a semicolon is always valid .scad even if it does not make sense
    to do so.
    """
    if isinstance(tree_or_token, Tree):
        return False
    return tree_or_token.type == 'TERMINATION'

def get_vars_and_funcs_in_expr(expr):
    """
    Returns a list of the variables used and functions called in the input
    expression. Two lists are returned. For variables the list is of
    sca2d.scadclasses.Variable objects but for the function calls they are
    lark.tree.Tree as they will require further processing in the calling scope.
    """
    var_tokens = get_all_matching_tokens(expr , 'VARIABLE')
    func_trees = get_all_matching_subtrees(expr , 'function_call')
    variables = [Variable(token) for token in var_tokens]
    return variables, func_trees

def parse_assignment(assign_tree):
    """
    Spits and asignment (could be a kwarg or a control assignment)
    into the assinged variable and the expression.
    """
    assigned_var = Variable(assign_tree.children[0])
    expr = assign_tree.children[1]
    used_vars, used_functions = get_vars_and_funcs_in_expr(expr)
    return assigned_var, used_vars, used_functions

def get_all_matching_subtrees(tree, tree_name):
    """
    Returns a list of all matching subtrees in the order they appear in the
    code. Trees match if Tree.data (i.e. the rule name in the .lark definion)
    matches the input "tree_name".
    """
    subtrees = []
    for child in tree.children:
        if isinstance(child, Tree):
            if child.data == tree_name:
                subtrees.append(child)
            subtrees += get_all_matching_subtrees(child, tree_name)
    return subtrees

def get_all_matching_tokens(tree, token):
    """
    Returns a list of all matching tokens in the order they appear in the
    code. Tokens match if Token.Type matches the input.
    """
    tokens = []
    for child in tree.children:
        if isinstance(child, Tree):
            tokens += get_all_matching_tokens(child, token)
        else:
            if child.type == token:
                tokens.append(child)
    return tokens

def get_all_tokens(tree):
    """
    Returns all tokens in a given lark Tree. Note that the tokens are the terminus or leaf
    of each branch of the tree, but not all trees terminate in tokens.
    """
    tokens = []
    for child in tree.children:
        if isinstance(child, Tree):
            tokens += get_all_tokens(child)
        else:
            tokens.append(child)
    return tokens
