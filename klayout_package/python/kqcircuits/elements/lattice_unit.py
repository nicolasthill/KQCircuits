# lattice unit
from kqcircuits.elements.element import Element
from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt
from kqcircuits.qubits.swissmon import Swissmon
from math import sqrt
class Lattice(Element):
    """
    lattice containing one qubit
    """

    b_lattice = Param(pdt.TypeDouble, "triangle width", 4000, unit="μm")
    h_lattice = Param(pdt.TypeDouble, "triangle height", 4000, unit="μm")

    def __init__(self):
        super().__init__()

    def build(self):
        # optical layer

        # shape for the inner conductor
        pts = [
            pya.DPoint(0,0),
            pya.DPoint(self.b_lattice*sqrt(3)/2,self.b_lattice/2),
            pya.DPoint(self.b_lattice*sqrt(3)/2,-self.b_lattice/2)
        ]

        pts2 = [
            pya.DPoint(10,10),
            pya.DPoint(10,20),
            pya.DPoint(20,20),
            pya.DPoint(20,10)
        ]

        # shifts = [
        #     pya.DVector(0, self.b),
        #     pya.DVector(0, self.s_lattice),
        #     pya.DVector(self.s_lattice, self.s_lattice)
        # ]
        # pts2 = [p + s for p, s in zip(pts, shifts)]
        # pts.reverse()
        shape = pya.DPolygon(pts)
        self.cell.shapes(self.get_layer("base_metal_gap_wo_grid")).insert(shape)
        _, self.swissmon_refpoints_abs = self.insert_cell(Swissmon, pya.DTrans(45, False, 1500, 0))
        # add reference point
        #self.add_port("", pya.DPoint(0, 0), pya.DVector(-1, 0))
