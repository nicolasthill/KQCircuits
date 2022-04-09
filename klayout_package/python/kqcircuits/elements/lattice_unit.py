# lattice unit
from kqcircuits.elements.element import Element
from kqcircuits.elements.fluxlines.fluxline_straight import FluxlineStraight
from kqcircuits.elements.meander import Meander
from kqcircuits.elements.waveguide_coplanar import WaveguideCoplanar
from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt
from kqcircuits.qubits.swissmon import Swissmon
from math import sqrt, pi, tan


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


        def curve_length_and_end_points(pnts, p):
            """Returns curve length, curve start point, and curve end point, for given point pnts[p] in list pnts."""
            if p == 0 or p + 1 >= len(pnts):
                return 0.0, pnts[p], pnts[p]
            v1, v2, alpha1, alpha2, _ = WaveguideCoplanar.get_corner_data(pnts[p-1], pnts[p], pnts[p+1], self.r)
            abs_turn = pi - abs(pi - abs(alpha2 - alpha1))
            cut_dist = self.r * tan(abs_turn / 2)
            return self.r * abs_turn, pnts[p] + (-cut_dist / v1.length()) * v1, pnts[p] + (cut_dist / v2.length()) * v2


        # shifts = [
        #     pya.DVector(0, self.b),
        #     pya.DVector(0, self.s_lattice),
        #     pya.DVector(self.s_lattice, self.s_lattice)
        # ]
        # pts2 = [p + s for p, s in zip(pts, shifts)]
        # pts.reverse()
        shape = pya.DPolygon(pts)
        self.cell.shapes(self.get_layer("base_metal_gap_wo_grid")).insert(shape)
        _, self.swissmon_refpoints_abs = self.insert_cell(Swissmon, pya.DCplxTrans(1, 45, False, 1500, 0))

        _, self.swissmon_refpoints_abs2 = self.insert_cell(Swissmon, pya.DCplxTrans(1, 45, False, 2500, 0))

        meander_start = self.swissmon_refpoints_abs
        meander_end = self.swissmon_refpoints_abs2

        self.insert_cell(Meander, start=pya.DPoint(400,0), end=pya.DPoint(1400,0),
                         length=1000)
        # add reference point
        #self.add_port("", pya.DPoint(0, 0), pya.DVector(-1, 0))
