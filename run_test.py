#!/usr/bin/env python3

import argparse
from bisect import bisect_left
import difflib
import json
from math import isclose
from numbers import Real
import re
import subprocess
from typing import Optional, Sequence

# https://www.regular-expressions.info/floatingpoint.html

number_re = re.compile(r'[-+]?[0-9]+\.?[0-9]*(?:[eE][-+]?[0-9]+)?')


def closest(seq: Sequence[Real], x: Real) -> Real:  # https://stackoverflow.com/a/12141511
    """
    Assumes seq is sorted. Returns the closest value to x.

    If two values are equally close, return the smallest number.
    """
    pos = bisect_left(seq, x)
    if pos == 0:
        return seq[0]
    if pos == len(seq):
        return seq[-1]
    before, after = seq[pos - 1], seq[pos]
    if after - x < x - before:
        return after
    else:
        return before


def test(spec, executable, firejail=False, verbose=False) -> Optional[str]:
    """Runs a test according to the specification. Returns an error message or None if all is ok."""

    spec.setdefault('error', False)  # a test case where 'error' isn't specified should return no error
    try:
        stdin = spec['input'].encode()
    except KeyError:
        stdin = '\n'.join(str(x) for x in spec['numeric_input']).encode()
    cmd = ['firejail', '--quiet', executable] if firejail else executable
    result = subprocess.run(cmd, input=stdin, capture_output=True)
    try:
        stdout, stderr = result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    except UnicodeDecodeError:
        stdout, stderr = result.stdout.decode('latin9'), result.stderr.decode('latin9')

    def check_error(expected_error):
        if expected_error:
            if result.returncode == 0:
                return "should have returned an error"
        else:
            if result.returncode != 0:
                return "should not have returned an error"
    
    def diff(expected, obtained):
        return '\n'.join(difflib.unified_diff(expected.splitlines(), obtained.splitlines(),
                                              fromfile='expected', tofile='obtained', lineterm=''))

    def check_stdout(expected_stdout):
        if stdout != expected_stdout:
            return f"differences in output\n{diff(expected_stdout, stdout)}"
    
    def check_stderr(expected_stderr):
        if stderr != expected_stderr:
            return f"differences in standard error\n{diff(expected_stderr, stderr)}"
    
    def check_in_stdout(substrings):
        for substring in substrings:
            if substring not in stdout:
                return f'expected string {repr(substring)} not in output'
    
    def check_close_values(close_values):
        values_in_output = sorted(float(v) for v in number_re.findall(stdout))
        if not values_in_output and close_values:
            return "numeric values expected in the output"
        for v in close_values:
            closest_value = closest(values_in_output, v)
            if not isclose(v, closest_value):
                if verbose:
                    print("output:", stdout)
                    print("values: ", values_in_output)
                return f"{v} expected in the output, closest value is {closest_value}"
    
    checks = [('error', check_error),
              ('stdout', check_stdout),
              ('stderr', check_stderr),
              ('in_stdout', check_in_stdout),
              ('close_values', check_close_values)]

    for field_name, checker in checks:
        try:
            spec_value = spec[field_name]
        except KeyError:
            pass
        else:
            error = checker(spec_value)
            if error is not None:
                return error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('test_data', help="JSON file containing test specification")
    parser.add_argument('exe', nargs='+', help="executables to test")
    parser.add_argument('--verbose', default=False, action='store_true')
    parser.add_argument('--firejail', default=False, action='store_true',
                        help="do not use the firejail sandbox")
    args = parser.parse_args()

    with open(args.test_data) as f:
        cases = json.load(f)

    for executable in args.exe:
        print(executable)
        for i, case in enumerate(cases):
            case_name = f"{i} ({case['name']})" if 'name' in case else f'{i}'
            print(f'test {case_name}:', end=' ', flush=True)
            error = test(case, executable, args.firejail, args.verbose)
            if error is None:
                print("OK")
            else:
                print(error)
        print()


if __name__ == '__main__':
    main()
