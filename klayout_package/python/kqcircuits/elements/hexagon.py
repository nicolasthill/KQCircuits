# Hexagon
from kqcircuits.elements.element import Element
from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt

from kqcircuits.elements.lattice_unit import Lattice


class Hexagon(Element):
    """
    Hexagon containing 6 lattice units
    """
    def build(self):
        # store refs of all lattices
        self.lattice_ref = []
        for phi in range(6):
            self.lattice_ref.append(
                self.insert_cell(Lattice, 
                pya.DCplxTrans(1, phi * 60, False, 0,0), inst_name=str(phi))
            )

        # add reference point
        self.add_port("", pya.DPoint(0, 0), pya.DVector(-1, 0))    