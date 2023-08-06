import vf;
import pytest;

class Subint (int): pass;
class Sublist (list): pass;
class Subdict (dict): pass;

eg_subint = Subint(100);
eg_sublist = Sublist([1, "a", True]);
eg_subdict = Subdict({"foo": "bar"});

def test_typeIs ():
    assert vf.typeIs(bool)(True) == True;
    assert vf.typeIs(int)(1) == True;
    assert vf.typeIs(int)("one") == False;
    assert vf.typeIs(float)(3.33) == True;
    assert vf.typeIs(str)("foo") == True;
    assert vf.typeIs(list)([]) == True;
    assert vf.typeIs(list)(eg_sublist) == False;
    assert vf.typeIs(dict)({"foo":" bar"}) == True;
    assert vf.typeIs(dict)(eg_subdict) == False;
    assert vf.typeIs(Subdict)(eg_subdict) == True;
    assert vf.typeIs(Subdict)({}) == False;

def test_instanceOf ():
    assert vf.instanceOf(int)(1) == True;
    assert vf.instanceOf(int)(eg_subint) == True;
    assert vf.instanceOf(dict)({}) == True;
    assert vf.instanceOf(dict)(eg_subdict) == True;
    assert vf.instanceOf(str)({}) == False;
    assert vf.instanceOf(str)(100) == False;
    
    assert vf.instanceOf(int, str)(1) == True;
    assert vf.instanceOf(int, str)("one") == True;
    assert vf.instanceOf(int, str)({}) == False;
    assert vf.instanceOf(int, dict)({}) == True;
    assert vf.instanceOf(int, dict)(eg_subdict) == True;

def test_typeIn ():
    assert vf.typeIn(int, dict)({}) == True;
    assert vf.typeIn(int, dict)(eg_subdict) == False;

def test_dictOf_basicPostSchema ():
    validator1 = vf.dictOf({
        "_id": vf.typeIs(str),
        "title": vf.typeIs(str),
        "body": vf.typeIs(str),
    });
    assert validator1({"_id": "i", "title": "t", "body": "b"});
    assert validator1({"_id": "", "title": "", "body": ""});
    
    with pytest.raises(vf.ValidationError) as e:
        validator1("Foo!");
    assert "Expected dict-like object" in e.value.args[0];
    
    with pytest.raises(vf.ValidationError) as e:
        validator1({"_id": "a", "title": "t"});
    assert "missing required keys: {'body'}" in e.value.args[0];
    
    with pytest.raises(vf.ValidationError) as e:
        validator1({"_id": "", "title": "", "body": "", "xtra": ""});
    assert "excess keys: {'xtra'}" in e.value.args[0];
    
    
    validator2 = vf.dictOf({
        "_id":   vf.allOf(vf.truthy, vf.typeIs(str)),
        "title": vf.allOf(vf.truthy, vf.typeIs(str)),
        "body":  vf.allOf(vf.truthy, vf.typeIs(str)),
    });
    assert validator1({"_id": "a", "title": "b", "body": "c"});
    with pytest.raises(vf.ValidationError) as e:
        validator2({"_id": "", "title": "b", "body": "c"});
    assert ("key: %r" % "_id") in e.value.args[0];

def test_wrt_readme ():
    personValidator = vf.dictOf({
        "_id": vf.typeIs(str),
        "name": vf.dictOf({
            "first": vf.typeIs(str),            # ---- Equivalent
            "last": lambda x: type(x) is str,   # -----^^^
        }),
        "birth_timestamp": vf.typeIs(int),
        "gender": lambda x: x in ["MALE", "FEMALE", "OTHER"],
        "parentIdList": vf.listOf(vf.typeIs(str)),
        "spouceId": lambda x: x is None or type(x) is str,
        "childrenIdList": vf.listOf(vf.typeIs(str)),
    });
    personValidator({
        "_id": "00a3",
        "name": {"first": "John", "last": "Doe"},
        "birth_timestamp": 318191400000,
        "gender": "MALE",
        "parentIdList": ["00a1", "00a2"],
        "spouceId": "87b1",
        "childrenIdList": ["00a6", "00a8"],
    });
    with pytest.raises(vf.ValidationError) as e:
        personValidator({
            "_id": "1c3f",
            "name": {"first": "Jane", "last": "Doe"},
            "birth_timestamp": "1990-01-01",
            "gender": "FEMALE",
            "parentIdList": ["1c3a", "1c3b"],
            "spouceId": None,
            "childrenIdList": [],
        });
    assert "key: 'birth_timestamp'" in e.value.args[0];

# End ######################################################
