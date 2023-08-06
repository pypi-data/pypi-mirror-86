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

from PySide2 import QtCore, QtWidgets
from .gpio_widget_ui import Ui_GpioWidget
from joulescope_ui.preferences import options_enum, to_bool
from joulescope_ui.ui_util import comboBoxConfig, comboBoxSelectItemByText
import numpy as np


VOLTAGES = ['1.8V', '2.1V', '2.5V', '2.7V', '3.0V', '3.3V', '5.0V']


class GpioWidget(QtWidgets.QWidget):
    on_changeSignal = QtCore.Signal(object)

    def __init__(self, parent, cmdp, state_preference):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_GpioWidget()
        self.ui.setupUi(self)
        h = self.minimumSizeHint().height()
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)

        self._cmdp = cmdp
        self._state = None
        self._update_active = False
        self._inputs = [('current_lsb', self.ui.input0CheckBox, self.ui.input0Label),
                        ('voltage_lsb', self.ui.input1CheckBox, self.ui.input1Label)]

        self.init()
        cmdp.subscribe('DataView/#data', self._on_device_state_data, update_now=True)
        cmdp.subscribe('Device/extio/io_voltage', self._on_io_voltage, update_now=True)
        cmdp.subscribe('Device/extio/current_lsb', self._on_current_lsb, update_now=True)
        cmdp.subscribe('Device/extio/voltage_lsb', self._on_voltage_lsb, update_now=True)
        cmdp.subscribe('Device/extio/gpo0', self._on_gpo0, update_now=True)
        cmdp.subscribe('Device/extio/gpo1', self._on_gpo1, update_now=True)

    def init(self):
        io_voltages = options_enum(self._cmdp.preferences.definition_options('Device/extio/io_voltage'))
        io_voltage = self._cmdp['Device/extio/io_voltage']
        comboBoxConfig(self.ui.voltageComboBox, io_voltages, io_voltage)
        self.ui.voltageComboBox.currentIndexChanged.connect(self._on_voltage_combobox)
        self.ui.output0Button.toggled.connect(self._on_output0_button)
        self.ui.output1Button.toggled.connect(self._on_output1_button)
        self.ui.input0CheckBox.toggled.connect(self._on_input0_button)
        self.ui.input1CheckBox.toggled.connect(self._on_input1_button)

    def _on_voltage_combobox(self, index):
        voltage_io = self.ui.voltageComboBox.currentText()
        self._cmdp.publish('Device/extio/io_voltage', voltage_io)

    def _on_output0_button(self, checked):
        self._cmdp.publish('Device/extio/gpo0', '1' if checked else '0')

    def _on_output1_button(self, checked):
        self._cmdp.publish('Device/extio/gpo1', '1' if checked else '0')

    def _on_input0_button(self, checked):
        self._cmdp.publish('Device/extio/current_lsb', 'gpi0' if checked else 'normal')

    def _on_input1_button(self, checked):
        self._cmdp.publish('Device/extio/voltage_lsb', 'gpi1' if checked else 'normal')

    def _on_io_voltage(self, topic, data):
        comboBoxSelectItemByText(self.ui.voltageComboBox, data)

    def _on_current_lsb(self, topic, data):
        if data == 'normal':
            self.ui.input0CheckBox.setChecked(False)
            self.ui.input0CheckBox.setEnabled(True)
        elif data == 'gpi0':
            self.ui.input0CheckBox.setChecked(True)
            self.ui.input0CheckBox.setEnabled(True)
        else:
            self.ui.input0CheckBox.setEnabled(False)

    def _on_voltage_lsb(self, topic, data):
        if data == 'normal':
            self.ui.input1CheckBox.setChecked(False)
            self.ui.input1CheckBox.setEnabled(True)
        elif data == 'gpi1':
            self.ui.input1CheckBox.setChecked(True)
            self.ui.input1CheckBox.setEnabled(True)
        else:
            self.ui.input1CheckBox.setEnabled(False)

    def _on_gpo0(self, topic, data):
        self.ui.output0Button.setChecked(to_bool(data))

    def _on_gpo1(self, topic, data):
        self.ui.output1Button.setChecked(to_bool(data))

    def _on_device_state_data(self, topic, data):
        if not self.isVisible() or data is None:
            return
        for signal_name, checkbox, label in self._inputs:
            if signal_name not in data['signals']:
                continue
            v = data['signals'][signal_name]['µ']['value']
            if len(v) and np.isfinite(v[-1]):
                v = str(int(v[-1]))
            else:
                v = '_'
            label.setText(v)


def widget_register(cmdp):
    return {
        'name': 'GPIO',
        'brief': 'General purpose input/output control and display',
        'class': GpioWidget,
        'location': QtCore.Qt.RightDockWidgetArea,
        'singleton': True,
    }
