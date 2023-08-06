semantics2021_toy_languages
===========================

A Python implementation of the toy languages used in [Part IB "Semantics of Programming Languages" (2020 - 2021)](https://www.cl.cam.ac.uk/teaching/2021/Semantics/)

Source hosted at: https://github.com/MitalAshok/semantics2021_toy_languages  
Package hosted at: https://pypi.org/project/semantics2021-toy-languages/

---

Use as a module, like:

```bash
$ python3 -m semantics2021_toy_languages --help
```

You should use a file like `example.L1`:

```
l -> 1234, l0 -> -134, l1 -> 123
l + l0 + l1
```

Where the first line is the initial mappings, and any subsequent lines an L1 expression.

See examples/ for more examples.
