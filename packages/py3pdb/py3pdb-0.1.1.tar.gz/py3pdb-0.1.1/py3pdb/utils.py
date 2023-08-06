from colorama import Style, Fore


def error(string):
    print(Fore.RED + 'Error: ' + string + f'{Style.RESET_ALL}')