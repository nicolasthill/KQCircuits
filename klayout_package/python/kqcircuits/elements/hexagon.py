# Hexagon
from kqcircuits.elements.element import Element
from kqcircuits.elements.waveguide_composite import WaveguideComposite, Node
from kqcircuits.pya_resolver import pya
from kqcircuits.util.geometry_helper import point_shift_along_vector
from kqcircuits.util.netlist_extraction import log
from kqcircuits.util.parameters import Param, pdt

from kqcircuits.elements.lattice_unit import Lattice


class Hexagon(Element):
    """
    Hexagon containing 6 lattice units
    """
    def produce_couplers(self):
        self.produce_coupler("Q", "QB2", 2)

    def produce_coupler(self, qubit_a_name, qubit_b_name, port_nr):
        self.insert_cell(WaveguideComposite, nodes=[

            Node(self.refpoints["{}_port_cplr{}".format(qubit_a_name, port_nr)]),
            Node(point_shift_along_vector(self.refpoints["{}_port_cplr{}".format(qubit_a_name, port_nr)],
                                          self.refpoints["{}_base".format(qubit_a_name)], -40)),

            Node(point_shift_along_vector(self.refpoints["{}_port_cplr{}".format(qubit_b_name, port_nr)],
                                          self.refpoints["{}_base".format(qubit_b_name)], -40),
                 n_bridges=3),
            Node(self.refpoints["{}_port_cplr{}".format(qubit_b_name, port_nr)])])


    def build(self):
        # store refs of all lattices
        log.critical("Building Hexagon {}".format(self.display_name))
        self.lattice_ref = []
        for phi in range(6):
            self.lattice_ref.append(
                self.insert_cell(Lattice,
                                 pya.DCplxTrans(1, phi * 60, False, 0, 0), inst_name=f"lattice_{str(phi)}")
            )

        # add reference point
        self.add_port("", pya.DPoint(0, 0), pya.DVector(-1, 0))

        #self.produce_couplers()

        super().build()

        log.critical("Building Hexagon_end")
        log.critical(self.refpoints)
