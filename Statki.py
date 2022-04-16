import random
import numpy
import printboard as pb

def clearConsole():
    print('\n' * 50)


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

def draw(tab):
    for x in tab:
        print(x)


# wypisuje plansze

def sunk(x, y, tab):
    if check(x, y, tab) == 1:

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if tab[j][i] == '□':
                    tab[j][i] = 'x'


# zatapia (obrysowuje) daną kratkę

def wreck(x, y, tab, h):
    a = 0  # funkcja sumuje jedynki wszystko musi zwracać zera by okęt był zatopiony
    if check(x, y, tab, h) != 1:
        return (1)

    ini = tab[h[1]][h[0]]
    tab[h[1]][h[0]] = 'wreck podmiana'  # zmienia wartośćaby schodząc w dół aby sie nie zapętlał
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if tab[j][i] == '⛝':
                a = a + wreck(i, j, tab, [i, j])

    if a != 0:
        tab[h[1]][h[0]] = ini  # przywraca wartość orginalną
        return 1

    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if tab[j][i] == '⛝':
                sunk(i, j, tab)

    tab[h[1]][h[0]] = ini  # przywraca wartość orginalną

    return a  # funkcja sumuje jedynki wszystko musi zwracać zera by okęt był zatopiony


# sprawdza czy statek jest zatopiony

def shoot(tab):
    x = int(input("podaj x"))  # todo wpisywanie liter zamiast liczb
    y = int(input("podaj Y"))

    if tab[y][x] == '■':
        tab[y][x] = '⛝'
        a = wreck(x, y, tab, [x, y])
        if a == 0:
            sunk(x, y, tab)

    elif tab[y][x] == '□':
        tab[y][x] = 'x'


# pobiera kordynaty z klawiatury i strzela

def player_view(oldtab):
    tab = numpy.copy(oldtab)

    # for rows in tab:
    #    for cell in rows:
    #        if cell == '■':
    #            cell = '□' #idk dlaczego nie działa

    for x in range(0, len(tab)):
        for y in range(0, len(tab)):
            if tab[y][x] == '■':
                tab[y][x] = '□'

    draw(tab)


# wypisuje to co widzi gracz

def player_board(size, ship):
    tab = create(size + 2)
    return (tab)


# generuje plansze gracza

def settings(pack):
    print("modyfikacja liczby jedynek wcisnij 1")
    print("modyfikacja  liczby dwójek 2")
    print("modyfikacja liczby trójek 3")
    print("modyfikacja liczby czwórek 4")
    print("własne wielkosci statków wcisnij 5")
    print("modyfikacja rozmiaru planszy wcisnij 6")
    print("powrót 7")
    num = int(input())

    if num > 0 and num < 5:
        pack[0] = ships_change(pack[0], num)
    elif num == 5:
        num = int(input("jaką wartość chcesz zmienić?"))
        pack[0] = ships_change(pack[0], num)
    elif num == 6:
        print("docelowa wartość")
        pack[1] = int(input())


# mapa ustawień (zmienia mapę lub odsyła do zmiany liczby statków

def ships_change(ship, num):
    new = numpy.zeros(num, dtype=int)

    if num >= len(ship) + 1:

        for x in range(0, len(ship)):
            new[x] = ship[x]

        print("liczba statków o wielkości", num, 0)
    else:
        new = ship
        print("liczba statków o wielkości", num, ship[num - 1])
    print("docelowa wartość:")

    new[num - 1] = int(input())
    clearConsole()
    return (new)


# zmiany liczby statków

def welcome(pack):
    print("Losowa plansza wcisnij 1", '\n', "Własna plansza wcisnij 2", '\n', "Ustawienia wcisnij 3")
    num = int(input())

    if num == 3:
        settings(pack)
        tab = welcome(pack)

    elif num == 1:
        tab = rand(pack[1], pack[0])
        while tab == 0:
            tab = rand(pack[1], pack[
                0])  # todo jak zadasz zbyt trudne ustawienia musi konczyć program w wszystkich takich pętlach z rand (może kolejna funkcja pośrednia)

    elif num == 2:
        tab = player_board(pack[1], pack[0])
    return tab


# witam

if __name__ == '__main__':
    ship = [4, 3, 2, 1]
    size = 10  # rozmiar
    pack = [ship, size]  # zrobione jak wskaznik by settings miało dostęp

    tab = welcome(pack)
    draw(tab)

    i = 0
    bot = rand(pack[1], pack[0])  # plansza dla bota w którą strzelamy
    while bot == 0:
        bot = rand(pack[1],
                   pack[0])  # algorytm który szuka możliwej kombinacji jak jest zbyt trudna lub niemożliwa to rip
        i = i + 1
    player_view(bot)
    print(i)  # liczy ile razy się program odpalił

    i = 0  # 10 krotne wywołanie strzału dla testów
    while i != 10:  # todo strzały od bota
        shoot(bot)
        clearConsole()
        player_view(bot)
        i = i + 1

    draw(bot)
    # todo wygrana
