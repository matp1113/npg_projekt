import random
import numpy
import printboard as pb
import generateships as gs
import settings


# import os


def clearConsole():
    print('\n' * 50)
    # os.system('cls' if os.name == 'nt' else 'clear') # w pycharmie daje mi kwadracik


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
        return 1

    ini = tab[h[1]][h[0]]
    tab[h[1]][h[0]] = 'wreck podmiana'  # zmienia wartośćaby schodząc w dół aby sie nie zapętlał
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if tab[j][i] == '░':
                a = a + wreck(i, j, tab, [i, j])

    if a != 0:
        tab[h[1]][h[0]] = ini  # przywraca wartość orginalną
        return 1

    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if tab[j][i] == '░':
                sunk(i, j, tab)

    tab[h[1]][h[0]] = ini  # przywraca wartość orginalną

    return a  # funkcja sumuje jedynki wszystko musi zwracać zera by okęt był zatopiony

# sprawdza czy statek jest zatopiony


def shoot(tab, ifbot=False):
    alphabet = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                'm': 13, 'n': 14, 'o': 15, 'p': 16,
                'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}
    y = 0
    x = 0

    if not ifbot:
        size = len(tab) - 1
        n_r = range(1, size)

        while True:
            data = input("Wpisz koordynaty strzalu (np. c6):\n")
            if data == "esc":
                global running
                running = False
                pb.clear_console()
                return 0
            try:
                y = int(data[1:])
                x = alphabet[data[0]]
            except:
                print("Koordynaty podane nieprawidlowo! Sprobuj ponownie:")
                continue
            if x in n_r and y in n_r:
                if tab[y][x] == 'x' or tab[y][x] == '░':
                    print("W podane pole oddano już strzal! Sprobuj ponownie:")
                    continue
                else:
                    break
            else:
                print("Koordynaty podane nieprawidlowo! Sprobuj ponownie:")
                continue

    elif ifbot:
        target = where_to_shoot(tab)
        x = target[1]
        y = target[0]

    global bot_shoots

    if tab[y][x] == '■':
        tab[y][x] = '░'
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

        if not ifbot:
            pb.clear_console()
            if a == 0 and wygrana(bot) == 0:
                print("Okręt przeciwnika zatopiony! Oddaj kolejny strzał!\n")
            elif wygrana(bot) == 1:
                print("Okręt przeciwnika zatopiony!\n")
                return 0
            else:
                print("Okręt przeciwnika trafiony! Oddaj kolejny strzał!\n")

        if ifbot and wygrana(tab) == 1:
            if bot_shoots >= 2:
                print("Przeciwnik oddał salwę, trafiając twoje okręty " + str(bot_shoots) + " razy!\n")
            elif bot_shoots == 1:
                print("Przeciwnik oddał salwę, trafiając twój okręt!\n")
            pb.print_both_boards(tab, bot)
            return 1

        return 1  # czy masz następny strzał

    elif tab[y][x] == '□':
        tab[y][x] = 'x'
        if not ifbot:
            pb.clear_console()
            print("Pudło!\n")
            return 0

    if ifbot:
        if bot_shoots >= 2:
            print("Przeciwnik oddał salwę, trafiając twoje okręty " + str(bot_shoots) + " razy!\n")
        elif bot_shoots == 1:
            print("Przeciwnik oddał salwę, trafiając twój okręt!\n")
        elif bot_shoots <= 0:
            print("Przeciwnik spudłował!\n")

        bot_shoots = 0

        return 0

    return 0

# strzela


def where_to_shoot(tab):
    x = 0
    y = 0
    size = len(tab)
    n_r = range(1, size)

    while tab[y][x] != '□' and tab[y][x] != '■':
        x = random.randint(1, size - 1)
        y = random.randint(1, size - 1)

    for q in n_r:
        for w in n_r:
            if tab[q][w] == '░':

                if tab[q + 1][w] == '░' or tab[q - 1][w] == '░':
                    if tab[q + 1][w] == '□' or tab[q + 1][w] == '■':
                        return [q + 1, w]
                    elif tab[q - 1][w] == '□' or tab[q - 1][w] == '■':
                        return [q - 1, w]

                elif tab[q][w + 1] == '░' or tab[q][w - 1] == '░':
                    if tab[q][w + 1] == '□' or tab[q][w + 1] == '■':
                        return [q, w + 1]
                    elif tab[q][w - 1] == '□' or tab[q][w - 1] == '■':
                        return [q, w - 1]

                if tab[q + 1][w] == '□' or tab[q + 1][w] == '■':
                    return [q + 1, w]
                elif tab[q][w + 1] == '□' or tab[q][w + 1] == '■':
                    return [q, w + 1]
                elif tab[q - 1][w] == '□' or tab[q - 1][w] == '■':
                    return [q - 1, w]
                elif tab[q][w - 1] == '□' or tab[q][w - 1] == '■':
                    return [q, w - 1]

    return [y, x]

# wybiera gdzie bot strzeli


def player_view(oldtab):
    tab = numpy.copy(oldtab)

    # for rows in tab:
    #    for cell in rows:
    #        if cell == '■':
    #            cell = '□' #idk dlaczego nie działa
    n_r = range(0, len(tab))

    for x in n_r:
        for y in n_r:
            if tab[y][x] == '■':
                tab[y][x] = '□'

    return tab

# wypisuje to co widzi gracz
# generuje plansze gracza


def welcome(pack):
    num = settings.print_main_menu()

    i = 0
    tab = []
    while True:
        if num == "1":
            i = 0
            if False if False in [el == 0 for el in pack[0]] else True:
                pb.clear_console()
                num = "3"
                i = -1
                continue
            tab = gs.rand(pack[1], pack[0])
            while tab == 0:
                tab = gs.rand(pack[1], pack[0])
                i = i + 1
                if i > 1000000:  # maks milion powtórzeń
                    pb.clear_console()
                    num = "3"
                    break
            if tab != 0:
                pb.clear_console()
                print("Wylosowana dla Ciebie plansza:\n")
                pb.print_board(tab)
                input("\nWpisz dowolną wartość, aby rozopocząć grę.\n")
                break
    
        elif num == "2":
            pb.clear_console()
            tab = gs.generate(pack[1], pack[0])
            if tab == 1:
                num = settings.print_main_menu()
            else:
                break
    
        elif num == "3":
            if i > 1000000:
                print("Proszę o lepsze ustawienia!\n")
                i = 0
            elif i == -1:
                print("Proszę wybrać rozmiary statków!\n")
                i = 0
            else:
                pb.clear_console()
            while settings.settings(pack) != 0:
                pb.clear_console()
            pb.clear_console()
            num = settings.print_main_menu()
    
        elif num == "4":
            i = 0
            pack[0] = [2, 2, 1]
            pack[1] = 5
            tab = gs.rand(pack[1], pack[0])
            while tab == 0:
                tab = gs.rand(pack[1], pack[0])
                i = i + 1
                if i > 1000000:  # maks milion powtórzeń
                    print("Proszę o lepsze ustawienia!\n")
                    i = 0
                    num = "3"
                    break
            if tab != 0:
                pb.clear_console()
                print("Wylosowana dla Ciebie plansza:\n")
                pb.print_board(tab)
                input("Wpisz dowolną wartość, aby rozopocząć grę.\n")
                break
                
        elif num == "5":
            pb.clear_console()
            data = ''
            while data != 'esc':
                data = settings.print_rules()
            pb.clear_console()
            num = settings.print_main_menu()
    
        elif num == "esc":
            exit(0)
    
        else:
            print("Proszę wybrać inny numer\n")
            num = input()
        
    return tab

# witam


def wygrana(tab):
    n_r = range(1, len(tab) - 1)

    for y in n_r:
        for x in n_r:
            if tab[y][x] == "■":
                return 0
    return 1


if __name__ == '__main__':
    ship = [4, 3, 2, 1]
    size = 10  # rozmiar
    pack = [ship, size]  # zrobione jak wskaznik by settings miało dostęp
    running = True
    
    while running:
        tab = welcome(pack)
    
        bot = gs.rand(pack[1], pack[0])  # plansza dla bota w którą strzelamy
        while bot == 0:
            bot = gs.rand(pack[1], pack[0])
    
        pb.clear_console()
    
        i = 0  # liczebie strzałów
        bot_shoots = 0

        first_shoot = random.randint(0, 1)
        if first_shoot == 0:
            pb.print_both_boards(tab, player_view(bot))
            print("Rozpoczynasz!\n")
        else:
            print("Przeciwnik rozpoczął!\n")


        wt = 0
        wb = 0

        while wt == 0 and wb == 0:  # chyba można by trochę zoptymalizować z wyskakiwaniem

            if first_shoot != 1:
                while wb == 0 and wt == 0 and shoot(bot) == 1:  # Gracz trafił
                    print (wb, wt)
                    wb = wygrana(bot)
                    pb.print_both_boards(tab, player_view(bot))


            wb = wygrana(bot) #idk dlaczego ale musi tu być

            if not running:
                break
    
            while wb == 0 and wt == 0 and shoot(tab, True) == 1:  # Bot trafił
                wt = wygrana(tab)
                bot_shoots += 1

            i = i + 1
            if first_shoot == 1:
                first_shoot = 0

            pb.print_both_boards(tab, player_view(bot))

        if not running:
            running = True
            continue
    
        if wt == 1:
            print("Komputer wygrał w", i, "salwach!\n")
    
        if wb == 1:
            print("Wygrałeś w ", i, "salwach!\n\nGratuluję!\n")
        
        a = ''
        while a != 'esc' and a != 'reset':
            a = input("\n\nWpisz reset, aby zagrać od nowa.\nWpisz esc, aby zamknąć program.\n\n")
            # nie wyłącza się od razu po końcu
        if a == 'esc':
            break
        if a == 'reset':
            pb.clear_console()
            continue

    exit(0)
