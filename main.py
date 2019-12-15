from grid import *


class Minesweeper:
    def __init__(self):
        self.grid = Grid()


    def _num_atleast_2(self, string):
        """
        Returns True if string is numeric and represents a number at
        least 2, and False otherwise.

        :param string: string
        :return: bool
        """
        return s.isnumeric() and int(s) >= 2


    def _convert(self, str_input):
        """
        Splits str_input and returns the result.

        :param str_input: string with ',' in it
        :return: list
        """
        strlist = str_input.split(",")
        strlist[0] = strlist[0].strip()
        strlist[1] = strlist[1].strip()
        return strlist

    def _set_flag(self, x_in, y_in, flag):
        """
        Sets the value of is_flagged of the square at coordinate (x_in, y_in)
        to flag.

        :param x_in: int. Must be in range
        :param y_in: int. Must be in range
        :return: None
        """
        xpos, ypos = x_in - 1, self.grid.dim - y_in
        self.grid.gridlist[ypos * self.grid.dim + xpos].is_flagged = flag

    def _set_flag_intent(self, command):
        """
        Determine values of flag_intent and unflag_intent, and splits the
        command into coordinates, and returns them as a tuple.

        :param command: string of form "flag x, y" or "unflag x, y" or "x, y"
        :return: tuple
        """
        flag_intent = command[:4].lower()
        unflag_intent = command[:6].lower()

        if flag_intent == "flag":
            split_list = self._convert(command[4:].lstrip())
                    
        elif unflag_intent == "unflag":
            split_list = self._convert(command[6:].lstrip())
                    
        else:
            split_list = self._convert(command)

        return flag_intent, unflag_intent, split_list

    def _show_results(self):
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


    def _try_replay(self):
        """
        Prompts the player for a replay. Returns True if the player
        wishes to replay and False otherwise.

        :return: bool
        """
        retry = input("Play again? (y/n) ").lower()
        while retry != "y" and retry != "n":
            retry = input("Enter 'y' or 'n'. Play again? ").lower()
            
        if retry == "y":
            self.grid.is_retry = True
            return True

        else:
            return False


    def play(self):
        """
        Play the game.
        """
        continue_playing = True
        
        while continue_playing:
            
            self.grid.initialize_game()
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
            self.grid.print_grid()
            
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

                elif "," not in command:
                    print(IMPROPER_COORD_MSG)
                    command = input().strip()
                    continue

                flag_intent, unflag_intent, split_list = \
                             self._set_flag_intent(command)

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
                    self._set_flag(x_input, y_input,
                                   True if flag_intent == "flag"
                                   else False)
                    print("\n")
                    self.grid.print_grid()
                    command = input().strip()
                    continue

                bomb = self.grid.reveal(x_input - 1, self.grid.dim - y_input)

                if bomb == "bomb revealed":
                    pos = 0
                    while pos < self.grid.dim * self.grid.dim:
                        if self.grid.gridlist[pos].has_bomb:
                            self.grid.gridlist[pos].is_revealed = True
                        pos += 1

                    self.grid.print_grid()
                    print("\n{}, {} had a bomb. Game over!"
                          .format(x_input, y_input))

                    self._show_results()
                    continue_playing = self._try_replay()
                    break

                else:
                    if self.grid.revealed == self.grid.possible:
                        self.grid.print_grid()
                        self._show_results()
                        continue_playing = self._try_replay()
                        break

                print("\n")
                self.grid.print_grid()
                command = input().strip()

m = Minesweeper()
m.play()
