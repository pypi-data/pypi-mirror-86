#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['print_sep']


class bcolors:
    EMPTY = ''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_sep(arr: list, size: int = -1, error: bool = False, table: bool = False, header: bool = False, spaces: int = -1):
    r"""
    print_sep : a function to print tab in plain, with header or in table

    :param arr list: A list of list
    :param size int: size of arr (can be manualy calculated)
    :param error bool: 
    """
    if size < 0:
        if type(arr[0]) == list:
            size = len(arr[0])
        else:
            return
    if spaces <= 1:
        spaces = 6

    tab_size: list = []
    for i in range(size):
        local_size: int = 0
        for j in range(len(arr)):
            lg: int = len(arr[j][i])
            if local_size < lg:
                local_size = lg
        tab_size.append(local_size)
    start: int = 0
    length: int = 0

    if header:
        length = (lambda x: sum(x))(tab_size) + \
            (spaces*(len(tab_size))) + 3
        delimitor: str = "-"*length
        print(f"{bcolors.OKGREEN}", end=f"{delimitor}\n")
        print("|", end=" ")
        for j in range(size):
            sep: str = " " * \
                (tab_size[j] - len(arr[0][j]) + spaces - 1) + "|" + " "
            print(arr[0][j], end=sep)
        print()
        print(delimitor, end=f"{bcolors.ENDC}\n")
        start = 1

    elif table:
        length = (lambda x: sum(x))(tab_size) + \
            (spaces*(len(tab_size))) + 3
        delimitor: str = "-"*length
        print(f"{delimitor}")
        print("|", end=" ")
        for j in range(size):
            sep: str = " " * \
                (tab_size[j] - len(arr[0][j]) + spaces - 1) + "|" + " "
            print(arr[0][j], end=sep)
        print()
        print(delimitor)
        start = 1

    for i in range(start, len(arr)):
        if table:
            print("|", end=" ")
        elif header:
            print("  ", end="")
        for j in range(size):
            if table:
                sep: str = " " * \
                    (tab_size[j] - len(arr[i][j]) + spaces - 1) + "|" + " "
            else:
                sep: str = " "*(tab_size[j] - len(arr[i][j]) + spaces)
            print(arr[i][j], end=sep)
        print()
        if table:
            print("-"*length)


if __name__ == "__main__":
    tab_test = [["blabla", "blibli"], [
        "bloblooooooo", "blbll"], ["bloblo", "blbl"]]
    print_sep(tab_test)
    print("\n\n")
    print_sep(tab_test, table=True, spaces=5, header=True)
    print("\n\n")
    print_sep(tab_test, header=True)
    print("\n\n")
    print_sep(tab_test, table=True)
    print("\n\n")
    print_sep(tab_test, spaces=10)
