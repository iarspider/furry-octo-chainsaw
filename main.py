import copy
from functools import total_ordering


class Direction(object):
    ROW = 1
    COL = 2

    _value = ROW

    def __init__(self, value):
        super(Direction, self).__init__()
        if value == self.ROW or value == self.COL:
            self._value = value

    def toggle(self):
        if self._value == self.ROW:
            self._value = self.COL
        else:
            self._value = self.ROW

    def __eq__(self, other):
        if isinstance(other, Direction):
            return self._value == other._value
        elif isinstance(other, int):
            return self._value == other
        else:
            raise TypeError("Can't compare Direction to {0}".format(type(other)))


@total_ordering
class Chain(object):
    cells = None
    score = 0
    score_cnt = 0
    score_l = None
    chain_s = ""
    fully_solved = False

    def __init__(self, cells):
        self.cells = copy.copy(cells)
        chain_ = (get(c) for c in self.cells)

        self.chain_s = ';'.join(chain_)
        self.score_l = []
        self.get_chain_score()

    def __str__(self):
        return self.chain_s

    def print_mat(self):
        s = []
        for r in range(msize):
            ss = []
            for c in range(msize):
                for i, this_c in enumerate(self.cells):
                    if this_c == (r, c):
                        ss.append('{0:02d}'.format(i + 1))
                        break
                else:
                    ss.append('xx')
            s.append(' '.join(ss))

        return '\n'.join(s)

    def get_chain_score(self):
        self.score = 0
        for i, target in enumerate(targets):
            if target in self.chain_s:
                self.score += (1 << i)
                self.score_cnt += 1
                self.score_l.append(i)

        if self.score == (1 << len(targets)) - 1:
            self.fully_solved = True

    def __eq__(self, other):
        if not isinstance(other, Chain):
            raise TypeError(f"Can't compare Chain to {type(other)}")
        if other.score_cnt == self.score_cnt:
            return other.score == self.score
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if other.score_cnt == self.score_cnt:
            return other.score > self.score
        else:
            return other.score_cnt > self.score_cnt

    def __hash__(self):
        return hash(str(self))


matrix = [x.split() for x in ("1c 1c bd e9 55 e9", "55 55 e9 7a 55 55", "7a e9 e9 7a 1c bd",
                              "7a 1c e9 1c 1c 1c", "1c 55 6a 55 55 7a", "55 bd 7a bd 1c 7a")]
targets = [";".join(x) for x in [y.split() for y in ("7a 1c 55", "55 bd 55", "55 55 55 7a")]]

buffer_l = 8
msize = 0

chains = []
steps = 0


def get(c):
    return matrix[c[0]][c[1]]


def loop(dir_, c, used):
    global chains, steps
    if len(used) == buffer_l:
        steps += 1
        # chains.add(chain)
        this_chain = Chain(used)

        if this_chain.score == 0:
            return False

        chains.append(this_chain)
        if len(chains) % 10000 == 0:
            print(f"Now have {len(chains)}")

        if this_chain.fully_solved:
            print(f"Solved after checking {len(chains)} good chains")
            chains = [this_chain]
            return True

        return False

    this_row, this_col = c

    for i in range(msize):
        if dir_ == Direction.ROW:
            this_cell = (this_row, i)
        else:
            this_cell = (i, this_col)

        if this_cell in used:
            continue
        else:
            # if dir_ == Direction.ROW:
            #     this_col = i
            # else:
            #     this_row = i

            used.append(this_cell)
            dir_.toggle()

            res = loop(dir_, this_cell, used)
            if res:
                return True

            used.pop()
            dir_.toggle()


def main():
    global msize
    dir_ = Direction(Direction.ROW)
    msize = len(matrix)
    if not all(len(x) == msize for x in matrix):
        raise RuntimeError("Invalid matrix!")

    res = loop(dir_, (0, 0), [])
    if res:
        print(f"Full solution found after checking {steps} chains")
    else:
        print(f"Only partial solution(s) found after checking {steps} chains")

    seen_scores = set()

    print(f"Printing solutions (filterd from a list of {len(chains)})")

    for chain in sorted(chains):
        if chain.score not in seen_scores:
            print(f'=== Solution ===')
            print('Sequence:', chain.chain_s.replace(';', ' '), 'score:', chain.score)
            print('Completed targets:', ', '.join(str(x) for x in chain.score_l))
            print('Steps:', ', '.join(str(x) for x in chain.cells))
            print('Matrix:')
            print(chain.print_mat())
            seen_scores.add(chain.score)


if __name__ == '__main__':
    main()
