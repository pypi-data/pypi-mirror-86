# Copyright 2018 University of Groningen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import copy

import numpy as np
import pytest

from vermouth import ffinput
from vermouth.molecule import Choice, Link, Block
from vermouth import forcefield



CHOICE = Choice(['A', 'B'])


@pytest.mark.parametrize('key, ref_prefix, ref_base', (
    ('BB', '', 'BB'),
    ('+XX', '+', 'XX'),
    ('--UNK', '--', 'UNK'),
    ('>>>PLOP', '>>>', 'PLOP'),
    ('<<KEY', '<<', 'KEY'),
    ('++ONE+TWO', '++', 'ONE+TWO'),
    ('*****NODE', '*****', 'NODE'),
))
def test_split_node_key(key, ref_prefix, ref_base):
    """
    Test _split_node_key works as expected.
    """
    prefix, base = ffinput._split_node_key(key)
    assert prefix == ref_prefix
    assert base == ref_base


@pytest.mark.parametrize('key', (
    '',  # empty key
    '++',  # no base
    '++-BB',  # mixed prefix
))
def test_split_node_key_error(key):
    """
    Test _split_node_key raises an error when expected.
    """
    with pytest.raises(IOError):
        prefix, base = ffinput._split_node_key(key)
        print('prefix: "{}"; base: "{}"'.format(prefix, base))


@pytest.mark.parametrize('attributes, ref_prefix, ref_order', (
    ({}, '', None),
    ({'order': None}, '', None),
    ({'arbitrary': 'something'}, '', None),
    ({'atomname': 'BB'}, '', None),
    ({'order': 4}, '++++', 4),
    ({'order': -2}, '--', -2),
    ({'order': 0}, '', 0),
    ({'order': np.int16(4)}, '++++', 4),
    ({'order': '>'}, '>', '>'),
    ({'order': '>>'}, '>>', '>>'),
    ({'order': '<'}, '<', '<'),
    ({'order': '<<<'}, '<<<', '<<<'),
    ({'order': '*'}, '*', '*'),
    ({'order': '****'}, '****', '****'),
))
def test_get_order_and_prefix_from_attributes(attributes, ref_prefix, ref_order):
    """
    Test _get_order_and_prefix_from_attributes works as expected.
    """
    (result_prefix,
     result_order) = ffinput._get_order_and_prefix_from_attributes(attributes)
    assert result_prefix == ref_prefix
    assert result_order == ref_order


@pytest.mark.parametrize('attributes', (
    {'order': ''},
    {'order': 4.5},
    {'order': True},
    {'order': False},
    {'order': np.True_},
    {'order': '++'},
    {'order': '-'},
    {'order': '><'},
    {'order': 'invalid'},
))
def test_get_order_and_prefix_from_attributes_error(attributes):
    """
    Test _get_order_and_prefix_from_attributes fails when expected.
    """
    with pytest.raises(IOError):
        result = ffinput._get_order_and_prefix_from_attributes(attributes)
        print(result)


@pytest.mark.parametrize('prefix, ref_prefix, ref_order', (
    ('', None, 0),
    ('+', '+', 1),
    ('++', '++', 2),
    ('-', '-', -1),
    ('---', '---', -3),
    ('>', '>', '>'),
    ('>>>>', '>>>>', '>>>>'),
    ('<', '<', '<'),
    ('<<<', '<<<', '<<<'),
    ('*', '*', '*'),
    ('**', '**', '**'),
))
def test_get_order_and_prefix_from_prefix(prefix, ref_prefix, ref_order):
    """
    Test _get_order_and_prefix_from_prefix works as expected.
    """
    result_prefix, result_order = ffinput._get_order_and_prefix_from_prefix(prefix)
    assert result_prefix == ref_prefix
    assert result_order == ref_order


@pytest.mark.parametrize('key, attributes, ref_prefixed, ref_attributes', (
    # No attribute given
    ('BB', {}, 'BB', {'atomname': 'BB', 'order': 0}),
    ('+BB', {}, '+BB', {'atomname': 'BB', 'order': 1}),
    ('--BB', {}, '--BB', {'atomname': 'BB', 'order': -2}),
    ('>>XX', {}, '>>XX', {'atomname': 'XX', 'order': '>>'}),
    ('<<<YYY', {}, '<<<YYY', {'atomname': 'YYY', 'order': '<<<'}),
    ('****Z', {}, '****Z', {'atomname': 'Z', 'order': '****'}),
    # Order given by the attribute
    ('BB', {'order': 3}, '+++BB', {'atomname': 'BB', 'order': 3}),
    ('XX', {'order': -4}, '----XX', {'atomname': 'XX', 'order': -4}),
    ('YYY', {'order': '>'}, '>YYY', {'atomname': 'YYY', 'order': '>'}),
    ('ZZZZ', {'order': '<<<'}, '<<<ZZZZ', {'atomname': 'ZZZZ', 'order': '<<<'}),
    ('A', {'order': '**'}, '**A', {'atomname': 'A', 'order': '**'}),
    # Order given both with prefix and attribute
    ('BB', {'order': 0}, 'BB', {'atomname': 'BB', 'order': 0}),
    ('++BB', {'order': 2}, '++BB', {'atomname': 'BB', 'order': 2}),
    ('--BB', {'order': -2}, '--BB', {'atomname': 'BB', 'order': -2}),
    ('>>BB', {'order': '>>'}, '>>BB', {'atomname': 'BB', 'order': '>>'}),
    ('<<BB', {'order': '<<'}, '<<BB', {'atomname': 'BB', 'order': '<<'}),
    ('**BB', {'order': '**'}, '**BB', {'atomname': 'BB', 'order': '**'}),
    # atomname given in attribute
    ('BB', {'atomname': 'BB'}, 'BB', {'atomname': 'BB', 'order': 0}),
    ('>>XX', {'atomname': 'BB'}, '>>XX', {'atomname': 'BB', 'order': '>>'}),
    ('YYY', {'atomname': 'BB', 'order': '**'}, '**YYY', {'atomname': 'BB', 'order': '**'}),
    # CHOICE is `Choice(['A', 'B'])`, it is an instance of `molecule.LinkPredicate`.
    ('XX', {'atomname': CHOICE}, 'XX', {'atomname': CHOICE, 'order': 0}),
))
def test_treat_atom_prefix(key, attributes,
                           ref_prefixed, ref_attributes):
    """
    Test _treat_atom_prefix works as expected.
    """
    (result_prefixed,
     result_attributes) = ffinput._treat_atom_prefix(key, attributes)
    assert result_prefixed == ref_prefixed
    assert result_attributes == ref_attributes
    assert result_attributes is not attributes  # We do a shallow copy


def test_treat_atom_prefix_error():
    """
    Test _treat_atom_prefix fails when order is inconsistent.
    """
    with pytest.raises(IOError):
        ffinput._treat_atom_prefix('+A', {'order': -1})


@pytest.mark.parametrize('line, tokens', (
    ('2  3  1  0.2  1000', ['2', '3', '1', '0.2', '1000']),
    ('PO4  GL1  1 0.2  1000', ['PO4', 'GL1', '1', '0.2', '1000']),
    ('PO4  GL1  --  1 0.2  1000', ['PO4', 'GL1', '--', '1', '0.2', '1000']),
    (
        "BB {'resname': 'ALA', 'secstruc': 'H'} BB "
        "{'resname': 'LYS', 'secstruc': 'H', 'order': +1} 1 0.2 1000",
        ['BB', "{'resname': 'ALA', 'secstruc': 'H'}", 'BB',
         "{'resname': 'LYS', 'secstruc': 'H', 'order': +1}",
         '1', '0.2', '1000']
    ),
    (
        "BB {'resname': 'ALA', 'secstruc': 'H'} "
        "+BB {'resname': 'LYS', 'secstruc': 'H'} -- 1 0.2 1000",
        ['BB', "{'resname': 'ALA', 'secstruc': 'H'}",
         '+BB', "{'resname': 'LYS', 'secstruc': 'H'}",
         '--', '1', '0.2', '1000']
    ),
    ('ATOM1{attributes}ATOM2', ['ATOM1', '{attributes}', 'ATOM2']),
    ('ATOM1 {attributes} ATOM2', ['ATOM1', '{attributes}', 'ATOM2']),
    # Note: the brackets here are NOT for str.format!
    ('{} {{}} {{}{{}}}', ['{}', '{{}}', '{{}{{}}}']),  # not str.format
    ('{}{{}}{{}{{}}}', ['{}', '{{}}', '{{}{{}}}']),  # not str.format
    ('', []),
    ('    ', []),
    ('\t', []),
))
def test_tokenize(line, tokens):
    """
    Test that _tokenize works as expected.
    """
    found = ffinput._tokenize(line)
    assert found == tokens


@pytest.mark.parametrize('token', (
    '{{{}}',  # missing closing bracket
    '{{}}}',  # missing openning bracket
))
def test_tokenize_bracket_error(token):
    """
    Test that _tokenize recognizes missing brackets.
    """
    with pytest.raises(IOError):
        # One closing bracket is missing.
        ffinput._tokenize(token)


@pytest.mark.parametrize('line, macros, expected', (
    (  # base case
        'content $macro other content',
        {'macro': 'plop'},
        'content plop other content',
    ),
    (  # non-separated macros
        'content $macro$other end',
        {'macro': 'plop', 'other': 'toto'},
        'content ploptoto end',
    ),
    ('hop $macro{toto}', {'macro': 'plop'}, 'hop plop{toto}'),
    ('hop $macro\n', {'macro': 'plop'}, 'hop plop\n'),
    ('hop $macro\t', {'macro': 'plop'}, 'hop plop\t'),
    ('hop $macro', {'macro': 'plop'}, 'hop plop'),
    (  # nothing to replace
        'hop hop hop',
        {'macro': 'plop'},
        'hop hop hop',
    ),
    (  # empty string
        '',
        {'macro': 'plop'},
        '',
    ),
    (  # multiple times the same
        'content $macro $macro content',
        {'macro': 'plop'},
        'content plop plop content',
    ),
    ('$macro', {'macro': 'plop'}, 'plop'),  # only the macro
    ('start $macro', {'macro': 'plop'}, 'start plop'),  # end with macro
    ('$macro end', {'macro': 'plop'}, 'plop end'),  # start with macro
    ('A {$key : "$value"} B',  # there *must* be a space between the
                               # macro and the colon, otherwise the key is
                               # 'key:' with the colon as a colon is not a
                               # token separator.
     {'key': '"a_key"', 'value': 'a_value'},
     'A {"a_key" : "a_value"} B'),  # play with json dicts
))
def test_substitute_macros(line, macros, expected):
    """
    Test _substitute_macros works as expected.
    """
    found = ffinput._substitute_macros(line, macros)
    assert found == expected


def test_substitute_macros_missing():
    """
    Test _substitute_macros fails when a macro is missing.
    """
    with pytest.raises(KeyError):
        ffinput._substitute_macros('hop $missing end', {'macro': 'plop'})


@pytest.mark.parametrize('tokens, atoms, natoms, expected', (
    (['A', 'B', 'C'], [], 2, True),
    (['A', 'B', 'C'], [], 0, False),
    (['A', 'B', 'C'], ['X', 'Y'], 3, True),
    (['A', 'B', 'C'], ['X', 'Y'], 2, False),
    (['A', 'B', '--', 'C'], [], None, True),
    (['--', 'A', 'B', 'C'], [], None, False),
    ([], [], None, False),
))
def test_some_atoms_left(tokens, atoms, natoms, expected):
    """
    Test _some_atoms_left works as expected.
    """
    tokens = collections.deque(tokens)
    found = ffinput._some_atoms_left(tokens, atoms, natoms)
    assert found == expected


@pytest.mark.parametrize('token, expected', (
    ('{}', {}),
    ('{"atomname": "PO4"}', {'atomname': 'PO4'}),
    ('{"a": "abc", "b": "def"}', {'a': 'abc', 'b': 'def'}),
    ('{"a": "123"}', {'a': '123'}),
    ('{"a": 123}', {'a': 123}),
    ('{"a": null}', {'a': None}),
    ('{"a": true}', {'a': True}),
    ('{"a": false}', {'a': False}),
    ('{"a": "A|B|C"}', {'a': Choice(['A', 'B', 'C'])}),
    ('{"a": {"b": "123"}}', {'a': {'b': '123'}}),
))
def test_parse_atom_attributes(token, expected):
    """
    Test _parse_atom_attributes works as expected.
    """
    found = ffinput._parse_atom_attributes(token)
    assert found == expected


@pytest.mark.parametrize('token', (
    '[1, 2]', '1', 'true', 'false', 'null',  # not dict-like
    "{'a': 123}", '{"a", "b"}',
))
def test_parse_atom_attributes_error(token):
    """
    Test _parse_atom_attributes fails as expected.
    """
    with pytest.raises(ValueError):
        ffinput._parse_atom_attributes(token)


@pytest.mark.parametrize('tokens, natoms, expected', (
    (['A', 'B', 'C'], None, [['A', {}], ['B', {}], ['C', {}]]),
    (['A', 'B'], 2, [['A', {}], ['B', {}]]),
    (['A', '{"a": "abc"}', 'B'], 2, [['A', {'a': 'abc'}], ['B', {}]]),
    (
        ['A', '{"a": "abc"}', 'B', '{"b": 0}'],
        2,
        [['A', {'a': 'abc'}], ['B', {'b': 0}]],
    ),
    (
        ['A', '{"a": "abc"}', 'B', '{"b": 0}', 'C'],
        2,
        [['A', {'a': 'abc'}], ['B', {'b': 0}]],
    ),
    (['1', '2', '1', '0.31', '7500'], 2, [['1', {}], ['2', {}]]),
    (
        ['BB', '{"replace": {"atype": "Qd", "charge": 1}}'],
        1,
        [['BB', {'replace': {'atype': 'Qd', 'charge': 1}}]],
    ),
    (
        ['BB', '++BB', '1', '0.640', '2500', '{"g": "Short", "edge": false}'],
        2,
        [['BB', {}], ['++BB', {}]],
    ),
    (
        ['-BB', 'BB', '+BB', '{"c": "C"}'],
        None,
        [['-BB', {}], ['BB', {}], ['+BB', {'c': 'C'}]],
    ),
    (
        ['-BB', '{"a": 1}', 'BB', '{"b": 2}', '+BB', '{"c": 3}'],
        None,
        [['-BB', {'a': 1}], ['BB', {'b': 2}], ['+BB', {'c': 3}]],
    ),
    (
        ['4', '6', '5', '--', '2'],
        None,
        [['4', {}], ['6', {}], ['5', {}]],
    ),
    (
        ['--'],
        None,
        [],
    ),
))
def test_get_atoms(tokens, natoms, expected):
    """
    Test _get_atoms works as expected.
    """
    tokens = collections.deque(tokens)
    remaining = collections.deque(tokens)
    found = ffinput._get_atoms(tokens, natoms)
    assert found == expected
    # Make sure '--' is consumed if needed
    if tokens:
        assert not tokens[0] == '--'


@pytest.mark.parametrize('token_list, remaining', (
    (['XX', 'YY', '--', 'AA', '--', 'BB'], ['AA', '--', 'BB']),
    (['A', 'B', '--', '--', '1', '2', '--', '3'], ['--', '1', '2', '--', '3']),
    (['A', 'B', '--'], []),
    (['--', 'A', 'B'], ['A', 'B']),
))
def test_separator(token_list, remaining):
    """
    _get_atoms only remove the appropriate separator.
    """
    tokens = collections.deque(token_list)
    ffinput._get_atoms(tokens, None)
    assert list(tokens) == remaining


@pytest.mark.parametrize('tokens, natoms', (
    (['{"a": "abc"}', 'A'], None),  # atom attributes without an atom
))
def test_get_atoms_errors(tokens, natoms):
    """
    Test _get_atoms fails when expected.
    """
    tokens = collections.deque(tokens)
    with pytest.raises(IOError):
        ffinput._get_atoms(tokens, natoms)


@pytest.mark.parametrize('atoms, apply_to_all, existing, expected', (
    ((), {}, {}, {}),
    (
        (('A', {}), ),
        {},
        {},
        {'A': {'atomname': 'A', 'order': 0}}
    ),
    (
        (('A', {}), ('B', {}), ),
        {},
        {},
        {'A': {'atomname': 'A', 'order': 0}, 'B': {'atomname': 'B', 'order':0}},
    ),
    (
        (('+A', {}), ),
        {},
        {},
        {'+A': {'atomname': 'A', 'order': 1}},
    ),
    (
        (('A', {}), ('B', {}), ),
        {'attr': 0},
        {},
        {
            'A': {'atomname': 'A', 'order': 0, 'attr': 0},
            'B': {'atomname': 'B', 'order': 0, 'attr': 0},
        }
    ),
    (
        (('A', {'exist': 'hello'}), ('B', {}), ),
        {},
        {'A': {'new': 'world'}},
        {
            'A': {'atomname': 'A', 'order': 0, 'exist': 'hello', 'new': 'world'},
            'B': {'atomname': 'B', 'order': 0},
        },
    ),
    (
        (('A', {'exist': 'hello'}), ('B', {}), ),
        {'attr': 'plop'},
        {'A': {'new': 'world'}},
        {
            'A': {
                'atomname': 'A', 'order': 0,
                'exist': 'hello', 'new': 'world',
                'attr': 'plop',
            },
            'B': {'atomname': 'B', 'order': 0, 'attr': 'plop'},
        },
    ),
    (
        (('A', {'exist': 'hello'}), ('B', {}), ),
        {'attr': 'plop', 'attr2': 'other plop'},
        {'A': {'new': 'world', 'new2': 'globe'}},
        {
            'A': {
                'atomname': 'A', 'order': 0,
                'exist': 'hello', 'new': 'world', 'new2': 'globe',
                'attr': 'plop', 'attr2': 'other plop',
            },
            'B': {
                'atomname': 'B', 'order': 0,
                'attr': 'plop', 'attr2': 'other plop',
            },
        },
    ),
))
def test_treat_link_interaction_atoms(atoms, apply_to_all, existing, expected):
    """
    Test that _treat_link_interaction_atoms works as expected.
    """
    context = Link()
    if apply_to_all:
        context._apply_to_all_nodes = apply_to_all
    context.add_nodes_from(existing.items())
    ffinput._treat_link_interaction_atoms(atoms, context, 'section')
    found = dict(context.nodes.items())
    assert found == expected


def test_treat_link_interaction_atoms_conflicts():
    """
    Test that _treat_link_interaction_atoms fails when there is a conflict
    between the atoms to add ans the existing atoms.
    """
    context = Link()
    context.add_nodes_from({
        'A': {'exist': 'before'},
    }.items())
    atoms = (('A', {'exist': 'after'}), )
    with pytest.raises(IOError):
        ffinput._treat_link_interaction_atoms(atoms, context, 'section')


@pytest.mark.parametrize('token, expected', (
    ('', False),
    ('(something)', False),
    ('before(inside)after', False),
    ('something()', True),
    ('something(inside)', True),
    ('partial(end', False),
    ('partialend)', False),
    ('(something)(or_other)', False),
    ('(something)or_other', False),
))
def test_is_param_effector(token, expected):
    """
    Test that _is_param_effector recognizes param effector tokens.
    """
    found = ffinput._is_param_effector(token)
    assert found == expected


@pytest.mark.parametrize('tokens, existing', (
    (['A'], set()),
    (['A', 'B'], set()),
    (['A', 'B'], {'X', 'Y'}),
    ([], set()),
    ([], {'X', 'Y'}),
))
def test_parse_features(tokens, existing):
    """
    Test that _parse_features works as expected.
    """
    context = Link()
    if existing:
        context.features = existing
    expected = existing | set(tokens)
    ffinput._parse_features(tokens, context, 'link')
    assert context.features == expected


def test_parse_features_wrong_type():
    """
    Test that _parse_features complains for context different than 'link'.
    """
    context = Link()
    with pytest.raises(IOError):
        ffinput._parse_features(['A', 'B'], context, 'not-link')


@pytest.mark.parametrize('tokens, expected', (
    (['A'], [['A', {}]]),
    (['A', 'B'], [['A', {}], ['B', {}]]),
    (['+A', '{"attr": 0}', 'B'], [['+A', {'attr': 0}], ['B', {}]]),
))
def test_parse_patterns(tokens, expected):
    """
    Test that _parse_patterns works as expected.
    """
    existing = [[['X', {}], ['Y', {}]]]
    full_expected = copy.copy(existing)
    full_expected.append(expected)
    tokens = collections.deque(tokens)
    context = Link()
    context.patterns = existing
    ffinput._parse_patterns(tokens, context, 'link')
    assert context.patterns == full_expected


def test_parse_patterns_wrong_type():
    """
    Test that _parse_patterns complains for context different than 'link'.
    """
    context = Link()
    with pytest.raises(IOError):
        ffinput._parse_patterns(['A', 'B'], context, 'not-link')


@pytest.mark.parametrize('tokens, expected', (
    (['name', '"value"'], {'name': 'value'}),
    (['name', '"a|b|c"'], {'name': 'a|b|c'}),
    (['name', 'value'], {'name': 'value'}),
    (['other-name', '0'], {'other-name': 0}),
    (
        ['name', '{"key": 123, "key2": "value"}'],
        {'name': {'key': 123, 'key2': 'value'}},
    ),
))
def test_parse_variables(tokens, expected):
    """
    Test that _parse_variables works as expected.
    """
    existing = {'existing': 'I was there'}
    full_expected = copy.copy(existing)
    full_expected.update(expected)
    force_field = forcefield.ForceField('dummy')
    force_field.variables = existing

    ffinput._parse_variables(tokens, force_field, 'section')

    assert force_field.variables == full_expected


@pytest.mark.parametrize('tokens', (
    [],
    ['single'],
    ['one', 'two', 'extra'],
))
def test_parse_variables_wrong_length(tokens):
    """
    Test that _parse_variables fails when the number of tokens is wrong.
    """
    force_field = forcefield.ForceField('dummy')
    with pytest.raises(IOError):
        ffinput._parse_variables(tokens, force_field, 'section')


@pytest.mark.parametrize('tokens', (
    ['key', 'value'],
    ['key1', 'new-value'],
    ['key', '"quoted-value"'],
))
def test_parse_macro(tokens):
    """
    Test that _parse_macro works as expected.
    """
    macros = {'key1': 'value1', 'key2': 'value2'}
    expected = copy.copy(macros)
    expected[tokens[0]] = tokens[1]
    tokens = collections.deque(tokens)
    ffinput._parse_macro(tokens, macros)
    assert macros == expected


@pytest.mark.parametrize('tokens', (
    [],
    ['one'],
    ['one', 'two', 'three'],
))
def test_parse_macro_wrong_length(tokens):
    """
    Test that _parse_macro fails when the number of tokens is wrong.
    """
    tokens = collections.deque(tokens)
    with pytest.raises(IOError):
        ffinput._parse_macro(tokens, {})


@pytest.mark.parametrize('tokens, expected', (
    (['#meta', '{"a": "123", "b": 123}'], {'a': '123', 'b': 123}),
    (['ignored', '{"a": "123", "b": 123}'], {'a': '123', 'b': 123}),
))
@pytest.mark.parametrize('context_class, context_type', (
    (Link, 'link'),
    (Block, 'block'),
    (Link, 'modification'),
))
def test_parse_meta(tokens, expected, context_class, context_type):
    """
    Test that _parse_meta works as expected.
    """
    existing = {'key': 'value'}

    full_expected = copy.copy(existing)
    full_expected.update(expected)

    context = context_class()
    context._apply_to_all_interactions['section'] = existing

    ffinput._parse_meta(tokens, context, context_type, 'section')
    assert context._apply_to_all_interactions['section'] == full_expected


@pytest.mark.parametrize('tokens', (
    [],
    ['one'],
    ['one', 'two', 'three'],
))
def test_parse_meta_wrong_length(tokens):
    """
    Test that _parse_meta fails when the number of tokens is wrong.
    """
    with pytest.raises(IOError):
        ffinput._parse_meta(tokens, None, 'type', 'section')
