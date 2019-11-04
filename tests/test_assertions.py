import unittest

from rdflib import RDFS, XSD, Graph, OWL

from funowl.annotations import Annotation
from funowl.assertions import SameIndividual, DifferentIndividuals, ClassAssertion, ObjectPropertyAssertion, \
    NegativeObjectPropertyAssertion, DataPropertyAssertion, NegativeDataPropertyAssertion
from funowl.literals import Literal, TypedLiteral
from tests.utils.base import TestBase, A


class AssertionsTestCase(TestBase):

    def test_sameindividual(self):
        self.assertEqual('SameIndividual( a:Peter a:Peter_Griffin )',
                         SameIndividual(A.Peter, A.Peter_Griffin).to_functional(self.wa).getvalue())
        with self.assertRaises(ValueError):
            # Only one individual
            SameIndividual(A.Peter).to_functional(self.wa)
        self.wa.reset()
        self.assertEqual("""SameIndividual(
    Annotation( rdfs:comment "Many aliases" )
    a:Alex a:Bob a:Charlie
)""", SameIndividual(A.Alex, A.Bob, A.Charlie,
                     annotations=Annotation(RDFS.comment, "Many aliases")).to_functional(self.wa).getvalue())

    def test_sameindividual_rdf(self):
        g = Graph()
        g.bind('owl', str(OWL))
        SameIndividual(A.Peter, A.Peter_Griffin).to_rdf(g)
        print(g.serialize(format="turtle").decode())

    def test_differentindividuals(self):
        self.assertEqual('DifferentIndividuals( a:Peter a:Peter_Griffin )',
                         DifferentIndividuals(A.Peter, A.Peter_Griffin).to_functional(self.wa).getvalue())
        with self.assertRaises(ValueError):
            # Only one individual
            DifferentIndividuals(A.Peter).to_functional(self.wa)
        self.wa.reset()
        self.assertEqual("""DifferentIndividuals(
    Annotation( rdfs:comment "We know better" )
    a:Alex a:Bob a:Charlie
)""", DifferentIndividuals(A.Alex, A.Bob, A.Charlie,
                           annotations=Annotation(RDFS.comment, "We know better")).to_functional(self.wa).getvalue())

    def test_differentindividuals_rdf(self):
        g = Graph()
        g.bind('owl', str(OWL))
        DifferentIndividuals(A.Alex, A.Bob).to_rdf(g)
        self.assertEqual("""@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/a#Alex> a owl:NamedIndividual ;
    owl:differentFrom <http://example.org/a#Bob> .

<http://example.org/a#Bob> a owl:NamedIndividual .""", g.serialize(format="turtle").decode().strip())

        g = Graph(namespace_manager=g.namespace_manager)
        DifferentIndividuals(A.Alex, A.Bob, A.Fred, A.Joe).to_rdf(g)
        print(g.serialize(format="turtle").decode())
        g = Graph(namespace_manager=g.namespace_manager)
        DifferentIndividuals(A.Alex, A.Bob, annotations=[Annotation(RDFS.label, "Test")]).to_rdf(g)
        print(g.serialize(format="turtle").decode())

    def test_classassertion(self):
        self.assertEqual('ClassAssertion( a:GriffinFamilyMember a:Peter_Griffin )',
                         ClassAssertion(A.GriffinFamilyMember, A.Peter_Griffin).to_functional(self.wa).getvalue())
        self.wa.reset()
        self.assertEqual("""ClassAssertion(
    Annotation( rdfs:comment "It runs in..." )
    a:GriffinFamilyMember a:Peter_Griffin
)""", ClassAssertion(A.GriffinFamilyMember, A.Peter_Griffin,
                     Annotation(RDFS.comment, "It runs in...")).to_functional(self.wa).getvalue())

    def test_classassertion_rdf(self):
        g = Graph()
        ClassAssertion(A.GriffinFamilyMember, A.Peter_Griffin).to_rdf(g)
        print('test_classassertion_rdf')
        print(g.serialize(format='turtle').decode())

    def test_objectpropertyassertion(self):
        self.assertEqual('ObjectPropertyAssertion( a:hasBrother a:Meg a:Stewie )',
                         ObjectPropertyAssertion(A.hasBrother, A.Meg, A.Stewie).to_functional(self.wa).getvalue())

    # def test_objectpropertyassertion_rdf(self):
    #     g = Graph()
    #     ObjectPropertyAssertion(A.hasBrother, A.Meg, A.Stewie).to_rdf(g)
    #     print('test_objectpropertyassertion_rdf')
    #     print(g.serialize(format='turtle').decode())

    def test_negativeobjectpropertyassertion(self):
        self.assertEqual('NegativeObjectPropertyAssertion( a:hasBrother a:Meg a:Stewie )',
                         NegativeObjectPropertyAssertion(A.hasBrother, A.Meg, A.Stewie).
                         to_functional(self.wa).getvalue())

    def test_negativeobjectpropertyassertion_rdf(self):
        g = Graph()
        g.bind('owl', str(OWL))
        NegativeObjectPropertyAssertion(A.hasBrother, A.Meg, A.Stewie).to_rdf(g)
        print('test_negativeobejctpropertyassertion_rdf')
        print(g.serialize(format='turtle').decode())


    def test_datapropertyassertion(self):
        x = Literal('"17"^^xsd:integer')
        y = DataPropertyAssertion(A.hasAge, A.Meg, x)
        self.assertEqual('DataPropertyAssertion( a:hasAge a:Meg "17"^^xsd:integer )',
                         DataPropertyAssertion(A.hasAge, A.Meg, Literal('"17"^^xsd:integer')).
                         to_functional(self.wa).getvalue())

    # def test_datapropertyassertion_rdf(self):
    #     x = Literal('"17"^^xsd:integer')
    #     g = Graph()
    #     DataPropertyAssertion(A.hasAge, A.Meg, x).to_rdf(g)
    #     print('test_datapropertyassertion_rdf')
    #     print(g.serialize(format='turtle').decode())

    def test_negativedatapropertyassertion(self):
        TypedLiteral(5, XSD.integer)
        self.assertEqual('NegativeDataPropertyAssertion( a:hasBrother a:Meg "5"^^xsd:integer )',
                         NegativeDataPropertyAssertion(A.hasBrother, A.Meg, TypedLiteral(5, XSD.integer)).
                         to_functional(self.wa).getvalue())

    # def test_negativedatapropertyassertion_rdf(self):
    #     g = Graph()
    #     NegativeDataPropertyAssertion(A.hasBrother, A.Meg, TypedLiteral(5, XSD.integer)).to_rdf(g)
    #     print(g.serialize(format='turtle').decode())

if __name__ == '__main__':
    unittest.main()
