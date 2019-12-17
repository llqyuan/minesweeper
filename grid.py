import random


CHECK_FONT_MSG = """
This is a text based game.\n
+--+--+--+--+--+
|  |  |  |  |  |
+--+--+--+--+--+\n
The above should look like a line of five squares.
If you do not see the shape, please change your font until you do.
Press enter when you are ready.
"""

HOW_TO_PLAY_MSG = """
HOW TO PLAY:

Enter the coordinates of the square you want to reveal.\n
The coordinates should be of the form "x, y", where x 
denotes the column number and y denotes the row number.
For instance, 1,2 denotes the upper left corner on a 2x2 grid.\n
If you reveal a square with a bomb, it's game over.\n
(Press enter to continue)
"""

COMMAND_LIST_MSG = """
COMMANDS:

 * To see these instructions again later, enter "help".
 * To flag a square, enter your coordinate preceded by "flag"
   ("flag 1,1").
 * To unflag a square, enter your coordinate preceded by "unflag"
   ("unflag 1,1")
 * To reprint the grid, enter "grid".
 * To see the meaning of a symbol on the grid, enter "symbols".
 * To ask for a hint, enter "hint".
 * To quit, enter "quit".
 
"""

INIT_GRID_SIZE_MSG = """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default grid size is 15x15.
To choose a different grid size, enter a natural number
greater than or equal to 2. The grid will be of size nxn, where
n is your number of choice. Excessively large numbers are not
recommended, as the grid may be printed weirdly (this is a text
based game, after all).

To proceed with the default size, press enter (or enter anything
that isn't a natural number).

"""

IMPROPER_COORD_MSG = """
The coordinate must be of the form "x,y", where x and y are natural numbers.

To flag a square (eg. 1,1), enter "flag 1,1". To unflag the square,
enter "unflag 1,1".

"""

COORD_OUT_OF_RANGE_MSG = """
That coordinate was out of range.
"""

SYMBOLS_MSG = """
 * : Flagged square
 - : No adjacent squares have a bomb
 2 : 2 adjacent squares have a bomb
XX : Revealed square has a bomb
"""


class _Square(object):
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


class Grid(object):
    
    def __init__(self):
        self.is_retry = False
        self.gridlist = None
        self.dim = None
        self.revealed = 0
        self.possible = 0


    def __create_new_grid(self, n=0.16):
        """
        Sets self.gridlist to a newly generated grid of dimension self.dim. Each square has a
        probability n of having a bomb.

        :param n: float
        :return: None
        """
        grid = []
        for i in range(self.dim * self.dim):
            grid.append(_Square(False,
                                True if random.random() <= n else False,
                                False))
        self.gridlist = grid


    def __read_and_store_preferred_grid_dimension(self):
        """
        Reads input and sets self.dim.
        """
        global INIT_GRID_SIZE_MSG
        ready = input(INIT_GRID_SIZE_MSG).strip()
        self.dim = 15
        
        while ready.isnumeric():

            if int(ready) < 2:
                ready = input(
                    "\nPlease enter a higher number, that'd be too "
                    "trivial. ")\
                    .strip()

            elif 25 <= int(ready) < 50:

                check = input(
                    "\nThat's a pretty large number, you want to continue? "
                    "(y/n) ").strip().lower()

                while check != "y" and check != "n":
                    check = input(
                        "I didn't understand that. Do you want to play with "
                        "a grid size of {0} by {0}? (Enter 'y' or 'n') "
                        .format(ready))\
                        .strip().lower()

                if check == "y":
                    self.dim = int(ready)
                    break
                
                else:
                    ready = input(INIT_GRID_SIZE_MSG).strip()

            elif 50 <= int(ready) < 100:
                check = input(
                    "\nThat's a REALLY large number, you want to continue? "
                    "(y/n) ")\
                    .strip().lower()

                while check != "y" and check != "n":
                    check = input(
                        "\nI didn't understand that. Do you want to play "
                        "with a grid size of {0} by {0}? (Enter 'y' or 'n') "
                        .format(ready))\
                        .strip().lower()

                if check == "y":
                    self.dim = int(ready)
                    break

                else:
                    ready = input(INIT_GRID_SIZE_MSG).strip()

            elif int(ready) >= 100:
                ready = input(
                    "That's a bit ridiculous now. Choose something lower than "
                    "that, please. (You can enter anything that isn't a natural "
                    "number at any time to proceed with the default 15x15 "
                    "board) ")\
                    .strip()

            else:
                self.dim = int(ready)
                break


    def initialize_game(self):
        """
        Initializes the game by reading and storing the player's preferred grid
        dimension, and creating the new grid. Also resets self.possible and self.revealed.
        """
        if not self.is_retry:
            global CHECK_FONT_MSG
            global HOW_TO_PLAY_MSG
            global COMMAND_LIST_MSG
            ready = input(CHECK_FONT_MSG)
            ready = input(HOW_TO_PLAY_MSG)
            ready = input(COMMAND_LIST_MSG)

        self.__read_and_store_preferred_grid_dimension()
        self.__create_new_grid()

        self.possible = 0
        self.revealed = 0
        for square in self.gridlist:
            if not square.has_bomb:
                self.possible += 1


    def print_grid(self):
        """
        Prints the grid.
        """
        s = ""

        column_label = "    "
        xlabel = 1
        while xlabel <= self.dim:
            column_label += " " * (2 - len(str(xlabel))) # Note max 2 digits
            column_label += "{} ".format(xlabel)
            xlabel += 1

        s += column_label + "\n"

        ypos = 0
        while ypos < self.dim:
            s += "   " + "+--" * self.dim + "+\n"
            row_label = self.dim - ypos
            s += " " * (2 - len(str(row_label)))
            s += "{} ".format(row_label)
            xpos = 0

            while xpos < self.dim:

                s += "|"
                
                if self.gridlist[ypos * self.dim + xpos].is_revealed and \
                   self.gridlist[ypos * self.dim + xpos].has_bomb:
                    
                    s += "XX"

                elif self.gridlist[ypos * self.dim + xpos].is_revealed:
                    
                    num_adj_bombs = self.__adj_with_bombs(xpos, ypos)
                    
                    if num_adj_bombs == 0:
                        s += "*-" \
                             if self.gridlist[ypos * self.dim + xpos].is_flagged \
                             else " -"

                    else:
                        s += "{}{}".format(
                            "*" \
                            if self.gridlist[ypos * self.dim + xpos].is_flagged \
                            else " ",
                            num_adj_bombs)

                else:
                    s += "* " \
                         if self.gridlist[ypos * self.dim + xpos].is_flagged \
                         else "  "

                xpos += 1

            s += "|"
            s += " {}\n".format(row_label)
            ypos += 1

        s += "   " + "+--" * self.dim + "+\n"
        s += column_label + "\n"
        print(s)


    def __adj_with_bombs(self, x, y):
        """
        Returns the number of squares adjacent to (x, y) (0,0 is top left) which have bombs

        :param x: int. Must be in range
        :param y: int. Must be in range
        :return: int
        """
        adjacent = [(x-1,y-1), (x,y-1), (x+1,y-1),
                    (x-1,y),            (x+1,y),
                    (x-1,y+1), (x,y+1), (x+1,y+1)]
        num_bombs = 0

        for pos in adjacent:
            xnew = pos[0]
            ynew = pos[1]
            if xnew in range(self.dim) and ynew in range(self.dim) and \
               self.gridlist[ynew * self.dim + xnew].has_bomb:
                num_bombs += 1

        return num_bombs


    def reveal(self, xpos, ypos):
        """
        Reveals the position at xpos, ypos (0,0 at upper left).
        If there are no bombs in adjacent squares,recursively reveals adjacent
        spaces. If the position being revealed has a bomb, returns True;
        otherwise returns False.
        If this space is bombless and hasn't yet been revealed,
        increments self.revealed (for revealed bombless squares) by 1.

        :param xpos: int. Must be in range
        :param ypos: int. Must be in range
        :return: bool
        """

        if self.gridlist[ypos * self.dim + xpos].has_bomb:
            return True

        elif self.gridlist[ypos * self.dim + xpos].is_revealed:
            return False

        self.gridlist[ypos * self.dim + xpos].is_revealed = True
        self.revealed += 1

        if self.__adj_with_bombs(xpos, ypos) == 0:
            adjacent = [ (xpos - 1,  ypos - 1),
                         (xpos,      ypos - 1),
                         (xpos + 1,  ypos - 1),
                         (xpos - 1,  ypos),
                         (xpos + 1,  ypos),
                         (xpos - 1,  ypos + 1),
                         (xpos,      ypos + 1),
                         (xpos + 1,  ypos + 1) ]
            adj_inrange = list(filter(lambda pos: 0 <= pos[0] < self.dim \
                                                  and 0 <= pos[1] < self.dim,
                                      adjacent))
            adj_not_revealed = list(
                filter(lambda pos:
                       not self.gridlist[pos[1] * self.dim + pos[0]].is_revealed,
                       adj_inrange))
            for pos in adj_not_revealed:
                self.reveal(pos[0], pos[1])

        return False

