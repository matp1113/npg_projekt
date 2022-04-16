# plik na wszystkie funkcje zwiazane z wypisywaniem na ekran

import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


# elegancko czysci konsole i na windowsie i na linuksie


def print_both_boards(player_b, si_b):
    # przyjmuje tablice(plansze) gracza i bota. Zakladam, ze rozmiary obu tablic sa jednakowe
    # funkcja zwraca tablice w postaci stringa
    # funkcja (sama!) wypisuje obie plansze obok siebie w ladnej formie
    n = len(player_b)
    b1 = 4 * ' '
    for i in range(n - 2):
        b1 += "/{:^3}".format(player_b[0][i + 1])
    b1 += '/'
    gap = "{:^11}".format('|')
    boards = b1 + gap + ' ' + b1
    sep_line = 4 * '-' + ((n - 2) * 4 + 1) * '='
    f_sep_line = '\n' + sep_line + gap + sep_line + '\n'
    boards += f_sep_line
    for i in range(n - 2):
        boards += ' '
        for j in range(n - 1):
            boards += "{:^3}|".format(player_b[i + 1][j])
        boards += gap + ' '
        for j in range(n - 1):
            boards += "{:^3}|".format(si_b[i + 1][j])
        boards += f_sep_line
    boards += "{0:^45}{1:11}{0:^45}".format(5 * '_', '') + '\n'
    boards += "{:^45}{:11}{:^45}".format("| YOU |", '', "| ENEMY |") + '\n'
    print(boards)
    return boards

# def print_player_board(player_b):
# przyjmuje plansze gracza
# wypisuje te tablice jak powyzsza
# zwraca stringa
