class CommandError(Exception):
    default_errors = {
        'no command': 'Empty command. Check your spelling. Required at least an argument with a value or one option',
        'bad arg': '[STRICT] Got argument "{}" without any value.',
        'bad option': '[STRICT] Got option "{}" with the value "{}". Not allowed to put a value after an option',
        'string command': 'Got the string command "{}". Expected a line command',
        'line command': 'Got the line command "{}". Expected a string command',
        'command not str': 'Got the command type "{}". Expected type str',
        'command not list': 'Got the command type "{}". Expected type list',
        'line command has not str values': 'Not all parameters have type str. {}',
    }
    dev_erros = {
        1: '[DEV] Try to get not existing error "{}"',
        2: '[DEV] Not enough values in arg {} to compose error message "{}"'
    }


    def __init__(self, error: str ='', msg: str ='', arg: list =[]):
        self.msg = msg
        self.error = error
        self.arg = self.perp_arg(arg)

    def perp_arg(self, arg: list) -> list:
        try:
            iter(arg)
        except TypeError:
            raise TypeError(f'[DEV] Try to get the error "{self.error}" with not iterable arg: "{arg}" ')
        if isinstance(arg, str):
            raise TypeError(f'[DEV] Try to get the error "{self.error}" with not correct arg: "{arg}" ')
        return arg

    def __get_error(self):
        if self.error:
            try:
                form_er = self.default_errors[self.error].format(*self.arg)
            except KeyError:
                form_er = self.dev_erros[1].format(self.error)
            except IndexError:
                form_er = self.dev_erros[2].format(self.arg, self.error)
            return f"{form_er}"
        return f"{self.msg}"
        
    def __repr__(self):
        return self.__get_error()

    def __str__(self):
        return self.__get_error()


class PermissionError(Exception):
    def __init__(self, error: str ='', msg: str =''):
        self.msg = msg
        self.error = error

    def __repr__(self):
        return f"[{self.error.upper()}] {self.msg}"

    def __str__(self):
        return f"[{self.error.upper()}] {self.msg}"