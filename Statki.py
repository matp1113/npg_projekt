import random
import numpy
import printboard as pb
import generateships as gs
import settings




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


def shoot(tab, ifbot=False, x = 0, y = 0):
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
                return 1
            else:
                print("Okręt przeciwnika trafiony! Oddaj kolejny strzał!\n")


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

def welcomemenu(ekran, menu):
    while True:
        ekran.flip()
        ekran.show_menu(menu)
        num = ekran.menu_cord(menu)
        if num != None:
            ekran.clear()
            break
    return (num)

def newwelcome(ekran, pack, menu =["Gra z losową planszą", "Gra z własną planszą", "Ustawienia", "Szybka Gra", "Zasady Gry"]):
    num = welcomemenu(ekran, menu)
    i = 0
    tab = []

    while True:
        if num == 0:
            i = 0
            if False if False in [el == 0 for el in pack[0]] else True:
                num = 2
                i = -1
                continue
            tab = gs.rand(pack[1], pack[0])
            while tab == 0:
                tab = gs.rand(pack[1], pack[0])
                i = i + 1
                if i > 1000000:  # maks milion powtórzeń
                    num = 2
                    break
            if tab != 0:
                print("Wylosowana dla Ciebie plansza:\n") #TODO można to zrobić
                pb.print_board(tab)
                # input("\nWpisz dowolną wartość, aby rozopocząć grę.\n")
                break

        elif num == 1:
            tab = gs.generate(pack[1], pack[0])
            if tab == 1:
                num = welcomemenu(ekran, menu)
            else:
                break

        elif num == 2:
            if i > 1000000:
                print("Proszę o lepsze ustawienia!\n") #TODO tekst
                i = 0
            elif i == -1:
                print("Proszę wybrać rozmiary statków!\n") #TODO tekst
                i = 0
            else:
                pb.clear_console()
            while settings.settings(pack) != 0:
                pb.clear_console()
            pb.clear_console()
            num = settings.print_main_menu()

        elif num == 3:
            i = 0
            pack[0] = [2, 2, 1]
            pack[1] = 5
            tab = gs.rand(pack[1], pack[0])
            while tab == 0:
                tab = gs.rand(pack[1], pack[0])
                i = i + 1
                if i > 1000000:  # maks milion powtórzeń
                    print("Proszę o lepsze ustawienia!\n") #TODO tekst
                    i = 0
                    num = 2
                    break
            if tab != 0:
                pb.clear_console()
                print("Wylosowana dla Ciebie plansza:\n") #TODO można to zrobić
                pb.print_board(tab)
                #input("Wpisz dowolną wartość, aby rozopocząć grę.\n")
                break

        elif num == 4:
            pb.clear_console()
            data = ''
            while data != 'esc':
                data = settings.print_rules() #TODO zrób to
            pb.clear_console()
            num = settings.print_main_menu()

        elif num == "esc": #TODO zrób to
            exit(0)

    return tab


# witam

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
                #input("\nWpisz dowolną wartość, aby rozopocząć grę.\n")
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


def trytoshoot(tab, ekran, size):
    x, y = ekran.get_box_cord()
    n_r = range(1, size + 1)
    if x == -1 and y == -1:
        print("tak")
        return None, None #jak klikniesz x

    elif x in n_r and y in n_r and tab[y][x] != 'x' and tab[y][x] != '░':
        a = shoot(tab, False, x, y)
        if a == 1:
            return True, True #trafiony, nastepny strzał
        else:
            return True, 0 #nietrafiony, bez nastepnego strzału
    else:
        return False, 0 #brak strzału

if __name__ == '__main__':

    pack = [[4, 3, 2, 1], 10]  # podstawowe ustawienia
    running = True
    menu = ["Gra z losową planszą", "Gra z własną planszą", "Ustawienia", "Szybka Gra", "Zasady Gry"]



    while running:
        ekran = pb.Display(pack[1] + 2)

        tab = newwelcome(ekran, pack)
    
        bot = gs.rand(pack[1], pack[0])  # plansza dla bota w którą strzelamy
        while bot == 0:
            bot = gs.rand(pack[1], pack[0])

    
        player_shoots = 0  # liczebie strzałów
        bot_shoots = 0
        ekran = pb.Display(pack[1] + 2)
        wt = wygrana(tab)
        wb = wygrana(bot)
        end = 0
        licznik = 0

        first_shoot = random.randint(0, 1)
        if first_shoot == 0:
            pb.print_both_boards(tab, player_view(bot))
            print("Rozpoczynasz!\n")
        else:
            print("Przeciwnik rozpoczął!\n")
            if wt == 0 and wb == 0:
                target = where_to_shoot(tab)
                while wt == 0 and shoot(tab, True, target[1], target[0]) == 1:
                    wt = wygrana(tab)
                    if wt == 0:
                        target = where_to_shoot(tab)
                bot_shoots += 1




        while  end == 0:
            ekran.flip()
            ekran.show_text("Wybierz pole do strzału")
            strike = [0, 0]

            if wb == 0:
                strike = trytoshoot(bot, ekran, pack[1])

                if strike[0] == None and strike[1] == None: #wcisniecie x
                    ekran.clear()
                    break

            if wt == 0 and wb == 0 and strike[0]:
                wb = wygrana(bot)
                if wb == 0 and strike[1]:
                    continue
                player_shoots += 1

                target = where_to_shoot(tab)
                while wt == 0 and wb == 0 and shoot(tab, True, target[1], target[0]) == 1:
                    wt = wygrana(tab)
                    if wt == 0:
                        target = where_to_shoot(tab)
                    bot_shoots += 1
                bot_shoots += 1
                wb = wygrana(bot)
                wt = wygrana(tab)

            if wt == 0 and wb == 0:
                ekran.show(tab, player_view(bot))


            if wt != 0 or wb != 0:
                ekran.show(tab, bot)
                licznik += 1
                if wt == 1:
                    ekran.show_text("Komputer wygrał w " + str(bot_shoots) + " salwach!")

                if wb == 1:
                    ekran.show_text(str("Wygrałeś w " + str(player_shoots) + " salwach! Gratuluję!"))

                if licznik > 200:
                    end = 1
                    ekran.clear()
                    break




        a = welcomemenu(ekran, ["Wyjście", "Reset"])
        while a != 1 and a != 0:
            a = welcomemenu(ekran, ["Wyjście", "Reset"])
            # nie wyłącza się od razu po końcu
        if a == 0:
            break
        if a == 1:
            pb.clear_console()
            pack[0] = [4, 3, 2, 1]
            pack[1] = 10
            continue
    ekran.close()
    exit(0)
