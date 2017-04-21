from hashlib import sha256


class SafePRNG:

    def __init__(self, seed):
        seed = str(seed).encode('utf-8')
        self.state = sha256(seed).digest()

    def _get_random_sequence(self):
        new_state = sha256(self.state).digest()
        res = sha256(self.state + new_state).digest()
        self.state = new_state
        return res

    def _get_random_bit(self):
        return self._get_random_sequence()[0] % 2

    @staticmethod
    def _check_range_validity(curr_range, valid_ranges):
        return next(idx for (idx, el) in enumerate(valid_ranges) if curr_range[0] >= el[0] and curr_range[1] <= el[1])

    @staticmethod
    def _divide_range(r, side):
        if side == 0:
            return r[0], r[0] + (r[1] - r[0]) / 2.
        else:
            return r[0] + (r[1] - r[0]) / 2., r[1]

    def get_random_integer(self, min_val, max_val):

        if max_val == min_val:
            return max_val

        valid_ranges = [(val - .5, val + .5) for val in range(min_val, max_val + 1)]
        curr_range = (min_val - .5, max_val + .5)
        range_is_valid = False

        while not range_is_valid:
            curr_range = self._divide_range(curr_range, self._get_random_bit())
            try:
                return min_val + self._check_range_validity(curr_range, valid_ranges)
            except StopIteration:
                continue

    def get_random_choice(self, array):
        return array[self.get_random_integer(0, len(array) - 1)]
