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

    if num > 0 and num < 5:
        pack[0] = ships_change(pack[0], num)
        return 1

    elif num == 5:
        num = int(input("jaką wartość chcesz zmienić?"))
        pack[0] = ships_change(pack[0], num)
        return 1

    elif num == 6:
        print("docelowa wartość")
        pack[1] = int(input())
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
    print("docelowa wartość:")

    new[num - 1] = int(input())
    return (new)


# zmiany liczby statków
