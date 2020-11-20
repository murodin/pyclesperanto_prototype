from qtpy.QtWidgets import (
    QPushButton,
    QComboBox,
    QTabWidget,
    QVBoxLayout,
    QGridLayout,
    QFileDialog,
    QDialogButtonBox,
    QWidget,
    QSlider
)
from qtpy.QtCore import Qt
import napari
import numpy as np
from napari.layers import Image
from magicgui import magicgui

import pyclesperanto_prototype as cle


class Gui(QWidget):
    # I hate using global variables.
    # But that's what it is.
    # It's a global variable.
    #                            haesleinhuepf
    global_last_filter_applied = None

    def __init__(self, viewer):
        super().__init__()

        self.viewer = viewer
        self.items = []

        self.layout = QVBoxLayout()

        self.init_gui()

        self.setLayout(self.layout)

        self.dock_widget = None

    def init_gui(self, active : bool = True):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        if active:
            self._add_button("Filter", self.add_filter_clicked)
            self._add_button("Binarize", self.add_binarize_clicked)
            self._add_button("Combine", self.add_combine_clicked)
        else:
            self._add_button("Done", self.done_clicked)
            self._add_button("Cancel", self.cancel_clicked)
        #self.layout.addStretch()

        self.setLayout(self.layout)

    def _add_button(self, title : str, handler : callable):
        btn = QPushButton(title, self)
        btn.clicked.connect(handler)
        self.layout.addWidget(btn)
        self.items.append(btn)

    def add_filter_clicked(self):
        print("Filter")
        self.filter_gui = cle_filter_execution.Gui()
        self.dock_widget = viewer.window.add_dock_widget(self.filter_gui, area='right')
        self.init_gui(False)

    def add_binarize_clicked(self):
        print("Binarize")
        self.filter_gui = cle_binarization_execution.Gui()
        self.dock_widget = viewer.window.add_dock_widget(self.filter_gui, area='right')
        self.init_gui(False)

    def add_combine_clicked(self):
        print("Combine")
        self.filter_gui = cle_combine_execution.Gui()
        self.dock_widget = viewer.window.add_dock_widget(self.filter_gui, area='right')
        self.init_gui(False)

    def done_clicked(self):
        # magicqui somehow internally keeps the layer.
        # Thus, we need to destroy magicguis layer and add it again
        data = viewer.layers.selected[0].data
        viewer.layers.remove_selected()
        viewer.add_image(data, name = str(Gui.global_last_filter_applied))

        print("Main menu")
        self.viewer.window.remove_dock_widget(self.dock_widget)
        self.init_gui(True)

    def cancel_clicked(self):
        viewer.layers.remove_selected()

        print("Main menu")
        self.viewer.window.remove_dock_widget(self.dock_widget)
        self.init_gui(True)



# inspired from https://github.com/pr4deepr/pyclesperanto_prototype/blob/master/napari_clij_widget.py# Using Enums for getting a dropdown menu
# clesperanto functions are not being passed as enum values for some reason, so they are defined as strings
from enum import Enum
from functools import partial

class binarize(Enum):
    threshold_otsu = partial(cle.threshold_otsu)
    greater_constant = partial(cle.greater_constant)
    smaller_constant = partial(cle.smaller_constant)
    equal_constant = partial(cle.equal_constant)
    not_equal_constant = partial(cle.not_equal_constant)

    #define the call method for the functions or it won't return anything
    def __call__(self, *args):
        return self.value(*args)

@magicgui(auto_call=True, layout='vertical') #, call_button='Compute')
def cle_binarization_execution(input1: Image, operation: binarize, constant : int = 0) -> Image:
    if input1 is not None:
        cle_input1 = cle.push_zyx(input1.data)

        operation = operation
        output = cle.create_like(cle_input1)
        operation(cle_input1, output, constant)
        Gui.global_last_filter_applied = operation

        output = cle.pull_zyx(output)
        return output







class combine(Enum):
    binary_and = partial(cle.binary_and)
    binary_or = partial(cle.binary_or)
    binary_xor = partial(cle.binary_xor)
    add = partial(cle.add_images_weighted)
    subtract = partial(cle.subtract_images)
    multiply = partial(cle.multiply_images)
    divide = partial(cle.divide_images)
    greater = partial(cle.greater)
    smaller = partial(cle.smaller)
    equal = partial(cle.equal)
    not_equal = partial(cle.not_equal)

    #define the call method for the functions or it won't return anything
    def __call__(self, *args):
        return self.value(*args)

@magicgui(auto_call=True, layout='vertical') #, call_button='Compute')
def cle_combine_execution(input1: Image, input2: Image, operation: combine) -> Image:
    if input1 is not None:
        cle_input1 = cle.push_zyx(input1.data)
        cle_input2 = cle.push_zyx(input2.data)

        operation = operation
        output = cle.create_like(cle_input1)
        operation(cle_input1, cle_input2, output)
        Gui.global_last_filter_applied = operation

        output = cle.pull_zyx(output)
        return output









class cle_filter(Enum):
    # using pyclesperanto filtering images with a gpu
    #using functools.partial to return functions as enum values:
    #https://stackoverflow.com/questions/40338652/how-to-define-enum-values-that-are-functions
    mean_box = partial(cle.minimum_box)
    maximum_box = partial(cle.maximum_box)
    minimum_box = partial(cle.minimum_box)
    top_hat_box = partial(cle.top_hat_box)
    bottom_hat_box = partial(cle.bottom_hat_box)
    gaussian_blur = partial(cle.gaussian_blur)
    gradient_x = partial(cle.gradient_x)
    gradient_y = partial(cle.gradient_y)
    gradient_z = partial(cle.gradient_z)

    #define the call method for the functions or it won't return anything
    def __call__(self, *args):
        return self.value(*args)

@magicgui(auto_call=True, layout='vertical') #, call_button='Compute')
def cle_filter_execution(input: Image, operation: cle_filter, x: float = 1, y: float = 1, z: float = 0) -> Image:
    if input:
        cle_input = cle.push_zyx(input.data)
        operation = operation
        output = cle.create_like(cle_input)
        operation(cle_input, output, x, y, z)
        Gui.global_last_filter_applied = operation

        output = cle.pull_zyx(output)
        return output




from skimage.io import imread
image = imread('https://samples.fiji.sc/blobs.png')

with napari.gui_qt():
    # create a viewer and add some images
    viewer = napari.Viewer()
    # add the gui to the viewer as a dock widget
    dock_widget = viewer.window.add_dock_widget(Gui(viewer), area='right')

    viewer.add_image(image)











