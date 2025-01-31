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


from autologging import logged, traced

from kqcircuits.util.library_helper import load_libraries, to_library_name
from kqcircuits.elements.element import Element
from kqcircuits.defaults import default_tsv_type


@traced
@logged
class Tsv(Element):
    """Base Class for TSVs."""

    @classmethod
    def create(cls, layout, library=None, tsv_type=None, **parameters):
        """Create a TSV cell in layout.

        Args:
            layout: pya.Layout object where the cell is created
            library: LIBRARY_NAME of the calling PCell instance
            tsv_type: (str): name of the TSV subclass
            **parameters: PCell parameters as keyword arguments

        Returns:
            the created TSV cell
        """

        if tsv_type is None:
            tsv_type = to_library_name(cls.__name__)

        library_layout = (load_libraries(path=cls.LIBRARY_PATH)[cls.LIBRARY_NAME]).layout()
        if tsv_type in library_layout.pcell_names():
            pcell_class = type(library_layout.pcell_declaration(tsv_type))
            return Element._create_cell(pcell_class, layout, library, **parameters)
        elif tsv_type != default_tsv_type:
            return Tsv.create(layout, library, tsv_type=default_tsv_type, **parameters)
        else:
            raise ValueError(f'Unknown TSV subclass "{tsv_type}"!')
