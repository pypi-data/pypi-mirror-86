'''
This module defines the ScopeContents class and a number of its sub classes. These
are used to count the definitions and uses of variables, modules, and functions in
different scopes.

These are all automatically generated recursivley by the OuterScope class which can
be found in outerscope.py.
'''
from copy import copy
from dataclasses import dataclass
from lark.tree import Tree
from sca2d import utilities
from sca2d.scadclasses import Variable, ModuleDef, FunctionDef, ModuleCall, FunctionCall

@dataclass
class Message:
    """Class for storing the analysis messages."""
    tree: Tree
    code: str
    message: str

class ScopeContents:
    '''
    This is the base class of OuterScope and all of the module/function/control
    scopes. It should not be used as it is.
    All ScopeContents include the original Lark parse tree for their scope.
    '''
    def __init__(self, tree, parent, top_level, preassigned_vars=None):
        if not top_level:
            if not isinstance(parent, ScopeContents):
                raise ValueError("Non top-level scopes require a parent scope.")
        if preassigned_vars is None:
            self._assigned_vars = []
        else:
            self._assigned_vars = preassigned_vars
        self._used_vars = []
        self._tree = tree
        self._defined_modules = []
        self._used_modules = []
        self._defined_functions = []
        self._used_functions = []
        self._internal_scopes = []
        self._parent = parent
        self.messages = []
        self._parse_scope()

    def __str__(self):
        """
        The string representation of the scope is the pretty print with all the
        whitespace stripped out except after commas.
        """
        printstr = self.pretty(0,0)
        printstr = printstr.replace('\n','')
        printstr = printstr.replace(' ','')
        printstr = printstr.replace(',',', ')
        return printstr

    @property
    def tree(self):
        '''
        This is the original unmodified lark.tree.Tree for this scope.
        '''
        return self._tree

    def collate_messages(self):
        """
        Get all messages from subscopes and this scope
        """
        messages = copy(self.messages)
        for scope in self._internal_scopes:
            messages += scope.collate_messages()
        return messages

    def pretty(self, indent=2, this_indent=0):
        """
        This pretty prints the scope. The indent can be customised.
        `this_indent sets the initial indent.`
        """
        indent_txt = ' '*this_indent

        return (indent_txt + "{\n" +
                indent_txt + " " +
                f"\n{indent_txt} ".join(self._printed_var_lists(indent, this_indent)) +
                "\n"+ indent_txt + "}")

    def _printed_var_lists(self, indent=2, this_indent=0):
        """
        This is seperate from pretty print so other child classes can
        overload it to add extra information to the print.
        """
        #This might be for pretty printing but it is the ugliest code in the
        #library!
        indent_txt = ' '*this_indent
        def print_list(plist):
            return '[' + ', '.join([str(item) for item in plist]) + ']'
        def print_scope_list(scopes):
            if len(scopes) == 0:
                return []
            return ('\n' + indent_txt + ' [\n'+
                    ',\n'.join([scope.pretty(indent, indent+this_indent) for scope in scopes]) +
                    '\n'+ indent_txt + ' ]')

        var_lists= [f"assigned_vars: {print_list(self._assigned_vars)}",
                    f"used_vars: {print_list(self._used_vars)}",
                    f"defined_modules: {print_list(self._defined_modules)}",
                    f"used_modules: {print_list(self._used_modules)}",
                    f"defined_functions: {print_list(self._defined_functions)}",
                    f"used_functions: {print_list(self._used_functions)}",
                    f"scopes: {print_scope_list(self._internal_scopes)}"]
        return var_lists

    def _record_message(self, tree, code, message):
        """
        Appends a message to self._messages.
        """
        self.messages.append(Message(tree, code, message))

    def _parse_scope(self, overload_tree=None):
        '''This function should be able to parse all rules in `_terminated_statements`
        in the lark file. For any rules that are anonymous (starting with _) the rules
        inside the anonymous rule must be parsed'''
        if overload_tree is None:
            tree = self._tree
        else:
            tree = overload_tree
        for child in tree.children:
            if child.data == "variable_assignment":
                self._count_assignment(child)
            elif child.data == "module_def":
                self._count_module_definition(child)
            elif child.data == "function_def":
                self._count_function_definition(child)
            elif child.data == "module_call":
                self._count_module_call(child)
            elif child.data == "pointless_scope":
                self._parse_scope(child)
            elif child.data in ["for", "intersection_for", "let"]:
                self._count_let_and_for(child)
            elif child.data == "if":
                self._count_if(child)
            elif child.data in ["include_statement", "use_statement"]:
                self._count_use_include(child)

    def _count_assignment(self, assign_tree):
        assigned_var, used_vars, func_calls = utilities.parse_assignment(assign_tree)
        self._assigned_vars.append(assigned_var)
        self._used_vars += used_vars
        self._count_function_calls(func_calls)

    def _count_module_definition(self, mod_def_tree):
        name, args = self._parse_header(mod_def_tree.children[0])
        n_kwargs, module_vars = self._parse_def_args(args)
        module_scope = mod_def_tree.children[1]
        if utilities.is_termination(module_scope):
            scope = None
        else:
            scope = ModuleDefScope(module_scope,
                                   parent=self,
                                   preassigned_vars=module_vars)
            self._internal_scopes.append(scope)
        module_def = ModuleDef(name, len(args), n_kwargs, mod_def_tree, scope)
        self._defined_modules.append(module_def)

    def _count_function_definition(self, func_def_tree):
        name, args = self._parse_header(func_def_tree.children[0])
        n_kwargs, module_vars = self._parse_def_args(args)
        function_scope = func_def_tree.children[1]
        if utilities.is_termination(function_scope):
            scope = None
        else:
            scope = FunctionDefScope(function_scope,
                                     parent=self,
                                     preassigned_vars=module_vars)
            self._internal_scopes.append(scope)
        function_def = FunctionDef(name, len(args), n_kwargs, func_def_tree, scope)
        self._defined_functions.append(function_def)

    def _count_module_call(self, mod_call_tree):
        name, args = self._parse_header(mod_call_tree.children[0])
        n_kwargs, _ = self._parse_call_args(args)
        module_scope = mod_call_tree.children[1]
        if utilities.is_termination(module_scope):
            scope = None
        else:
            scope = ModuleCallScope(module_scope, parent=self)
            self._internal_scopes.append(scope)
        module_call = ModuleCall(name, len(args), n_kwargs, mod_call_tree, scope)
        self._used_modules.append(module_call)

    def _count_function_calls(self, func_call_trees):
        for func_call_tree in func_call_trees:
            name, args = self._parse_header(func_call_tree.children[0])
            n_kwargs, _ = self._parse_call_args(args)
            function_call = FunctionCall(name, len(args), n_kwargs, func_call_tree)
            self._used_functions.append(function_call)

    def _count_let_and_for(self, control_tree):
        control_assign_list = control_tree.children[0].children
        assigned_vars = []
        for assignment in  control_assign_list:
            assigned_var, used_vars, func_calls  = utilities.parse_assignment(assignment)
            assigned_vars.append(assigned_var)
            self._used_vars += used_vars
            self._count_function_calls(func_calls)

        control_scope = control_tree.children[1]
        self._add_control_scope(control_scope, assigned_vars)

    def _count_if(self, control_tree):
        control_condition = control_tree.children[0]
        var_list, func_calls = utilities.get_vars_and_funcs_in_expr(control_condition)
        self._used_vars += var_list
        self._count_function_calls(func_calls)

        control_scope = control_tree.children[1]
        self._add_control_scope(control_scope)
        if len(control_tree.children)>2:
            #If we are here then the if statment had an else
            control_scope = control_tree.children[3]
            self._add_control_scope(control_scope)

    def _count_use_include(self, statement_tree):
        self._record_message(statement_tree,
                             "E1001",
                             "`use` or `include` can only be used in the outer scope.")

    def _add_control_scope(self, control_scope, preassigned_vars=None):
        if utilities.is_termination(control_scope):
            scope = None
        else:
            scope = ControlScope(control_scope,
                                 parent=self,
                                 preassigned_vars=preassigned_vars )
            self._internal_scopes.append(scope)

    def _parse_header(self, header_tree):
        """
        This is used to parse the function header for both
        definitions and calls, the argment lists are returned and
        passd to wither parse_def_args or parse_call_args
        """
        name = header_tree.children[0].children[0].value
        arg_trees = header_tree.children[1:]
        if utilities.is_empty_arg(arg_trees[0]):
            args = []
        else:
            args = [tree.children[0] for tree in arg_trees]
        return name, args

    def _parse_def_args(self, args):
        """
        This parses the arguments of a function or module definition.
        As it is only for a definition only variables or keyword-arguments
        (kwargs) are allowed.
        """
        assigned_vars = []
        n_kwargs = 0
        for arg in args:
            if arg.data == 'kwarg':
                assigned_var, used_vars, func_calls  = utilities.parse_assignment(arg)
                assigned_vars.append(assigned_var)
                self._used_vars += used_vars
                self._count_function_calls(func_calls)

                n_kwargs += 1
            elif arg.data == 'variable':
                assigned_vars.append(Variable(arg.children[0]))
                if n_kwargs>0:
                    self._record_message(arg,
                                         "E0002",
                                         "Defining an non-keyword argument after a"
                                         "keyword argument.")
            else:
                self._record_message(arg,
                                     "E0001",
                                     "Argument in definition should be a variable"
                                     " or a variable with default value.")
        return n_kwargs, assigned_vars

    def _parse_call_args(self, args):
        """
        This parses the arguments of a fucnction or module call. As such
        any matched expressions are allowed. However kwargs need to be treated
        differently so that the assigned variable can be passed onto the new scope.
        """
        assigned_vars = []
        n_kwargs = 0
        for arg in args:
            if arg.data == 'kwarg':
                assigned_var, used_vars, func_calls  = utilities.parse_assignment(arg)
                assigned_vars.append(assigned_var)
                self._used_vars += used_vars
                self._count_function_calls(func_calls)
                n_kwargs += 1
            else:
                var_list, func_calls = utilities.get_vars_and_funcs_in_expr(arg)
                self._used_vars += var_list
                self._count_function_calls(func_calls)
                if n_kwargs>0:
                    self._record_message(arg,
                                         "E0002",
                                         "Defining an non-keyword argument after a"
                                         "keyword argument.")

        return n_kwargs, assigned_vars

    def propogate_defs_and_use(self, var_defs, mod_defs, func_defs):
        """
        This should be called from the parent scope. The inputs are
        the variables, modules, and functions defined by the parent
        (or its parents, etc). What is returned is the variable use
        by this scope and all internal scopes.
        """

        self._check_overwrite_var(var_defs)
        self._check_overwrite_mod(mod_defs)
        self._check_overwrite_func(func_defs)

        all_var_defs = var_defs + self._assigned_vars
        all_mod_defs = mod_defs + self._defined_modules
        all_func_defs = func_defs + self._defined_functions
        all_var_use = copy(self._used_vars)
        all_mod_use = copy(self._used_modules)
        all_func_use = copy(self._used_functions)

        for scope in self._internal_scopes:

            [var_use, mod_use, func_use] = scope.propogate_defs_and_use(all_var_defs,
                                                                        all_mod_defs,
                                                                        all_func_defs)
            all_var_use += var_use
            all_mod_use += mod_use
            all_func_use += func_use

        self._check_var_use(all_var_defs, all_var_use)
        self._check_mod_use(all_mod_defs, all_mod_use)
        self._check_func_use(all_func_defs, all_func_use)

        return all_var_use, all_mod_use, all_func_use

    #TODO: Combine overwrite functions once warning definitions are defined externally
    def _check_overwrite_var(self, var_defs):
        '''
        Check if variable overwritten in this scope
        '''
        for n, definition in enumerate(self._assigned_vars):
            if definition in self._assigned_vars[:n]:
                self._record_message(definition.tree,
                                     "W2001",
                                     f"Variable `{definition.name}` overwritten within"
                                     " scope.")
            elif definition in var_defs:
                self._record_message(definition.tree,
                                     "W2002",
                                     f"Overwriting `{definition.name}` variable from a"
                                     " lower scope.")

    def _check_overwrite_mod(self, mod_defs):
        '''
        Check if module defintion overwritten in this scope
        '''
        for n, definition in enumerate(self._defined_modules):
            if definition in self._defined_modules[:n]:
                self._record_message(definition.tree,
                                     "W2003",
                                     f"Module `{definition.name}` multiply defined within"
                                     " scope.")
            elif definition in mod_defs:
                self._record_message(definition.tree,
                                     "W2004",
                                     f"Overwriting `{definition.name}` module definition from"
                                     " a lower scope.")

    def _check_overwrite_func(self,func_defs):
        '''
        Check if function definition overwritten in this scope
        '''
        for n, definition in enumerate(self._defined_functions):
            if definition in self._defined_functions[:n]:
                self._record_message(definition.tree,
                                     "W2005",
                                     f"Function `{definition.name}` multiply defined within"
                                     " scope.")
            elif definition in func_defs:
                self._record_message(definition.tree,
                                     "W2006",
                                     f"Overwriting `{definition.name}` function definition"
                                     " from a lower scope.")

    #TODO: Combine check use functions once warning definitions are defined externally
    def _check_var_use(self, all_var_defs, all_var_use):
        '''
        Check if variables defined in this scope is used. Also check all variables used
        in this scope are defined. Only check variables used or defined directly in this
        scope as others will be picked up in the scope they are used/defined in.
        '''
        for var in self._assigned_vars:
            if var not in all_var_use:
                self._record_message(var.tree,
                                     "W2007",
                                     f"Variable `{var.name}` defined but never used.")
        for var in self._used_vars:
            if var not in all_var_defs:
                self._record_message(var.tree,
                                     "W2008",
                                     f"Variable `{var.name}` used but never defined.")

    def _check_mod_use(self, all_mod_defs, all_mod_use):
        '''
        Check if modules defined in this scope is used. Also check all modules used in
        this scope are defined. Only check modules used or defined directly in this
        scope as others will be picked up in the scope they are used/defined in.
        '''
        for mod in self._defined_modules:
            if mod not in all_mod_use:
                self._record_message(mod.tree,
                                     "W2009",
                                     f"Module `{mod.name}` defined but never used.")
        for mod in self._used_modules:
            if mod not in all_mod_defs:
                self._record_message(mod.tree,
                                     "W2010",
                                     f"Module `{mod.name}` used but never defined.")

    def _check_func_use(self, all_func_defs, all_func_use):
        '''
        Check if functions defined in this scope is used. Also check all functions used
        in this scope are defined. Only check functions used or defined directly in this
        scope as others will be picked up in the scope they are used/defined in.
        '''
        for func in self._defined_functions:
            if func not in all_func_use:
                self._record_message(func.tree,
                                     "W2011",
                                     f"Function `{func.name}` defined but never used.")
        for func in self._used_functions:
            if func not in all_func_defs:
                self._record_message(func.tree,
                                     "W2012",
                                     f"Function `{func.name}` used but never defined.")


class ModuleDefScope(ScopeContents):
    '''
    This is a child class of ScopeContents. It hold the defined and used variables
    moduled and functions for the scope of a module definition. i.e. the code in the
    braces after `module foo(a)`.

    For the scope of the called module see ModuleCallScope
    '''
    def __init__(self, tree, parent, preassigned_vars):
        super().__init__(tree, parent, top_level=False, preassigned_vars=preassigned_vars)

class FunctionDefScope(ScopeContents):
    '''
    This is a child class of ScopeContents. It hold the defined and used variables
    (etc) for the scope of a function definition.
    Making a whole class for this scope is perhaps overkill as
    functions are simply an expression. However this exists to be
    future-proof (if OpenSCAD introduce multi line functons) and consistent.
    '''

    def __init__(self, tree, parent, preassigned_vars):
        super().__init__(tree,
                         parent,
                         top_level=False,
                         preassigned_vars=preassigned_vars)

    def _parse_scope(self, overload_tree=None):
        '''
        Overloading parse scope as the expected scope is a simply an expression
        '''
        var_list, func_calls = utilities.get_vars_and_funcs_in_expr(self._tree)
        self._used_vars += var_list
        self._count_function_calls(func_calls)

class ModuleCallScope(ScopeContents):
    '''
    This is a child class of ScopeContents. It hold the defined and used variables
    moduled and functions for the scope of a module call. i.e. the code in the
    braces of `foo(a){CODE GOES HERE}`. If a single module or flow control element
    (if statement, for loop) follows the module rather than code in braces. This
    class is still used to define that scope.

    For the scope of the module definition see ModuleDefScope.
    '''
    def __init__(self, tree, parent):
        super().__init__(tree, parent, top_level=False)

class ControlScope(ScopeContents):
    '''
    This is a child class of ScopeContents. It hold the defined and used variables
    moduled and functions for the scope inside a flow control statment. This is used
    for the scopes of both `if` and `else` (seperate ControlScope for each) as well as
    `for`, `intersection_for`, and `let`.
    '''
    def __init__(self, tree, parent, preassigned_vars):
        super().__init__(tree, parent, top_level=False, preassigned_vars=preassigned_vars)
