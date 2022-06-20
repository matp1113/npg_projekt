# Plik na wszystkie funkcje zwiazane z wypisywaniem na ekran

import os
import pygame


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


    def __init__(self, board_size=10, cell_size=30, margin=15):
        self.board_size = board_size
        self.cell_size = cell_size
        self.margin = margin

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Helvetica", 14)

        screen_width = self.cell_size * board_size + 2 * margin
        screen_height = 2 * self.cell_size * board_size + 3 * margin
        self.screen = pygame.display.set_mode(
            [screen_width, screen_height])
        pygame.display.set_caption("Battleships")

    def show(self, player_b, si_b):
        if player_b is not None and si_b is not None:
            for y in range(self.board_size):
                for x in range(self.board_size):
                    pygame.draw.rect(self.screen, colours[si_b[y][x]] if player_b[y][x] in colours else "black",
                                     [self.margin + x * self.cell_size,
                                      self.margin + y * self.cell_size,
                                      self.cell_size, self.cell_size])

                    offset = self.margin * 2 + self.board_size * self.cell_size
                    pygame.draw.rect(self.screen, colours[player_b[y][x]] if player_b[y][x] in colours else "black",
                                     [self.margin + x * self.cell_size,
                                      offset + y * self.cell_size,
                                      self.cell_size, self.cell_size])



    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Display.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y = y
                x = (x - self.margin) // self.cell_size
                y = (y - self.margin) // self.cell_size
                return x, y
        return None, None

    def show_text(self, text, upper=False, lower=False):
        x = self.margin
        y_up = x
        y_lo = self.board_size * self.cell_size + self.margin
        label = self.font.render(text, True, Display.colours["text"])
        if upper:
            self.screen.blit(label, (x, y_up))
        if lower:
            self.screen.blit(label, (x, y_lo))

    @staticmethod
    def flip():
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    @staticmethod
    def close():
        pygame.display.quit()
        pygame.quit()

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