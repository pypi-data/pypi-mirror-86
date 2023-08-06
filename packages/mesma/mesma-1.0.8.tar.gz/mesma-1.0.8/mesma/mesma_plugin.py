"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : June 2018
| Copyright           : © 2018 - 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
|
| This file is part of the MESMA plugin and python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License (COPYING.txt). If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
from os import path

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu

from mesma.interfaces.mesma_gui import MesmaWidget
from mesma.interfaces.mesma_visualisation_gui import ModelVisualizationWidget
from mesma.interfaces.shade_normalisation_gui import ShadeNormalisationWidget
from mesma.interfaces.hard_classification_gui import HardClassificationWidget
from mesma.images.mesma_resources_rc import qInitResources as Resources
Resources()


class MesmaPlugin:
    """ QGIS Plugin Implementation """

    def __init__(self, iface):
        """
        :param QgsInterface iface: the interface instance which provides the hook to manipulate the QGIS GUI at run time
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = path.dirname(__file__)

        # List of actions added by this plugin
        self.actions = []

        # Add an empty menu to the Raster Menu
        self.main_menu = QMenu(title='MESMA', parent=self.iface.rasterMenu())
        self.main_menu.setIcon(QIcon(':/mesma'))
        self.iface.rasterMenu().addMenu(self.main_menu)

        # Add an empty toolbar
        self.toolbar = self.iface.addToolBar('MESMA Toolbar')

    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI """

        action = QAction(QIcon(':/mesma'), 'MESMA', self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('mesma'))
        action.setStatusTip('MESMA')
        self.toolbar.addAction(action)
        self.main_menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/mesma-vis'), 'MESMA Visualisation', self.iface.mainWindow())
        action.triggered.connect(self.run_vis)
        action.setStatusTip('MESMA Visualisation')
        self.toolbar.addAction(action)
        self.main_menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/histogram'), 'Soft to Hard Classification', self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('hc'))
        action.setStatusTip('Soft to Hard Classification')
        self.toolbar.addAction(action)
        self.main_menu.addAction(action)
        self.actions.append(action)

        action = QAction(QIcon(':/shade'), 'Shade Normalisation', self.iface.mainWindow())
        action.triggered.connect(lambda: self.run_widget('shade'))
        action.setStatusTip('Shade Normalisation')
        self.toolbar.addAction(action)
        self.main_menu.addAction(action)
        self.actions.append(action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.rasterMenu().removeAction(self.main_menu.menuAction())

        for action in self.actions:
            self.iface.removeToolBarIcon(action)

        # remove the toolbar
        del self.toolbar

    @staticmethod
    def run_widget(plugin: str):
        switcher = {
            'mesma': MesmaWidget(),
            'hc': HardClassificationWidget(),
            'shade': ShadeNormalisationWidget()
        }

        widget = switcher[plugin]
        widget.show()
        widget.exec_()

    @staticmethod
    def run_vis():
        widget = ModelVisualizationWidget()
        widget.show()
