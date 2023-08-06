'''
SCA2D is an experimental static code analyser for OpenSCAD.
'''

import os
from lark import Lark
from lark.exceptions import LarkError
from sca2d.outerscope import OuterScope
from sca2d.scadclasses import UseIncStatment
from sca2d.utilities import locate_file, DummyTree
from sca2d.messages import Message, print_messages

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

    def __init__(self, verbose=False):
        self._parser = ScadParser()
        self._parsed_files = {}
        self._verbose = verbose

    def _parse_file(self, filename):
        '''
        Parses the input file returns an OuterScope object. This object is also stored by the
        Analyzer for future use.
        '''
        if self._verbose:
            print(f'parsing {filename}')
        try:
            with open(filename, 'r') as file_obj:
                scad_code = file_obj.read()
        except (OSError, IOError) as error:
            return Message("F0002", DummyTree())
        try:
            tree = self._parser.parse(scad_code)
        except LarkError as error:
            err_str = "\n"+str(error)
            err_str = err_str.replace('\n', '\n   - ')
            return Message("F0001", DummyTree(), [err_str])
        self._parsed_files[filename] = OuterScope(tree, filename)
        return self._parsed_files[filename]

    def analyse_file(self, filename, output_tree=False, colour=False):
        """
        Runs sca2d on the imput filed
        """
        #set defaults before running

        scope = self.get_scope(filename)
        if isinstance(scope, Message):
            #Get_scope may return a Fatal message instead of a scope
            #Print and exit.
            print_messages([scope], filename, colour=colour)
            return False
        if output_tree:
            with open('output.sca2d', 'w') as file_obj:
                file_obj.write(scope.tree.pretty())

        scope.analyse_tree(self)
        all_messages = scope.collate_messages()
        print_messages(all_messages, filename, colour=colour)
        return True

    def get_scope(self, file_reference):
        '''
        Returns the OuterScope for a given file. Will parse it only if it has not already been
        parsed.
        The input can either be a string containing the file path or a UseIncStatment object
        created when a scad file parses a use or include statment.
        '''
        if isinstance(file_reference, str):
            filename = file_reference
        elif isinstance(file_reference, UseIncStatment):
            filename = locate_file(file_reference)
        else:
            raise TypeError('Analyser.parse_file cannot accept an input of type '
                            f'{type(file_reference)}')

        if filename in self._parsed_files:
            return self._parsed_files[filename]
        return self._parse_file(filename)
