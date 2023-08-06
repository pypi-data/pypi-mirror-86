"""
An implementation for parsing, stepping, running and evaluating
the toy languages whose syntax and semantics are defined in the
part IB "Semantics of Programming Languages" course, lectured
in the 2020-21 Michaelmas term.
"""

from semantics2021_toy_languages import L1

L1.parse_source('l := ((l := 1; 0) + (l := 2; !l)); l', automatic_zeros=1)