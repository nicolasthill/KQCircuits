# lattice unit
from kqcircuits.elements.element import Element
from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt


class Lattice(Element):
    """
    lattice containing one qubit
    """

    b_lattice = Param(pdt.TypeDouble, "triangle width", 300, unit="μm")
    h_lattice = Param(pdt.TypeDouble, "triangle height", 300, unit="μm")
    s_lattice = Param(pdt.TypeDouble, "triangle width", 300, unit="μm")

    def build(self):
        # optical layer

        # shape for the inner conductor
        pts = [
            pya.DPoint(0,0),
            pya.DPoint(self.h_lattice,self.b_lattice / 2),
            pya.DPoint(self.h_lattice,-self.b_lattice / 2)
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

        # protection layer
        shifts = [
            pya.DVector(0, self.margin),
            pya.DVector(0, self.margin),
            pya.DVector(self.margin, self.margin)
        ]
        pts2 = [p + s for p, s in zip(pts2, shifts)]
        shape = pya.DPolygon(pts2)
        self.cell.shapes(self.get_layer("ground_grid_avoidance")).insert(shape)

        # add reference point
        self.add_port("", pya.DPoint(0, 0), pya.DVector(-1, 0))


