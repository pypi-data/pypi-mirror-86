VF
==

#### VF = Validation Functions (for Python dicts.)

## Installation
For now, please download the `vf.py` module into your project directory. We should soon introduce a simpler installation method.

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

Use validator function to test if dicts are valid:
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
If validation fails, `vf.ValidationError` will be raised:
```py
personValidator({
    "_id": "1c3f",
    "name": {"first": "Jane", "last": "Doe"},
    "birth_timestamp": "1990-01-01",
    "gender": "FEMALE",
    "parentIdList": ["1c3a", "1c3b"],
    "spouceId": None,
    "childrenIdList": [],
}); # Raises `vf.ValidationError` => Invalid
```

Schema
---------
The schema supplied to `vf.dictOf(.)` should be a `dict`, where each value is a boolean functions. In the above example, `vf.typeIs(str)` is a shorthand for `lambda x: type(x) is str`.

Licensing
------------
Copyright (c) 2020 Polydojo, Inc.

**Software Licensing:**  
The software is released "AS IS" under the **MIT license**, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Kindly see [LICENSE.txt](https://github.com/polydojo/vf/blob/master/LICENSE.txt) for more details.

**No Trademark Rights:**  
The above software licensing terms **do not** grant any right in the trademarks, service marks, brand names or logos of Polydojo, Inc.

