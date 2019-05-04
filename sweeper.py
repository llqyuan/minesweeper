import random

'''
Work on:

Presentation-related stuff
 * spacing
 * clarify instructions ("help" part for instance)
 
Win state
'''
# ====================

'''
A Grid is a (listof (listof [Bool Bool Bool])), where
  * each sublist is of the same length
  * the sublists are of the same length as the full list itself
    (that is, it represents a square grid)
  * the first boolean value represents whether or not the square
    has been revealed
  * the second boolean value represents whether or not it has a bomb
  * the third boolean value represents whether or not the square was flagged
'''


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
           G[pos_y][pos_x][1]:
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
            
            if G[y][x][0]:

                flag_char = " "

                if G[y][x][2]:
                    flag_char = "*"
            
                if G[y][x][1]: # bomb revealed
                    s = s + "XX"
                else:
                    adj_bombs = adj_with_bombs(G,x,y)
                    if adj_bombs==0:
                        s = s + "{0}-".format(flag_char)
                    else:
                        s = s + "{1}{0}".format(adj_bombs, flag_char)
            
            else:
                
                if G[y][x][2]: # flagged
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


def create_grid(dim,n=0.15):
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
            if random.random() <= n:
                sub.append([False, True, False])
            else:
                sub.append([False, False, False])
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

    if G[y][x][1]:
        G[y][x][0] = True
        return "bomb revealed"

    elif adj_with_bombs(G,x,y)!=0:
        G[y][x][0] = True
        return

    else:
    
        G[y][x][0] = True
        adjacent = [ [in_x-1, in_y-1], [in_x, in_y-1], [in_x+1, in_y-1],
                     [in_x-1, in_y],                   [in_x+1, in_y],
                     [in_x-1, in_y+1], [in_x, in_y+1], [in_x+1, in_y+1] ]
        adj_inrange = list(filter(lambda pos: 1<=pos[0]<=dim \
                                              and 1<=pos[1]<=dim,
                                  adjacent))
        adj_notrevealed = list(
            filter(lambda pos: not G[dim-pos[1]][pos[0]-1][0],
                   adj_inrange))
        for pos in adj_notrevealed:
            reveal(G, pos[0], pos[1])


def play():

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
        strlist[0] = strlist[0]
        strlist[1] = strlist[1].lstrip()
        return strlist
    
    dim = 15
    
    how_to_play = \
                "\nHOW TO PLAY:\n\n" +\
                "Enter the coordinates of the square you want to reveal.\n\n" +\
                "The coordinates should be of the form 'x, y', where x \n"+\
                "denotes the column number and y denotes the row number.\n"+\
                "For instance, 1,15 denotes the upper left corner on\n"+\
                "a 15x15 grid.\n\n" +\
                "If you reveal a square with a bomb, it's game over.\n\n" +\
                "COMMANDS:\n\n" +\
                " * To reprint the grid, enter 'grid'.\n"+\
                " * To quit, enter 'quit'.\n"+\
                " * To flag a square, enter your coordinate preceded by 'flag'\n"+\
                "   ('flag 1,1').\n"+\
                " * To unflag a square, enter your coordinate preceded by\n"+\
                "   'unflag' ('unflag 1,1').\n"+\
                " * To see the meaning of a symbol on the grid, enter 'symbols'.\n\n"+\
                " * If you need to see these instructions again later,\n" +\
                "   enter 'help'.\n\n"
    gamestart_msg = \
                  "~~~~~~~~~~~~~~~~~~~~~~~\n\n"+\
                  "Default grid size is 15x15.\n\n" +\
                  "To choose a different grid size, enter a natural number\n" +\
                  "greater than or equal to 2. The grid will be of size nxn,\n" +\
                  "where n is your inputted number of choice. Excessively\n" +\
                  "large numbers are not recommended, as the grid may be\n"+\
                  "printed weirdly (this is a text based game).\n\n"+\
                  "To proceed with the default size, press enter (or\n"+\
                  "enter anything else that isn't a natural number).\n\n"
    improper_coord_msg = \
                       "\nThe coordinate must be of the form 'x, y', where\n" +\
                       "x and y are natural numbers.\n"
    coord_outofrange_msg = \
                         "\nThat coordinate was out of range.\n"
    symbols_msg = \
                " * -- Flagged square\n"+\
                " - -- No bombs in adjacent squares\n"+\
                " 2 -- 2 adjacent squares have a bomb\n"+\
                "XX -- Revealed square has a bomb\n"
    
    preready = input(how_to_play + "(Press enter to continue)\n")
    
    ready = input(gamestart_msg)
    
    while ready.isnumeric():

        if int(ready) < 2:
            ready = input(
                "\nUnfortunately that'd be too trivial, choose something\n"+\
                "else (or enter anything that isn't a natural number to\n"+\
                "stick with 15x15 instead): ")
        
        elif 25 <= int(ready) < 50:
            
            check = input(
                "\nThat's a pretty large number, are you sure? (y/n) ")
            
            while check.lower()!="y" and check.lower()!="n":
                check = input(
                    "\nSay again? Are you sure you want to play with "+\
                    "a grid size of {0}x{0}?\n(Enter 'y' or 'n') "\
                    .format(int(ready)))
                
            if check.lower()=="y":
                dim = int(ready)
                ready = ""
            else:
                ready = input(gamestart_msg)
        
        elif 50<=int(ready)<100:
            
            check = input(
                "\nThat's a REALLY large number, are you sure? (y/n) ")
            
            while check.lower()!="y" and check.lower()!="n":
                check = input(
                    "\nSay again? Are you sure you want to play with "+\
                    "a grid size of {0}x{0}? (Enter 'y' or 'n') "\
                    .format(int(ready)))
            
            if check.lower()=="y":
                dim = int(ready)
                ready = ""
            else:
                ready = input(gamestart_msg)

        elif int(ready) >= 100:
            ready = input(
                "\nOkay that's a little ridiculous, choose something lower\n" +\
                "than that, please (or just enter anything that isn't a\n"+\
                "natural number for a 15x15 board): ")
        
        else:
            dim = int(ready)
            ready = ""

    G = create_grid(dim)
    print("\n~~~~~~~~~~~~~~~~~\n\n")
    print_grid(G)
    
    coord = input()
    coord = coord.lstrip()
    coord = coord.rstrip()

    while True:

        if coord.lower()=="help":
            print(how_to_play)
            
        elif coord.lower()=="quit":
            print("Goodbye.")
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
            unflag_intent = coord[:6]
            
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
                    # Coordinate valid, not flagging/unflagging

                    flag = reveal(G, in_x, in_y)
                    
                    if flag=="bomb revealed":
                        y = 0
                        while y<dim:
                            x=0
                            while x<dim:
                                if G[y][x][1]: # has bomb
                                    reveal(G,x+1,dim-y) # "in" format
                                x+=1
                            y+=1
                        print("\n{0},{1} had a bomb.\n".format(in_x,in_y))
                        print_grid(G)
                        print("Game over!")
                        return

                    print("\n")
                    print_grid(G)

                elif flag_intent=="flag":

                    G[dim-in_y][in_x-1][2] = True
                    print("\n")
                    print_grid(G)

                else:

                    G[dim-in_y][in_x-1][2] = False
                    print("\n")
                    print_grid(G)

        coord = input()
        coord = coord.lstrip()
        coord = coord.rstrip()
