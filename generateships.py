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

    for j in range(1, len(ship) + 1):  # kolejne wielkości statków
        for i in range(0, ship[j - 1]):  # liczba statków
            x = random.randint(1, n)
            y = random.randint(1, n)

            dir = twist(x, y, j, n)

            if dir == 0:
                return (0)

            tiles = check(x, y, tab)
            if tiles == 0:
                return (0)

            if (dir[0] > 0):  # sprawdzenie w którą stronę wylosowało
                for a in range(1, j):
                    tiles = check(x + a, y, tab, [x + a - 1, y])
                    if tiles == 0:
                        return (0)
                    tab[y][x + a] = '■'

            if (dir[0] < 0):
                for a in range(1, j):
                    tiles = check(x - a, y, tab, [x - a + 1, y])
                    if tiles == 0:
                        return (0)
                    tab[y][x - a] = '■'

            if (dir[1] > 0):
                for a in range(1, j):
                    tiles = check(x, y + a, tab, [x, y + a - 1])
                    if tiles == 0:
                        return (0)
                    tab[y + a][x] = '■'

            if (dir[1] < 0):
                for a in range(1, j):
                    tiles = check(x, y - a, tab, [x, y - a + 1])
                    if tiles == 0:
                        return (0)
                    tab[y - a][x] = '■'

            tab[y][x] = '■'

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
