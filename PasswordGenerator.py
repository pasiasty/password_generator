#!/usr/bin/env python3

import argparse
import json
import sys
from SafePRNG import SafePRNG


class PasswordGenerator:

    @staticmethod
    def _check_if_static_parameter_is_boolean(params, parameter_name):
        if parameter_name in params:
            res = params[parameter_name]
            if type(res) != bool:
                raise ValueError('{} should be boolean'.format(parameter_name))
        else:
            res = False

        return res

    def _extract_and_validate_params(self, params):
        try:

            self.password_length = int(params['password_length'])
            self.allowed_letters = params['allowed_letters']

            if type(self.allowed_letters) != str:
                raise ValueError('Allowed letters should be string!')

            if 'obligatory_sets' in params:
                self.obligatory_sets = params['obligatory_sets']
                if type(self.obligatory_sets) != list or any(type(el) != str for el in self.obligatory_sets):
                    raise ValueError('Obligatory sets should be list of strings')
            else:
                self.obligatory_sets = []

            self.upper_and_lowercase = self._check_if_static_parameter_is_boolean(params, 'upper_and_lowercase')
            self.ends_with_letter = self._check_if_static_parameter_is_boolean(params, 'ends_with_letter')
            self.starts_with_letter = self._check_if_static_parameter_is_boolean(params, 'starts_with_letter')

        except KeyError as ex:
            print('Obligatory field "{}" not found in args'.format(ex.args[0]), file=sys.stderr)
            sys.exit(1)

        except ValueError as ex:
            print('Invalid argument conversion: {}'.format(str(ex)), file=sys.stderr)
            sys.exit(1)

    def __init__(self, seed, params):

        self.prng = SafePRNG(seed)
        self._extract_and_validate_params(params)

    def _prepare_letters_set(self):

        res = self.allowed_letters

        if self.upper_and_lowercase:
            low = ''.join(set(self.allowed_letters.lower()))
            high = ''.join(set(self.allowed_letters.upper()))
            res = low + high

        return res

    def _prepare_characters_set(self, letters_set):
        return letters_set + ''.join(self.obligatory_sets)

    def _calculate_num_of_characters(self):
        num_of_characters = self.password_length - len(self.obligatory_sets)

        if self.starts_with_letter:
            num_of_characters -= 1
        if self.ends_with_letter:
            num_of_characters -= 1

        return num_of_characters

    def _prepare_random_string_of_characters(self, characters_set, num_of_characters):
        res = ''

        for _ in range(num_of_characters):
            res += self.prng.get_random_choice(characters_set)

        return res

    def _append_obligatory_characters(self, res):
        for obligatory_set in self.obligatory_sets:
            position = self.prng.get_random_integer(0, len(res))
            res = res[:position] + self.prng.get_random_choice(obligatory_set) + res[position:]

        return res

    def _append_letters_on_ends_if_necessary(self, res, letters_set):
        if self.starts_with_letter:
            res = self.prng.get_random_choice(letters_set) + res
        if self.ends_with_letter:
            res = res + self.prng.get_random_choice(letters_set)

        return res

    def generate(self):

        letters_set = self._prepare_letters_set()
        characters_set = self._prepare_characters_set(letters_set)
        num_of_characters = self._calculate_num_of_characters()

        res = self._prepare_random_string_of_characters(characters_set, num_of_characters)
        res = self._append_obligatory_characters(res)
        res = self._append_letters_on_ends_if_necessary(res, letters_set)

        return res

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--seed', dest='seed', help='Seed used for pseudo random number generator', required=True)
    parser.add_argument('-c', '--config', dest='config', help='path to config json file', required=True)

    args = parser.parse_args()

    params = json.load(open(args.config, 'r'))

    generator = PasswordGenerator(args.seed, params)
    print(generator.generate())

