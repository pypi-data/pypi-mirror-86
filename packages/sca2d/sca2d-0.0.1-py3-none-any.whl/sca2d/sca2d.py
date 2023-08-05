'''
SCA2D is an experimental static code analyser for OpenSCAD.
'''

import os
from lark import Lark
from lark.exceptions import LarkError
from sca2d.outerscope import OuterScope

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

    def parse_file(self, filename):
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
        if output_tree:
            with open('output.sca2d', 'w') as file_obj:
                file_obj.write(scope.tree.pretty())
        included_files = scope.included_files
        used_files = scope.used_files
        for inc_file in included_files:
            if inc_file.filename in self._parsed_files:
                continue
            inc_scope = self.parse_file(inc_file.filename)
            extra_includes = inc_scope.included_files
            for extra_include in extra_includes:
                if extra_include not in [included_files, filename]:
                    included_files.append(extra_include)
        for used_file in used_files:
            if used_file.filename not in self._parsed_files:
                self.parse_file(used_file.filename)

        scope.analyse_tree(self._parsed_files)
        scope.print_messages()
        return True
