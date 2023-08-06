'''
Defines the messages used by SCA2D when checks fail.
'''

import logging
from colorama import Fore, Back, Style

class Message:
    """Class for storing the analysis messages."""

    def __init__(self, code, tree, args=None):
        if args is None:
            args = []
        self.code = code
        self.tree = tree
        expected_args = self.raw_message.count('%s')
        if expected_args == 0:
            if args != []:
                logging.warning('Unexpected args sent to warning %s. '
                                'This is a problem with SCA2D not with your scad code.',
                                code)
                args = []
        else:
            if len(args) != expected_args:
                logging.warning('Wrong number of args sent to %s.'
                                'This is a problem with SCA2D not with your scad code.',
                                code)
                args = ['X']*expected_args
        self.args = tuple(args)

    @property
    def line(self):
        '''
        The line in the code where the a check raised this message.
        '''
        return self.tree.line

    @property
    def column(self):
        '''
        The column on Message.line of the code where the a check raised this message.
        '''
        return self.tree.column

    @property
    def raw_message(self):
        '''
        The message describing the check that failed without any arguments from
        this instance of the message
        '''
        if self.code in MESSAGES:
            message_txt = MESSAGES[self.code]
        else:
            message_txt = 'Unknown message'
        return message_txt

    @property
    def message(self):
        '''
        The message describing the check that failed.
        '''
        message_txt = self.raw_message
        expected_args = message_txt.count('%s')
        if expected_args>0:
            return message_txt%self.args
        return message_txt

    def pretty(self, filename, colour=False):
        '''
        Pretty printing the error message. Requires the filename.
        '''
        msg = f'{filename}:{self.line}:{self.column}: {self.code}: {self.message}'
        if colour:
            if self.code.startswith('F'):
                msg = Back.RED + msg + Style.RESET_ALL
            elif self.code.startswith('E'):
                msg = Fore.RED + msg + Style.RESET_ALL
            elif self.code.startswith('W'):
                msg = Fore.YELLOW + msg + Style.RESET_ALL
        return msg






MESSAGES = {
    "E0001": "Argument in definition should be a variable or a variable with default value.",
    "E0002": "Defining an non-keyword argument after a keyword argument.",
    "E1001": "`use` or `include` can only be used in the outer scope.",
    "E2001": "Variable `%s` used but never defined.",
    "E2002": "Module `%s` used but never defined.",
    "E2003": "Function `%s` used but never defined.",
    "W2001": "Variable `%s` overwritten within scope.",
    "W2002": "Overwriting `%s` variable from a lower scope.",
    "W2003": "Module `%s` multiply defined within scope.",
    "W2004": "Overwriting `%s` module definition from a lower scope.",
    "W2005": "Function `%s` multiply defined within scope.",
    "W2006": "Overwriting `%s` function definition from a lower scope.",
    "W2007": "Variable `%s` defined but never used.",
    "W2008": "Module `%s` defined but never used.",
    "W2009": "Function `%s` defined but never used.",
    "I0001": "Semicolon not required",
    "I0002": "Empty scope",
    "I1001": "Overly complicated argument contains %s tokens.",
    "D0001": "Assign is depreciated. Use a regular assignment."
}
