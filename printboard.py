# Plik na wszystkie funkcje zwiazane z wypisywaniem na ekran

import os
import pygame
import math


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

colours = {
        "□": pygame.color.Color("blue"),
        "■": pygame.color.Color("gray"),
        "░": pygame.color.Color("red"),
        "x": pygame.color.Color("lightcyan"),
        "background": pygame.color.Color("navy"),
        "text": pygame.color.Color("white")

    }

class Display:                                              # Klasa Display czyli frontend to co gracz widzi, spawn statkow wybuchy itp


    def __init__(self, board_size=10, margin=15):
        self.board_size = board_size
        self.cell_size = 2 * margin
        self.margin = margin

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Helvetica", self.margin)

        screen_width = 2 * self.cell_size * board_size + 3 * margin + self.board_size
        screen_height = self.cell_size * board_size + 4 * margin + self.board_size
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)




    def show(self, player_b, si_b):
        offset = self.margin * 2 + self.board_size * self.cell_size + self.board_size

        pygame.draw.rect(self.screen, "red",
                         [offset + self.margin + (self.board_size - 2) * self.cell_size + (self.board_size - 2),
                                       3 * self.margin + -1 * self.cell_size - 1 ,
                          self.cell_size, self.cell_size])
        font1 = pygame.font.SysFont("Helvetica", 2 * self.margin)
        label = font1.render("x", True, "black")
        text_rect = label.get_rect(center=(offset + self.margin + (self.board_size - 2) * self.cell_size + (self.board_size - 2) +int(self.cell_size / 2), 3 * self.margin + -1 * self.cell_size - 1 + int(self.cell_size / 2)))
        self.screen.blit(label, text_rect)

        if player_b is not None and si_b is not None:
            for y in range(self.board_size):
                for x in range(self.board_size):
                    pygame.draw.rect(self.screen, colours[si_b[y][x]] if player_b[y][x] in colours else "black",
                                     [self.margin + x * self.cell_size + x,
                                       3 * self.margin + y * self.cell_size + y,
                                      self.cell_size, self.cell_size])

                    pygame.draw.rect(self.screen, colours[player_b[y][x]] if player_b[y][x] in colours else "black",
                                     [ offset + self.margin + x * self.cell_size + x,
                                       3 * self.margin + y * self.cell_size + y,
                                      self.cell_size, self.cell_size])

    def show_menu(self, menu, upp_text = "STATKI"):
        opt_amount = len(menu)
        w, h = pygame.display.get_surface().get_size()
        dis = int((h - 4 *self.margin)/(2*opt_amount + 1))


        menufont = pygame.font.SysFont("Helvetica", 2*self.margin)
        label = menufont.render(upp_text, True, colours["text"])
        text_rect = label.get_rect(center=(w/2, 2 * self.margin))
        self.screen.blit(label, text_rect)


        for x in range(opt_amount):
            pygame.draw.rect(self.screen, "white",
                             [int(w/5),
                              4* self.margin +2 * x * dis,
                              int(w*3/5), dis])

            label = menufont.render(menu[x], True, "black")
            text_rect = label.get_rect(center=(w / 2, 4* self.margin +2 * x * dis + int((dis)/2)))
            self.screen.blit(label, text_rect)


    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Display.close()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                return x, y

            elif event.type == pygame.VIDEORESIZE:
                self.adjust()

        return None, None

    def exit(self, x, y):

        offset = self.margin * 2 + self.board_size * self.cell_size + self.board_size
        if (x - (offset + self.margin * 2)) // (self.cell_size + 1) == (self.board_size - 2) and (y - 3 * self.margin + 1) // (self.cell_size + 1) == -1:
            return True
        return False

    def get_box_cord(self):
        x, y = self.get_input()
        if x == None or y == None:
            return None, None

        if self.exit(x, y) == True:
            return -1, -1

        x = (x - self.margin) // (self.cell_size + 1)
        y = (y - 3 * self.margin) // (self.cell_size + 1)

        return x, y

    def menu_cord(self, menu):
        opt_amount = len(menu)
        x, y = self.get_input()
        if x == None or y == None:
            return None

        w, h = pygame.display.get_surface().get_size()
        dis = int((h - 4 *self.margin)/(2*opt_amount + 1))
        if x > w/5 and x < 4/5 * w:
            y = (y - 4* self.margin) // (dis)
            if y % 2 == 0:
                return y / 2 if  y / 2 in range(opt_amount) else None
        return None


    def show_text(self, text):
        self.hide_text()
        label = self.font.render(text, True, colours["text"])
        self.screen.blit(label, (self.margin, self.margin))

    def hide_text(self):
        pygame.draw.rect(self.screen, "black",
                         [0,
                          0,
                          2 * self.cell_size * self.board_size + 3 * self.margin, 3 * self.margin])

    def flip(self):
        pygame.display.flip()
        pygame.time.Clock().tick(60)



    @staticmethod
    def close():
        pygame.display.quit()
        pygame.quit()

    def adjust(self):
        w, h = pygame.display.get_surface().get_size()
        wmargin = math.floor((w - 2 * self.board_size)/(3 + 4 * self.board_size))
        hmargin = math.floor((h - self.board_size)/(4 + 2 * self.board_size))
        self.margin = hmargin if (hmargin <= wmargin) else wmargin
        self.cell_size = 2 * self.margin
        self.font = pygame.font.SysFont("Helvetica", 2 * self.margin)

    def clear(self):
        w, h = pygame.display.get_surface().get_size()
        pygame.draw.rect(self.screen, "black",
                         [0,
                          0,
                          w, h])


def colour_grid(self, colours, include_ships=True):
    grid = [[colours["water"] for _ in range(self.size)] for _ in range(self.size)]
    if include_ships:
        for ship in self.ships_list:
            for x, y in ship.coordinate_list:
                grid[y][x] = colours["ship"]
    for x, y in self.hits_list:
        grid[y][x] = colours["hit"]
    for x, y in self.misses_list:
        grid[y][x] = colours["miss"]
    return grid


