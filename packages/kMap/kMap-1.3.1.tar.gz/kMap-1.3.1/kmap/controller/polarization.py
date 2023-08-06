# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget

# Own Imports
from kmap import __directory__

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/polarization.ui')
Polarization_UI, _ = uic.loadUiType(UI_file)


class Polarization(QWidget, Polarization_UI):

    polarization_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(Polarization, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._connect()

    def change_polarization(self):

        self.polarization_changed.emit()

    def get_parameters(self):

        Ak_type, polarization = self._get_polarization()
        factor = self._get_factor()
        Ak_type = factor if factor == 'no' else factor + Ak_type
        angles = self._get_angles()

        return (Ak_type, polarization, *angles)

    def _get_factor(self):

        Ak_index = self.ak_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = 'no'

        elif Ak_index == 1:
            Ak_type = 'only-'

        else:
            Ak_type = ''

        return Ak_type

    def _get_polarization(self):

        Ak_index = self.polarization_combobox.currentIndex()

        if Ak_index == 0:
            Ak_type = 'toroid'
            polarization = 'p'

        else:
            Ak_type = 'NanoESCA'

            if Ak_index == 1:
                polarization = 'p'

            elif Ak_index == 2:
                polarization = 's'

            elif Ak_index == 3:
                polarization = 'unpolarized'                

            elif Ak_index == 4:
                polarization = 'C+'

            elif Ak_index == 5:
                polarization = 'C-'

            elif Ak_index == 6:
                polarization = 'CDAD'

        return Ak_type, polarization

    def _get_angles(self):

        alpha = self.angle_spinbox.value()
        beta = self.azimuth_spinbox.value()
        gamma = 'auto'

        return alpha, beta, gamma

    def _connect(self):

        self.polarization_combobox.currentIndexChanged.connect(
            self.change_polarization)
        self.angle_spinbox.valueChanged.connect(self.change_polarization)
        self.azimuth_spinbox.valueChanged.connect(self.change_polarization)
        self.ak_combobox.currentIndexChanged.connect(self.change_polarization)
