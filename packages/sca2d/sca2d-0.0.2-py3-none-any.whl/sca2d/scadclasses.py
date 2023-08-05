'''
This module contains simple classes to provide easy access to
information about certain objects parsed from the .scad file.
'''

from dataclasses import dataclass
from lark.tree import Tree

#TODO: make a base class for all of these and make the __eq__ method safer!

@dataclass
class ModuleDef:
    '''
    A class for a module definition. Contains the name of the defined module.
    The number of args (inc. kwargs) and the number of kwargs. The original
    Lark tree and and the ScopeContents for this definition.
    '''
    name: str
    # total number of arguments including keyword arguments
    n_args: int
    n_kwargs: int
    tree: Tree
    scope: object

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name


@dataclass
class FunctionDef:
    '''
    A class for a function definition. Contains the name of the defined function
    The number of args (inc. kwargs) and the number of kwargs. The original
    Lark tree and and the ScopeContents for this definition.
    '''
    name: str
    # total number of arguments including keyword arguments
    n_args: int
    n_kwargs: int
    tree: Tree
    scope: object

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

@dataclass
class ModuleCall:
    '''
    A class for a module call. Contains the name of the called module.
    The number of args (inc. kwargs) and the number of kwargs. The original
    Lark tree and and the ScopeContents for this definition. A new ModuleCall
    object is created each time the module is called. Using ModuleCall.tree
    the position in the scad file can be located.
    '''
    name: str
    # total number of arguments including keyword arguments
    n_args: int
    n_kwargs: int
    tree: Tree
    scope: object

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

@dataclass
class FunctionCall:
    '''
    A class for a function call. Contains the name of the called function.
    The number of args (inc. kwargs) and the number of kwargs. The original
    Lark tree and and the ScopeContents for this definition. A new FunctionCall
    object is created each time the function is called. Using FunctionCall.tree
    the position in the scad file can be located.
    '''
    name: str
    # total number of arguments including keyword arguments
    n_args: int
    n_kwargs: int
    tree: Tree

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

class Variable:
    '''
    A class for a scad variable. A new Variable object is created each time the
    variable is used or defined. Using Variable.tree the position in the scad file
    can be located.
    '''
    def __init__(self, token):
        if isinstance(token, Tree):
            token = token.children[0]
        if token.type != 'VARIABLE':
            raise ValueError('Cannot make a variable from a non-variable Token')
        self.name = token.value
        self.token = token

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

    @property
    def tree(self):
        """
        returns the token for the variable. This is the same as Variable.token.
        Despite not being a tree this is safe to use when fidning line and column
        numbers.
        """
        return self.token

class UseIncStatment:
    '''
    Class for a scad use or include statment
    '''
    def __init__(self, tree, calling_file):
        self.filename = tree.children[0].value
        self.tree = tree
        self.calling_file = calling_file

    def __str__(self):
        return self.filename

    def __repr__(self):
        return f"<sca2d.scadclasses.UseIncStatment: {self.filename}>"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.filename==other
        if isinstance(other, UseIncStatment):
            return self.filename == other.filename
        return False
