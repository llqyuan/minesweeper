CHECK_FONT_MSG = """
This is a text based game.\n
+--+--+--+--+--+
|  |  |  |  |  |
+--+--+--+--+--+\n
The above should look like a line of five squares.
If you do not see the shape, please change your font accordingly.
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

