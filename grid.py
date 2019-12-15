import random


CHECK_FONT_MSG = "This is a text-based game.\n\n"\
                 "+--+--+--+--+--+\n"\
                 "|  |  |  |  |  |\n"\
                 "+--+--+--+--+--+\n\n"\
                 "The above shape should look like a line of five squares.\n"\
                 "If you do not see the shape, please change your font\n"\
                 "accordingly (Deja Vu Sans Mono is a good bet).\n\n"\
                 "Press enter when you are ready.\n"

HOW_TO_PLAY_MSG = \
                "\nHOW TO PLAY:\n\n"\
                "Enter the coordinates of the square you want to reveal.\n\n"\
                "The coordinates should be of the form 'x,y', where x \n"\
                "denotes the column number and y denotes the row number.\n"\
                "For instance, 1,2 denotes the upper left corner on\n"\
                "a 2x2 grid.\n\n"\
                "If you reveal a square with a bomb, it's game over.\n\n"\
                "(Press enter to continue)"

COMMAND_LIST_MSG = \
                 "COMMANDS:\n\n"\
                " * To see these instructions again later, enter 'help'.\n"\
                " * To flag a square, enter your coordinate preceded by 'flag'"\
                "\n   ('flag 1,1').\n"\
                " * To unflag a square, enter your coordinate preceded by\n"\
                "   'unflag' ('unflag 1,1').\n" \
                " * To reprint the grid, enter 'grid'.\n"\
                " * To see the meaning of a symbol on the grid, enter "\
                "'symbols'.\n" \
                " * To quit, enter 'quit'.\n\n"

INIT_GRID_SIZE_MSG = \
                   "\n~~~~~~~~~~~~~~~~~~~~~~~\n\n"\
                  "Default grid size is 15x15.\n\n" \
                  "To choose a different grid size, enter a natural number\n"\
                  "greater than or equal to 2. The grid will be of size nxn,\n" +\
                  "where n is your inputted number of choice. Excessively\n" \
                  "large numbers are not recommended, as the grid may be\n"\
                  "printed weirdly (this is a text based game, after all).\n\n"\
                  "To proceed with the default size, press enter (or\n"\
                  "enter anything else that isn't a natural number).\n\n"

IMPROPER_COORD_MSG = \
                   "\nThe coordinate must be of the form 'x,y', where\n"\
                    "x and y are natural numbers.\n\n"\
                    "To flag a square (eg. 1,1), enter 'flag 1,1'. To \n"\
                    "unflag the square 1,1, enter 'unflag 1,1'.\n"

COORD_OUT_OF_RANGE_MSG = \
                       "\nThat coordinate was out of range.\n"
SYMBOLS_MSG = \
            " * : Flagged square\n"\
            " - : No adjacent squares have a bomb\n"\
            " 2 : 2 adjacent squares have a bomb\n"\
            "XX : Revealed square has a bomb\n"


class Square:
    '''
    Fields:
     * is_revealed (Bool)
     * has_bomb (Bool)
     * is_flagged (Bool)
    '''
    def __init__(self, rev, bomb, flag):
        self.is_revealed = rev
        self.has_bomb = bomb
        self.is_flagged = flag


class Grid:
    
    def __init__(self):
        self.is_retry = False
        self.gridlist = None
        self.grid_dim = None


    def create_new_grid(self, dim, n=0.16):
        self.grid_dim = dim
        grid = []
        for i in range(dim * dim):
            grid.append(Square(False,
                               True if random.random() <= n else False,
                               False))
        self.gridlist = grid


    def read_and_store_preferred_grid_dimension(self):
        global INIT_GRID_SIZE_MSG
        ready = input(INIT_GRID_SIZE_MSG).strip()
        
        while ready.isnumeric():

            if int(ready) < 2:
                ready = input(
                    "\nPlease enter a higher number, that'd be too "
                    "trivial. ")\
                    .strip()

            elif 25 <= int(ready) < 50:

                check = input(
                    "\nThat's a pretty large number, you want to continue? "
                    "(y/n) ").strip()

                while check.lower() != "y" and check.lower() != "n":
                    check = input(
                        "I didn't understand that. Do you want to play with "
                        "a grid size of {0} by {0}? (Enter 'y' or 'n') "
                        .format(ready))\
                        .strip()

                if check.lower() == "y":
                    self.grid_dim = int(ready)
                    break
                
                else:
                    ready = input(INIT_GRID_SIZE_MSG).strip()

            elif 50 <= int(ready) < 100:
                check = input(
                    "\nThat's a REALLY large number, you want to continue? "
                    "(y/n) ")\
                    .strip()

                while check.lower() != "y" and check.lower() != "n":
                    check = input(
                        "\nI didn't understand that. Do you want to play "
                        "with a grid size of {0} by {0}? (Enter 'y' or 'n') "
                        .format(ready))\
                        .strip()

                if check.lower() == "y":
                    self.grid_dim = int(ready)
                    break

                else:
                    ready = input(INIT_GRID_SIZE_MSG).strip()

            elif int(ready) >= 100:
                ready = input(
                    "That's a bit ridiculous, now. Choose something lower than "
                    "that, please. (You can enter anything that isn't a natural "
                    "number at any time to proceed with the default 15x15 "
                    "board) ")\
                    .strip()


    def initialize_game(self):
        if not self.is_retry:
            global CHECK_FONT_MSG
            global HOW_TO_PLAY_MSG
            ready = input(CHECK_FONT_MSG)
            ready = input(HOW_TO_PLAY_MSG)

        self.read_and_store_preferred_grid_dimension()
        self.create_new_grid()


    def print_grid(self):
        s = ""

        column_label = "    "
        xlabel = 1
        while xlabel <= self.grid_dim:
            column_label += " " * (2 - len(str(xlabel))) # Note max 2 digits
            column_label += "{} ".format(xlabel)
            xlabel += 1

        s += column_label + "\n"

        ypos = 0
        while ypos < self.grid_dim:
            s += "   " + "+--" * self.grid_dim + "+\n"
            row_label = self.grid_dim - ypos
            s += " " * (2 - len(str(row_label)))
            s += "{} ".format(row_label)
            xpos = 0

            while xpos < self.grid_dim:

                s += "|"
                if self.gridlist[ypos * self.grid_dim + xpos].is_revealed:
                    
                    if self.gridlist[ypos * self.grid_dim + xpos].has_bomb:
                        s += "XX"
                        
                    else:
                        num_adj_bombs = self.adj_with_bombs(xpos, ypos)
                        if num_adj_bombs == 0:
                            s += "*-" if self.gridlist[ypos * self.grid_dim + xpos].is_flagged \
                                 else " -"
                            
                        else:
                            s += "{}{}".format(
                                "*" if self.gridlist[ypos * self.grid_dim + xpos].is_flagged
                                else " ",
                                num_adj_bombs)

                else:
                    s += "* " if self.gridlist[ypos * self.grid_dim + xpos].is_flagged \
                         else "  "

                xpos += 1

            s += "|"
            s += " {}\n".format(row_label)
            ypos += 1

        s += "   " + "+--" * self.grid_dim + "+\n"
        s += column_label + "\n"
        print(s)


    def adj_with_bombs(self, x, y):
        adjacent = [(x-1,y-1), (x,y-1), (x+1,y-1),
                    (x-1,y),            (x+1,y),
                    (x-1,y+1), (x,y+1), (x+1,y+1)]
        num_bombs = 0

        for pos in adjacent:
            x = pos[0]
            y = pos[1]
            if x in range(self.grid_dim) and y in range(self.grid_dim) and \
               self.gridlist[y * self.grid_dim + x].has_bomb:
                num_bombs += 1

        return num_bombs


    def reveal(self, xpos, ypos):
        self.gridlist[ypos * self.grid_dim + xpos].is_revealed = True

        if self.gridlist[ypos * self.grid_dim + xpos].has_bomb:
            return "bomb revealed"

        elif self.adj_with_bombs(xpos, ypos) == 0:
            adjacent = [ (xpos - 1,  ypos - 1),
                         (xpos,      ypos - 1),
                         (xpos + 1,  ypos - 1),
                         (xpos - 1,  ypos),
                         (xpos + 1,  ypos),
                         (xpos - 1,  ypos + 1),
                         (xpos,      ypos + 1),
                         (xpos + 1,  ypos + 1) ]
            adj_inrange = list(filter(lambda pos: 0 <= pos[0] < self.grid_dim \
                                                  and 0 <= pos[1] < self.grid_dim,
                                      adjacent))
            adj_not_revealed = list(
                filter(lambda pos:
                       not self.gridlist[pos[1] * self.grid_dim + pos[0]].is_revealed,
                       adj_inrange))
            for pos in adj_not_revealed:
                self.reveal(pos[0], pos[1])

