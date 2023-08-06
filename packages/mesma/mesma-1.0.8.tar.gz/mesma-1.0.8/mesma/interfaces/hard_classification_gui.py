# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : February 2019
| Copyright           : © 2019 - 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab).
|                       Dar Roberts, Kerry Halligan, Philip Dennison, Kenneth Dudley, Ben Somers, Ann Crabbé
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
import os
import tempfile

from osgeo import gdal
from qgis.gui import QgsFileWidget
from qgis.core import QgsRasterLayer, QgsProject, QgsMapLayerProxyModel, QgsProviderRegistry
from qgis.core import QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterShader
from qgis.utils import iface
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QDialogButtonBox

from mesma.interfaces.imports import import_band_names
from mesma.interfaces.operators import HardClassificationOperator, GUIProgressBar
from mesma.hubdc.applier import Applier, ApplierInputRaster, ApplierOutputRaster

COLORS = [QColor("green"), QColor("yellow"), QColor("lightGray"), QColor("red"), QColor("cyan"), QColor("gray"),
          QColor("darkBlue"), QColor("darkGreen"), QColor("darkYellow"), QColor("black"), QColor("darkRed"),
          QColor("darkCyan"), QColor("darkGray"), QColor("darkMagenta"), QColor("blue")]


class HardClassificationWidget(QDialog):
    """ QDialog to interactively set up the Hard Classification input and output. """

    def __init__(self):
        super(HardClassificationWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'hard_classification.ui'), self)

        # image
        self.inputComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.inputAction.triggered.connect(self._image_browse)
        self.inputButton.setDefaultAction(self.inputAction)

        # output
        self.outputFileWidget.setStorageMode(QgsFileWidget.SaveFile)
        self.outputFileWidget.lineEdit().setPlaceholderText('[Create temporary layer]')
        self.outputFileWidget.lineEdit().setReadOnly(True)

        # Open in QGIS?
        try:
            iface.activeLayer
        except AttributeError:
            self.openInQGIS.setChecked(False)
            self.openInQGIS.setDisabled(True)

        # run or cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_hard_classification)
        self.OKClose.rejected.connect(self.close)

    def log(self, text):
        # append text to log window
        self.logBrowser.append(str(text) + '\n')
        # open the widget on the log screen
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab_log))

    def _image_browse(self):
        """ Browse for an image raster file. """

        path = QFileDialog.getOpenFileName(filter=QgsProviderRegistry.instance().fileRasterFilters())[0]

        try:
            if len(path) > 0:
                gdal.UseExceptions()
                layer = QgsRasterLayer(path, os.path.basename(path), 'gdal')
                assert layer.isValid()
                QgsProject.instance().addMapLayer(layer, True)
                self.inputComboBox.setLayer(layer)

        except AssertionError:
            self.log("'" + path + "' not recognized as a supported file format.")
        except Exception as e:
            self.log(e)

    def _run_hard_classification(self):
        """ Read all parameters and pass them on to the HardClassificationOperator. """

        try:
            image_path = self.inputComboBox.currentLayer().source()
            band_names, shade_band_index = import_band_names(image_path)

            # Only temp file possible when result is opened in QGIS
            output_path = self.outputFileWidget.filePath()
            if not self.openInQGIS.isChecked() and len(output_path) == 0:
                raise Exception("If you won't open the result in QGIS, you must select an output file.")

            if len(output_path) == 0:
                basename, extension = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(tempfile.gettempdir(), basename + "_classification" + extension)

            # set up the applier
            applier = Applier()
            applier.controls.setProgressBar(GUIProgressBar(q_progress_bar=self.progressBar))
            applier.inputRaster.setRaster(key='raster', value=ApplierInputRaster(filename=image_path))
            applier.outputRaster.setRaster(key='classification', value=ApplierOutputRaster(filename=output_path))

            # apply hard classification
            applier.apply(operatorType=HardClassificationOperator, band_names=band_names, shade_band=shade_band_index)
            self.log("Done.")

            if self.openInQGIS.isChecked():
                items = []
                for i, name in enumerate(band_names):
                    items.append(QgsColorRampShader.ColorRampItem(i, COLORS[i], name.split("_fraction")[0]))

                shader_function = QgsColorRampShader(type=QgsColorRampShader.Exact,
                                                     classificationMode=QgsColorRampShader.EqualInterval)
                shader_function.setColorRampItemList(items)
                shader = QgsRasterShader()
                shader.setRasterShaderFunction(shader_function)

                new_layer = QgsRasterLayer(output_path, "Classification Image")
                new_layer.setRenderer(QgsSingleBandPseudoColorRenderer(new_layer.dataProvider(), 1, shader))

                QgsProject.instance().addMapLayer(new_layer, True)

        except AttributeError:
            self.log("Select a MESMA Fractions image as input.")
        except Exception as e:
            self.log(e)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = HardClassificationWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
