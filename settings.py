import numpy


def settings(pack):
    num = print_settings(pack)

    while True:
        if num == '1' or num == '2' or num == '3' or num == '4':
            pack[0] = ships_change(pack[0], int(num))
            return 1

        elif num == '5':
            num = int(input("Podaj rozmiar okrętu, którego liczbę chcesz zmodyfikować:\n"))
            pack[0] = ships_change(pack[0], int(num))
            return 1

        elif num == '6':
            while True:
                print("Docelowa wartość:")
                try:
                    x = int(input())
                except:
                    print("Podaj poprawną warość!")
                    continue
                if x > 25:
                    print("Maksymalna dozwolona wartość to 25!")
                    continue
                if x <= 2:
                    print("Za mała wartość")
                    continue
                pack[1] = x
                break
            return 1

        elif num == '7':
            pack[0] = [4, 3, 2, 1]
            pack[1] = 10
            return 1

        elif num == 'esc':
            return 0

        else:
            num = input("Podaj poprawną warość!")
            continue


# mapa ustawień (zmienia mapę lub odsyła do zmiany liczby statków

def ships_change(ship, num):
    new = numpy.zeros(num, dtype=int)

    if num >= len(ship) + 1:

        for x in range(0, len(ship)):
            new[x] = ship[x]

        print("Obecnie ustawiona liczba statków o wielkości", num, '-', 0)
    else:
        new = ship
        print("Obecnie ustawiona liczba statków o wielkości", num, '-', ship[num - 1])
    print("Docelowa wartość:")

    new[num - 1] = int(input())
    return (new)


# zmiany liczby statków


def print_main_menu() -> str:
    print("{:^50}\n".format("STATKI") + 50 * "=")
    menu = ("{:<40} wciśnij 1\n".format("Gra z losową planszą") +
            "{:<40} wciśnij 2\n".format("Gra z własną planszą") +
            "{:<40} wciśnij 3\n".format("Ustawienia") +
            "{:<40} wciśnij 4\n".format("Szybka Gra") +
            "{:<40} wciśnij 5\n".format("Zasady Gry")).replace("  ", " .")  # TODO: zrobic printowanie zasad (w nowej
                                                                            # funkcji - wywoływanej w welcome())
    
    print(menu)

    return input()


def print_settings(pack):
    print("{:^60}\n".format("USTAWIENIA") + 60 * "=")
    print("{:<50} wciśnij 1\n".format("Zmiana liczby okrętów o długości 1").replace("  ", " .") +
          "   Obecna wartość: " + (str(pack[0][0]) if len(pack[0]) >= 1 else '0') + '\n' +
          "{:<50} wciśnij 2\n".format("Zmiana liczby okrętów o długości 2").replace("  ", " .") +
          "   Obecna wartość: " + (str((pack[0])[1]) if len(pack[0]) >= 2 else '0') + '\n' +
          "{:<50} wciśnij 3\n".format("Zmiana liczby okrętów o długości 3").replace("  ", " .") +
          "   Obecna wartość: " + (str((pack[0])[2]) if len(pack[0]) >= 3 else '0') + '\n' +
          "{:<50} wciśnij 4\n".format("Zmiana liczby okrętów o długości 4").replace("  ", " .") +
          "   Obecna wartość: " + (str((pack[0])[3]) if len(pack[0]) >= 4 else '0') + '\n' +
          "{:<50} wciśnij 5\n".format("Dodawanie okrętów o własnej długości").replace("  ", " ."), end='')

    [print(el) if el != '' else print('', end='') for el in
     ([("   Okręty o długości " + str(i + 1) + ": " + str(pack[0][i]) if pack[0][i] > 0 else '')
       for i in range(4, len(pack[0]))] if len(pack[0]) > 4 else "")]

    print("{:<50} wciśnij 6\n".format("Modyfikacja rozmiaru planszy").replace("  ", " .") +
          "   Obecna wartość: " + str(pack[1]) + '\n' +
          "{:<50} wciśnij 7\n".format("Powrót do ustawień początkowych.").replace("  ", " .") +
          "{:<50} wpisz esc\n".format("Powrót do głównego menu.").replace("  ", " ."))

    return input()

