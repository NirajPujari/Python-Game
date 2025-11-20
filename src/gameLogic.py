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
        return list(zip(*np.where(self.grid == 0)))

    def new_number(self, k=1):
        empties = self.get_empty_cells()
        if not empties:
            return
        k = min(k, len(empties))
        for pos in random.sample(empties, k):
            self.grid[pos] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def _collapse_line(line):
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
        return np.array(new + [0] * (len(line) - len(new)), dtype=int), score

    def _grid_after_move(self, move):
        grid_copy = self.grid.copy()
        total_gained = 0
        for i in range(N):
            if move in ('l', 'r'):
                line = list(grid_copy[i, :])
            else:
                line = list(grid_copy[:, i])

            flipped = move in ('r', 'd')
            if flipped:
                line = line[::-1]

            collapsed, gained = self._collapse_line(line)
            if flipped:
                collapsed = collapsed[::-1]

            if move in ('l', 'r'):
                grid_copy[i, :] = collapsed
            else:
                grid_copy[:, i] = collapsed

            total_gained += gained
        return grid_copy, total_gained

    def make_move(self, move):
        new_grid, gained = self._grid_after_move(move)
        changed = not np.array_equal(new_grid, self.grid)
        if changed:
            self.grid = new_grid
            self.score += gained
        return changed, gained

    def can_move(self):
        if np.any(self.grid == 0):
            return True
        for i in range(N):
            for j in range(N - 1):
                if self.grid[i, j] == self.grid[i, j + 1]:
                    return True
                if self.grid[j, i] == self.grid[j + 1, i]:
                    return True
        return False

    def has_won(self, target=2048):
        return np.any(self.grid >= target)

    def move_and_get_changes(self, move):
        old = self.grid.copy()
        # positions before move
        old_pos = []
        for r in range(N):
            for c in range(N):
                v = int(old[r, c])
                if v != 0:
                    old_pos.append({'pos': (r, c), 'value': v, 'used': False})

        new_grid, gained = self._grid_after_move(move)
        moved = not np.array_equal(old, new_grid)

        # Build list of new tiles with values and positions
        new_tiles = []
        for r in range(N):
            for c in range(N):
                v = int(new_grid[r, c])
                if v != 0:
                    new_tiles.append({'pos': (r, c), 'value': v, 'filled_sources': []})

        used_old_idx = set()
        for nt in new_tiles:
            v = nt['value']
            # attempt merge detection
            if v % 2 == 0:
                src_val = v // 2
                # find up to two old tiles with value src_val (not used)
                matches = []
                for idx, op in enumerate(old_pos):
                    if idx in used_old_idx:
                        continue
                    if op['value'] == src_val:
                        matches.append((idx, op))
                        if len(matches) == 2:
                            break
                if len(matches) == 2:
                    # merged from two sources
                    nt['starts'] = [matches[0][1]['pos'], matches[1][1]['pos']]
                    nt['merged'] = True
                    used_old_idx.add(matches[0][0])
                    used_old_idx.add(matches[1][0])
                    continue
            # else try single-source match: value equal or, as fallback, closest same-valued tile
            single_match = None
            for idx, op in enumerate(old_pos):
                if idx in used_old_idx:
                    continue
                if op['value'] == v:
                    single_match = (idx, op)
                    break
            if single_match:
                nt['starts'] = [single_match[1]['pos']]
                nt['merged'] = False
                used_old_idx.add(single_match[0])
            else:
                # fallback: find any unused tile (rare)
                for idx, op in enumerate(old_pos):
                    if idx in used_old_idx:
                        continue
                    nt['starts'] = [op['pos']]
                    nt['merged'] = False
                    used_old_idx.add(idx)
                    break

        # If tile moved from same pos (no movement), starts==end indicates no movement but still animate small pop on merge.
        movements = []
        for nt in new_tiles:
            movements.append({
                'starts': nt.get('starts', []),
                'end': nt['pos'],
                'value': nt['value'],
                'merged': nt.get('merged', False)
            })

        # commit the move
        if moved:
            self.grid = new_grid
            self.score += gained

        return moved, gained, movements
