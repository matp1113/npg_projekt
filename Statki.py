import random
import numpy
import printboard as pb
import generateships as gs
import settings


def clearConsole():
    print('\n' * 50)

def sunk(x, y, tab):
    if check(x, y, tab) == 1:

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if tab[j][i] == '□':
                    tab[j][i] = 'x'

# zatapia (obrysowuje) daną kratkę

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

def shoot(tab, ifbot = False):
    alphabet = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                'm': 13, 'n': 14, 'o': 15, 'p': 16,
                'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

    if (~ifbot):
        y = 0
        x = 0
        n_r = range(1, len(tab) - 1)
        while True:
            data = input("Wpisz koordynaty strzalu (np. c6):\n")
            try:
                y = int(data[1:])
                x = alphabet[data[0]]
            except:
                print("Koordynaty podane nieprawidlowo! Sprobuj ponownie:")
                continue
            if x in n_r and y in n_r:
                if tab[y][x] == 'x' or tab[y][x] == '⛝':
                    print("W podane pole oddano już strzal! Sprobuj ponownie:")
                    continue
                else:
                    break
            else:
                print("Koordynaty podane nieprawidlowo! Sprobuj ponownie:")
                continue


    if tab[y][x] == '■':
        tab[y][x] = '⛝'
        a = wreck(x, y, tab, [x, y])
        if a == 0:
            sunk(x, y, tab)
        else:
            if tab[y - 1][x - 1] == '□':
                tab[y - 1][x - 1] = 'x'
            if tab[y - 1][x + 1] == '□':
                tab[y - 1][x + 1] = 'x'
            if tab[y + 1][x - 1] == '□':
                tab[y + 1][x - 1] = 'x'
            if tab[y + 1][x + 1] == '□':
                tab[y + 1][x + 1] = 'x'

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

    pb.print_board(tab)


# wypisuje to co widzi gracz

def player_board(size, ship):
    tab = create(size + 2)
    return (tab)


# generuje plansze gracza


def welcome(pack):
    print("Losowa plansza wcisnij 1", '\n', "Własna plansza wcisnij 2", '\n', "Ustawienia wcisnij 3")
    num = int(input())

    if num == 3:
        clearConsole()
        while settings.settings(pack) != 0:
            clearConsole()
        clearConsole()
        tab = welcome(pack)

    elif num == 1:
        i = 0
        tab = gs.rand(pack[1], pack[0])
        while tab == 0:
            tab = gs.rand(pack[1], pack[
                0])
            i = i + 1
            if i > 1000000: #maks milion powtórzeń
                print("Proszę o lepsze ustawienia!\n")
                i = 0
                settings.settings(pack)

        print(i)  # liczy ile razy się program odpalił
    elif num == 2:
        tab = player_board(pack[1], pack[0])
    return tab


# witam

if __name__ == '__main__':
    ship = [4, 3, 2, 1]
    size = 10  # rozmiar
    pack = [ship, size]  # zrobione jak wskaznik by settings miało dostęp

    tab = welcome(pack)
    pb.print_board(tab)


    bot = gs.rand(pack[1], pack[0])  # plansza dla bota w którą strzelamy
    while bot == 0:
        bot = gs.rand(pack[1],
                   pack[0])

    player_view(bot)

    i = 0  # 10 krotne wywołanie strzału dla testów
    while i != 10:  #todo strzały od bota
        shoot(bot)
        clearConsole()
        player_view(bot)
        i = i + 1

    pb.print_board(bot)
    #TODO wygrana

