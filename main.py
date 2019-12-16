from grid import *
import random


class Minesweeper(object):
    def __init__(self):
        self.grid = Grid()
        self.allowed_hints = 0
        self.given_hints = 0


    def __split_str_input(self, str_input):
        """
        Splits str_input and returns the result.

        :param str_input: string with ',' in it
        :return: list
        """
        strlist = str_input.split(",")
        strlist[0] = strlist[0].strip()
        strlist[1] = strlist[1].strip()
        return strlist

    def __set_flag(self, x_in, y_in, flag):
        """
        Sets the value of is_flagged of the square at coordinate (x_in, y_in)
        to flag.

        :param x_in: int. Must be in range
        :param y_in: int. Must be in range
        :return: None
        """
        xpos, ypos = x_in - 1, self.grid.dim - y_in
        self.grid.gridlist[ypos * self.grid.dim + xpos].is_flagged = flag

    def __process_flag_intent(self, command):
        """
        Determine values of flag_intent and unflag_intent, and splits the
        command into coordinates, and returns them as a tuple.

        :param command: string of form "flag x, y" or "unflag x, y" or "x, y"
        :return: tuple
        """
        flag_intent = command[:4].lower()
        unflag_intent = command[:6].lower()

        if flag_intent == "flag":
            split_list = self.__split_str_input(command[4:].lstrip())
                    
        elif unflag_intent == "unflag":
            split_list = self.__split_str_input(command[6:].lstrip())
                    
        else:
            split_list = self.__split_str_input(command)

        return flag_intent, unflag_intent, split_list

    def __reveal_all_bombs(self):
        """
        Reveals all squares with bombs.
        """
        pos = 0
        for square in self.grid.gridlist:
            if square.has_bomb:
                square.is_revealed = True

    def __show_results(self):
        """
        Assumes the game has ended. Shows the results to the player.

        :return: None
        """
        if self.grid.possible == 0:
            print(
                "Somehow every single square had a bomb.\n")

        else:
            percent = (self.grid.revealed / self.grid.possible) * 100
            percent = round(percent, 1)
            print(
                "You revealed {} out of {} bombless squares, "
                "earning you \na score of {}%.\n"
                .format(self.grid.revealed, self.grid.possible, percent))
            if self.allowed_hints:
                print("You used {} hint(s) out of {}.\n"
                      .format(self.given_hints, self.allowed_hints))


    def __try_replay(self):
        """
        Prompts the player for a replay. Returns True if the player
        wishes to replay and False otherwise.

        :return: bool
        """
        retry = input("Play again? (y/n) ").lower().strip()
        while retry != "y" and retry != "n":
            retry = input("Enter 'y' or 'n'. Play again? ").lower().strip()
            
        if retry == "y":
            self.grid.is_retry = True
            return True

        else:
            return False


    def __set_hints(self):
        """
        Assuming the game board has been fully initialized, sets the number
        of allowed hints (self.allowed_hints) based on board size and resets
        self.given_hints to 0.
        """
        self.given_hints = 0
        self.allowed_hints = 0
        
        if 6 <= self.grid.dim < 9:
            self.allowed_hints = 1

        elif 9 <= self.grid.dim < 13:
            self.allowed_hints = 2

        elif self.grid.dim >= 13:
            self.allowed_hints = 3


    def __process_hint(self):
        """
        Reveals one random unrevealed square that doesn't have a bomb, unless
        there are no unrevealed bombless squares left (in the case where
        somehow all squares have initialized with bombs), in which case
        all bombs will be revealed before exiting the function. Helper
        for show_hints.
        """
        index = 0
        bombless_unrevealed = []
        
        while index < self.grid.dim * self.grid.dim:
            if not self.grid.gridlist[index].has_bomb and \
               not self.grid.gridlist[index].is_revealed:
                bombless_unrevealed.append(index)
            index += 1
            
        if len(bombless_unrevealed) == 0:
            self.__reveal_all_bombs()
            return

        to_reveal = random.choice(bombless_unrevealed)
        self.grid.reveal(to_reveal % self.grid.dim, to_reveal // self.grid.dim)


    def __show_hints(self):
        """
        Asks the player if they wish to see a hint. If they say yes and
        it is allowed, reveals one random unrevealed square without a bomb in
        it.
        """
        if self.allowed_hints == 0:
            print("\nHints are not given for a board of this size.\n")

        elif self.allowed_hints - self.given_hints <= 0:
            print("\nYou have used all available hints and no more hints will \n"
                  "be given.\n")

        else:
            show = input(
                "You have {} hint(s) left out of a total of {}. You may \n"
                "receive a hint and reveal a random bombless square if \n"
                "you wish.\n\n"
                "Show hint? (y/n) "
                .format(self.allowed_hints - self.given_hints,
                        self.allowed_hints)).lower().strip()

            while show != "y" and show != "n":
                show = input(
                    "I didn't understand that. Show hint? (y/n) ").lower().strip()

            if show == "y":
                self.__process_hint()
                self.given_hints += 1

            print("\n")
            self.grid.print_grid()


    def play(self):
        """
        Play the game.
        """
        continue_playing = True
        
        while continue_playing:
            
            self.grid.initialize_game()
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
            self.grid.print_grid()
            self.__set_hints()
            
            command = input().strip()

            while 1:
                
                if command.lower() == "help":
                    print(COMMAND_LIST_MSG)
                    command = input().strip()
                    continue
                    
                elif command.lower() == "quit":
                    print("Bye.")
                    return
                
                elif command.lower() == "grid":
                    print("\n")
                    self.grid.print_grid()
                    command = input().strip()
                    continue

                elif command.lower() == "symbols":
                    print(SYMBOLS_MSG)
                    command = input().strip()
                    continue

                elif command.lower() == "hint":
                    self.__show_hints()
                    if self.grid.revealed == self.grid.possible:
                        self.__show_results()
                        continue_playing = self.__try_replay()
                        break
                    command = input().strip()
                    continue

                elif "," not in command:
                    print(IMPROPER_COORD_MSG)
                    command = input().strip()
                    continue

                flag_intent, unflag_intent, split_list = \
                             self.__process_flag_intent(command)

                if len(split_list) > 2 or not (split_list[0].isnumeric()) \
                   or not (split_list[1].isnumeric()):
                    print(IMPROPER_COORD_MSG)
                    command= input().strip()
                    continue
                
                x_input, y_input = int(split_list[0]), int(split_list[1])

                if not (1 <= x_input <= self.grid.dim and \
                        1 <= y_input <= self.grid.dim):
                    print(COORD_OUT_OF_RANGE_MSG)
                    command = input().strip()
                    continue

                elif flag_intent == "flag" or unflag_intent == "unflag":
                    self.__set_flag(x_input, y_input,
                                    True if flag_intent == "flag"
                                    else False)
                    print("\n")
                    self.grid.print_grid()
                    command = input().strip()
                    continue

                bomb = self.grid.reveal(x_input - 1, self.grid.dim - y_input)

                if bomb:
                    self.__reveal_all_bombs()
                    self.grid.print_grid()
                    
                    print("\n{}, {} had a bomb. Game over!"
                          .format(x_input, y_input))

                    self.__show_results()
                    continue_playing = self.__try_replay()
                    break

                elif self.grid.revealed == self.grid.possible:
                    self.grid.print_grid()
                    self.__show_results()
                    continue_playing = self.__try_replay()
                    break

                print("\n")
                self.grid.print_grid()
                command = input().strip()

m = Minesweeper()
m.play()
