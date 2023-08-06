"""An implementation of L1

Values:

𝑏 ∈ 𝔹 = { true, false }
𝑛 ∈ ℤ = { ..., -1, 0, 1, ... }
𝑙 ∈ 𝕃 = { l, l0, l1, l2, ... }

Operations:

op ∈ { +, ≥ }

Grammar:

(Quoted strings are literal, spaces (U+0020) do not matter between tokens,
including integer digits, but they do matter in literal tokens)

𝑒 ::= 𝑒 ";" 𝑒
    | 𝑏
    | 𝑛
    | 𝑒 op 𝑒
    | "if" 𝑒 "then" 𝑒 "else" 𝑒
    | 𝑙 ":=" 𝑒
    | "!" 𝑙
    | 𝑙
    | "skip"
    | "while" 𝑒 "do" 𝑒
    | "(" 𝑒 ")"

𝑏 ::= "true" | "false"

digit_non_zero ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
digit ::= digit_non_zero | "0"
digits ::= digit digits
positive_integer = digit_non_zero digits | digit_non_zero
non_negative_integer = positive_integer | "0"

𝑛 ::= non_negative_integer | "-" positive_integer

op ::= "+" | "≥"

As an extension, allow
op ::= "+" | "≥" | ">="

𝑙 ::= "l" | "l" non_negative_integer

Where a greedy algorithm is employed to parse this grammar, so every
rule is left-to-right associative when parsing tokens

As an extension to the language, if the first line starts with "#!",
it is ignored up to the first \n.
Then, a list of initial states can be specified in the form of:

initial_states = 𝑙 "->" 𝑒 "," initial_states | ""

Where 𝑒 will be evaluated with all the mappings given so far, and it
is an error for the same mapping to appear multiple times.

Semantics:

TODO: Complete Semantics section
"""

# TODO: Allow more error conditions rather than just generic errors

import abc
import re
import enum
import typing


__all__ = (
    'Options', 'State', 'Type',

    'Expression',
    'Seq', 'Boolean', 'Integer', 'Operation',
    'Conditional', 'Assignment', 'Dereference',
    'Location', 'Skip', 'WhileLoop', 'Parenthesised',

    'to_ml', 'to_java'
)


SPACE = '[ \\r\\n]'
S = SPACE + '*'  # Any amount of space
SPACE_PATTERN = re.compile(S)
POSITIVE_INTEGER_PATTERN = re.compile(f'{S}[1-9]{S}(?:[0-9]{S})*')
NON_NEGATIVE_INTEGER_PATTERN = re.compile(f'{POSITIVE_INTEGER_PATTERN.pattern}|{S}0{S}')
INTEGER_PATTERN = re.compile(f'{NON_NEGATIVE_INTEGER_PATTERN.pattern}|{S}-{POSITIVE_INTEGER_PATTERN.pattern}')
LOCATION_PATTERN = re.compile(f'{S}l{S}({NON_NEGATIVE_INTEGER_PATTERN.pattern}|)')
BOOLEAN_PATTERN = re.compile(f'{S}(?:true|false){S}')
_SPACE_TO_NONE_TRANSLATION = str.maketrans(dict.fromkeys(' \n\r', None))


def _matches_pattern(pattern, string):
    return bool(pattern.fullmatch(string))


def _purge_spaces(s):
    return s.translate(_SPACE_TO_NONE_TRANSLATION)


def _skip_spaces(source, index):
    return SPACE_PATTERN.match(source, index).end(0)


def integer_token_to_integer(integer_token):
    if not _matches_pattern(INTEGER_PATTERN, integer_token):
        raise ValueError(f'Invalid integer token: {integer_token!r}')
    return int(_purge_spaces(integer_token))


def integer_to_integer_token(integer):
    return str(integer)


def location_token_to_index(location_token):
    match = LOCATION_PATTERN.match(location_token)
    if not match:
        raise ValueError(f'Invalid location token: {location_token!r}')
    index = _purge_spaces(match.group(1))
    if not index:
        return None
    return int(index)


def index_to_location_token(index):
    if index is None:
        return 'l'
    else:
        return f'l{index}'


class Options:
    __slots__ = (
        'L1b_mode', 'allow_two_character_ge', 'allow_non_integer_programs',
        'assign_returns_new_value', 'seq_allows_non_unit',
        'allow_assignment_to_create_new_location',
        'all_locations_implicitly_zero'
    )

    def __init__(self, other=None):
        if isinstance(other, Options):
            self.L1b_mode = other.L1b_mode
            self.allow_two_character_ge = other.allow_two_character_ge
            self.allow_non_integer_programs = other.allow_non_integer_programs
            self.assign_returns_new_value = other.assign_returns_new_value
            self.seq_allows_non_unit = other.seq_allows_non_unit
            self.allow_assignment_to_create_new_location = other.allow_assignment_to_create_new_location
            self.all_locations_implicitly_zero = other.all_locations_implicitly_zero
            return
        self.L1b_mode = False
        self.allow_two_character_ge = True
        self.allow_non_integer_programs = True
        self.assign_returns_new_value = False
        self.seq_allows_non_unit = False
        self.allow_assignment_to_create_new_location = False
        self.all_locations_implicitly_zero = False


class State:
    __slots__ = 'mappings',

    def __init__(self, mappings=None, **extra_mappings):
        if isinstance(mappings, State):
            self.mappings = dict(mappings.mappings)
            return

        normalised_mapping = {}
        for m in (mappings, extra_mappings):
            for k, v in (m.items() if isinstance(m, dict) else () if m is None else m):
                if k is not None:
                    if isinstance(k, int):
                        k = int(k)
                    else:
                        k = location_token_to_index(k)
                if k in normalised_mapping:
                    raise ValueError(f'Duplicate location when initialising environment: {index_to_location_token(k)}')
                if isinstance(v, int):
                    v = int(v)
                else:
                    v = integer_token_to_integer(v)
                normalised_mapping[k] = v
        self.mappings = normalised_mapping

    def __getitem__(self, item):
        try:
            return self.mappings[item]
        except KeyError:
            raise ValueError(f'Tried to access (read) location {index_to_location_token(item)} when there is no such location') from None

    def __setitem__(self, item, value):
        if item not in self.mappings:
            raise ValueError(f'Tried to access (write {value}) location {index_to_location_token(item)} when there is no such location') from None
        self.mappings[item] = value

    def __contains__(self, item):
        return item in self.mappings

    def copy(self):
        return State(self)

    def __add__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            index, new_value = other
            if (index is None or isinstance(index, int)) and isinstance(new_value, int):
                if index is not None:
                    index = int(index)
                new_value = int(new_value)
                copy = self.copy()
                copy[index] = new_value
                return copy
        return NotImplemented

    def __repr__(self):
        return f'State({self.mappings!r})'

    def sorted_keys(self):
        return sorted(self.mappings.keys(), key=(lambda n: -1 if n is None else n))

    def __str__(self):
        keys = self.sorted_keys()
        m = self.mappings
        mappings = ', '.join(f'{index_to_location_token(k)} ↦ {m[k]}' for k in keys)
        return f'{{{mappings}}}'

    def ml_repr(self):
        keys = self.sorted_keys()
        m = self.mappings
        pairs = ', '.join(f'("{index_to_location_token(k)}", {m[k]!s})' for k in keys)
        return f'[{pairs}]'

    def java_repr(self):
        keys = self.sorted_keys()
        if not keys:
            return 'new State()'
        m = self.mappings
        pairs = '; '.join(f'this.add({index_to_location_token(k)}, new Int({m[k]}))' for k in keys) + ';'
        return f'new State(){{{{ {pairs} }}}}'


class Type(enum.Enum):
    UNIT = 0
    INTEGER = 1
    BOOLEAN = 2
    LOCATION = 3


class Expression(abc.ABC):
    __slots__ = 'options',

    def __init__(self, options):
        self.options = options

    @abc.abstractmethod
    def step(self, s: State) -> typing.Tuple['Expression', State]:
        """
        Throws an error if this expression cannot be stepped, otherwise
        a pair (e, s), where e is a new expression, and
        """
        raise NotImplementedError()

    @staticmethod
    def create(source: str, allow_any_type=True, options : Options = Options()) -> 'Expression':
        """
        Parses an Expression and returns the result

        source is a string of the source code
        If allow_any_type is True, allow the expression to have any type
        This is an extension if this expression is the whole program, and
        should have the following results printed:
            UNIT: The entire state at the end of the program
            INTEGER: The integer value
            BOOLEAN: true or false, the boolean value
            LOCATION: The value at the location in the state
        Without this extension, only INTEGER types are allowed as a top-level
        expression
        """
        e = Expression.parse(source, 0, None, None if allow_any_type else {Type.INTEGER}, options)
        if e is None:
            raise ValueError(f'Could not parse {source!r} as an expression')
        e, index = e
        if index != len(source):
            raise ValueError(f'Extraneous data after expression')
        return e

    @classmethod
    @abc.abstractmethod
    def parse(cls, source: str, start_index: int, except_, allow_types, options: Options) -> typing.Optional[typing.Tuple['Expression', int]]:
        """
        Returns (e, new_index) where e was parsed from
        source[start_index: new_index]. If not possible, returns None

        If except_ is a set, will not try to parse those types
        If allow_types is a set, will try to only parse expressions with those
        types
        """
        if except_ is None:
            except_ = frozenset()
        if allow_types is None:
            allow_types = frozenset(Type.__members__.values())
        if not allow_types:
            return None  # No allowed types
        for subclass in Expression._subclasses:
            if subclass in except_:
                continue
            result = subclass.parse(source, start_index, except_ | {subclass}, allow_types, options)
            if result is not None:
                return result

    @abc.abstractmethod
    def __repr__(self) -> str:
        """repr(self)"""
        return object.__repr__(self)

    @abc.abstractmethod
    def __str__(self) -> str:
        """str(self)"""
        return repr(self)

    @abc.abstractmethod
    def ml_repr(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def java_repr(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_type(self) -> Type:
        """Returns the type of this expression (A value from Type)"""
        raise NotImplementedError()

    _subclasses = ()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        Expression._subclasses += cls,

    def __ne__(self, other):
        eq = self.__eq__(other)
        if eq is NotImplemented:
            return NotImplemented
        return not eq

    @abc.abstractmethod
    def __eq__(self, other):
        if not isinstance(self, Expression) or not isinstance(other, Expression):
            return NotImplemented
        return type(self) == type(other)

    def step_all(self, s: State) -> typing.Tuple[typing.Union['Boolean', 'Integer', 'Location', 'Skip'], State]:
        finish_types = frozenset({Boolean, Integer, Location, Skip})
        e = self
        while type(e) not in finish_types:
            e, s = e.step(s)
        return e, s

    def evaluate(self, s):
        e, s = self.step_all(s)
        if type(e) is Skip:
            return s
        if type(e) is Location:
            return s[e.value]
        return e.value

    def print_steps(self, s: State):
        finish_types = frozenset({Boolean, Integer, Location, Skip})
        e = self
        first = True
        while type(e) not in finish_types:
            if first:
                first = False
            else:
                print('->')
            print(f'⟨{e}, {s}⟩')
            e, s = e.step(s)
        print(f'⟨{e}, {s}⟩')

    def visit(self, f):
        f(self)


class Seq(Expression):
    __slots__ = 'left', 'right'

    def __init__(self, left: Expression, right: Expression, options: Options):
        super().__init__(options)
        self.left = left
        self.right = right

    def step(self, s):
        if type(self.left) == Skip:
            return self.right, s  # (seq1)
        if type(self.left) in (Integer, Boolean, Location):
            if self.options.seq_allows_non_unit:
                return self.right, s  # (seq1)
            else:
                raise RuntimeError(f'Seq left ({self.left!r}; right) should be of type UNIT')
        e, s = self.left.step(s)
        return Seq(e, self.right, self.options), s  # (seq2)

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        left = Expression.parse(source, start_index, except_, {Type.UNIT}, options)
        if left is None:
            return None
        left, start_index = left
        if source[start_index: start_index + 1] != ';':
            return None
        right = Expression.parse(source, start_index + 1, None, allow_types, options)
        if right is None:
            return None
        right, start_index = right
        return Seq(left, right, options), start_index

    def __repr__(self):
        return f'Seq({self.left!r}, {self.right!r})'

    def __str__(self):
        return f'{self.left}; {self.right}'

    def ml_repr(self):
        return f'Seq ({self.left.ml_repr()}, {self.right.ml_repr()})'

    def java_repr(self):
        return f'new Seq({self.left.java_repr()}, {self.right.java_repr()})'

    def get_type(self):
        return self.right.get_type()

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.left == other.left and self.right == other.right
        return eq

    def visit(self, f):
        super().visit(f)
        self.left.visit(f)
        self.right.visit(f)


class Boolean(Expression):
    __slots__ = 'value'

    def __init__(self, value: bool, options: Options):
        super().__init__(options)
        if not isinstance(value, bool):
            raise TypeError(f'Boolean(value) should be bool; got {type(value).__name__}')
        self.value = bool(value)

    def step(self, s):
        # Stuck
        raise RuntimeError(f'Tried to step a {self!r}')

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.BOOLEAN not in allow_types:
            return None
        m = BOOLEAN_PATTERN.match(source, start_index)
        if m is None:
            return None
        return Boolean('t' in m.group(0), options), m.end(0)

    def __repr__(self):
        return f'Boolean({self.value})'

    def __str__(self):
        return str(self.value).lower()

    def ml_repr(self):
        return f'Boolean {str(self.value).lower()}'

    def java_repr(self):
        return f'new Bool({str(self.value).lower()})'

    def get_type(self):
        return Type.BOOLEAN

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.value is other.value
        return eq


class Integer(Expression):
    __slots__ = 'value'

    def __init__(self, value: int, options: Options):
        super().__init__(options)
        if not isinstance(value, int):
            raise TypeError(f'Integer(value) should be int; got {type(value).__name__}')
        self.value = int(value)

    def step(self, s):
        # Stuck
        raise RuntimeError(f'Tried to step a {self!r}')

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.INTEGER not in allow_types:
            return None
        m = INTEGER_PATTERN.match(source, start_index)
        if m is None:
            return None
        return Integer(integer_token_to_integer(m.group(0)), options), m.end(0)

    def __repr__(self):
        return f'Integer({self.value})'

    def __str__(self):
        return str(self.value)

    def ml_repr(self):
        return f'Integer {self.value}'

    def java_repr(self):
        return f'new Int({self.value})'

    def get_type(self):
        return Type.INTEGER

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.value is other.value
        return eq


class Operation(Expression):
    __slots__ = 'left', 'op', 'right'

    class Operations(enum.Enum):
        ge = 0
        plus = 1

        def __repr__(self):
            if self is Operation.Operations.ge:
                return 'Operation.Operations.ge'
            return 'Operation.Operations.plus'

    def __init__(self, left: Expression, op: Operations, right: Expression, options: Options):
        super().__init__(options)
        if op is not Operation.Operations.ge and op is not Operation.Operations.plus:
            raise TypeError(f'Operation(left, op, right): op should be Operation.Operations.plus; got {type(op).__name__}')
        if left.get_type() is not Type.INTEGER:
            raise TypeError(f'Operation left ({left!r} op right) should be of type INTEGER')
        if right.get_type() is not Type.INTEGER:
            raise TypeError(f'Operation left (left op {right!r}) should be of type INTEGER')
        self.left = left
        self.op = op
        self.right = right

    def step(self, s):
        left = self.left
        op = self.op
        right = self.right
        if self.options.L1b_mode:
            # Reverse the order of evaluation: Step right first
            if type(right) is not Integer:
                right, s = right.step(s)
                return Operation(left, op, right, self.options), s  # (op1b)
        if type(left) is not Integer:
            left, s = left.step(s)
            return Operation(left, op, right, self.options), s  # (op1) or (op2b)
        if type(right) is not Integer:
            right, s = right.step(s)
            return Operation(left, op, right, self.options), s  # (op2)
        if op is Operation.Operations.ge:
            return Boolean(left.value >= right.value, self.options), s  # (op>=)
        elif op is Operation.Operations.plus:
            return Integer(left.value + right.value, self.options), s  # (op+)

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.BOOLEAN not in allow_types and Type.INTEGER not in allow_types:
            return None
        left = Expression.parse(source, start_index, except_, {Type.INTEGER}, options)
        if left is None:
            return None
        left, start_index = left

        if source[start_index: start_index + 1] == '+':
            op = Operation.Operations.plus
            start_index += 1
        elif source[start_index: start_index + 1] == '≥':
            op = Operation.Operations.ge
            start_index += 1
        elif source[start_index: start_index + 2] == '>=' and options.allow_two_character_ge:
            op = Operation.Operations.ge
            start_index += 2
        else:
            return None
        if op is Operation.Operations.plus:
            if Type.INTEGER not in allow_types:
                return None
        elif op is Operation.Operations.ge:
            if Type.BOOLEAN not in allow_types:
                return None
        right = Expression.parse(source, start_index, None, {Type.INTEGER}, options)
        if right is None:
            return None
        right, start_index = right
        return Operation(left, op, right, options), start_index

    def __repr__(self):
        return f'Operation({self.left!r}, {self.op!r}, {self.right!r})'

    def ml_repr(self):
        op = 'Plus' if self.op is Operation.Operations.plus else 'GTEQ'
        return f'Op ({self.left.ml_repr()}, {op}, {self.right.ml_repr()})'

    def java_repr(self):
        op = 'Plus' if self.op is Operation.Operations.plus else 'GTeq'
        return f'new {op}({self.left.java_repr()}, {self.right.java_repr()})'

    def __str__(self):
        op = '+' if self.op == Operation.Operations.plus else '≥'
        return f'{self.left} {op} {self.right}'

    def get_type(self):
        op = self.op
        if op is Operation.Operations.ge:
            return Type.BOOLEAN
        elif op is Operation.Operations.plus:
            return Type.INTEGER

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.op is other.op and self.left == other.left and self.right == other.right
        return eq

    def visit(self, f):
        super().visit(f)
        self.left.visit(f)
        self.right.visit(f)


class Conditional(Expression):
    __slots__ = 'condition', 'if_true', 'if_false'

    def __init__(self, condition: Expression, if_true: Expression, if_false: Expression, options: Options):
        super().__init__(options)
        if condition.get_type() is not Type.BOOLEAN:
            raise TypeError(f'Conditional condition (if {condition!r} then if_true else if_false) should be of type BOOLEAN')
        if if_true.get_type() is not if_false.get_type():
            raise TypeError(f'Conditional if_true and if_false (if condition then {if_true!r} else {if_false!r}) should be of the same type')
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def step(self, s):
        condition = self.condition
        if type(condition) is Boolean:
            if condition.value:
                return self.if_true, s  # (if1)
            return self.if_false, s  # (if2)
        condition, s = condition.step(s)
        return Conditional(condition, self.if_true, self.if_false, self.options), s  # (if3)

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        start_index = _skip_spaces(source, start_index)
        if source[start_index: start_index + 2] != 'if':
            return None
        condition = Expression.parse(source, start_index + 2, None, {Type.BOOLEAN}, options)
        if condition is None:
            return None
        condition, start_index = condition
        if source[start_index: start_index + 4] != 'then':
            return None
        if_true = Expression.parse(source, start_index + 4, None, allow_types, options)
        if if_true is None:
            return None
        if_true, start_index = if_true
        if source[start_index: start_index + 4] != 'else':
            return None
        if_false = Expression.parse(source, start_index + 4, None, {if_true.get_type()}, options)
        if if_false is None:
            return None
        if_false, start_index = if_false
        return Conditional(condition, if_true, if_false, options), start_index

    def __repr__(self):
        return f'Conditional({self.condition!r}, {self.if_true!r}, {self.if_false!r})'

    def ml_repr(self):
        return f'If ({self.condition.ml_repr()}, {self.if_true.ml_repr()}, {self.if_false.ml_repr()})'

    def java_repr(self):
        return f'new IfThenElse({self.condition.java_repr()}, {self.if_true.java_repr()}, {self.if_false.java_repr()})'

    def __str__(self):
        return f'if {self.condition} then {self.if_true} else {self.if_false}'

    def get_type(self):
        return self.if_true.get_type()

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.condition == other.condition and self.if_true == other.if_true and self.if_false == other.if_false
        return eq

    def visit(self, f):
        super().visit(f)
        self.condition.visit(f)
        self.if_true.visit(f)
        self.if_false.visit(f)


class Assignment(Expression):
    __slots__ = 'location', 'value'

    def __init__(self, location: Expression, value: Expression, options: Options):
        super().__init__(options)
        if location.get_type() is not Type.LOCATION:
            raise TypeError(f'Assignment location ({location!r} := value) should be of type LOCATION')
        if value.get_type() is not Type.INTEGER:
            raise TypeError(f'Assignment value (location := {value!r}) should be of type INTEGER')
        self.location = location
        self.value = value

    def step(self, s):
        location = self.location
        value = self.value
        if type(location) is not Location:
            # Should never happen? All locations are literals
            # Maybe allow extension where (if ... then ... else ...)
            # can evaluate to locations
            location, s = location.step(s)
            return Assignment(location, value, self.options), s
        if type(value) is not Integer:
            value, s = value.step(s)
            return Assignment(location, value, self.options), s  # (assign2)
        l = location.value
        if not self.options.allow_assignment_to_create_new_location and l not in s:
            s[l] = value.value  # Throw error
            assert False
        return Skip(self.options), s + (l, value.value)  # (assign1)

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.UNIT not in allow_types:
            return None
        location = Expression.parse(source, start_index, except_, {Type.LOCATION}, options)
        if location is None:
            return None
        location, start_index = location
        if source[start_index: start_index+2] != ':=':
            return None
        value = Expression.parse(source, start_index + 2, None, {Type.INTEGER}, options)
        if value is None:
            return None
        value, start_index = value
        return Assignment(location, value, options), start_index

    def __repr__(self):
        return f'Assignment({self.location!r}, {self.value!r})'

    def ml_repr(self):
        if type(self.location) is not Location:
            raise ValueError('Using extension where expressions can be (indirect) locations; Cannot convert to ML')
        return f'Assign ("{index_to_location_token(self.location.value)}", {self.value.ml_repr()})'

    def java_repr(self):
        if type(self.location) is not Location:
            raise ValueError('Using extension where expressions can be (indirect) locations; Cannot convert to ML')
        return f'new Assign({index_to_location_token(self.location.value)}, {self.value.java_repr()})'

    def __str__(self):
        return f'{self.location} := {self.value}'

    def get_type(self):
        return Type.INTEGER if self.options.assign_returns_new_value else Type.UNIT

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.location == other.location and self.value == other.value
        return eq

    def visit(self, f):
        super().visit(f)
        self.location.visit(f)
        self.value.visit(f)


class Dereference(Expression):
    __slots__ = 'location',

    def __init__(self, location: Expression, options: Options):
        super().__init__(options)
        self.location = location

    def step(self, s):
        location = self.location
        if type(location) is not Location:
            # Never happens normally (location should be a fixed Location)
            location, s = location.step(s)
            return Dereference(location, self.options), s
        l = location.value
        if self.options.all_locations_implicitly_zero and l not in s:
            return Integer(0, self.options), s
        return Integer(s[l], self.options), s  # (deref)

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.INTEGER not in allow_types:
            return None
        start_index = _skip_spaces(source, start_index)
        if source[start_index:start_index + 1] != '!':
            return None
        location = Expression.parse(source, start_index + 1, None, {Type.LOCATION}, options)
        if location is None:
            return None
        location, start_index = location
        return Dereference(location, options), start_index

    def __repr__(self):
        return f'Dereference({self.location!r})'

    def ml_repr(self):
        if type(self.location) is not Location:
            raise ValueError('Using extension where expressions can be (indirect) locations; Cannot convert to ML')
        return f'Deref "{index_to_location_token(self.location.value)}"'

    def java_repr(self):
        if type(self.location) is not Location:
            raise ValueError('Using extension where expressions can be (indirect) locations; Cannot convert to ML')
        return f'new Deref({index_to_location_token(self.location.value)})'

    def __str__(self):
        return f'!{self.location}'

    def get_type(self):
        return Type.INTEGER

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.location == other.location
        return eq

    def visit(self, f):
        super().visit(f)
        self.location.visit(f)


class Location(Expression):
    __slots__ = 'value',

    def __init__(self, value: typing.Optional[int], options: Options):
        super().__init__(options)
        if value is not None:
            if not isinstance(value, int):
                raise TypeError(f'Location(value) should be None or int; got {type(value).__name__}')
            value = int(value)
        self.value = value

    def step(self, s):
        # stuck
        raise RuntimeError(f'Tried to step a {self!r}')

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.LOCATION not in allow_types:
            return None
        m = LOCATION_PATTERN.match(source, start_index)
        if m is None:
            return None
        return Location(location_token_to_index(m.group(0)), options), m.end(0)

    def __repr__(self):
        return f'Location({self.value!r})'

    def ml_repr(self):
        raise ValueError('Should never have to get the ml_repr of a Location')

    def java_repr(self):
        raise ValueError('Should never have to get the java_repr of a Location')

    def __str__(self):
        return index_to_location_token(self.value)

    def get_type(self):
        return Type.LOCATION

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.value == other.value
        return eq


class Skip(Expression):
    __slots__ = ()

    def __init__(self, options):
        super().__init__(options)

    def step(self, s):
        # stuck
        raise RuntimeError(f'Tried to step a {self!r}')

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.UNIT not in allow_types:
            return None
        start_index = _skip_spaces(source, start_index)
        if source[start_index: start_index + 4] != 'skip':
            return None
        return Skip(options), _skip_spaces(source, start_index + 4)

    def __repr__(self):
        return 'Skip()'

    def ml_repr(self):
        return 'Skip'

    def java_repr(self):
        return 'new Skip()'

    def __str__(self):
        return f'skip'

    def get_type(self):
        return Type.UNIT

    def __eq__(self, other):
        return super().__eq__(other)


class WhileLoop(Expression):
    __slots__ = 'condition', 'body'

    def __init__(self, condition: Expression, body: Expression, options: Options):
        super().__init__(options)
        if condition.get_type() is not Type.BOOLEAN:
            raise TypeError(f'WhileLoop condition (while {condition!r} do body) should be of type BOOLEAN')
        if body.get_type() is not Type.UNIT:
            raise TypeError(f'WhileLoop body (while condition do {body!r}) should be of type UNIT')
        self.condition = condition
        self.body = body

    def step(self, s):
        condition = self.condition
        body = self.body
        options = self.options
        return Conditional(condition, Parenthesised(Seq(body, WhileLoop(condition, body, options), options), options), Skip(options), options), s  # (while)

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        if Type.UNIT not in allow_types:
            return None
        start_index = _skip_spaces(source, start_index)
        if source[start_index: start_index + 5] != 'while':
            return None
        condition = Expression.parse(source, start_index + 5, None, {Type.BOOLEAN}, options)
        if condition is None:
            return None
        condition, start_index = condition
        if source[start_index: start_index + 2] != 'do':
            return None
        body = Expression.parse(source, start_index + 2, {Seq}, {Type.UNIT}, options)
        if body is None:
            return None
        body, start_index = body
        return WhileLoop(condition, body, options), start_index

    def __repr__(self):
        return f'WhileLoop({self.condition!r}, {self.body!r})'

    def ml_repr(self):
        return f'While ({self.condition.ml_repr()}, {self.body.ml_repr()})'

    def java_repr(self):
        return f'new While({self.condition.java_repr()}, {self.body.java_repr()})'

    def __str__(self):
        return f'while {self.condition} do {self.body}'

    def get_type(self):
        return Type.UNIT

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.condition == other.condition and self.body == other.body
        return eq

    def visit(self, f):
        super().visit(f)
        self.condition.visit(f)
        self.body.visit(f)


class Parenthesised(Expression):
    __slots__ = 'expression',

    def __init__(self, expression: Expression, options: Options):
        super().__init__(options)
        self.expression = expression

    def step(self, s):
        return self.expression, s

    @classmethod
    def parse(cls, source, start_index, except_, allow_types, options):
        start_index = _skip_spaces(source, start_index)
        if source[start_index: start_index + 1] != '(':
            return None
        expression = Expression.parse(source, start_index + 1, None, allow_types, options)
        if expression is None:
            return None
        expression, start_index = expression
        if source[start_index: start_index + 1] != ')':
            return None
        return Parenthesised(expression, options), _skip_spaces(source, start_index + 1)

    def __repr__(self):
        return f'Parenthesised({self.expression!r})'

    def ml_repr(self):
        return self.expression.ml_repr()

    def java_repr(self):
        return self.expression.java_repr()

    def __str__(self):
        return f'({self.expression})'

    def get_type(self):
        return self.expression.get_type()

    def __eq__(self, other):
        eq = super().__eq__(other)
        if eq is True:
            return self.expression == other.expression
        return eq

    def visit(self, f):
        super().visit(f)
        self.expression.visit(f)


def parse_source(source: str, automatic_zeros=None, options=Options()):
    if source[0: 2] == '#!':
        try:
            source = source[source.index('\n') + 1:]
        except ValueError:
            pass
    next_line = None
    try:
        next_line = source.index('\n')
    except ValueError:
        pass

    s = State()

    if next_line is not None:
        possible_initial_mapping = source[: next_line]
        pairs = []
        i = 0
        first = True
        while i != len(possible_initial_mapping):
            if first:
                first = False
            else:
                if possible_initial_mapping[i: i + 1] != ',':
                    i = 0
                    break
                i += 1

            location = Expression.parse(possible_initial_mapping, i, set(), {Type.LOCATION}, options)
            if location is None:
                i = 0
                break
            location, i = location
            if type(location) is Location:
                location = location.value
            else:
                try:
                    location, _ = location.step_all(State(pairs))
                except ValueError:
                    i = 0
                    break

            if any(l == location for (l, _) in pairs):
                i = 0
                break

            if possible_initial_mapping[i: i + 2] != '->':
                i = 0
                break

            value = Expression.parse(possible_initial_mapping, i + 2, set(), {Type.INTEGER}, options)
            if value is None:
                i = 0
                break
            value, i = value
            if type(value) is Integer:
                value = value.value
            else:
                try:
                    value, _ = value.step_all(State(pairs))
                except ValueError:
                    i = 0
                    break

            pairs.append((location, value))

        if i == len(possible_initial_mapping):
            try:
                s = State(pairs)
            except ValueError:
                i = 0
        if i == len(possible_initial_mapping):
            source = source[next_line + 1: ]

    e = Expression.create(source, options=options)

    if automatic_zeros is not None and automatic_zeros is not False:
        if automatic_zeros is True:
            automatic_zeros = 0
        else:
            automatic_zeros = int(automatic_zeros)
        all_locations = set()
        def visitor(e):
            if type(e) == Location:
                all_locations.add(e.value)
        e.visit(visitor)
        zeroed = dict.fromkeys(all_locations, automatic_zeros)
        zeroed.update(s.mappings)
        s.mappings = zeroed

    return e, s


def to_ml(e: Expression, s: State):
    return f'prettyreduce ({e.ml_repr()}, {s.ml_repr()})'


def to_java(e: Expression, s: State):
    sorted_keys = s.sorted_keys()
    l_names = tuple(map(index_to_location_token, sorted_keys))

    lines = [
        '// Matthew Parkinson, 1/2004',
        '',
        'public class L1 {',
        '',
        '    public static void main(String[] args) {'
    ]
    lines.extend([f'        Location {l} = new Location("{l}");' for l in l_names])
    lines.extend([
        '',
        '        State s = ' + s.java_repr() + ';',
        '',
        '        Environment env = new Environment()',
        '            ' + ''.join(f'.add({l})' for l in l_names) + ';',
        '',
        '        Expression e =',
        '            ' + e.java_repr(),
        '        ;',
        '',
        '        try {',
        '            // Type check',
        '            Type t = e.typeCheck(env);',
        '            System.out.println("Program has type: " + t);',
        '',
        '            // Evaluate the program',
        '            System.out.printf("%s%n%n", e);',
        '            while (!(e instanceof Value)) {',
        '                e = e.smallStep(s);',
        '                // Display each step of reduction',
        '                System.out.printf("%s%n%n", e);',
        '            }',
        '',
        '            // Give some output',
        '            System.out.println("Program has type: " + t);',
        '            System.out.println("Result has type: " + e.typeCheck(env));',
        '            System.out.println("Result: " + e);',
        '            System.out.println("Terminating State: " + s);',
        '        } catch (TypeError te) {',
        '            System.out.printf("Error:%n%s", te);',
        '            System.out.printf("From code:%n%s", e);',
        '        } catch (CanNotReduce cnr) {',
        '            System.out.println("Caught Following exception" + cnr);',
        '            System.out.printf("While trying to execute:%n%s", e);',
        '            System.out.printf("In state:%n%s", s);',
        '        }',
        '    }',
        '',
        '}',
        ''
    ])

    return '\n'.join(lines)
