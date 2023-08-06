#  This module is developed to parse a command line command,
#  or string command
# 
#  It is supposed to parse string as follows:
# 
#  [-f] - an argument of the command. Required to have a value
#  or list of values (separated by spaces) right after itself.
#  If there are not values, argument will be passed
# 
#  [--b] - an option of the command. Not allowed to put values after 
#  an option.
#  If there are values after an option, they will be put in the REST list

import os
import sys

from typing import Union
from collections import deque, defaultdict

from easypromtparse.command import Command
from easypromtparse.errors import CommandError



class CommandParser:
    """
    Parser for command line command or just string command
    It's to be a command like these
    Examples of string commands:

        "+f val1 val2 val3 ++quet ++ignore-fails"
        "#update file1 file2 ##do-copy #log-size ##warning"

    Examples of line commands:

       path, "+f", "val1", "val2", "val3", "++quet", "++ignore-fails"
       path, "#update", "file1", "file2", "##do-copy", "#log-size", "##warning"
    
    Yes it's jsut a string commnad resieved from the method split() with a path to the directory
    
    You should stick to structure like this:
    ponter = 'any you want', defaulf poiner = "-"
        for options will be used double pinter

    " pointer[argument name] value1 [value2 [value3]....[value n]] double-pointer[option name]"

    strc = What type of command you have
        If you have a command from the command line obtained with sys.argv - strc = False
        If you have a string command like in examples - strc = True

    strict - dafault False. If it's nassary to you to all arguments have their values
    and all option does not have any values right after itself set it to True.
    Example 
        strict = True
        commnad = "-argument --other"
        Will raise a TypeError, because -argument does not have a value / values
        
    args_strict (argumets strict) and opt_strict (options strict) works the same but 
    separetly

    key_len - default = 0. If you need to put sertain words at the beggining of a command
    set key_len to its count
    Example
    """

    def __init__(self, command: Union[str, list], strc=False, pointer='-',
                 strict:bool=False, args_strict: bool=False, opt_strict: bool=False,
                 key_len=0):

        self.__check_accordance(command, strc)
        self.path, self.command = self.__prepare_command(command, strc)
        self.row_command = deque(self.command)
        self.pointer = pointer
        self.strict = strict
        self.args_strict = args_strict
        self.opt_strict = opt_strict
        self.key_len = key_len

    def __prepare_command(self, command: Union[str, list], strc: bool) -> list:
        """
        Prepares command depending on the strc value
        if its value is True
            command is supposed to be string command
        else like a command line command
        """
        if strc:
            return [os.getcwd(), command.split()]
        else:
            return [os.path.split(command[0])[0], command[1:]]

    def __check_accordance(self, command: str, strc: bool) -> None:
        """ 
        Checks accordance of the command 
        if the [line commad] strc have to be [Fasle]

        if the [string commad] strc have to be [True]

        Also check if command is empty depending on a command type
        """
        if isinstance(command, str):
            self.__if_command_empty(command)
            self.__if_commnad_not_str(command)
            if not strc:
                self.raise_command_error(error='string command', args=[command])
        
        if isinstance(command, list):
            try:
                self.__if_command_empty(command[1])
                self.__if_command_contain_not_str_items(command[1])
            except IndexError:
                self.raise_command_error(error='no command')
            if strc:
                self.raise_command_error(error='line command', args=[command])

            
    
    def __if_command_empty(self, command: str) -> None:
        if not all(command) or not command:
            self.raise_command_error(error='no command')

    def __if_commnad_not_str(self, command: any) -> None:
        if not isinstance(command, str):
            self.raise_command_error(error='command not str',
                                     args=[type(command)])

    def __if_commnad_not_list(self, command: any) -> None:
        if not isinstance(command, list):
            self.raise_command_error(error='command not list',
                                     args=[type(command)])

    def __if_command_contain_not_str_items(self, command: list) -> None:
        """
        Checks single element in command. If element is not string 
        CommandError will raise
        
        """
        for i in command:
            n = type('')
            t = type(i)
            if n != t:
                self.raise_command_error(error='line command has not str values',
                                         args=[f"Parametr {i} has type {t}"])

    def parse(self, com=Command) -> Command:
        """ 
        Parses a formed command queue and separate arguments from options
        If a value does not have argument it will be passed in the REST list
        """
        com = com(self.path, self.row_command)
        key_len = self.key_len
        while self.row_command:
            item = self.row_command.popleft()

            if key_len:
                self.__put_key_option(com, item)
                key_len -= 1
                continue

            if self.__is_option(item):
                self.__put_option(com, item)

            elif self.__is_arg(item):
                self.__put_arg(com, item)
            else:
                com.add_rest(item)
        return com

    def __put_option(self, com: Command, item: str, ignore: bool=False) -> None:
        """
        Add the option to the Command 
        if any value appears after the option
        and strict=True or opt_strict=True
        CommandError will raise
        """
        if (self.strict or self.opt_strict) and not ignore:
            try:
                next_ = self.row_command[0]
            except IndexError:
                com.add_option(item)
                return 
            if not self.__is_both(next_):
                self.raise_command_error(error='bad option',
                                         args=[item, next_])
        com.add_option(item)

    def __put_arg(self, com: Command, item:str, ignore: bool=False) -> None:
        """
        Add all values right after the sertain flag to Command
        if no values and strict=True or arg_strict=True
        CommandError will raise
        """
        arg = item
        count = 0
        while self.row_command:
            next_item = self.row_command.popleft()
            if not self.__is_both(next_item):
                com.add_arg(arg, next_item)
                count += 1
            else:
                if (self.strict or self.args_strict) and not ignore:
                    if count < 1:
                        self.raise_command_error(error='bad arg', args=[arg])
                self.row_command.appendleft(next_item)
                break

    def __put_key_option(self, com: Command, val: str) -> None:
        com.add_key_option(val)
    
    def raise_command_error(self, error: str, args: list=[]) -> None:
        """ Raise a custom error with args to format the error with them """
        error = CommandError(error=error, arg=args)
        raise error

    def __is_both(self, val: str) -> bool:
        """ Whether the value an argument or an option """
        return self.__is_option(val) or self.__is_arg(val)

    def __is_option(self, val: str) -> bool:
        """ Is the value an option """
        return val.startswith(self.pointer*2)

    def __is_arg(self, val: str) -> bool:
        """ Is the value an argument """
        return val.startswith(self.pointer)

    def __get_command(self) -> str:
        """ Returns row command """
        return f"[COMMAND]: {self.row_command}"

    def __repr__(self):
        return self.__get_command()
