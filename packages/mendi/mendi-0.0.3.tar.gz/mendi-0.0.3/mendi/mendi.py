''' 
Simple wrapper that helps you write a menu-driven program easily.

> A menu-driven program is one, in which the user is provided a list of choices.
> A particular action is done when the user chooses a valid option.
> There is also an exit option, to break out of the loop.
> Error message is shown on selecting a wrong choice.

'''

import os
from tabulate import tabulate


def clear_screen() -> None:
    ''' Clears the current screen '''
    input('ENTER to continue: ')  # wait for user to see current screen
    if os.name == 'posix':
        # for Linux and Mac
        os.system('clear')
    else:
        # for Windows
        os.system('cls')


def drive_menu(heading: str, menus: dict) -> None:
    ''' The driver of menus

    Args:
        heading (str): A suitable heading of your choice
        menus (dict): Dictionary of menus, where key is choice no. and value is another dictionary containing `desc` and `func`.
    '''
    table = [[ch, menu['desc']] for ch, menu in menus.items()]
    menu_chart = f'''
        MENU for {heading}
    \n{tabulate(table,tablefmt='fancy_grid',headers=['Choice','Description'])}
    Enter your choice or X to quit
    \n>>> '''
    choice = ''
    while choice != 'X':
        clear_screen()
        choice = input(menu_chart)
        if choice in menus.keys():
            val = menus[choice]['func']()
            if val:
                print(val)
        elif choice == 'X':
            print('Bye 🤗')
        else:
            print('INVALID CHOICE')
