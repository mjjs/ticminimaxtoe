#!/usr/bin/env python
"""
Classes:
    Game: The game object which holds utility methods for printing the game board,
        calculating winner, making moves
    AI: The AI player
"""

from random import randint
from typing import List
import argparse

class Game():
    """
    Class for the game itself
    """
    # Three in a row combos that win the game
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    def __init__(self):
        """Constructor"""
        self.board = [None for i in range(9)]
        self.ai_moves_count = 0
        self.status = "Running"
        self.current_player = "X"

    def print_board(self) -> None:
        """Print the game board"""
        print('\n\n\n')
        for element in [self.board[i:i + 3] for i in range(0, len(self.board), 3)]:
            print(element)

    def change_player(self) -> None:
        """Change the current player"""
        self.current_player = self.get_enemy(self.current_player)

    @staticmethod
    def get_enemy(player: str) -> str:
        """Return the enemy player for a given player"""
        if player == "X":
            return "O"
        return "X"

    def available_cells(self) -> List[int]:
        """Return an array of empty board cells"""
        return [cell for cell, cell_value in enumerate(self.board) if cell_value is None]

    def get_own_squares(self, player: str) -> List[int]:
        """Return the board cells occupied by given player"""
        return [cell for cell, cell_value in enumerate(self.board) if cell_value == player]

    def get_winner(self):
        """
        Check for a winner

        Returns:
            Either the winning player or None
        """
        for player in ('X', 'O'):
            positions = self.get_own_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player

        return None

    def is_game_over(self) -> bool:
        """Check whether the game ends or not"""
        if not self.available_cells():
            return True
        if self.get_winner() is not None:
            return True
        return False

    def make_move(self, cell: int, player: str) -> None:
        """Make a move on the board"""
        self.board[cell] = player
        self.change_player()

    def validate_move(self, cell: int) -> bool:
        """Validate that the move is legal"""
        if cell < 0 or cell > 8:
            return False
        if self.board[cell] is not None:
            return False
        return True


class AI(object):
    """The AI class to play against"""

    def __init__(self, difficulty, game):
        """
        Args:
            difficulty: The difficulty level of the AI. Either master (default) or easy
            game: The current game being played
        """
        self.game = game
        self.difficulty = 'master'
        if difficulty:
            self.difficulty = difficulty

    def __minimax(self, game, depth, player) -> int:
        """Recursively calculate the minimax value of a given game state"""
        if game.is_game_over():
            if game.get_winner() == "X":
                return -1
            elif game.get_winner() == "Y":
                return 1
            return 0

        if player == "O":
            best_value = -1
            for move in game.available_cells():
                game.make_move(move, player)
                move_value = self.__minimax(game, depth-1, game.get_enemy(player))
                game.make_move(move, None)
                best_value = max(best_value, move_value)
            return best_value

        best_value = 1
        for move in game.available_cells():
            game.make_move(move, player)
            move_value = self.__minimax(game, depth-1, game.get_enemy(player))
            game.make_move(move, None)
            best_value = min(best_value, move_value)
        return best_value

    def __get_best_choice(self, game, depth, player) -> int:
        """
        Calculate the best possible move for the given game state

        Args:
            game: The current game being played
            depth: How far along the game is
            player: The player who wants to get the best choice

        Returns:
            The position of the cell to play
        """
        neutral_value = 0
        choices = []

        for move in game.available_cells():
            game.make_move(move, player)
            move_value = self.__minimax(game, depth-1, game.get_enemy(player))
            game.make_move(move, None)

            if move_value > neutral_value:
                choices = [move]
            elif move_value == neutral_value:
                choices.append(move)

        if choices is not None:
            return randint(min(choices), max(choices))
        free_cells = game.available_cells()
        return randint(min(free_cells), max(free_cells))


    def __make_easy_move(self) -> int:
        """Make a random move and return the played cell"""
        available_moves = self.game.available_cells()
        cell = randint(min(available_moves), max(available_moves))
        return cell

    def __make_master_move(self) -> int:
        """Make a calculated move"""
        turns_left = len(self.game.available_cells())
        move = self.__get_best_choice(self.game, turns_left, self.game.current_player)
        return move

    def play(self) -> int:
        """Call the correct function depending on the selected difficulty"""
        if self.difficulty == 'easy':
            return self.__make_easy_move()
        return self.__make_master_move()

def main() -> None:
    """Main game loop"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--easy", help="Run the AI in easy mode", action="store_true")
    args = parser.parse_args()

    if args.easy:
        difficulty = "easy"
    else:
        difficulty = "master"

    # Create the game and the ai player
    game = Game()
    ai_player = AI(difficulty, game)

    while game.is_game_over() is False:
        game.print_board()
        if game.current_player == "X":
            player_move = None
            while player_move is None or game.validate_move(player_move) is False:
                try:
                    player_move = int(input('0-8: '))
                except (ValueError, IndexError):
                    print("Please insert a number")
            game.make_move(player_move, game.current_player)
        else:
            game.make_move(ai_player.play(), game.current_player)

    game.print_board()

if __name__ == "__main__":
    main()
