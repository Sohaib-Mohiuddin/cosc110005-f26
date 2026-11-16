"""Check the Assignment 1 teaching solution against the handout's behaviour."""
import contextlib
import importlib.util
import io
import math
import re
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SOLUTION = ROOT / 'Assignment-1/square_numbers_solution.py'


def load_solution():
    spec = importlib.util.spec_from_file_location(
        'assignment1_solution', SOLUTION)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Assignment1SolutionTests(unittest.TestCase):
    def setUp(self):
        self.solution = load_solution()

    def result_rows(self, text):
        return re.findall(r'^\d+ \(\d+ squared\)$', text, re.MULTILINE)

    def test_complete_results_match_an_independent_integer_square_check(self):
        for lower, upper in [(4, 120), (1, 1), (10000, 10000), (1, 10000),
                             (4, 9), (5, 10), (10, 15), (2, 2), (16, 16),
                             (9800, 9999)]:
            with self.subTest(lower=lower, upper=upper):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.solution.display_square_numbers(lower, upper)
                expected = [f'{number} ({math.isqrt(number)} squared)'
                            for number in range(lower, upper + 1)
                            if math.isqrt(number) ** 2 == number]
                self.assertEqual(self.result_rows(output.getvalue()), expected)
                self.assertEqual('No square numbers were found in this range.'
                                 in output.getvalue(), not expected)
                self.assertIn(f'Square Numbers Between {lower} and {upper}',
                              output.getvalue())

    def test_lower_bound_retries_text_decimal_blank_and_out_of_range(self):
        entries = ['Chicken', '4.5', '4.0', '', '-1', '0', '10001', ' 4 ']
        output = io.StringIO()
        with patch('builtins.input', side_effect=entries) as prompt:
            with contextlib.redirect_stdout(output):
                value = self.solution.read_lower_bound()
        self.assertEqual(value, 4)
        self.assertEqual(prompt.call_count, len(entries))
        self.assertEqual(
            output.getvalue().count('Please enter a whole number.'), 4)
        self.assertEqual(output.getvalue().count('between 1 and 10000.'), 3)

    def test_upper_bound_retries_and_preserves_accepted_lower_bound(self):
        entries = ['hello', '5.5', '4.0', '', '-1', '0', '3', '10001', ' 120 ']
        output = io.StringIO()
        with patch('builtins.input', side_effect=entries) as prompt:
            with contextlib.redirect_stdout(output):
                value = self.solution.read_upper_bound(4)
        self.assertEqual(value, 120)
        self.assertEqual(prompt.call_count, len(entries))
        self.assertTrue(all(call.args == ('Please enter the upper bound: ',)
                            for call in prompt.call_args_list))
        self.assertEqual(
            output.getvalue().count('Please enter a whole number.'), 4)
        self.assertEqual(output.getvalue().count('between 4 and 10000.'), 4)

    def test_results_follow_validation_and_final_pause_occurs(self):
        entries = iter(['Chicken', '4', '3', '120', ''])
        output = io.StringIO()
        prompts = []

        def answer(prompt):
            prompts.append(prompt)
            if prompt.startswith('Please enter'):
                self.assertNotIn('Square Numbers Between', output.getvalue())
                self.assertEqual(self.result_rows(output.getvalue()), [])
            else:
                self.assertEqual(prompt, '\nPress Enter to exit...')
                self.assertEqual(len(self.result_rows(output.getvalue())), 9)
            return next(entries)

        with patch('builtins.input', side_effect=answer):
            with contextlib.redirect_stdout(output):
                self.solution.main()
        self.assertEqual(len(prompts), 5)
        self.assertEqual(prompts.count('Please enter the lower bound: '), 2)
        self.assertEqual(prompts.count('Please enter the upper bound: '), 2)

    def test_banner_has_matching_borders_and_centred_title(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.solution.display_banner('SQUARE NUMBER FINDER')
        self.assertEqual(output.getvalue().splitlines(), [
            '*' * 72, 'SQUARE NUMBER FINDER'.center(72), '*' * 72,
        ])

    def test_real_console_program_finishes_with_supplied_pause_answer(self):
        result = subprocess.run([sys.executable, str(SOLUTION)],
                                input='Chicken\n4.5\n10001\n4\n3\n120\n\n',
                                capture_output=True, text=True, timeout=3)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        self.assertEqual(
            result.stdout.count('Please enter the lower bound: '), 4)
        self.assertEqual(
            result.stdout.count('Please enter the upper bound: '), 2)
        self.assertEqual(self.result_rows(result.stdout), [
            '4 (2 squared)', '9 (3 squared)', '16 (4 squared)',
            '25 (5 squared)', '36 (6 squared)', '49 (7 squared)',
            '64 (8 squared)', '81 (9 squared)', '100 (10 squared)',
        ])
        self.assertTrue(result.stdout.endswith('Press Enter to exit...'))


if __name__ == '__main__':
    unittest.main()
