# lattice unit
from kqcircuits.elements.element import Element
from kqcircuits.elements.fluxlines.fluxline_straight import FluxlineStraight
from kqcircuits.elements.meander import Meander
from kqcircuits.elements.waveguide_coplanar import WaveguideCoplanar
from kqcircuits.pya_resolver import pya
from kqcircuits.util.netlist_extraction import log
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

        shape = pya.DPolygon(pts)
        self.cell.shapes(self.get_layer("base_metal_gap_wo_grid")).insert(shape)
        self.swissmon_inst, self.swissmon_refpoints_abs = self.insert_cell(Swissmon, pya.DCplxTrans(1, 45, False, 1500, 0), "Q")
        # add reference point
        #self.add_port("", pya.DPoint(0, 0), pya.DVector(-1, 0))
        super().build()
        log.critical("Building Lattice")
