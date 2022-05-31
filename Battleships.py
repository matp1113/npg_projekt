import pygame
import random
from enum import Enum
from abc import ABC
from itertools import zip_longest

class Direction(Enum):
    NTH = 0
    EAST = 1
    STH = 2
    WEST = 3

    def next(self):
        return Direction((self.value + 1) % 4)

class Ship:
    def __init__(self, x, y, d, l):
        self.location = (x,y)
        self.direction = d                          #Inicjalizuje klase Statek(tu ship) ktora okresla podstawowe zasady tworzenia
        self.length = l                             # nowych statków


    def coordinate_list(self):
        x, y = self.location
        if self.location == Direction.NTH:
            return ((x, y - i) for i in range(self.length))
        if self.location == Direction.EAST:
            return ((x + i, y) for i in range(self.length))             #Tworze liste, ktora przetrzymuje koordynaty statkow
        if self.location == Direction.STH:                                  # ktore zostana pozniej dodane
            return ((x, y + i) for i in range(self.length))
        if self.location == Direction.WEST:
            return ((x - i, y) for i in range(self.length))
    def rotate(self):
        self.direction = self.direction.next

class Board(ABC):
    def __init__(self, size = 10, ship_sizes = [2,3,3,4,6]):
        self.size = size
        self.ship_sizes = ship_sizes                                #Inicjalizuje klase tablicy(tu Board) ktora okresla ogolne wlasciwosci statkow
        self.ships_list = []
        self.hits_list = []
        self.misses_list = []
    def is_valid(self, ship):
        for x, y in ship.coordinate_list:                               #kolejne metody klasy to dodawanie i usuwanie statkow z calej gry
            if x < 0 or y < 0 or x >= self.size or y >= self.size:
                return False
        for otherShip in self.ships_list:
            if self.ships_overlap(ship, otherShip):
                return False
        return True
    def add_ship(self, ship: Ship):
        if self.is_valid(ship):
            self.ships_list.append(ship)
            return True
        else:
            return False
    def remove_ship(self, ship):
        self.ships_list.remove(ship)
    def ships_overlap(self, ship1, ship2):
        for ship1_coord in ship1.coordinate_list:
            for ship2_coord in ship2.coordinate_list:
                if ship1_coord == ship2_coord:
                    return True
        return False

    def get_ship(self, x, y):
        for ship in self.ships_list:
            if (x, y) in ship.coordinate_list:
                return ship
        return None

    def valid_target(self, x, y):
        if x not in range(self.size) or y not in range(self.size):
            return False
        for previous_shot in self.misses_list + self.hits_list:
            if (x, y) == previous_shot:
                return False
        return True

    def shoot(self, x, y):
        if not self.valid_target(x, y):
            return False
        for ship in self.ships_list:
            for ship_coordinate in ship.coordinate_list:
                if (x, y) == ship_coordinate:
                    return True
        self.misses_list.append((x, y))
        return True

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

    def gameover(self):
        for ship in self.ships_list:
            for coordinate in ship.coordinate_list:
                if coordinate not in self.hits_list:
                    return False
        return True

class PlayerBoard(Board):                                           #Klasa tablicy gracza definiuje co gracz bedzie widzial u siebie na monitorze

    def __init__(self, display, board_size, ship_sizes):
        super().__init__(board_size, ship_sizes)
        self.display = display

        direction = Direction.NTH
        while True:
            self.display.show(None, self)

            if self.ship_to_place:
                text = 'Click where you want your {}-long ship to be:'.format(
                    self.ship_to_place)
            else:
                text = 'Click again to rotate a ship, or elsewhere if ready.'
            self.display.show_text(text, lower=True)

            x, y = self.display.get_input()
            if x is not None and y is not None:
                ship = self.get_ship(x, y)
                if ship:
                    self.remove_ship(ship)
                    ship.rotate()
                    if self.is_valid(ship):
                        self.add_ship(ship)
                elif self.ship_to_place:
                    ship = Ship(x, y, direction, self.ship_to_place)
                    if self.is_valid(ship):
                        self.add_ship(ship)
                    else:
                        direction = direction.next
                else:
                    break

                if self.is_valid(ship):
                    self.add_ship(ship)

            Display.flip()

    def ship_to_place(self):
        placed_sizes = sorted(ship.length for ship in self.ships_list)
        sizes = sorted(self.ship_sizes)
        for placed, to_place in zip_longest(placed_sizes, sizes):
            if placed != to_place:
                return to_place
        return None

class AIBoard(Board):                                       #Klasa tablicy AI
    def __init__(self, board_size, ship_sizes):
        super().__init__(board_size, ship_sizes)
        for ship_length in self.ship_sizes:
            ship_added = False
            while not ship_added:
                x = random.randint(0, board_size - 1)
                y = random.randint(0, board_size - 1)
                ship_direction = random.choice(list(Direction))
                ship = Ship(x, y, ship_direction, ship_length)
                if self.is_valid(ship):
                    self.add_ship(ship)
                    ship_added = True

class Display:                                              # Klasa Display czyli frontend to co gracz widzi, spawn statkow wybuchy itp
    colours = {
        "water": pygame.color.Color("blue"),
        "ship": pygame.color.Color("gray"),
        "hit": pygame.color.Color("red"),
        "miss": pygame.color.Color("lightcyan"),
        "background": pygame.color.Color("navy"),
        "text": pygame.color.Color("white")
    }

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

    def show(self, upper_board, lower_board, include_top_ships=False):
        if upper_board is not None:
            upper_colours = upper_board.colour_grid(
                self.colours, include_top_ships)

        if lower_board is not None:
            lower_colours = lower_board.colour_grid(
                self.colours)

        self.screen.fill(Display.colours["background"])
        for y in range(self.board_size):
            for x in range(self.board_size):

                if upper_board is not None:
                    pygame.draw.rect(self.screen, upper_colours[y][x],
                                     [self.margin + x * self.cell_size,
                                      self.margin + y * self.cell_size,
                                      self.cell_size, self.cell_size])

                if lower_board is not None:
                    offset = self.margin * 2 + self.board_size * self.cell_size
                    pygame.draw.rect(self.screen, lower_colours[y][x],
                                     [self.margin + x * self.cell_size,
                                      offset + y * self.cell_size,
                                      self.cell_size, self.cell_size])

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Display.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y = y % (self.board_size * self.cell_size + self.margin)
                x = (x - self.margin) // self.cell_size
                y = (y - self.margin) // self.cell_size
                if x in range(self.board_size) and y in range(self.board_size):
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

    def flip(cls):
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def close(cls):
        pygame.display.quit()
        pygame.quit()


class Game:                                                     #Trzewia gry

    def __init__(self, display, size=10, ship_sizes=[6, 4, 3, 3, 2]):
        self.display = display
        self.board_size = size
        self.ai_board = AIBoard(size, ship_sizes)
        self.player_board = PlayerBoard(display, size, ship_sizes)

    def play(self):
        print("Play starts")
        while not self.gameover:
            if self.player_shot():
                self.ai_shot()
            self.display.show(self.ai_board, self.player_board)
            self.display.show_text("Click to guess:")
            Display.flip()

    def ai_shot(self):
        x, y = -1, -1
        while not self.player_board.valid_target(x, y):
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
        self.player_board.shoot(x, y)

    def player_shot(self):
        x, y = self.display.get_input()
        if self.ai_board.valid_target(x, y):
            self.ai_board.shoot(x, y)
            return True
        else:
            return False


    def gameover(self):
        if self.ai_board.gameover:
            print("Congratulations you won")
            return True
        elif self.player_board.gameover:
            print("Congratulations you lost")
            return True
        else:
            return False


if __name__ == "__main__":
    while True:
        d = Display()
        Game(d).play()
        # Game(d, 2, [1,1]).play()
        d.close()

        response = input("Replay? y/n: ").lower()
        while response not in ['y', 'n']:
            response = input("Must be y or n: ")
        if response == 'n':
            print("Thanks try again! Goodbye.")
            break