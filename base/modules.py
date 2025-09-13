def color_print(string, color=None):
    from termcolor import colored

    if color:
        return print(colored(string, color))
    else:
        return print(string)