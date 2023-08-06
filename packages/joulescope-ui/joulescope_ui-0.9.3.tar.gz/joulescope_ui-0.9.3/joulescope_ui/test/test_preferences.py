# Copyright 2019 Jetperch LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test the preferences
"""

import unittest
import json
import os
from joulescope_ui.preferences import Preferences, validate, options_conform, BASE_PROFILE
from joulescope_ui import paths


INVALID_CONFIG1 = {
  "type": "invalid",
  "version": 2,
  "profile": "Oscilloscope",
  "profiles": {
    "defaults": {},
    "Oscilloscope": {}
  }
}


class TestPreferences(unittest.TestCase):

    def setUp(self):
        self.listener_calls = []
        self.app = f'joulescope_preferences_{os.getpid()}'
        self.paths = paths.paths_current(app=self.app)
        os.makedirs(self.paths['dirs']['config'])
        self.p = Preferences(app=self.app)

    def tearDown(self):
        paths.clear(app=self.app, delete_data=True)

    def test_get_without_set_or_define(self):
        with self.assertRaises(KeyError):
            self.p.get('hello')
        with self.assertRaises(KeyError):
            self.p['hello']

    def test_set_get_without_define(self):
        self.p.set('hello', 'world')
        self.assertEqual('world', self.p.get('hello'))

    def test_get_set_get(self):
        with self.assertRaises(KeyError):
            self.p.get('hello')
        self.assertEqual('default', self.p.get('hello', default='default'))
        self.p.set('hello', 'world')
        self.assertEqual('world', self.p.get('hello'))
        self.assertEqual('world', self.p.get('hello', default='default'))

    def test_contains(self):
        self.assertFalse('hello' in self.p)
        self.p['hello'] = 'world'
        self.assertTrue('hello' in self.p)

    def test_set_profile_missing(self):
        with self.assertRaises(KeyError):
            self.p.set('hello', 'world', profile='p1')

    def test_get_profile_missing(self):
        with self.assertRaises(KeyError):
            self.p.get('hello', profile='p1')

    def test_set_clear(self):
        self.p.set('hello', 'world')
        self.p.clear('hello')
        with self.assertRaises(KeyError):
            self.p.get('hello')

    def test_define_set_clear(self):
        self.p.define(name='hello', default='default')
        self.p.set('hello', 'world')
        self.p.clear('hello')
        self.assertEqual('default', self.p.get('hello'))

    def test_profile_add_remove(self):
        self.assertEqual(BASE_PROFILE, self.p.profile)
        self.assertEqual([BASE_PROFILE], self.p.profiles)
        self.p.profile_add('p1')
        self.assertEqual([BASE_PROFILE, 'p1'], self.p.profiles)
        self.assertEqual(BASE_PROFILE, self.p.profile)
        self.p.profile = 'p1'
        self.assertEqual('p1', self.p.profile)
        self.p.profile_remove('p1')
        self.assertEqual(BASE_PROFILE, self.p.profile)
        self.assertEqual([BASE_PROFILE], self.p.profiles)

    def test_profile_override(self):
        self.p.set('hello', 'all_value')
        self.assertEqual('all_value', self.p.get('hello'))
        self.p.profile_add('p1', activate=True)
        self.assertEqual('all_value', self.p.get('hello'))
        self.assertFalse(self.p.is_in_profile('hello'))
        self.p.set('hello', 'p1_value')
        self.assertTrue(self.p.is_in_profile('hello'))
        self.assertEqual('p1_value', self.p.get('hello'))
        self.p.profile = BASE_PROFILE
        self.assertEqual('all_value', self.p.get('hello'))

    def test_load_not_found(self):
        self.p.define(name='hello', default='world')
        self.assertEqual('world', self.p['hello'])
        self.assertFalse(self.p.load())
        self.assertEqual('world', self.p['hello'])

    def test_load_invalid_json(self):
        with open(self.p._path, 'wt') as f:
            f.write('{"hello": "world",}')  # invalid JSON
        self.assertFalse(self.p.load())

    def test_load_invalid_type(self):
        with open(self.p._path, 'wt') as f:
            f.write(json.dumps(INVALID_CONFIG1))
        self.assertFalse(self.p.load())

    def test_save_load_simple(self):
        self.p.set('hello', 'world')
        self.p.save()
        p = Preferences(app=self.app)
        self.assertTrue(p.load())
        self.assertEqual('world', p.get('hello'))

    def test_save_load_skip_starting_with_pound(self):
        self.p.set('hello/#there', 'world')
        self.assertIn('hello/#there', self.p)
        self.p.save()
        p = Preferences(app=self.app)
        self.assertTrue(p.load())
        self.assertNotIn('hello/#there', p)

    def test_save_load_bytes(self):
        self.p.set('hello', b'world')
        self.p.save()
        p = Preferences(app=self.app)
        self.assertTrue(p.load())
        self.assertEqual(b'world', p.get('hello'))

    def test_define_default_when_new(self):
        self.p.define(name='hello', default='world')
        self.assertEqual('world', self.p.get('hello'))

    def test_define_default_when_existing(self):
        self.p.set('hello', 'there')
        self.p.define(name='hello', default='world')
        self.assertEqual('there', self.p.get('hello'))

    def test_validate_str(self):
        self.assertEqual('there', validate('there', 'str'))
        with self.assertRaises(ValueError):
            validate(1, 'str')
        with self.assertRaises(ValueError):
            validate(1.0, 'str')
        with self.assertRaises(ValueError):
            validate([], 'str')
        with self.assertRaises(ValueError):
            validate({}, 'str')

    def test_validate_str_options_list(self):
        options = options_conform(['a', 'b', 'c'])
        self.assertEqual('a', validate('a', 'str', options=options))
        with self.assertRaises(ValueError):
            validate('A', 'str', options=options)

    def test_validate_str_options_map(self):
        options = options_conform({
            'a': {'brief': 'option a'},
            'b': {'brief': 'option b'},
            'c': {}})
        self.assertEqual('a', validate('a', 'str', options=options))
        with self.assertRaises(ValueError):
            validate('A', 'str', options=options)

    def test_validate_str_options_map_with_aliases(self):
        options = options_conform({'a': {'brief': 'option a', 'aliases': ['b', 'c']}})
        self.assertEqual('a', validate('a', 'str', options=options))
        self.assertEqual('a', validate('b', 'str', options=options))
        self.assertEqual('a', validate('c', 'str', options=options))
        with self.assertRaises(ValueError):
            validate('d', 'str', options=options)

    def test_options_callable_list(self):
        self.assertEqual('a', validate('a', 'str', options=lambda: ['a']))
        with self.assertRaises(ValueError):
            validate('d', 'str', options=lambda: ['a'])

    def test_options_callable_dict(self):
        self.assertEqual('a', validate('a', 'str', options=lambda: {'a': 'a'}))
        with self.assertRaises(ValueError):
            validate('d', 'str', options=lambda: {'a': 'a'})

    def test_validate_int(self):
        self.assertEqual(1, validate(1, 'int'))
        self.assertEqual(1, validate('1', 'int'))
        with self.assertRaises(ValueError):
            validate('world', 'int')

    def test_validate_int_range(self):
        options = {'min': 1, 'max': 11, 'step': 2}
        self.assertEqual(1, validate(1, 'int', options=options))
        self.assertEqual(3, validate(3, 'int', options=options))
        self.assertEqual(11, validate(11, 'int', options=options))
        with self.assertRaises(ValueError):
            validate(-1, 'int', options=options)
        with self.assertRaises(ValueError):
            validate(2, 'int', options=options)
        with self.assertRaises(ValueError):
            validate(13, 'int', options=options)

    def test_validate_int_list(self):
        options = [6, 7, 8, 10, 12, 14, 16, 20, 24, 32, 40, 48, 64]
        self.assertEqual(10, validate(10, 'int', options=options))
        self.assertEqual(10, validate('10', 'int', options=options))
        with self.assertRaises(ValueError):
            self.assertEqual(10, validate(11, 'int', options=options))

    def test_validate_float(self):
        self.assertEqual(1, validate(1, 'float'))
        self.assertEqual(1.1, validate(1.1, 'float'))
        self.assertEqual(1.1, validate('1.1', 'float'))
        with self.assertRaises(ValueError):
            validate('world', 'float')

    def test_validate_bool(self):
        self.assertEqual(True, validate(True, 'bool'))
        self.assertEqual(False, validate(False, 'bool'))
        self.assertEqual(False, validate(None, 'bool'))
        self.assertEqual(False, validate('off', 'bool'))
        self.assertEqual(False, validate('none', 'bool'))
        self.assertEqual(False, validate('None', 'bool'))
        self.assertEqual(False, validate('0', 'bool'))
        self.assertEqual(True, validate(1, 'bool'))
        self.assertEqual(True, validate('1.1', 'bool'))

    def test_validate_bytes(self):
        self.assertEqual(True, validate(b'12345', 'bytes'))

    def test_validate_dict(self):
        self.assertEqual({}, validate({}, 'dict'))
        with self.assertRaises(ValueError):
            validate('world', 'dict')

    def test_validate_none(self):
        self.assertEqual('hi', validate('hi', 'none'))

    def test_validate_color(self):
        self.assertEqual((1, 2, 3, 255), validate([1, 2, 3], 'color'))
        self.assertEqual((1, 2, 3, 4), validate([1, 2, 3, 4], 'color'))
        self.assertEqual((255, 0, 0, 255), validate('red', 'color'))
        with self.assertRaises(ValueError):
            validate('djflkajfdsfklsj', 'color')
        with self.assertRaises(ValueError):
            validate([1, 2], 'color')

    def test_validate_font(self):
        validate('Monospaced', 'font')

    def test_set_invalid_type(self):
        self.p.define(name='hello', dtype='str', default='world')
        with self.assertRaises(ValueError):
            self.p.set('hello', 1)

    def test_set_invalid_option(self):
        self.p.define(name='hello', dtype='str', options=['there', 'world'], default='world')
        self.p.set('hello', 'there')
        with self.assertRaises(ValueError):
            self.p.set('hello', 'you')

    def test_set_invalid_default(self):
        with self.assertRaises(ValueError):
            self.p.define(name='hello', dtype='str', options=['there', 'world'], default='bad')

    def test_set_invalid_existing(self):
        self.p['hello'] = 'bad'
        self.p.define(name='hello', dtype='str', options=['there', 'world'], default='there')

    def test_definition_get(self):
        self.p.define(name='hello', dtype='str', default='world')
        d = self.p.definition_get(name='hello')

    def test_definitions_get(self):
        self.p.define(name='/', brief='top level', dtype='container')
        self.p.define(name='hello/', brief='holder', dtype='container')
        self.p.define(name='hello/world', brief='hello', dtype='str', default='world')
        self.p.define(name='hello/there/world', brief='hello', dtype='str', default='world')
        d = self.p.definitions
        self.assertEqual('/', d['name'])
        self.assertIn('children', d)
        self.assertEqual('hello/', d['children']['hello']['name'])
        self.assertEqual('hello/there/', d['children']['hello']['children']['there']['name'])

    def test_dict_style_access(self):
        p = self.p
        self.assertEqual(0, len(p))
        p.define(name='hello/a', dtype='str', default='a_default')
        p.define(name='hello/b', dtype='str', default='b_default')
        self.assertEqual(2, len(p))
        self.assertIn('hello/a', p)
        pairs = [(key, value) for key, value in p]
        self.assertEqual([('hello/a', 'a_default'), ('hello/b', 'b_default')], pairs)

        p.profile_add('p1', activate=True)
        p['hello/a'] = 'a_override'
        self.assertEqual('a_override', p['hello/a'])
        self.assertEqual('b_default', p['hello/b'])
        self.assertEqual(2, len(p))
        del p['hello/a']
        self.assertEqual(2, len(p))
        self.assertEqual('a_default', p['hello/a'])

    def test_items(self):
        p = self.p
        p.define(name='a', dtype='str', default='zz')
        p.define(name='a/0', dtype='str', default='0')
        p.define(name='a/1', dtype='str', default='1')
        p.define(name='b/2', dtype='str', default='2')
        p.profile_add('p1', activate=True)
        p['a/1'] = 'new'
        self.assertEqual([('a', 'zz'), ('a/0', '0'), ('a/1', 'new'), ('b/2', '2')], list(p.items()))
        self.assertEqual([('a', 'zz'), ('a/0', '0'), ('a/1', 'new')], list(p.items(prefix='a')))
        self.assertEqual([('a/0', '0'), ('a/1', 'new')], list(p.items(prefix='a/')))
        self.assertEqual([('b/2', '2')], list(p.items(prefix='b/')))

    def test_purge_single(self):
        self.p.define(name='a', dtype='str', default='zz')
        self.p.profile_add('p1', activate=True)
        self.p['a'] = '1'
        r = self.p.purge('a')
        self.assertEqual({BASE_PROFILE: {'a': 'zz'}, 'p1': {'a': '1'}}, r['profiles'])
        with self.assertRaises(KeyError):
            self.p['a']
        self.p.restore(r)
        self.assertEqual('1', self.p['a'])
        self.p.profile = BASE_PROFILE
        self.assertEqual('zz', self.p['a'])
        with self.assertRaises(ValueError):
            self.p['a'] = 1

    def test_purge_hierarchy(self):
        p = self.p
        p.define(name='a/0', dtype='str', default='0')
        p.define(name='a/1', dtype='str', default='1')
        self.p.profile_add('p1', activate=True)
        self.p['a/0'] = '00'
        r = self.p.purge('a/')
        with self.assertRaises(KeyError):
            self.p['a/0']
        self.p.restore(r)
        self.assertEqual('00', self.p['a/0'])
        self.p.profile = BASE_PROFILE
        self.assertEqual('0', self.p['a/0'])
        with self.assertRaises(ValueError):
            self.p['a/0'] = 1

    def test_match(self):
        p = self.p
        p.define(name='a/0', dtype='str', default='0')
        p.define(name='a/1', dtype='str', default='1')
        self.assertEqual(['a/0', 'a/1'], p.match('a/'))
        self.assertEqual(['a/0'], p.match('a/0'))
        p.profile_add('p1', activate=True)
        self.assertEqual([], p.match('a/'))
        p['a/0'] = 'zz'
        self.assertEqual(['a/0'], p.match('a/'))

    def test_singleton(self):
        self.p.define(name='a', dtype='str', default='0', default_profile_only=True)
        self.p.profile_add('p', activate=True)
        self.p['a'] = 'override'
        self.assertEqual('override', self.p.get('a', profile='p'))
        self.assertEqual('override', self.p.get('a', profile=BASE_PROFILE))

    def test_restore_base_default(self):
        self.p.define(name='a', dtype='str', default='0')
        self.p['a'] = 'base'
        self.p['b'] = 'no define'
        self.p.profile_add('p', activate=True)
        self.p['a'] = 'override'
        self.p.restore_base_defaults()
        self.assertEqual('override', self.p['a'])
        self.assertEqual('0', self.p.get('a', profile=BASE_PROFILE))
        self.assertEqual('no define', self.p.get('b', profile=BASE_PROFILE))

    def test_define_base_profile_only_but_already_exists(self):
        self.p.profile_add('p', activate=True)
        self.p['hello'] = 'world'
        self.p.define(name='hello', dtype='str', options=['there', 'world'],
                      default='there', default_profile_only=True)
        self.assertEqual('there', self.p['hello'])

    def test_get_defaults(self):
        self.p.define(name='hello', dtype='str', default='there')
        self.p['hello'] = 'world'
        self.assertEqual('world', self.p['hello'])
        self.assertEqual('there', self.p.definition_get('hello')['default'])
