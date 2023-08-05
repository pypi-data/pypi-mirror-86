'''
This module defines the OuterScope class. This is the main class needed by
sca2d to analyse the scad code.
'''

from copy import copy
from sca2d.scope import ScopeContents
from sca2d import utilities
from sca2d.scadclasses import UseIncStatment
from sca2d.definitions import SCAD_VARS, SCAD_MODS, SCAD_FUNCS

class OuterScope(ScopeContents):
    """
    This is a child class of ScopeContents but is the only class you should
    need to create. It will recursively create ScopeContents for each internal
    scope. Compared to all other ScopeContents classes it has some extra variables
    for storing used and included files as well as the filename of the file being
    analysed.
    """

    def __init__(self, tree, filename):
        self._filename = filename
        self._used_files = []
        self._included_files = []
        super().__init__(tree, None, top_level=True)

    @property
    def filename(self):
        return self._filename

    @property
    def used_files(self):
        '''
        Returns a list of the files used as UseIncStatment objects.
        '''
        return copy(self._used_files)

    @property
    def included_files(self):
        '''
        Returns a list of the files included as UseIncStatment objects.
        '''
        return copy(self._included_files)

    def get_use_defintions(self):
        """
        The definitions passed onto a file that when this file is used with a
        `use` statment.
        """
        return self._defined_modules, self._defined_functions

    def get_include_defintions(self, parsed_files, breadcrumbs):
        """
        The definitions passed onto a file that when this file is used with a
        `use` statment.
        """
        all_def_var = copy(self._assigned_vars)
        all_def_mod = copy(self._defined_modules)
        all_def_func = copy(self._defined_functions)
        for inc_file in self._included_files:
            filename = utilities.locate_file(inc_file)
            if filename in breadcrumbs:
                tree = inc_file.tree
                print(f"`{self._filename}`:{tree.line}:{tree.column}: F0003: Cannot include"
                      f" {filename} as the include definitions form a loop.\n")
            else:
                breadcrumbs = copy(breadcrumbs).append(self._filename)
                if filename not in parsed_files:
                    continue
                inc_scope = parsed_files[filename]
                def_var, def_mod, def_func = inc_scope.get_include_defintions(parsed_files,
                                                                              breadcrumbs)
                all_def_var += def_var
                all_def_mod += def_mod
                all_def_func += def_func
        return all_def_var, all_def_mod, all_def_func

    def _printed_var_lists(self, indent=2, this_indent=0):
        def print_list(plist):
            return '[' + ', '.join([str(item) for item in plist]) + ']'
        var_lists = [f"included_files: {print_list(self._included_files)}",
                     f"used_files: {print_list(self._used_files)}"]
        var_lists += super()._printed_var_lists(indent, this_indent)
        return var_lists

    def _count_use_include(self, statement_tree):
        if statement_tree.data == 'use_statement':
            self._used_files.append(UseIncStatment(statement_tree, self._filename))
        else:
            self._included_files.append(UseIncStatment(statement_tree, self._filename))

    def print_messages(self):
        """
        Print all collected messages for this file.
        """
        all_messages = self.collate_messages()
        all_messages.sort(key=lambda msg: (msg.tree.line, msg.tree.column))
        for message in all_messages:
            line = message.tree.line
            column = message.tree.column
            code = message.code
            message_text = message.message
            print(f'{self._filename}:{line}:{column}: {code}: {message_text}')

    def analyse_tree(self, parsed_files):
        """
        Perform analysis of the full tree and sub-scopes.
        """
        self._check_pointless_termination()
        self._check_pointless_scope()
        self._check_complicated_argument()
        self._check_defintions(parsed_files)

    def _check_defintions(self, parsed_files):
        all_def_var = copy(SCAD_VARS)
        all_def_mod = copy(SCAD_MODS)
        all_def_func = copy(SCAD_FUNCS)
        for used_file in self._used_files:
            used_scope = _get_scope(used_file, parsed_files)
            if used_scope is None:
                # File has not been parsed, warning already printed
                continue
            [mod_defs, func_defs] = used_scope.get_use_defintions()
            all_def_mod += mod_defs
            all_def_func += func_defs

        for inc_file in self._included_files:
            inc_scope = _get_scope(inc_file, parsed_files)
            if inc_scope is None:
                # File has not been parsed, warning already printed
                continue
            [var_defs, mod_defs, func_defs] = inc_scope.get_include_defintions(parsed_files,
                                                                               [self._filename])
            all_def_var += var_defs
            all_def_mod += mod_defs
            all_def_func += func_defs

        self.propogate_defs_and_use(all_def_var, all_def_mod, all_def_func)

    def _check_pointless_termination(self):
        subtrees = utilities.get_all_matching_subtrees(self._tree, 'pointless_termination')
        for tree in subtrees:
            self._record_message(tree, "W0001", "Semicolon not required.")

    def _check_pointless_scope(self):
        subtrees = utilities.get_all_matching_subtrees(self._tree, 'pointless_scoped_block')
        for tree in subtrees:
            self._record_message(tree, "W0002", "Empty scope.")

    def _check_complicated_argument(self):
        subtrees = utilities.get_all_matching_subtrees(self._tree, 'arg')
        for tree in subtrees:
            tokens = utilities.get_all_tokens(tree)
            n_tokens = len(tokens)
            if n_tokens>=8:
                self._record_message(tree,
                                     "W1001",
                                     f"Overly complicated argument contains {n_tokens} tokens.")

def _get_scope(use_inc_statement, parsed_files):
    filename = utilities.locate_file(use_inc_statement)
    if filename  in parsed_files:
        return parsed_files[filename]
    return None
