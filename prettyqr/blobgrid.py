import math
import itertools
from utils import pointwise


class BlobGrid(object):

    n_directions = 4
    # directions: left, down, right, up
    directions = range(0, n_directions)
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbours = [(-1, -1), (-1, 0), (0, 0), (0, -1)]

    def __init__(self, size):
        self.size = size

    def get_value(self, x, y):
        """ overload with method returning pixel values """
        raise NotImplementedError

    def can_move(self, pos, direction):
        # we always keep the blob on the right

        n1 = self.neighbours[direction]
        n2 = self.neighbours[(direction + 1) % self.n_directions]

        value1 = self.get_value(*pointwise('add', pos, n1))
        value2 = self.get_value(*pointwise('add', pos, n2))

        return (value1 == 0 and value2 == 1)

    def find_direction(self, pos, prev_dir=None):
        available_directions = list(self.directions)  # make a copy
        if prev_dir:
            available_directions = (
                n % self.n_directions for n in range(prev_dir, prev_dir + 4))
        for d in available_directions:
            if self.can_move(pos, d):
                return d
        return None

    def move(self, pos, direction):
        offset = self.moves[direction]
        return pointwise('add', pos, offset)

    def corner(self, prev_dir, curr_dir):
        # bezier circle estimate
        kappa = 4 * (math.sqrt(2) - 1) / 3
        final = pointwise('add', self.moves[prev_dir], self.moves[curr_dir])
        control1 = pointwise('mul', kappa, self.moves[prev_dir])
        control2 = pointwise('sub', final,
            pointwise('mul', 1 - kappa, self.moves[curr_dir]))
        replacements = pointwise('div', control1 + control2 + final, 2.0)
        return 'c %s,%s %s,%s %s,%s ' % tuple(replacements)

    def draw(self, prev_dir, curr_dir):
        if prev_dir == curr_dir:
            return 'l %s %s ' % self.moves[curr_dir]
        else:
            return self.corner(prev_dir, curr_dir)

    def start_draw(self, pos, direction):
        start = pointwise('add', pos,
            pointwise('div', self.moves[direction], 2.0))

        return '<path d="M %s %s ' % start

    def draw_blobs(self):
        output = ''

        remaining = []
        for x, y in itertools.product(xrange(self.size + 1), repeat=2):
            remaining.append((x, y))

        # we remove each intersection when visited. some are visited twice
        # when finished with a blob we start at the next unvisited intersection
        while remaining:
            start_pos = remaining.pop(0)
            start_dir = self.find_direction(start_pos)
            if start_dir is None:
                continue

            # use the list of directions for any region to colour
            # singletons and the corner markers
            direction_history = [start_dir]

            output += self.start_draw(start_pos, start_dir)
            curr_pos = self.move(start_pos, start_dir)
            curr_dir = start_dir

            # 'holes' will have opposite turning number -
            # colour these white
            total_turns = 0

            while curr_pos != start_pos:
                if curr_pos in remaining:
                    remaining.remove(curr_pos)
                prev_dir = curr_dir
                curr_dir = self.find_direction(curr_pos, prev_dir)
                output += self.draw(prev_dir, curr_dir)
                turn = (curr_dir - prev_dir) % self.n_directions
                if turn == 1:
                    # left turn
                    total_turns += 1
                elif turn == 3:
                    # right turn
                    total_turns -= 1
                direction_history.append(curr_dir)
                curr_pos = self.move(curr_pos, curr_dir)

            output += self.draw(curr_dir, start_dir)
            if total_turns < 0:  # reverse
                klass = 'class="reverse" '
            else:
                square = [1, 1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0]
                if (sorted(direction_history) == self.directions or
                    direction_history == square):
                    klass = 'class="colour" '
                else:
                    klass = ''
            output += ' z" %s/>\n' % klass

        return output
