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

from kqcircuits.elements.element import Element
from kqcircuits.elements.fluxlines.fluxline import Fluxline
from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt, add_parameters_from
from kqcircuits.squids.squid import Squid


@add_parameters_from(Fluxline, "fluxline_gap_width", "fluxline_type")
@add_parameters_from(Squid, "junction_width", "loop_area", "squid_type")
class Qubit(Element):
    """Base class for qubit objects without actual produce function.

    Collection of shared sub routines for shared parameters and producing shared aspects of qubit geometry including

    * possible fluxlines
    * e-beam layers for SQUIDs
    * SQUID name parameter
    """

    LIBRARY_NAME = "Qubit Library"
    LIBRARY_DESCRIPTION = "Library for qubits."
    LIBRARY_PATH = "qubits"

    mirror_squid =  Param(pdt.TypeBoolean, "Mirror SQUID by its Y axis", False)

    def produce_squid(self, transf, **parameters):
        """Produces the squid.

        Creates the squid cell and inserts it with the given transformation as a subcell. Also inserts the squid parts
        in "base_metal_gap_wo_grid"-layer to "base_metal_gap_for_EBL"-layer.

        Args:
            transf (DCplxTrans): squid transformation
            parameters: other parameters for the squid

        Returns:
            A tuple ``(squid_unetch_region, refpoints_rel)``

            * ``squid_unetch_region`` (Region):  squid unetch region
            * ``refpoints_rel`` (Dictionary): relative refpoints for the squid

        """
        cell = self.add_element(Squid, squid_type=self.squid_type, **parameters)
        refpoints_rel = self.get_refpoints(cell)
        squid_transf = transf * pya.DTrans.M90 if self.mirror_squid else transf

        # For the region transformation, we need to use ICplxTrans, which causes some rounding errors. For inserting
        # the cell, convert the integer transform back to float to keep cell and geometry consistent.
        integer_transf = squid_transf.to_itrans(self.layout.dbu)
        float_transf = integer_transf.to_itrans(self.layout.dbu)  # Note: ICplxTrans.to_itrans returns DCplxTrans

        if "squid_index" in parameters:
            s_index = int(parameters.pop('squid_index'))
            inst, _ = self.insert_cell(cell, float_transf, inst_name=f"squid_{s_index}")
            inst.set_property("squid_index", s_index)
        else:
            inst, _ = self.insert_cell(cell, float_transf, inst_name="squid")

        squid_unetch_region = pya.Region(cell.shapes(self.get_layer("base_metal_addition")))
        squid_unetch_region.transform(integer_transf)
        # add parts of qubit to the layer needed for EBL
        squid_etch_region = pya.Region(cell.shapes(self.get_layer("base_metal_gap_wo_grid")))
        squid_etch_region.transform(integer_transf)
        self.cell.shapes(self.get_layer("base_metal_gap_for_EBL")).insert(squid_etch_region)

        return squid_unetch_region, refpoints_rel

    def produce_fluxline(self, **parameters):
        """Produces the fluxline.

        Creates the fluxline cell and inserts it as a subcell. The "flux" and "flux_corner" ports
        are made available for the qubit.

        Args:
            parameters: parameters for the fluxline to overwrite default and subclass parameters

        Returns:
            The unetch region of the fluxline
        """

        if self.fluxline_type == "none":
            return pya.Region([])
        parameters = {"fluxline_type": self.fluxline_type, **parameters}

        cell = self.add_element(Fluxline, **parameters)

        refpoints_so_far = self.get_refpoints(self.cell)
        squid_edge = refpoints_so_far["origin_squid"]
        a = (squid_edge - refpoints_so_far['port_common'])
        rotation = math.atan2(a.y, a.x) / math.pi * 180 + 90
        transf = pya.DCplxTrans(1, rotation, False, squid_edge - self.refpoints["base"])

        # For the region transformation, we need to use ICplxTrans, which causes some rounding errors. For inserting
        # the cell, convert the integer transform back to float to keep cell and geometry consistent
        integer_transf = transf.to_itrans(self.layout.dbu)
        float_transf = integer_transf.to_itrans(self.layout.dbu)  # Note: ICplxTrans.to_itrans returns DCplxTrans

        cell_inst, _ = self.insert_cell(cell, float_transf)
        self.copy_port("flux", cell_inst)

        unetch_region = pya.Region(cell.shapes(self.get_layer("base_metal_addition")))
        unetch_region.transform(integer_transf)
        return unetch_region
