'''
This module defines the OuterScope class. This is the main class needed by
sca2d to analyse the scad code.
'''

from copy import copy
from sca2d.scope import ScopeContents
from sca2d import utilities
from sca2d.scadclasses import UseIncStatment
from sca2d.definitions import SCAD_VARS, SCAD_MODS, SCAD_FUNCS
from sca2d.messages import Message

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
        '''
        Returns the name of the file this outer scope represents.
        '''
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

    def analyse_tree(self, analyser):
        """
        Perform analysis of the full tree and sub-scopes. The analyser is taken
        as an input to analyse inlcuded or used files
        """
        self._check_pointless_termination()
        self._check_pointless_scope()
        self._check_complicated_argument()
        self._check_defintions(analyser)

    def _check_defintions(self, analyser):
        all_def_var = copy(SCAD_VARS)
        all_def_mod = copy(SCAD_MODS)
        all_def_func = copy(SCAD_FUNCS)

        #To get the definitions from use and included files we run the same import
        #as any other file including this file with an include statment. We just
        # do not count the definitions from this file. Hence count_own being off.
        defs_and_msgs = self.get_external_defintions(analyser,count_own=False)
        all_def_var += defs_and_msgs[0]
        all_def_mod += defs_and_msgs[1]
        all_def_func += defs_and_msgs[2]

        for message in defs_and_msgs[3]:
            self.messages.append(message)

        self.propogate_defs_and_use(all_def_var, all_def_mod, all_def_func)

    def get_external_defintions(self,
                                analyser,
                                breadcrumbs=None,
                                count_own=True,
                                inc_only=False):
        """
        The definitions passed onto a file that when this file is included with and
        include statment. Count own should only be false when this is being called
        from itself.
        """
        breadcrumbs, message = self._check_and_append_breadcrumbs(breadcrumbs)
        if message is not None:
            return [], [], [], message

        all_def_var = []
        all_def_mod = []
        all_def_func = []
        #The message raised when getting external definitions
        all_msgs = []
        if count_own:
            all_def_var += self._assigned_vars
            all_def_mod += self._defined_modules
            all_def_func += self._defined_functions

        if not inc_only:
            defs = _loop_over_external_files(self._used_files,
                                             analyser,
                                             breadcrumbs,
                                             inc_only=True)
            all_def_mod += defs[1]
            all_def_func += defs[2]
            all_msgs += defs[3]

        defs = _loop_over_external_files(self._included_files,
                                         analyser,
                                         breadcrumbs,
                                         inc_only=inc_only)
        all_def_var += defs[0]
        all_def_mod += defs[1]
        all_def_func += defs[2]
        all_msgs += defs[3]

        return all_def_var, all_def_mod, all_def_func, all_msgs

    def _check_and_append_breadcrumbs(self, breadcrumbs):
        if breadcrumbs is None:
            breadcrumbs = []
        else:
            breadcrumbs = copy(breadcrumbs)
        if self._filename in breadcrumbs:
            crumb_str = ' > '.join(breadcrumbs)
            breadcrumbs.append(self._filename)
            message = Message("E3003", self._tree, [self._filename, crumb_str])
        else:
            breadcrumbs.append(self._filename)
            message = None
        return breadcrumbs, message

    def get_use_defintions(self):
        """
        The definitions passed onto a file that when this file is used with a
        `use` statment.
        """
        return self._defined_modules, self._defined_functions

    def _check_pointless_termination(self):
        subtrees = utilities.get_all_matching_subtrees(self._tree, 'pointless_termination')
        for tree in subtrees:
            self._record_message("I0001", tree)

    def _check_pointless_scope(self):
        subtrees = utilities.get_all_matching_subtrees(self._tree, 'pointless_scoped_block')
        for tree in subtrees:
            self._record_message("I0002", tree)

    def _check_complicated_argument(self):
        subtrees = utilities.get_all_matching_subtrees(self._tree, 'arg')
        for tree in subtrees:
            tokens = utilities.get_all_tokens(tree)
            n_tokens = len(tokens)
            if n_tokens>=8:
                self._record_message("I1001", tree, [n_tokens])

    def _check_invalid_attributes(self):
        attrs = utilities.get_all_matching_tokens(self._tree, "ATTRIBUTE")
        for attr in attrs:
            if attr.value not in ['x', 'y', 'z']:
                self._record_message("E2004", attr)

def _loop_over_external_files(file_list, analyser, breadcrumbs, inc_only):
    all_defs_and_msgs = [[], [], [], []]
    for file_ref in file_list:
        file_scope = analyser.get_scope(file_ref)
        if isinstance(file_scope, Message):
            err_breadcrumbs = copy(breadcrumbs)
            err_breadcrumbs.append(file_ref.filename)
            message = file_scope
            #Overwrite the dummy mesage tree with the tree of calling statment
            if message.code == "F0001":
                args = [file_ref.filename, message.args[0], ' > '.join(err_breadcrumbs)]
                message = Message("E3001", file_ref.tree, args)
            if message.code == "F0002":
                args = [file_ref.filename, ' > '.join(err_breadcrumbs)]
                message = Message("E3002", file_ref.tree, args)
            all_defs_and_msgs[3].append(message)
            continue
        defs_and_msgs = file_scope.get_external_defintions(analyser,
                                                           breadcrumbs,
                                                           inc_only=inc_only)
        for message in defs_and_msgs[3]:
            #Also overwrite tree with calling statment for any messages raise before.
            message.tree = file_ref.tree
        #Concatenate the variable, module and function definition lists
        all_defs_and_msgs = [i+j for i, j in zip(all_defs_and_msgs, defs_and_msgs)]
    return all_defs_and_msgs
