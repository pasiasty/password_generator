import pytest
import mock
from SafePRNG import SafePRNG


class TestCheckRangeValidity:

    def test_completely_outside(self):
        curr_range = (0, 1)
        valid_ranges = [(2, 3), (3, 4)]

        with pytest.raises(StopIteration):
            SafePRNG._check_range_validity(curr_range, valid_ranges)

    def test_partially_outside(self):
        curr_range = (0, 2.5)
        valid_ranges = [(2, 3), (3, 4)]

        with pytest.raises(StopIteration):
            SafePRNG._check_range_validity(curr_range, valid_ranges)

    def test_inside(self):
        curr_range = (3.1, 3.5)
        valid_ranges = [(2, 3), (3, 4)]

        assert 1 == SafePRNG._check_range_validity(curr_range, valid_ranges)


class TestDivideRange:

    def test_choose_left_side(self):
        r = (1, 2)
        assert (1, 1.5) == SafePRNG._divide_range(r, 0)

    def test_choose_right_side(self):
        r = (1, 2)
        assert (1.5, 2) == SafePRNG._divide_range(r, 1)


@pytest.fixture
def foo_prng():
    return SafePRNG('foo')


class TestGetRandomInteger:

    @mock.patch('SafePRNG.SafePRNG._get_random_bit')
    def test_case_0(self, mocked_get_random_bit, foo_prng):
        mocked_get_random_bit.side_effect = [1, 0, 1]
        assert 4 == foo_prng.get_random_integer(1, 5)

    @mock.patch('SafePRNG.SafePRNG._get_random_bit')
    def test_case_1(self, mocked_get_random_bit, foo_prng):
        mocked_get_random_bit.side_effect = [1, 1, 1]
        assert 5 == foo_prng.get_random_integer(1, 5)

    @mock.patch('SafePRNG.SafePRNG._get_random_bit')
    def test_case_2(self, mocked_get_random_bit, foo_prng):
        mocked_get_random_bit.side_effect = [0, 0, 0]
        assert 1 == foo_prng.get_random_integer(1, 5)

    @mock.patch('SafePRNG.SafePRNG._get_random_bit')
    def test_case_3(self, mocked_get_random_bit, foo_prng):
        mocked_get_random_bit.side_effect = [0, 1, 0]
        assert 2 == foo_prng.get_random_integer(1, 5)


class TestGetRandomChoice:
    @mock.patch('SafePRNG.SafePRNG.get_random_integer')
    def test_choose_randomly_from_string(self, mocked_get_random_integer, foo_prng):
        input_string = 'anything'
        returned_index = 3
        mocked_get_random_integer.side_effect = [returned_index]
        assert input_string[returned_index] == foo_prng.get_random_choice(input_string)
        mocked_get_random_integer.assert_called_with(0, len(input_string) - 1)
