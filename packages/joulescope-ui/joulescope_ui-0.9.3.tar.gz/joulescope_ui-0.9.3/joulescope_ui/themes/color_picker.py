# Copyright 2020 Jetperch LLC
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


from PySide2 import QtCore, QtGui, QtWidgets
import re


_re_color_pattern = re.compile('#[0-9a-fA-F]*')


def color_as_string(color):
    if isinstance(color, QtGui.QColor):
        value = f'{color.rgba():08X}'
        return f'#{value[2:]}{value[:2]}'  # convert AARRGGBB to RRGGBBAA
    elif isinstance(color, str):
        return color
    else:
        raise ValueError(f'Invalid color type: {type(color)}')


def color_as_qcolor(color):
    if isinstance(color, str):
        clen = len(color)
        if clen == 9:
            color = f'#{color[7:]}{color[1:7]}'  # convert RRGGBBAA to AARRGGBB
        elif clen != 7:
            raise ValueError('Invalid color')
        return QtGui.QColor(color)
    elif isinstance(color, QtGui.QColor):
        return color
    else:
        raise ValueError(f'Invalid color type: {type(color)}')


class QColorValidator(QtGui.QValidator):

    def __init__(self, parent):
        QtGui.QValidator.__init__(self, parent)

    def validate(self, value, pos):
        vlen = len(value)
        if not vlen:
            return QtGui.QValidator.Intermediate
        if not _re_color_pattern.match(value):
            return QtGui.QValidator.Invalid
        if vlen not in [7, 9]:
            return QtGui.QValidator.Intermediate
        value = value.upper()
        c = color_as_qcolor(value)
        v = color_as_string(c)
        if v == value or v[:-2] == value:
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Invalid


class QColorLabel(QtWidgets.QLabel):
    color_changed = QtCore.Signal(str)

    def __init__(self, parent, color):
        QtWidgets.QLabel.__init__(self, parent)
        self._parent = parent
        self._color = color  # as "#RRGGBB" or "#RRGGBB"
        self._picture = QtGui.QPicture()
        self.draw()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        v = color_as_string(value)
        if v[-2:] == 'FF':
            v = v[:-2]
        self._color = v
        self.draw()

    @property
    def qcolor(self):
        return color_as_qcolor(self.color)

    def _on_current_color_changed(self, color):
        self.color = color
        self.color_changed.emit(self.color)

    def mousePressEvent(self, ev):
        dialog = QtWidgets.QColorDialog(self.qcolor, self._parent)
        dialog.setOption(QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
        color = self.color
        dialog.currentColorChanged.connect(self._on_current_color_changed)
        if dialog.exec_():
            self.color = dialog.selectedColor()
        else:
            self.color = color
        self.color_changed.emit(self.color)

    def draw(self):
        self.setStyleSheet('')
        painter = QtGui.QPainter()
        painter.begin(self._picture)
        # print('%s : %s' % (self._value, color.getRgb()))
        painter.fillRect(QtCore.QRect(0, 0, 60, 20), QtGui.QBrush(self.qcolor))
        painter.end()
        self.setPicture(self._picture)


class ColorItem(QtCore.QObject):
    color_changed = QtCore.Signal(str, str)  # name, color

    def __init__(self, parent, name, color):
        QtCore.QObject.__init__(self, parent)
        self._name = name
        self._color = color
        self.value_edit = QtWidgets.QLineEdit(color, parent)
        self.validator = QColorValidator(parent)
        self.value_edit.setValidator(self.validator)
        self.value_edit.textChanged.connect(self._on_text)
        self.value_edit.setProperty('has_acceptable_input', True)
        self.color_label = QColorLabel(parent, color)
        self.color_label.color_changed.connect(self._on_color)

    def _on_text(self, text):
        if self.value_edit.hasAcceptableInput():
            self.value_edit.setProperty('has_acceptable_input', True)
            self._on_color(text)
        else:
            self.value_edit.setProperty('has_acceptable_input', False)
        self.value_edit.style().unpolish(self.value_edit)
        self.value_edit.style().polish(self.value_edit)

    def _on_color(self, color):
        self._color = color
        self.value_edit.setText(color)
        self.color_label.color = color
        self.color_changed.emit(self._name, self._color)


class ColorPicker(QtWidgets.QWidget):

    def __init__(self, parent, colors):
        QtWidgets.QWidget.__init__(self, parent)
        self.colors = colors
        self._layout = QtWidgets.QGridLayout(self)
        self._widgets = []
        row = 0

        for name, color in self.colors.items():
            label = QtWidgets.QLabel(name, parent)
            w = ColorItem(self, name, color)
            self._widgets.extend([label, w])
            self._layout.addWidget(label, row, 0, 1, 1)
            self._layout.addWidget(w.value_edit, row, 1, 1, 1)
            self._layout.addWidget(w.color_label, row, 2, 1, 1)
            row += 1


if __name__ == '__main__':
    import ctypes
    import sys

    style = """\
    QLineEdit {
        color: #101010;
        background-color: #FFFFFF;
        selection-color: #FFFFFF;
        selection-background-color: #1080C0;
    }
    QLineEdit[has_acceptable_input=false] {
        background-color: #FF8080;
    }
    """

    colors = {
        'background': '#101010',
        'foreground': '#E0E0E0',
        'highlight': '#1080C0',
        'red': '#FF0000',
        'green': '#00FF00',
        'blue': '#0000FF',
        'green_alphaFF': '#008000FF',
        'green_alpha80': '#00800080',
        'green_alpha40': '#00800040',
    }
    if sys.platform.startswith('win'):
        ctypes.windll.user32.SetProcessDPIAware()
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication()
    window = QtWidgets.QMainWindow()
    widget = ColorPicker(window, colors)
    window.setCentralWidget(widget)
    widget.setStyleSheet(style)
    window.show()
    app.exec_()
