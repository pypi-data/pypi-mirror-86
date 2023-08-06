from semantics2021_toy_languages import *

import sys
import argparse


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser('semantics2021_toy_languages')
    parser.add_argument('file', help='The file to run')
    parser.add_argument('-x', '--lang', choices={'L1', 'L1b'}, default=None, help='The language to run the file as. Default to guess from the file extension (.l1 -> L1, .l1b -> L1b)')
    parser.add_argument('-z', '--zero', action='store_true', help='Initially set all locations accessed to 0')
    parser.add_argument('-s', '--steps', action='store_true', help='Show all the steps of derivation')
    parser.add_argument('--repr', action='store_true', help='Show a (Python) representation of the program before doing anything else')

    parsed = parser.parse_args(argv)
    file = parsed.file
    lang = parsed.lang
    print_repr = parsed.repr
    steps = parsed.steps
    zero = parsed.zero

    if lang is None:
        flower = file.lower()
        if flower.endswith('.l1'):
            lang = 'L1'
        elif flower.endswith('.l1b'):
            lang = 'L1B'
        else:
            print('Could not recognize language from file extension. Please run with `--lang LANGUAGE` (See `--help`)', file=sys.stderr, flush=True)
            return 1
    else:
        lang = lang.upper()

    if lang not in ('L1', 'L1B'):
        return 1

    sys.stdout.flush()
    sys.stderr.flush()

    if file == '-':
        source = sys.stdin.read()
    else:
        with open(file, 'r') as f:
            source = f.read()

    if lang == 'L1' or lang == 'L1B':
        options = L1.Options()
        if lang == 'L1B':
            options.L1b_mode = True
        e, s = L1.parse_source(source, zero, options)
        if print_repr:
            print('Python:')
            print(repr(e))
            print(repr(s))
            print('ML:')
            print(L1.to_ml(e, s))
            print('Java:')
            print(L1.to_java(e, s), flush=True)
        if steps:
            try:
                e.print_steps(s)
                sys.stdout.flush()
            except (RuntimeError, ValueError) as e:
                print(e, file=sys.stderr, flush=True)
                return 1
        else:
            try:
                print(e.evaluate(s), flush=True)
            except (RuntimeError, ValueError) as e:
                print(e, file=sys.stderr, flush=True)
                return 1
        return 0
    else:
        assert False


if __name__ == '__main__':
    ret = main()
    if ret:
        sys.exit(ret)
    else:
        del ret
