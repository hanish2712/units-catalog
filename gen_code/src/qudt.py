from pathlib import Path
from rdflib import RDF, RDFS, Graph, Namespace, URIRef
from typing import List, Union, Dict


class qudt_kg:
    # QUDT namespace
    QUDT: Namespace = Namespace("http://qudt.org/schema/qudt/")
    # stored quanitity and unit graphs
    quant_graph: Graph = None
    unit_graph: Graph = None
    # map of all quanities and units to their URI
    quants: Dict[str, str] = None
    units: Dict[str, str] = None

    # tuples of all (quantity, alias) and (unit, alias)
    quant_alias = None
    unit_alias = None

    def __init__(self):
        # Define namespace
        QUDT = Namespace("http://qudt.org/schema/qudt/")

        g = Graph()
        # load quant graph
        # https://qudt.org/2.1/vocab/quantitykind
        g.parse(
            Path(__file__).parent / "qudt/VOCAB_QUDT-QUANTITY-KINDS-ALL-v2.1.ttl", "n3"
        )
        self.quant_graph = g

        # load unit graph
        # https://qudt.org/2.1/vocab/unit
        h = Graph()
        h.parse(Path(__file__).parent / "qudt/VOCAB_QUDT-UNITS-ALL-v2.1.ttl", "n3")
        self.unit_graph = h

        # list all the quantities, ie where the subject is of type QUDT.QuantityKind
        self.quants = {
            str(s).split("/")[-1]: str(s)
            for s in g.subjects(RDF.type, QUDT.QuantityKind)
        }

        self.units = {
            str(s).split("/")[-1]: str(s) for s in h.subjects(RDF.type, QUDT.Unit)
        }

        # ---------------------------
        # quant and unit aliases
        # currently taking all the RDFS.label with english
        self.quant_alias = [
            (o.value, s.toPython())
            for s in g.subjects(RDF.type, QUDT.QuantityKind)
            for o in g.objects(s, RDFS.label)
            if o.language in ["", "en", "en-us"]
        ]
        self.unit_alias = [
            (o.value, s.toPython())
            for s in h.subjects(RDF.type, QUDT.Unit)
            for o in h.objects(s, RDFS.label)
            if o.language in ["", "en", "en-us"]
        ]

    def get_quant(self, string: str):
        #
        return self.quants.get(string)

    def get_unit(self, string: str):
        #
        return self.units.get(string)

    def find_units_for_unitsystem(
        self, quant: Union[str, URIRef], unit_sys: Union[str, URIRef]
    ):
        """return units for given quantity and unit_system
        Args:
            quant - quantity that is in the quantity graph
            unit_sys - unit system defined by QUDT.applicableSystem
        """
        quant = URIRef(quant)
        unit_sys = URIRef(unit_sys)
        return [
            (u.toPython(), quant.toPython())
            for u in self.quant_graph.objects(
                subject=quant, predicate=self.QUDT.applicableUnit
            )
            for su in self.unit_graph.objects(
                subject=u, predicate=self.QUDT.applicableSystem
            )
            if su == unit_sys
        ]

    def search_quants(self, string: str):
        # search for quantities
        # input needs to be string or list of strings
        res = self._query(str(string), self.quant_alias)
        if len(res) >= 1:
            return res

    def search_units(self, string: str):
        # input needs to be string or list of strings
        res = self._query(str(string), self.unit_alias)
        if len(res) >= 1:
            return res

    def _query(self, string, unitmap):
        """
        search prop map prop
        """
        result = []
        for alias, obj_id in unitmap:
            if string.lower() == alias.lower():
                result.append(obj_id)
        return list(set(result))


def get_qudt_prefixes_inrange(multiplierrange=[1e-6, 1e6]):
    """
    retrieve prefixes within the multiplier range
    """

    QUDT = Namespace("http://qudt.org/schema/qudt/")
    pg = Graph()
    # load prefix graph
    pg.parse("src/qudt/VOCAB_QUDT-PREFIXES-v2.1.ttl", "n3")

    return [
        p.toPython()
        for p in pg.subjects(RDF.type, QUDT.Prefix)
        for mf in pg.objects(p, QUDT.prefixMultiplier)
        if min(multiplierrange) <= mf.toPython() <= max(multiplierrange)
    ]
