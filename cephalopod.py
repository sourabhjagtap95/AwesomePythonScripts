# -*- coding: utf-8 -*-

import random
import itertools

class Cephalopod(object):

    """
    < 0 : RED
    > 0 : WHITE
    First take WHITE

      -1 0 1
    -1
     0
     1
    """

    ROW_NUMS = 5
    COL_NUMS = 5

    PENDING = 0
    AI_ONE_WON = 1
    AI_TWO_WON = 2

    AI_ONE = 1
    AI_TWO = 2
    BLANK = 3

    deltas = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    mapping = {
        "U": (-1, 0),
        "L": (0, -1),
        "R": (0, 1),
        "D": (1, 0)
    }

    def __init__(self, first_move):
        self.state = self.PENDING
        self.current_turn = 0
        self.first_move = first_move
        self.board = [[0 for i in range(self.ROW_NUMS)] for j in range(self.COL_NUMS)]
        self.game_log = []


    def get_color(self, player):
        if self.first_move == self.AI_ONE:
            return 1 if player == self.AI_ONE else -1
        else:
            return -1 if player == self.AI_ONE else 1

    def set_value(self, player, row, col, value):
        self.board[row][col] = self.get_color(player) * value

    def clear_cell(self, row, col):
        self.board[row][col] = 0

    def make_a_move(self, player, move):
        self.current_turn += 1
        if self.is_valid_move(move):
            parts = move.split(" ")
            row, col = int(parts[0]), int(parts[1])

            if len(parts) == 2:
                if self.is_mergeable(row, col):
                    surrounds = self.get_mergeable_surrounds(row, col)
                    total = 0
                    for delta, value in surrounds[0]:
                        self.clear_cell(row + delta[0], col + delta[1])
                        total += value
                    self.set_value(player, row, col, total)
                else:
                    self.set_value(player, row, col, 1)
            else:
                total = 0
                for direction in parts[2:]:
                    dr, dc = self.mapping[direction]
                    total += self.value_of(row + dr, col + dc)
                    self.clear_cell(row + dr, col + dc)
                self.set_value(player, row, col, total)
            self.game_log.append(move)
            self.check_status()
            print game.board_state()
            print "*" * 10
            return True
        else:
            self.state = self.AI_TWO_WON if player == self.AI_ONE else self.AI_ONE_WON
            return False

    def is_in_bound(self, row, col):
        return (row >= 0 and row < self.ROW_NUMS ) and (col >= 0 and col < self.COL_NUMS)

    def is_ai_one_won(self):
        return self.state == self.AI_ONE_WON

    def is_ai_two_won(self):
        return self.state == self.AI_TWO_WON

    def is_pending(self):
        return self.state == self.PENDING

    def value_of(self, row, col):
        return abs(self.board[row][col])

    def is_blank(self, row, col):
        return self.value_of(row, col) == 0

    def get_surrounds(self, row, col):
        surrounds = {}
        for dr, dc in self.deltas:
            if self.is_in_bound(row + dr, col + dc) and not self.is_blank(row + dr, col + dc):
                surrounds[(dr, dc)] = self.value_of(row + dr, col + dc)

        return surrounds

    def is_mergeable(self, row, col):
        surrounds = self.get_surrounds(row, col)
        if len(surrounds.keys()) < 2:
            return False
        else:
            for count in range(2, len(surrounds.keys())+1):
              for subset in itertools.combinations(surrounds.values(), count):
                if sum(subset) <= 6:
                    #print "sum < 6"
                    return True

        return False


    def get_mergeable_surrounds(self, row, col):
        surrounds = self.get_surrounds(row, col)
        result = []
        for count in range(2, len(surrounds.keys())+1):
            print surrounds.items()
            for subset in itertools.combinations(surrounds.items(), count):
                print subset
                if sum([v for k, v in subset]) <= 6:
                    result.append(subset)

        return result

    def is_valid_merge(self, row, col, directions):
        if not directions:
            return False

        total = 0
        for direction in directions:
            dr, dc = self.mapping[direction]
            if self.is_in_bound(row + dr, col + dc) and not self.is_blank(row + dr, col + dc):
                total += self.value_of(row + dr, col + dc)
            else:
                return False

        return total != 0 and total <= 6

    def is_valid_move(self, move):
        try:
            parts = move.split(" ")
            row, col = int(parts[0]), int(parts[1])
            if not self.is_in_bound(row, col) or not self.is_blank(row, col):
                return False
            #print "In bound"
            if len(parts) != 2:
                if not self.is_mergeable(row, col):
                    return False
                else:
                    return self.is_valid_merge(row, col, parts[2:])
            else:
                if self.is_mergeable(row, col):
                    return len(self.get_mergeable_surrounds(row, col)) == 1
                else:
                    return True
        except Exception:
            return False

    def is_win_move(self, player, row, col):
        pass


    def move_owner(self, row, col):
        pass


    def check_status(self):
        if self.state == self.PENDING:
            red = 0
            white = 0
            for row in range(self.ROW_NUMS):
                for col in range(self.ROW_NUMS):
                    if self.board[row][col] == 0:
                        return
                    else:
                        if self.board[row][col] > 0:
                            white += 1
                        else:
                            red += 1

            if red < white:
                self.state = self.AI_ONE_WON if self.first_move == self.AI_ONE else self.AI_TWO_WON
            else:
                self.state = self.AI_ONE_WON if self.first_move == self.AI_TWO else self.AI_ONE_WON

    def board_state(self):
        return "\n".join([" ".join("%2d" % i for i in row) for row in self.board])


    def get_replay_data(self):
        return [move for move in self.game_log]


if __name__ == '__main__':
    game = Cephalopod(Cephalopod.AI_TWO)
    game.board[1][0] = 2
    game.board[0][1] = 3
    game.board[1][2] = 4
    game.board[2][1] = 5
    game.make_a_move(2, "1 1")
    print game.get_mergeable_surrounds(1, 1)
    print game.board_state()
    print game.state
    print game.get_replay_data()
