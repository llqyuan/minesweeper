import random

print("To play, call play().")


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

    def __repr__(self):
        return "<rev, bomb, flag>"+\
               ": <{0.is_revealed}, {0.has_bomb}, {0.is_flagged}>"\
               .format(self)


'''
A Grid is a (listof (listof Square), where
  * each sublist is of the same length
  * the sublists are of the same length as the full list itself
    (that is, it represents a square grid)
'''

# ===============================================

def adj_with_bombs(G,x,y):
    '''
    Returns the number of adjacent spaces with bombs, given position
    (x,y) on grid G. (refers to position in list, ie. count from 0)

    adj_with_bombs: Grid Nat Nat -> Nat
    requires: x,y are valid positions in l
    '''
    adjacent = [[x-1,y-1], [x,y-1], [x+1,y-1],
                [x-1,y],            [x+1,y],
                [x-1,y+1], [x,y+1], [x+1,y+1]]
    num_bombs = 0
    dim = len(G)
    
    for pos in adjacent:
        pos_x = pos[0]
        pos_y = pos[1]
        if pos_x in range(dim) and pos_y in range(dim) and \
           G[pos_y][pos_x].has_bomb:
            num_bombs += 1

    return num_bombs


def print_grid(G):
    '''
    Prints G, assuming G represents a grid of size at least 1x1.

    Effects: Prints to the screen

    print_grid: Grid -> None
    '''
    dim = len(G) # note, square grid
    s=""

    # Column label
    column_label = "    "
    xlabel=1
    while xlabel<=dim:
        column_label += " "*(2-len(str(xlabel))) # Max grid size 99
        column_label += "{0} ".format(xlabel)
        xlabel += 1

    s += column_label + "\n"

    y = 0
    while y<dim:
        
        s = s + "   " + "+--"*dim + "+\n"
        ylabel = dim-y
        s = s + " "*(2-len(str(ylabel)))
        s = s + "{0} ".format(ylabel)
        x = 0
        
        while x<dim:
            
            s = s + "|"
            
            if G[y][x].is_revealed:

                flag_char = " "

                if G[y][x].is_flagged:
                    flag_char = "*"
            
                if G[y][x].has_bomb:
                    s = s + "XX"
                else:
                    adj_bombs = adj_with_bombs(G,x,y)
                    if adj_bombs==0:
                        s = s + "{0}-".format(flag_char)
                    else:
                        s = s + "{1}{0}".format(adj_bombs, flag_char)
            
            else:
                
                if G[y][x].is_flagged:
                    s = s + "* "
                else:
                    s = s + "  "

            x+=1

        s = s + "|"
        s = s + " {0}\n".format(ylabel) 

        y+=1
        
    s = s + "   " + "+--"*dim + "+\n"
    s = s + column_label + "\n"
    print(s)


def create_grid(dim,n=0.16):
    '''
    Returns a grid of dimension dim*dim. n is a float between 0 and 1
    that is involved in the calculation of whether or not a space has
    a bomb (the higher the number, the more likely any given space is
    to have a bomb).

    create_grid: Nat Float -> Grid
    requires: dim>=1
              0<n<1
    '''
    
    y=0
    g=[]
    while y<dim:
        x=0
        sub = []
        while x<dim:
            if random.random() <= n: # Initialize with bomb
                sub.append(Square(False, True, False))
            else:
                sub.append(Square(False, False, False))
            x+=1
        g.append(sub)
        y+=1
    return g


def reveal(G, in_x, in_y):
    '''
    Reveals the position represented by (in_x,in_y).
    If there are no bombs in any adjacent spaces, recursively reveals
    adjacent spaces. If the position being revealed has a bomb, return
    "bomb revealed".

    Effects: Mutates G

    reveal: Grid Nat Nat -> (anyof None "bomb revealed")
    requires: (in_x, in_y) represents a valid position
    '''
    dim = len(G)
    x = in_x - 1
    y = dim - in_y

    if G[y][x].has_bomb:
        G[y][x].is_revealed = True
        return "bomb revealed"

    elif adj_with_bombs(G,x,y)!=0:
        G[y][x].is_revealed = True
        return

    else:
    
        G[y][x].is_revealed = True
        adjacent = [ [in_x-1, in_y-1], [in_x, in_y-1], [in_x+1, in_y-1],
                     [in_x-1, in_y],                   [in_x+1, in_y],
                     [in_x-1, in_y+1], [in_x, in_y+1], [in_x+1, in_y+1] ]
        adj_inrange = list(filter(lambda pos: 1<=pos[0]<=dim \
                                              and 1<=pos[1]<=dim,
                                  adjacent))
        adj_notrevealed = list(
            filter(lambda pos: not G[dim-pos[1]][pos[0]-1].is_revealed,
                   adj_inrange))
        for pos in adj_notrevealed:
            reveal(G, pos[0], pos[1])


def play(is_retry=False):

    '''
    Executes the game. is_retry indicates whether or not the function
    was called through a replay of the game.

    Effects:
    * Reads from the keyboard
    * Prints to the screen

    play: Bool -> None
    '''

    def num_atleast_2(s):
        '''
        Returns True if s represents a natural number at least 2, and
        False otherwise.

        num_atleast_2: Str -> Bool
        '''
        return (s.isnumeric() and int(s)>=2)

    def convert(in_str):
        '''
        Returns a list of form ['x','y'], assuming in_str is of form 'x,y',
        'x, y', etc. (Does not result in an error as long as in_str has
        at least one comma).

        convert: Str -> (list Nat Nat)
        '''
        strlist = in_str.split(",")
        strlist[0] = strlist[0].rstrip()
        strlist[1] = strlist[1].lstrip()
        return strlist

    def num_revealed(G):
        '''
        Returns a list of the form [revealed, possible] where revealed
        represents the number of squares without bombs that were revealed
        in G, and possible represents the number of squares without bombs
        in G.

        num_revealed: Grid -> (list Nat Nat)
        '''
        rev, pos = 0,0
        dim = len(G)

        y=0
        
        while y<dim:
            
            x=0
            
            while x<dim:
                
                if not G[y][x].has_bomb:
                    if G[y][x].is_revealed:
                        rev += 1
                    pos += 1

                x+=1

            y+=1

        return [rev,pos]

    def try_replay():
        '''
        Calls play(is_retry=True) if the player indicates that they
        wish to play again.

        Effects:
        * Reads from the keyboard
        * Prints to the screen

        try_replay: None -> None
        '''
        retry = input("Want to play again? (y/n) ").lower()
        while retry!="y" and retry!="n":
            retry = input(
                "Enter 'y' or 'n', do you want to play again? ")
        if retry=="y":
            play(is_retry=True)
        return
    
    
    dim = 15

    test_font = "This is a text-based game.\n\n"+\
                "+--+--+--+--+--+\n"+\
                "|  |  |  |  |  |\n"+\
                "+--+--+--+--+--+\n\n"+\
                "The above shape should look like a line of five squares.\n"+\
                "If you do not see the shape, please change your font\n"+\
                "accordingly (Deja Vu Sans Mono is a good bet).\n\n"+\
                "Press enter when you are ready.\n"
    
    how_to_play = \
                "\nHOW TO PLAY:\n\n" +\
                "Enter the coordinates of the square you want to reveal.\n\n" +\
                "The coordinates should be of the form 'x,y', where x \n"+\
                "denotes the column number and y denotes the row number.\n"+\
                "For instance, 1,2 denotes the upper left corner on\n"+\
                "a 2x2 grid.\n\n" +\
                "If you reveal a square with a bomb, it's game over.\n\n"
    how_to_play +=\
                "COMMANDS:\n\n" +\
                " * To see these instructions again later, enter 'help'.\n" +\
                " * To flag a square, enter your coordinate preceded by 'flag'\n"+\
                "   ('flag 1,1').\n"+\
                " * To unflag a square, enter your coordinate preceded by\n"+\
                "   'unflag' ('unflag 1,1').\n" +\
                " * To reprint the grid, enter 'grid'.\n"+\
                " * To see the meaning of a symbol on the grid, enter "+\
                "'symbols'.\n" +\
                " * To quit, enter 'quit'.\n\n"
    gamestart_msg =\
                  "\n~~~~~~~~~~~~~~~~~~~~~~~\n\n"+\
                  "Default grid size is 15x15.\n\n" +\
                  "To choose a different grid size, enter a natural number\n" +\
                  "greater than or equal to 2. The grid will be of size nxn,\n" +\
                  "where n is your inputted number of choice. Excessively\n" +\
                  "large numbers are not recommended, as the grid may be\n"+\
                  "printed weirdly (this is a text based game, after all).\n\n"+\
                  "To proceed with the default size, press enter (or\n"+\
                  "enter anything else that isn't a natural number).\n\n"
    improper_coord_msg = \
                       "\nThe coordinate must be of the form 'x,y', where\n" +\
                       "x and y are natural numbers.\n\n"+\
                       "To flag a square (eg. 1,1), enter 'flag 1,1'. To \n"+\
                       "unflag the square 1,1, enter 'unflag 1,1'.\n"
    coord_outofrange_msg = \
                         "\nThat coordinate was out of range.\n"
    symbols_msg = \
                " * : Flagged square\n"+\
                " - : No adjacent squares have a bomb\n"+\
                " 2 : 2 adjacent squares have a bomb\n"+\
                "XX : Revealed square has a bomb\n"

    if not is_retry:
        ready = input(test_font)
        ready = input(how_to_play + "(Press enter to continue)")
    
    ready = input(gamestart_msg).lstrip().rstrip()
    
    while ready.isnumeric():

        if int(ready) < 2:
            ready = input(
                "\nUnfortunately that'd be too trivial, choose something\n"+\
                "higher (or enter anything that isn't a natural number to\n"+\
                "stick with 15x15 instead): ")\
                .lstrip().rstrip()
        
        elif 25 <= int(ready) < 50:
            
            check = input(
                "\nThat's a pretty large number, are you sure? (y/n) ")\
                .lstrip().rstrip()
            
            while check.lower()!="y" and check.lower()!="n":
                check = input(
                    "\nSay again? Are you sure you want to play with "+\
                    "a grid size of {0}x{0}?\n(Enter 'y' or 'n') "\
                    .format(int(ready)))\
                    .lstrip().rstrip()
                
            if check.lower()=="y":
                dim = int(ready)
                ready = ""
            else:
                ready = input(gamestart_msg).lstrip().rstrip()
        
        elif 50<=int(ready)<100:
            
            check = input(
                "\nThat's a REALLY large number, are you sure? (y/n) ")\
                .lstrip().rstrip()
            
            while check.lower()!="y" and check.lower()!="n":
                check = input(
                    "\nSay again? Are you sure you want to play with "+\
                    "a grid size of {0}x{0}?\n(Enter 'y' or 'n') "\
                    .format(int(ready)))\
                    .lstrip().rstrip()
            
            if check.lower()=="y":
                dim = int(ready)
                ready = ""
            else:
                ready = input(gamestart_msg).lstrip().rstrip()

        elif int(ready) >= 100:
            ready = input(
                "\nOkay that's a little ridiculous, choose something lower\n" +\
                "than that, please (or just enter anything that isn't a\n"+\
                "natural number for a 15x15 board): ").lstrip().rstrip()
        
        else:
            dim = int(ready)
            ready = ""

    G = create_grid(dim)
    print("\n~~~~~~~~~~~~~~~~~\n\n")
    print_grid(G)
    
    coord = input().lstrip().rstrip()

    while True:

        if coord.lower()=="help":
            print(how_to_play)
        
        elif coord.lower()=="quit":
            print("Bye.")
            return
        
        elif coord.lower()=="grid":
            print("\n")
            print_grid(G)

        elif coord.lower()=="symbols":
            print("\n")
            print(symbols_msg)

        elif "," not in coord:
            print(improper_coord_msg)


        else: # Using the function convert won't result in an error

            flag_intent = coord[:4].lower()
            unflag_intent = coord[:6].lower()
            
            if flag_intent=="flag":
                cstrlist = convert(coord[4:].lstrip())
            elif unflag_intent=="unflag":
                cstrlist = convert(coord[6:].lstrip())
            else:
                cstrlist = convert(coord)
            
            
            if len(cstrlist)!=2 or not (cstrlist[0].isnumeric()) \
               or not (cstrlist[1].isnumeric()):
                print(improper_coord_msg)

            else: # Casting coordinates to integers won't result in an error

                in_x, in_y = int(cstrlist[0]), int(cstrlist[1])
                
                if not (1<=in_x<=dim and 1<=in_y<=dim):
                    print(coord_outofrange_msg)


                elif flag_intent!="flag" and unflag_intent!="unflag":

                    flag = reveal(G, in_x, in_y)
                    
                    if flag=="bomb revealed":
                        y = 0
                        # Reveal all bombs for player
                        while y<dim:
                            x=0
                            while x<dim:
                                if G[y][x].has_bomb:
                                    reveal(G,x+1,dim-y) # "in" format
                                x+=1
                            y+=1
                        print_grid(G)
                        print("\n{0},{1} had a bomb.".format(in_x,in_y),end=" ")
                        print("Game over!\n")

                        results = num_revealed(G)
                        rev, pos = results[0], results[1]
                        if pos!=0:
                            percent = (rev/pos)*100
                            percent = round(percent, 1)
                            print(
                                "You revealed {0} out of {1} bombless squares, "\
                                .format(rev,pos)+\
                                "earning you\n"+\
                                "a score of {0}%.\n".format(percent))
                        else:
                            print(
                                "Somehow, you were so unlucky that every single"+\
                                " square had a bomb.\n"+\
                                "This was unwinnable. Sorry!\n")

                        try_replay()
                        return

                    # Alternate ending: all possible squares revealed
                    
                    results = num_revealed(G)
                    rev, pos = results[0], results[1]
                    if rev==pos:
                        print_grid(G)
                        print("You revealed all {0} out of {1} bombless "\
                              .format(rev,pos)+\
                              "squares, earning you\n"+\
                              "a score of 100%. Congratulations.\n")
                        try_replay()
                        return


                    print("\n")
                    print_grid(G)


                elif flag_intent=="flag":

                    G[dim-in_y][in_x-1].is_flagged = True
                    print("\n")
                    print_grid(G)

                else:

                    G[dim-in_y][in_x-1].is_flagged = False
                    print("\n")
                    print_grid(G)

        coord = input().lstrip().rstrip()
