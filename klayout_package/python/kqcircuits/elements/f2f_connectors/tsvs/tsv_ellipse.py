# This code is part of KQCircuits
# Copyright (C) 2021 IQM Finland Oy
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see
# https://www.gnu.org/licenses/gpl-3.0.html.
#
# The software distribution should follow IQM trademark policy for open-source software
# (meetiqm.com/developers/osstmpolicy). IQM welcomes contributions to the code. Please see our contribution agreements
# for individuals (meetiqm.com/developers/clas/individual) and organizations (meetiqm.com/developers/clas/organization).

import math
import numpy
from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt
from kqcircuits.elements.f2f_connectors.tsvs.tsv import Tsv
from kqcircuits.defaults import default_tsv_parameters


class TsvEllipse(Tsv):
    """Connector between faces of two sides of a substrate.
    Origin is at the geometric center. Geometry es elliptical.
    """

    tsv_diameter = Param(pdt.TypeDouble, "TSV diameter", default_tsv_parameters['tsv_diameter'], unit="μm")
    tsv_elliptical_width = Param(pdt.TypeDouble, "TSV elliptical width",
                                 default_tsv_parameters['tsv_elliptical_width'], unit="μm")

    def produce_impl(self):
        self.create_tsv_connector()

    def create_tsv_connector(self):
        """
        Generate elliptical TSV
        """
        # shorthand
        r = self.tsv_diameter / 2
        w = self.tsv_elliptical_width / 2
        m = self.margin

        # parametric representation is taken from https://en.wikipedia.org/wiki/Superellipse
        p1 = 6
        p2 = 2
        # Protection layer
        tsv_pts_avoidance = [pya.DPoint(
            numpy.abs(math.cos(a)) ** (2 / p1) * (w + m) * numpy.sign(math.cos(a)),
            numpy.abs(math.sin(a)) ** (2 / p2) * (r + m) * numpy.sign(math.sin(a))) for a in
            (x / 32 * math.pi for x in range(0, 65))]

        tsv_pts = [
            pya.DPoint(numpy.abs(math.cos(a)) ** (2 / p1) * w * numpy.sign(math.cos(a)),
                       numpy.abs(math.sin(a)) ** (2 / p2) * r * numpy.sign(math.sin(a))) for
            a in (x / 32 * math.pi for x in range(0, 65))]

        shape = pya.DPolygon(tsv_pts_avoidance)
        # ground avoidance layer b face
        self.cell.shapes(self.get_layer("ground_grid_avoidance")).insert(shape)
        self.cell.shapes(self.get_layer("through_silicon_via")).insert(pya.DPolygon(tsv_pts))  # TSV only on b face
