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

from kqcircuits.util.parameters import Param, pdt, add_parameters_from
from kqcircuits.elements.chip_frame import ChipFrame
from kqcircuits.chips.chip import Chip
from kqcircuits.pya_resolver import pya
from kqcircuits.test_structures.junction_test_pads import JunctionTestPads
from kqcircuits.squids.squid import Squid


@add_parameters_from(Squid, "squid_type")
@add_parameters_from(ChipFrame, "marker_types")
class JunctionTest2(Chip):
    """The PCell declaration for a JunctionTest2 chip."""

    pad_width = Param(pdt.TypeDouble, "Pad Width", 500, unit="[μm]")
    junctions_horizontal = Param(pdt.TypeBoolean, "Horizontal (True) or vertical (False) junctions", True)
    pad_spacing = Param(pdt.TypeDouble, "Spacing between different pad pairs", 100, unit="[μm]")

    def build(self):
        left = self.box.left
        right = self.box.right
        top = self.box.top

        junction_test_side = self.add_element(
            JunctionTestPads,
            area_height=6000,
            area_width=1700,
            junction_type="both",
        )
        junction_test_center = self.add_element(
            JunctionTestPads,
            area_height=9400,
            area_width=6000,
            junction_type="both",
        )

        self.insert_cell(junction_test_side, pya.DTrans(0, False, left + 300, top - 2000 - 6000), "testarray_1")
        self.insert_cell(junction_test_side, pya.DTrans(0, False, right - 300 - 1700, top - 2000 - 6000), "testarray_2")
        self.insert_cell(junction_test_center, pya.DTrans(0, False, left + 2000, top - 300 - 9400), "testarray_3")

        super().build()
