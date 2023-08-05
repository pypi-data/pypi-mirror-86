'''
SCA2D is an experimental static code analyser for OpenSCAD.
'''

import os
from lark import Lark
from lark.exceptions import LarkError
from sca2d.outerscope import OuterScope
from sca2d.scadclasses import UseIncStatment
from sca2d.utilities import locate_file

class ScadParser():
    '''
    This is the main parser for the scad.
    '''
    def __init__(self):
        self._parser = self._create_parser()

    def _create_parser(self):
        sca2d_dir = os.path.dirname(__file__)
        lark_dir = os.path.join(sca2d_dir, 'lark')
        scad_lark_filename = os.path.join(lark_dir, 'scad.lark')

        with open(scad_lark_filename, 'r') as scad_lark_file:
            scad_lark = scad_lark_file.read()
        return Lark(scad_lark, propagate_positions=True)

    def parse(self, scad):
        '''
        The input should be a string containing scad code.
        '''
        return self._parser.parse(scad)

class Analyser:
    """
    This will parse scad to get a parse tree and then analyse if for possible
    code problems.
    """

    def __init__(self):
        self._parser = ScadParser()
        self._parsed_files = {}

    def parse_file(self, file_reference):
        if isinstance(file_reference, str):
            filename = file_reference
        elif isinstance(file_reference, UseIncStatment):
            filename = locate_file(file_reference)
        else:
            raise TypeError('Analyser.parse_file cannot accept an input of type '
                            f'{type(file_reference)}')

        print(f'parsing {filename}')
        try:
            with open(filename, 'r') as file_obj:
                scad_code = file_obj.read()
        except (OSError, IOError) as error:
            print(f"`{filename}`:0:0: F0002: Cannot open file.\n")
            return None
        try:
            tree = self._parser.parse(scad_code)
        except LarkError as error:
            err_str = "\n"+str(error)
            err_str = err_str.replace('\n', '\n   - ')
            print(f"`{filename}`:0:0: F0001: Cannot read file due to syntax error:{err_str}\n"
                  f"If you belive this is a bug in SCA2D please report it to us.\n")
            return None
        self._parsed_files[filename] = OuterScope(tree, filename)
        return self._parsed_files[filename]

    def analyse_file(self, filename, output_tree=False):
        """
        Runs sca2d on the imput file
        """
        #set defaults before running

        scope = self.parse_file(filename)
        if scope is None:
            return False
        if output_tree:
            with open('output.sca2d', 'w') as file_obj:
                file_obj.write(scope.tree.pretty())

        self._parse_required_files(scope)

        scope.analyse_tree(self._parsed_files)
        scope.print_messages()
        return True

    def _parse_required_files(self, scope):
        self._parse_used_files(scope)
        self._parse_included_files(scope)

    def _parse_used_files(self, scope):
        used_files = scope.used_files
        for used_file in used_files:
            if used_file.filename not in self._parsed_files:
                self.parse_file(used_file)

    def _parse_included_files(self, scope):
        included_files = scope.included_files
        for inc_file in included_files:
            if inc_file.filename not in self._parsed_files:
                inc_scope = self.parse_file(inc_file)
                if inc_scope is None:
                    continue
                extra_includes = inc_scope.included_files
                for extra_include in extra_includes:
                    if extra_include not in [included_files, scope.filename]:
                        included_files.append(extra_include)
