"""
VF: Validation Functions (for Python dicts.)

Copyright (c) 2020 Polydojo, Inc.

SOFTWARE LICENSING
------------------
The software is released "AS IS" under the MIT License,
WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Kindly
see LICENSE.txt for more details.

NO TRADEMARK RIGHTS
-------------------
The above software licensing terms DO NOT grant any right in the
trademarks, service marks, brand names or logos of Polydojo, Inc.
""";

import functools;
import re;

__version__ = "0.0.1";  # Req'd by flit.

identity = lambda x: x;
truthy = lambda x: bool(x);
falsy = lambda x: not x;
noneIs = lambda x: x is None;

def typeIs (typ):
    "Makes `func (x)` for checking `type(x) is typ`.";
    return lambda x: type(x) is typ;

def instanceOf (*typs):
    "Makes `func (x)` for checking `isinstance(x, typs)`.";
    return lambda x: isinstance(x, typs);

def typeIn (*typs):
    "Makes `func (x)` for checking `type(x) in typs`.";
    return lambda x: type(x) in typs;

def patternIs (pattern):
    "Makes `func (s)` for checking `s` against `pattern`.";
    if type(pattern) is str:
        return lambda s: re.match(pattern, s);
    if type(pattern) is re.Pattern:
        return lambda s: pattern.match(s);
    raise ValueError("Expected `pattern` to be of type "
        "`str` or `re.Pattern`, not: %r" % (pattern,)
    );

def allOf (*fns):
    "Makes `func (x)` for checking `all(fn(x) for fn in fns)`.";
    return lambda x: all(map(lambda fn: fn(x), fns));

def anyOf (*fns):
    "Makes `func (x)` for checking `any(fn(x) for fn in fns)`.";
    return lambda x: any(map(lambda fn: fn(x), fns));

def listOf (fn):
    "Makes `func (li)` for checking `all(fn(x) for x in li)`.";
    return lambda li: isinstance(li, list) and all(map(fn, li));

class BadSchemaError (ValueError): pass;
class ValidationError (ValueError): pass;

def _validateSchemaItself (schema):
    "Ensures that `schema` itself is valid.";
    if not isinstance(schema, dict):
        raise BadSchemaError("Not an instance of `dict`.");
    for key, rhsFn in schema.items():
        if not callable(rhsFn):
            raise BadSchemaError(
                "Non-callable value against key: %r" % (key,),
            );
    return True;

def dictOf (schema, extraKeysOk=False):
    "Makes `func (d)` for VALIDATING `d` against `schema`.";
    assert _validateSchemaItself(schema);
    def validateFn (d):
        if not isinstance(d, dict):
            raise ValidationError(
                "Expected dict-like object, not: %r" % (d,),
            );
        dKeySet = set(d.keys());
        sKeySet = set(schema.keys());
        if not dKeySet.issuperset(sKeySet):
            raise ValidationError("Dict-like object is missing " +
                "required keys: {}".format(sKeySet - dKeySet) #+
            );
        if (not extraKeysOk) and (dKeySet != sKeySet):
            raise ValidationError("Dict-like object has " +
                "excess keys: {}".format(dKeySet - sKeySet) #+
            );
        for key, rhsFn in schema.items():
            assert callable(rhsFn);
            if not rhsFn(d[key]):
                raise ValidationError(
                    ("Against key: %r\n" % (key,)) +
                    ("Unexpected value: %r" % (d[key],)) #+
                );
        return True;
    return validateFn;

# End ######################################################
