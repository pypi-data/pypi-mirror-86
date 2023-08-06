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
Test the configuration file
"""

import unittest
import threading
from joulescope_ui import update_check


class TestUpdateCheck(unittest.TestCase):

    def setUp(self):
        self.lock = threading.Lock()
        self.lock.acquire()
        self.update = None

    def callback(self, current_version, latest_version, url):
        self.update = (current_version, latest_version, url)
        self.lock.release()

    def test_is_newer(self):
        update_check.__version__ = "1.2.3"
        self.assertTrue(update_check.is_newer("1.2.4"))
        self.assertTrue(update_check.is_newer("1.3.0"))
        self.assertTrue(update_check.is_newer("2.0.0"))
        self.assertFalse(update_check.is_newer("1.2.3"))
        self.assertFalse(update_check.is_newer("1.2.2"))
        self.assertFalse(update_check.is_newer("1.1.4"))
        self.assertFalse(update_check.is_newer("0.9.9"))

    def test_fetch_invalid_channel(self):
        update_check.__version__ = "999999.0.0"
        with self.assertRaises(ValueError):
            update_check.fetch(self.callback, '__INVALID__')

    def test_fetch_no_update(self):
        update_check.__version__ = "999999.0.0"
        self.assertFalse(update_check.fetch(self.callback))
        self.assertFalse(update_check.fetch(self.callback, 'alpha'))
        self.assertFalse(update_check.fetch(self.callback, 'beta'))
        self.assertFalse(update_check.fetch(self.callback, 'stable'))

    def test_has_update(self):
        update_check.__version__ = "0.0.0"
        update_check.check(self.callback)
        self.lock.acquire()
        self.assertEqual(update_check.__version__, self.update[0])
