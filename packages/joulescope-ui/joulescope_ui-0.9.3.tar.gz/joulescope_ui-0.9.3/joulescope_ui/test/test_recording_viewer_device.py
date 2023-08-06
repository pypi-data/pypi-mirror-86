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
from unittest.mock import MagicMock
from joulescope_ui.recording_viewer_device import RecordingViewerDevice
from joulescope.stream_buffer import StreamBuffer, usb_packet_factory
import io
from joulescope.data_recorder import DataRecorder
from joulescope.calibration import Calibration
import threading


class TestRecordingViewerDevice(unittest.TestCase):

    def _create_file(self, packet_index, count=None):
        stream_buffer = StreamBuffer(401.0, [200, 100], 1000.0)
        stream_buffer.suppress_mode = 'off'
        if packet_index > 0:
            data = usb_packet_factory(0, packet_index - 1)
            stream_buffer.insert(data)
            stream_buffer.process()

        fh = io.BytesIO()
        d = DataRecorder(fh)
        d.stream_notify(stream_buffer)
        data = usb_packet_factory(packet_index, count)
        stream_buffer.insert(data)
        stream_buffer.process()
        d.stream_notify(stream_buffer)
        d.close()
        fh.seek(0)
        return fh

    def setUp(self):
        self.lock = threading.Lock()
        self.lock.acquire()
        self.updates = []
        self.d = RecordingViewerDevice(self._create_file(0, 2))
        self.d.open()

    def tearDown(self):
        self.d.close()

    def on_update_fn(self, data):
        self.updates.append(data)
        self.lock.release()

    def test_properties(self):
        self.assertEqual(1000.0, self.d.sampling_frequency)
        self.assertIsInstance(self.d.calibration, Calibration)

    def test_view_open_close(self):
        v = self.d.view_factory()
        v.open()
        self.assertEqual(1000.0, v.sampling_frequency)
        self.assertIsInstance(v.calibration, Calibration)
        self.assertEqual([0.0, 0.252], v.limits)
        self.assertEqual(0, v.time_to_sample_id(v.sample_id_to_time(0)))
        self.assertEqual(0.0, v.sample_id_to_time(0))
        self.assertEqual(0.2, v.sample_id_to_time(200))
        self.assertEqual(200, v.time_to_sample_id(0.2))
        v.close()

    def test_view_close_after_device(self):
        v = self.d.view_factory()
        v.open()
        self.d.close()
        v.close()

    @unittest.SkipTest  # warning: causing memory corruption, todo fix
    def test_view_update(self):
        v = self.d.view_factory()
        v.on_update_fn = self.on_update_fn
        v.open()
        try:
            v.refresh()
            self.lock.acquire()
            self.assertEqual((('hello',), {'one': 1}), v.ping('hello', one=1))
        finally:
            v.close()
        self.assertEqual(1, len(self.updates))
        d = self.updates[0]
        self.assertIn('time', d)
        self.assertEqual([0.0, 0.252], d['time']['limits']['value'])
        self.assertEqual([0.028, 0.226], d['time']['range']['value'])
        self.assertEqual(0.198, d['time']['delta']['value'])
        self.assertEqual('s', d['time']['delta']['units'])
        self.assertIn('x', d['time'])
        self.assertEqual(d['time']['range']['value'], [d['time']['x']['value'][0], d['time']['x']['value'][-1]])
        self.assertEqual(99, len(d['time']['x']['value']))  # is this right?

        self.assertIn('signals', d)
        self.assertIn('state', d)
        self.assertEqual('buffer', d['state']['source_type'])

    def test_view_get_samples(self):
        v = self.d.view_factory()
        v.open()
        try:
            s = v.samples_get(0, 100, fields=['current', 'voltage'])
            self.assertEqual([0.0, 0.1], s['time']['range']['value'])
            self.assertEqual(0.1, s['time']['delta']['value'])
            self.assertEqual('s', s['time']['delta']['units'])
            self.assertEqual(100, len(s['signals']['current']['value']))
            self.assertEqual(100, len(s['signals']['voltage']['value']))
        finally:
            v.close()

    def test_view_get_statistics(self):
        v = self.d.view_factory()
        v.open()
        s = v.statistics_get(0, 100)
        self.assertIn('time', s)
        self.assertEqual([0.0, 0.1], s['time']['range']['value'])
        self.assertEqual(0.1, s['time']['delta']['value'])
        self.assertEqual('s', s['time']['delta']['units'])
        self.assertIn('signals', s)
        self.assertIn('current', s['signals'])
        self.assertIn('voltage', s['signals'])
        self.assertIn('power', s['signals'])
        k = s['signals']['current']
        self.assertIn('µ', k)
        self.assertIn('σ2', k)
        self.assertIn('min', k)
        self.assertIn('max', k)
        self.assertIn('p2p', k)
        self.assertEqual('A', s['signals']['current']['µ']['units'])
        self.assertEqual('C', s['signals']['current']['∫']['units'])
        print(s)
        v.close()
