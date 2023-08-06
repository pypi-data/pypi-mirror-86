VF: Validation Functions (for py dicts.)
========================

VF is a simple tool for validating the **schema** of dict-like Python objects. It is well suited for validating user-submitted forms, JSON requests, etc.

## Installation
Install via pip:
```
pip install vf
```
Or download `vf.py` into your project directory.


## Quickstart
Create a validator function by supplying a schema:
```py
import vf;
personValidator = vf.dictOf({
    "_id": vf.typeIs(str),
    "name": vf.dictOf({
        "first": vf.typeIs(str),
        "last": lambda x: type(x) is str,
    }),
    "birth_timestamp": vf.typeIs(int),
    "gender": lambda x: x in ["MALE", "FEMALE", "OTHER"],
    "parentIdList": vf.listOf(vf.typeIs(str)),
    "spouceId": lambda x: x is None or type(x) is str,
    "childrenIdList": vf.listOf(vf.typeIs(str)),
});
```
`vf.dictOf(.)` returns a function for schema validation. (Above, `personValidator` is the returned validation function.)

Use the validator function to test if dicts are valid:
```py
personValidator({
    "_id": "00a3",
    "name": {"first": "John", "last": "Doe"},
    "birth_timestamp": 318191400000,
    "gender": "MALE",
    "parentIdList": ["00a1", "00a2"],
    "spouceId": "87b1",
    "childrenIdList": ["00a6", "00a8"],
}); # Returns `True` => Valid
```
If validation fails, a `vf.ValidationError` will be raised:
```py
personValidator({
    "_id": "1c3f",
    "name": {"first": "Jane", "last": "Doe"},
    "birth_timestamp": "1990-01-01",# NOT int => Invalid
    "gender": "FEMALE",
    "parentIdList": ["1c3a", "1c3b"],
    "spouceId": None,
    "childrenIdList": [],
}); # Raises `vf.ValidationError` => Invalid
```

Schema Validation: How It Works
-----------------------------------------

The schema supplied to `vf.dictOf(.)` should be a `dict`, where each value is a function. In the above example, `vf.typeIs(str)` is a shorthand for `lambda x: type(x) is str`.

For validating a test-dict `tDict` against a schema `schema`, we first ensure that the two have matching keys. Then, each value in `tDict` is supplied to the corresponding function in `schema`. If that function returns `True` (or a truthy value), the key/value pair is considered to be valid, invalid otherwise.

VF includes a number of helpers for generating simple type-checking functions, which are documented below. But as a quick example,

- `vf.typeIs(int)` returns a function for checking if the type of it's argument is an `int`.
- `vf.listOf(vf.typeIs(str))` returns a function for checking for a list of strings.
- `vf.allOf(vf.truthy, vf.typeIs(str))` returns a function that checks for non-blank (i.e. truthy) strings.

#### Write Your Own `lambda`s!

Please note that you aren't limited to VF's helpers. You can write any `lambda` (or reference a `def`'d function) in your schema. For example:
- instead of `vf.allOf(vf.truthy, vf.typeIs(str))`,
- you may write `lambda x: x and type(x) is str`.

More importantly, you will likely have custom validation logic that VF can't anticipate. For example, you may want to match integers between `10` and `1500`. In that case, you could use something like:  
- `lambda x: type(x) is int and 10 <= x <= 1500`

Quick Plug
--------------
VF built and maintained by the folks at [Polydojo, Inc.](https://www.polydojo.com/), led by [Sumukh Barve](https://www.sumukhbarve.com/). If your team is looking for a simple project management tool, please check out our latest product: [**BoardBell.com**](https://www.boardbell.com/).

Helper Nomenclature
---------------------------

At Polydojo, boolean variables are typically given names starting with `is`, `did`, etc. That is, `isNone`, `isType`, `didConfirm` etc. would typically be booleans. Thus, instead of `isType`, VF includes `typeIs(.)`, which is a *helper* that returns a *function* for type-checking.

List Of Helpers
------------------
### Simple functions:

These helpers are simple functions that return `True` or `False`.

- `vf.truthy`: Helper function for checking truthy-ness.
- `vf.falsy`: Helper function for checking falsy-ness.
- `vf.noneIs`: Helper for checking `None`.

### Helpers for generating functions:

These helpers return type-checking functions, which in-turn return `True` or `False`. Here-below, the phrase ***"Makes `func(x)` for ..."*** should be read as ***"Returns a function on `x` for ..."***

- `vf.typeIs(typ)`: Makes `func (x)` for checking `type(x) is typ`.
- `vf.typeIn(*typs)`: Makes `func (x)` for checking `type(x) in typs`.
- `vf.instanceOf(*typs)`: Makes `func (x)` for checking `isinstance(x, typs)`.
- `vf.patternIs(pattern)`: Makes `func (s)` for checking `s` against `pattern` via `re.match` or `re.Pattern.match`. (`s` may be a `str` or a compiled `re.Pattern`.)
- `allOf (*fns)`: Makes `func (x)` for checking `all(fn(x) for fn in fns)`.;
- `anyOf (*fns)`: Makes `func (x)` for checking `any(fn(x) for fn in fns)`.
- `listOf (fn, minLen=0)`: Makes `func (li)` for checking `isinstance(li, list)`, `len(li) >= minLen` and `all(fn(x) for x in li)`.

#### Dict Validation:
And finally, of course, the dict validation function:

- `dictOf(schema, extraKeysOk=False)`: Makes `func (d)` for **validating** `d` against `schema`. Raises `vf.ValidationError` if validation fails.

If `extraKeysOk=True` is passed, it is then acceptable for `d.keys()` to be a superset of `schema.keys()`. Otherwise, `d.keys()` must exactly match `schema.keys()` (irrespective of key-order).

Testing & Contributing
---------------------------

Install pytest via `pip install -U pytest`. Run tests with:
```
pytest
```

If you encounter a bug, please open an issue on GitHub; but if you find a security vulnerability, please email security@polydojo.com instead.

If you'd like to see a new feature or contribute code, please open a GitHub issue. We'd love to hear from you! Suggestions and code contributions will always be appreciated, big and small.

Licensing
------------
Copyright (c) 2020 Polydojo, Inc.

**Software Licensing:**  
The software is released "AS IS" under the **MIT License**, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Kindly see [LICENSE.txt](https://github.com/polydojo/vf/blob/master/LICENSE.txt) for more details.

**No Trademark Rights:**  
The above software licensing terms **do not** grant any right in the trademarks, service marks, brand names or logos of Polydojo, Inc.
