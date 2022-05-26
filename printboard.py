# Plik na wszystkie funkcje zwiazane z wypisywaniem na ekran

import os


def clear_console():
    # Elegancko czysci konsole i na windowsie i na linuksie
    os.system('cls' if os.name == 'nt' else 'clear')


# Obie ponizsze funkcje dzialaja dla tablic stworzynych funkcja create,
# przy jej zmianie te funkcje tez trzeba bedzie poprawic.
def print_both_boards(player_b, si_b):
    # Przyjmuje tablice(plansze) gracza i bota. Zakladam, ze rozmiary obu tablic sa jednakowe
    # Funkcja zwraca tablice w postaci stringa
    # Funkcja (sama!) wypisuje obie plansze obok siebie w ladnej formie
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

    gap2 = 5 + 4 * (n - 2)

    boards += ((gap2 - 5) // 2) * ' ' + 5 * '_' + ((gap2 - 5) // 2) * ' ' + 11 * ' ' + \
              ((gap2 - 7) // 2) * ' ' + 7 * '_' + ((gap2 - 7) // 2) * ' ' + '\n'
    boards += ((gap2 - 7) // 2) * ' ' + "| YOU |" + ((gap2 - 7) // 2) * ' ' + \
              11 * ' ' + ((gap2 - 9) // 2) * ' ' + "| ENEMY |" + '\n'

    # boards += "{0:^45}{1:11}{0:^45}".format(5 * '_', '') + '\n'
    # boards += "{:^45}{:11}{:^45}".format("| YOU |", '', "| ENEMY |") + '\n'

    print(boards)
    return boards


def print_board(tab_b):
    # Przyjmuje jedna plansze (gracza lub bota)
    # Wypisuje te tablice jak powyzsza
    # Zwraca stringa
    n = len(tab_b)
    board = 4 * ' '
    for i in range(n - 2):
        board += "/{:^3}".format(tab_b[0][i + 1])
    board += '/'
    sep_line = '\n' + 4 * '-' + ((n - 2) * 4 + 1) * '=' + '\n'
    board += sep_line
    for i in range(n - 2):
        board += ' '
        for j in range(n - 1):
            board += "{:^3}|".format(tab_b[i + 1][j])
        board += sep_line
    print(board)
    return board
