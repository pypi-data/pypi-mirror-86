from collections import deque, defaultdict
from easypromtparse.errors import PermissionError

class BaseCommand:
    arguments = defaultdict(list)
    options = defaultdict(str)
    key_options = []
    rest = []

    def add_arg(self, arg: str, val: str) -> None:
        self.arguments[arg].append(val)
    
    def add_option(self, option: str) -> None:
        self.options[option] = 'function holder'
    
    def add_rest(self, val: str) -> None:
        self.rest.append(val)

    def add_key_option(self, val: str) -> None:
        self.key_options.append(val)

    def get_args(self) -> dict:
        return {x:y for x,y in self.arguments.items()}

    def get_options(self) -> dict:
        return {x:y for x,y in self.options.items()}

    def get_rest(self) -> list:
        return self.rest
        
    def get_key_opt(self) -> list:
        return self.key_options

    def __getattr__(self, name):
        err = "NO METHOD"
        msg = f"Cannot acsess to method '{name}'"
        raise PermissionError(error=err, msg=msg)

    def __get_all(self):
        r = {
            **self.arguments,
            **self.options
        }
        return r

    def __getitem__(self, name):
        try:
            res = self.__get_all()[name]
            if len(res) == 1:
                return res[0]
            return res
        except KeyError:
            msg = f'No such flag "{name}" in the command.'
            return KeyError(msg)
            
    def get(self, name: any):
        try:
            res = self.__get_all()[name]
            if len(res) == 1:
                return res[0]
            return res
        except KeyError:
            return -1

    def __repr__(self):
        all_ = {'ARGUMENTS': "\n\t".join(map(lambda x: str(x)[1:-1].replace("\'", ""), self.get_args().items())),
                'OPTIONS': "\n\t".join(map(lambda x: str(x)[1:-1].replace("\'", ""), self.get_options().items())),
                'KEY OPTIONS': "\n\t".join(map(lambda x: str(x).replace("\'", ""), self.get_key_opt())),
                'REST': "\n\t".join(map(lambda x: str(x).replace("\'", ""), self.get_rest())),
                }
        final_repr = ""
        for name, res in all_.items():
            if res:
                final_repr += f"\n\n[{name}]\n\t{res}"

        return final_repr

    def __setattr__(self, name: str, val: any) -> None:
        self.__dict__[name] = val

class Command(BaseCommand):
    """ Actual command after command parsing """

    def __init__(self, path, command):
        super().__init__()
        self.path = path
        self.row_command = command
    
    def bind_func_to_arg(self, func, arg: str, activate: bool=True, pass_args=True) -> None:
        """ 
        Set a result of the function call with dict[arg] parameters to itself
        Be carefult, parameters contaied in any flag have type STRING

        Example
            You have a command "-f path, filename, smth-else --ignore-fails -update all"
            wich is already parsed and have a structure like this:
            {
                '-f': ['path', 'filename', 'smth-else'],
                '-update': ['all']
            }
            '--ignore-fails' does not appear here because it is an option

            and you have a function somewhere wich is to process 
            sertain parameters (path, filename, smth-else)
                a(b, c, e): 
                    ... 
                    return smth

            and you need to put this parameters to the function and deal with them later
            the result of this method 
                bind_func_to_arg(a, '-f')
            is a call of the function "a" with parameters contained dict['-f']
            and set a result to itself

            After this metod you have a structure
            {
                '-f': result of the  function "a" call,
                '-update': ['all']
            }

            If in some reason you need just assing the func to the flag and call it
            with arg values set activate=False
            then a structure will be like:
            bind_func_to_arg(a, '-f', activate=False)
            {
                '-f': function,
                '-update': ['all']
            }
            When you will want to call this functions just call it function()
            
            If you want not pass value to not activated function set pass_args=False
            then a structure will be like:
            bind_func_to_arg(a, '-f', activate=False, pass_args=False)
            {
                '-f': [function, ['path', 'filename', 'smth-else']],
                '-update': ['all']
            }
        """
        args = self.arguments[arg]
        if not args:
            msg = f'Tried to get the "{arg}" flag but there is no such flag'
            raise TypeError(msg)

        #  here expected some errors when user will try to call func with unsupposed arguments
        if activate:
            if pass_args:
                self.arguments[arg] = func(*args)
            else:
                self.arguments[arg] = [func(), args]
        else:
            if pass_args:
                self.arguments[arg] = self.__deferred_execution(func, args)
            else:
                self.arguments[arg] = [self.__deferred_execution(func), args]

    def bind_func_to_option(self, func, option: str, activate: bool=True) -> None:
        """
        Same as bind_func_to_arg but some features
        Instead of passing parameters just call the function and set a 
        result to its option.
        If in some reason you need to the option in the function,
        set use_option to True

        """
        if option not in self.options:
            msg = f"Tried to call option {option} but there is no such option"
            raise TypeError(msg)

        if activate:
            self.options[option] = func()
        else:
            self.options[option] = func

    def __deferred_execution(self, func: callable, args: list=[]):
        def execute(args=args):
            if isinstance(args, list) or isinstance(args, tuple):
                return func(*args)
            else:
                return func(args)
        return execute