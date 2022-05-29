import numpy


def settings(pack):
    print("modyfikacja liczby jedynek wcisnij 1")
    print("modyfikacja  liczby dwójek 2")
    print("modyfikacja liczby trójek 3")
    print("modyfikacja liczby czwórek 4")
    print("własne wielkosci statków wcisnij 5")
    print("modyfikacja rozmiaru planszy wcisnij 6")
    print("powrót 7")
    num = int(input())

    if 0 < num < 5:
        pack[0] = ships_change(pack[0], num)
        return 1

    elif num == 5:
        num = int(input("jaką wartość chcesz zmienić?"))
        pack[0] = ships_change(pack[0], num)
        return 1

    elif num == 6:
        while True:
            print("docelowa wartość- maks 25")
            x = int(input())
            if x > 25:
                print("wartość za duża")
                continue
            pack[1] = x
            break
        return 1

    elif num == 7:
        return 0


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
    print("docelowa wartość: ")

    new[num - 1] = int(input())
    return (new)


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


# zmiany liczby statków
