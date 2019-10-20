import markup
import os

def test_doc_props_init():
    prop = "lol: nope\nfoo:      bar\nths:is_random\n nope : var\n!slave | slave2:true\n!slave|master:master"
    prop_dict = markup.doc_props.doc_properties(prop)
    expected = {
        "lol": "nope",
        "foo": "bar",
        "ths": "is_random",
        "nope": "var",
        "slave": "False",
        "slave2": "true",
        "master": "master"
    }
    assert prop_dict.prop_d == expected


def test_doc_props_tag_rep():
    prop = "lol: nope\nfoo:      bar\nths:is_random\n nope : var\n!slave | slave2:true\n!slave|master:master"
    prop_dict = markup.doc_props.doc_properties(prop)
    rep = "()lol()"
    output = prop_dict.tag_rep(rep)
    expected = "nope"
    assert output == expected
