import random

def twist(x, y, l, n):
    tab = []

    if (x + l > 1 and x + l < n + 1):
        tab.append([l, 0])

    if (x - l > 1 and x - l < n + 1):
        tab.append([-l, 0])

    if (y + l > 1 and y + l < n + 1):
        tab.append([0, l])

    if (y - l > 0 and y - l < n + 1):
        tab.append([0, -l])

    if len(tab) == 0:
        return (0)

    return (random.choice(tab))  # losowa strona wylosowana z tabeli


# sprawdza czy możliwe jest obrócenie statku o długości l i zwraca tablie z możliwymi obrotami

def rand(n, ship):  # n wymiar planszy, ship liczba statków o konkretnym wymiarze
    tab = create(n + 2)

    j = len(ship)
    while j > 0:  # kolejne wielkości statków
        for i in range(0, ship[j - 1]):  # liczba statków
            x = random.randint(1, n)
            y = random.randint(1, n)

            if check(x, y, tab) == 0:
                return (0)

            if j > 1:
                dir = twist(x, y, j, n)

                if dir == 0:
                    return (0)

                if (dir[0] > 0):  # sprawdzenie w którą stronę wylosowało
                    for a in range(1, j):
                        if check(x + a, y, tab, [x + a - 1, y]) == 0:
                            return (0)
                        tab[y][x + a] = '■'

                if (dir[0] < 0):
                    for a in range(1, j):
                        if check(x - a, y, tab, [x - a + 1, y]) == 0:
                            return (0)
                        tab[y][x - a] = '■'

                if (dir[1] > 0):
                    for a in range(1, j):
                        if check(x, y + a, tab, [x, y + a - 1]) == 0:
                            return (0)
                        tab[y + a][x] = '■'

                if (dir[1] < 0):
                    for a in range(1, j):
                        if check(x, y - a, tab, [x, y - a + 1]) == 0:
                            return (0)
                        tab[y - a][x] = '■'

            tab[y][x] = '■'
        j = j - 1

    return tab

# tworzy planszę z losowym ułożeniem statków i sprawdza czy jest ok
# jak jest zle to zwraca 0

def create(n):
    dict = {-1: '', 0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
            12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
            24: 'Y', 25: 'Z'}
    tab = [[0] * n for l in range(n)]
    for i in range(n):
        for j in range(n):
            tab[i][j] = '□'
        tab[i][n - 1] = ' '
        tab[i][0] = i
    for j in range(n):
        tab[0][j] = dict[j - 1]
        tab[n - 1][j] = ' '
        tab[0][n - 1] = ' '

    return (tab)

# tworzy plansze z obramowaniem

def check(x, y, tab, h=[0, 0]):
    ini = tab[h[1]][h[0]]
    tab[h[1]][h[0]] = 'check podmiana'
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if tab[j][i] == '■':
                tab[h[1]][h[0]] = ini
                return 0
    tab[h[1]][h[0]] = ini
    return 1


# sprawdzanie czy dokoła pola (x, y) jest pole z statkiem + może pominąć jedną kratkę h (potrzebne do funkcji rand)

def generate(n, ship):  # n wymiar planszy, ship liczba statków o konkretnym wymiarze
    alphabet = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                'm': 13, 'n': 14, 'o': 15, 'p': 16,
                'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}
    tab = create(n + 2)
    n_r = range(1, len(tab) - 1)


    j = len(ship)
    while j > 0:
        for i in range(0, ship[j - 1]):  # liczba statków
            a = 2


            print_board(tab)
            while True:
                data = input("Wpisz koordynaty pierwszej komórki statku (np. c6):\n Powrót - wpisz esc\n")
                if data == "esc":
                    return 1
                try:
                    y = int(data[1:])
                    x = alphabet[data[0]]
                except:
                    print("Koordynaty podane nieprawidlowo! Sprobuj ponownie:")
                    continue
                if x in n_r and y in n_r:
                    if check(x, y, tab) == 0 or tab[y][x] != '□' or four_multiples_check(x, y, j, tab, n) == 1:
                        print("Nieprawidłowe pole! Sprobuj ponownie:")
                        continue
                    else:
                        break
                else:
                    print("Koordynaty podane nieprawidlowo! Sprobuj ponownie:")
                    continue

            if j > 1:
                while a != 0:
                    data = input("Wpisz stronę w którą ma się obrócić okręt(↑:w, ←:a, ↓:s, →:d):\n")
                    a = multiple_check(x, y, j, data, tab, n)
                    if a == 1:
                        print("Kierunek podany nieprawidlowo! Sprobuj ponownie:")
                multiple_check(x, y, j, data, tab, n, 1)


            tab[y][x] = '■'
        j = j - 1

    return tab

def multiple_check(x, y, j, data, tab, n, case = 0):
    if data == 'w' and y - j > 1:
        for a in range(1, j):
            if check(x, y - a, tab, [x, y - a + 1]) == 0:
                return 1
            if case != 0:
                tab[y - a][x] = '■'


        return 0

    elif data == 'a' and x - j > 1:
        for a in range(1, j):
            if check(x - a, y, tab, [x - a + 1, y]) == 0:
                return 1
            if case != 0:
                tab[y][x - a] = '■'
        return 0

    elif data == 's' and y + j < n +2 :
        for a in range(1, j):
            if check(x, y + a, tab, [x, y + a - 1]) == 0:
                return 1
            if case != 0:
                tab[y + a][x] = '■'
        return 0

    elif data == 'd' and x + j < n +2:
        for a in range(1, j):
            if check(x + a, y, tab, [x + a - 1, y]) == 0:
                return 1
            if case != 0:
                tab[y][x + a] = '■'
        return 0

    else:
        return 1

def four_multiples_check(x, y, j, tab, n):
    if multiple_check(x, y, j, 'w', tab, n) == 0:
        return 0
    if multiple_check(x, y, j, 's', tab, n) == 0:
        return 0
    if multiple_check(x, y, j, 'a', tab, n) == 0:
        return 0
    if multiple_check(x, y, j, 'd', tab, n) == 0:
        return 0
    return 1


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