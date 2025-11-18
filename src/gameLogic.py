# gameLogic.py
import numpy as np
import random
from constants import N

class GameLogic:
    def __init__(self):
        self.grid = np.zeros((N, N), dtype=int)
        self.score = 0
        self.reset()

    def reset(self):
        self.grid.fill(0)
        self.score = 0
        self.new_number(k=2)

    def get_empty_cells(self):
        empties = list(zip(*np.where(self.grid == 0)))
        return empties

    def new_number(self, k=1):
        empties = self.get_empty_cells()
        if not empties:
            return
        k = min(k, len(empties))
        for pos in random.sample(empties, k):
            self.grid[pos] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def _collapse_line(line):
        """
        Given a 1D array-like, compress (remove zeros), merge equal neighbours once,
        and return the collapsed line and the score gained.
        """
        arr = [x for x in line if x != 0]
        new = []
        score = 0
        skip = False
        for i in range(len(arr)):
            if skip:
                skip = False
                continue
            if i + 1 < len(arr) and arr[i] == arr[i + 1]:
                merged = arr[i] * 2
                new.append(merged)
                score += merged
                skip = True
            else:
                new.append(arr[i])
        # pad zeros to the right to match original length
        return np.array(new + [0] * (len(line) - len(new)), dtype=int), score

    def make_move(self, move):
        """
        move: 'l', 'r', 'u', 'd'
        Returns True if grid changed, False otherwise.
        """
        moved = False
        total_gained = 0

        for i in range(N):
            if move in ('l', 'r'):
                line = list(self.grid[i, :])
            else:
                line = list(self.grid[:, i])

            flipped = move in ('r', 'd')
            if flipped:
                line = line[::-1]

            collapsed, gained = self._collapse_line(line)
            if flipped:
                collapsed = collapsed[::-1]

            if move in ('l', 'r'):
                if not np.array_equal(self.grid[i, :], collapsed):
                    moved = True
                self.grid[i, :] = collapsed
            else:
                if not np.array_equal(self.grid[:, i], collapsed):
                    moved = True
                self.grid[:, i] = collapsed

            total_gained += gained

        self.score += total_gained
        return moved

    def can_move(self):
        # if there's an empty cell, we can move
        if np.any(self.grid == 0):
            return True
        # check adjacent merges horizontally and vertically
        for i in range(N):
            for j in range(N - 1):
                if self.grid[i, j] == self.grid[i, j + 1]:
                    return True
                if self.grid[j, i] == self.grid[j + 1, i]:
                    return True
        return False

    def has_won(self, target=2048):
        return np.any(self.grid >= target)
