import mock
import pytest
from io import StringIO
from PasswordGenerator import PasswordGenerator


class TestPasswordGeneratorConstruction:

    @staticmethod
    def check_error_print_for_given_args(mock_stderr, args, missing_param):
        with pytest.raises(SystemExit) as exception_info:
            PasswordGenerator('foo', args)

        assert 1 == exception_info.value.args[0]
        assert 'Obligatory field "{}" not found in args\n'.format(missing_param) == mock_stderr.getvalue()

    @staticmethod
    def check_if_value_error_occurred_for_given_args(mock_stderr, args):
        with pytest.raises(SystemExit) as exception_info:
            PasswordGenerator('foo', args)

        assert 1 == exception_info.value.args[0]
        assert 'Invalid argument conversion' in mock_stderr.getvalue()

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_password_length_missing(self, mock_stderr):
        args = {}

        self.check_error_print_for_given_args(mock_stderr, args, 'password_length')

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_password_length_malformed(self, mock_stderr):
        args = {'password_length': '#'}

        self.check_if_value_error_occurred_for_given_args(mock_stderr, args)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_allowed_letters_missing(self, mock_stderr):
        args = {'password_length': 1}

        self.check_error_print_for_given_args(mock_stderr, args, 'allowed_letters')

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_allowed_letters_malformed(self, mock_stderr):
        args = {
            'password_length': 1,
            'allowed_letters': 2
        }

        self.check_if_value_error_occurred_for_given_args(mock_stderr, args)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_obligatory_sets_as_not_list(self, mock_stderr):
        args = {
            'password_length': 1,
            'allowed_letters': 'abc',
            'obligatory_sets': 1
        }

        self.check_if_value_error_occurred_for_given_args(mock_stderr, args)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_obligatory_sets_with_non_string_element(self, mock_stderr):
        args = {
            'password_length': 1,
            'allowed_letters': 'abc',
            'obligatory_sets': ['abc', 2]
        }

        self.check_if_value_error_occurred_for_given_args(mock_stderr, args)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_upper_and_lowercase_malformed(self, mock_stderr):
        args = {
            'password_length': 1,
            'allowed_letters': 'abc',
            'upper_and_lowercase': 'f'
        }

        self.check_if_value_error_occurred_for_given_args(mock_stderr, args)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_upper_and_lowercase_malformed(self, mock_stderr):
        args = {
            'password_length': 1,
            'allowed_letters': 'abc',
            'ends_with_letter': 'f'
        }

        self.check_if_value_error_occurred_for_given_args(mock_stderr, args)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_construct_generator_with_upper_and_lowercase_malformed(self, mock_stderr):
        args = {
            'password_length': 1,
            'allowed_letters': 'abc',
            'starts_with_letter': 'f'
        }

        self.check_if_value_error_occurred_for_given_args(mock_stderr, args)

@pytest.fixture
def foo_password_generator():
    params = \
    {
        "password_length": 6,
        "allowed_letters": "abcA",
        "obligatory_sets": [
            "1",
            "2",
        ],
        "upper_and_lowercase": True,
        "ends_with_letter": True,
        "starts_with_letter": True
    }

    return PasswordGenerator('foo', params)


class TestPasswordGenerationProcess:

    def test_prepare_higher_and_lower_letters(self, foo_password_generator):
        assert 'ABCabc' == ''.join(sorted(foo_password_generator._prepare_letters_set()))

    def test_prepare_characters_set(self, foo_password_generator):
        assert '12' == foo_password_generator._prepare_characters_set('')

    def test_calculate_num_of_characters(self, foo_password_generator):
        assert 2 == foo_password_generator._calculate_num_of_characters()

    def test_prepare_random_string_of_characters(self, foo_password_generator):
        set_of_characters = '12345'
        res = foo_password_generator._prepare_random_string_of_characters(set_of_characters, 3)
        assert all(el in set_of_characters for el in res)

    def test_append_obligatory_characters(self, foo_password_generator):
        assert '12' == foo_password_generator._append_obligatory_characters('')

    def test_append_letters_on_ends_if_necessary(self, foo_password_generator):
        assert 'a123a' == foo_password_generator._append_letters_on_ends_if_necessary('123', 'a')

    @mock.patch('PasswordGenerator.PasswordGenerator._append_letters_on_ends_if_necessary')
    @mock.patch('PasswordGenerator.PasswordGenerator._append_obligatory_characters')
    @mock.patch('PasswordGenerator.PasswordGenerator._prepare_random_string_of_characters')
    @mock.patch('PasswordGenerator.PasswordGenerator._calculate_num_of_characters')
    @mock.patch('PasswordGenerator.PasswordGenerator._prepare_characters_set')
    @mock.patch('PasswordGenerator.PasswordGenerator._prepare_letters_set')
    def test_generation_procedure(self,
                                  mocked_prepare_letters_set,
                                  mocked_prepare_characters_set,
                                  mocked_calculate_num_of_characters,
                                  mocked_prepare_random_string_of_characters,
                                  mocked_append_obligatory_characters,
                                  mocked_append_letters_on_ends_if_necessary,
                                  foo_password_generator):

        mocked_prepare_letters_set.side_effect = [mock.sentinel.prepare_letters_set]
        mocked_prepare_characters_set.side_effect = [mock.sentinel.prepare_characters_set]
        mocked_calculate_num_of_characters.side_effect = [mock.sentinel.calculate_num_of_characters]
        mocked_prepare_random_string_of_characters.side_effect = [mock.sentinel.prepare_random_string_of_characters]
        mocked_append_obligatory_characters.side_effect = [mock.sentinel.append_obligatory_characters]
        mocked_append_letters_on_ends_if_necessary.side_effect = [mock.sentinel.append_letters_on_ends_if_necessary]

        assert mock.sentinel.append_letters_on_ends_if_necessary == foo_password_generator.generate()

        mocked_prepare_letters_set.assert_called_once()
        mocked_prepare_characters_set.assert_called_once_with(mock.sentinel.prepare_letters_set)
        mocked_calculate_num_of_characters.assert_called_once()

        mocked_prepare_random_string_of_characters.assert_called_once_with(mock.sentinel.prepare_characters_set,
                                                                           mock.sentinel.calculate_num_of_characters)

        mocked_append_obligatory_characters.assert_called_once_with(mock.sentinel.prepare_random_string_of_characters)

        mocked_append_letters_on_ends_if_necessary.assert_called_once_with(mock.sentinel.append_obligatory_characters,
                                                                           mock.sentinel.prepare_letters_set)
