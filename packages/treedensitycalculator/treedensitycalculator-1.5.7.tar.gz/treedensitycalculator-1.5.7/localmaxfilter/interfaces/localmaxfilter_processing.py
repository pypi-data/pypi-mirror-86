# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : November 2018
| Copyright           : © 2018 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from Local Maximum Filter [C++ software]
|                       Ghent University, Laboratory of Forest Management and Spatial Information Techniques
|                       Lieven P.C. Verbeke
|
| This file is part of the QGIS Tree Density Calculator plugin and treedensitycalculator python package.
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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingContext,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFileDestination,)

from localmaxfilter.interfaces import run_algorithm_local_max_filter


class LocalMaxFilterProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    Local Max Filter algorithm returns the tree density using the reflectance values of the local maxima
    of a sliding window going over the input image. It is possible to include an area of interest,
    to create a vonoroi layer or to snap local maxima.
    """

    # Constants used to refer to parameters and outputs.
    # They will be used when calling the algorithm from another algorithm, or when calling from the QGIS console.
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    AREA_LAYER = 'AREA_LAYER'
    WINDOW = 'WINDOW'
    SNAP = 'SNAP'
    VORONOI = 'VORONOI'

    def tr(self, string):
        """ Returns a translatable string with the self.tr() function. """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return LocalMaxFilterProcessingAlgorithm()

    def name(self):
        """ Returns the algorithm name, used for identifying the algorithm. This string should be:
          - fixed for the algorithm + unique within each provider
          - must not be localised
          - lowercase alphanumeric characters only and no spaces or other formatting characters
        """
        return 'tree_density_calculator'

    def displayName(self):
        """ Returns the translated algorithm name. Should be used for any user-visible display of the algorithm name."""
        return self.tr('Tree Density Calculator')

    def icon(self):
        """ Should return a QIcon which is used for your provider inside the Processing toolbox. """
        return QIcon(':/lmf_logo')

    def shortHelpString(self):
        """ Returns a localised short helper string for the algorithm. This string should provide a basic description
        about what the algorithm does and the parameters and outputs associated with it. """
        return self.tr("Estimate the tree density of the input image based on the local maximum in a sliding window.\n"
                       "Image: Brightness image for estimating the tree density.\n"
                       "Sliding window size: size of the window to look for local maxima.\n"
                       "Area of interest: Polygons to limit the tree search.\n"
                       "Snap distance: Snap local maxima together if closer than this distance (meters). Can not be "
                       "more than half of sliding window size.\n"
                       "Voronoi polygons: Create voronoi polygons based on the found tree tops.\n"
                       "Output file: Set path for saving the outputs to file. Base name. Tree output files possible:"
                       "[base name]_point.shp for the tree tops; "
                       "[base name]_mask.shp for the tree density per area of interest;"
                       "[base name]_voronoi.shp for the voronoi polygons.")

    def initAlgorithm(self, configuration, p_str=None, Any=None, *args, **kwargs):
        """ Here we define the inputs and output of the algorithm, along with some other properties. """

        # We add the input image
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT,
                self.tr('Image')
            )
        )

        param_window = QgsProcessingParameterNumber(
                self.WINDOW,
                self.tr('Sliding window size'),
                type=1,           # type=1 is Double, 0 is int
                minValue=0,
                defaultValue=5)
        param_window.setMetadata({'widget_wrapper': {'decimals': 2}})

        self.addParameter(param_window)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.AREA_LAYER,
                self.tr('Area of interest'),
                optional=True
            )
        )

        param_snap = QgsProcessingParameterNumber(
            self.SNAP,
            self.tr('Snap distance in meters, max half of sliding window size'),
            type=1,  # type=1 is Double, 0 is int
            optional=True,
            minValue=0
            # max value should be max half of the window. It's not possible to make this value
            # depended on another parameter, see: https://gis.stackexchange.com/questions/285570/
            #                   changing-parameter-values-according-to-other-parameter-choice-in-processing-scri
            )
        param_snap.setMetadata({'widget_wrapper': {'decimals': 2}})
        self.addParameter(param_snap)

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.VORONOI,
                self.tr('Voronoi polygons')
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output file'),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """ Here is where the processing itself takes place. """

        area = self.parameterAsVectorLayer(parameters, self.AREA_LAYER, context).source() \
            if parameters[self.AREA_LAYER] else None
        voronoi = self.parameterAsBool(parameters, self.VORONOI, context)

        # Snap constraint
        window = self.parameterAsInt(parameters, self.WINDOW, context)
        snap = self.parameterAsDouble(parameters, self.SNAP, context) \
            if parameters[self.SNAP] else None

        if snap and snap > window/2:
            raise QgsProcessingException('Snap distance should be max half of the window length')

        # Execute algorithm
        output_point_path, output_mask_path, output_voronoi_path = run_algorithm_local_max_filter(
            image_path=self.parameterAsRasterLayer(parameters, self.INPUT, context).source(),
            window=window,
            update_progress_bar=feedback.setProgress,
            log_function=feedback.pushInfo,
            mask_path=area,
            output_base_path=self.parameterAsFileOutput(parameters, self.OUTPUT, context),
            snap_distance=snap,
            voronoi=voronoi,
            feedback=feedback,
            context=context)

        # Open resulting layers in QGIS
        context.addLayerToLoadOnCompletion(
            output_point_path, QgsProcessingContext.LayerDetails(name='Tree Tops', project=context.project()))
        if area:
            context.addLayerToLoadOnCompletion(
                output_mask_path, QgsProcessingContext.LayerDetails(name='Tree Density', project=context.project()))
        if voronoi:
            context.addLayerToLoadOnCompletion(
                output_voronoi_path, QgsProcessingContext.LayerDetails(name='Voronoi', project=context.project()))

        return {'TREE_TOPS_POINT': output_point_path,
                'TREE_DENSITY_POLYGON': output_mask_path,
                'VORONOI_POLYGON': output_voronoi_path}
