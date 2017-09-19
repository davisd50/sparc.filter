import os
import unittest
import zope.testrunner
from sparc.testing.fixture import test_suite_mixin
from sparc.filter.testing import SPARC_FILTER_INTEGRATION_LAYER

from zope import component
from .. import testing, interfaces

class SparcFilterResolverTestCase(unittest.TestCase):
    layer = SPARC_FILTER_INTEGRATION_LAYER
    
    def test_single_equal_single(self):
        """
        source: non-collection
        condition: ==
        value: non-collection
        """
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '==',
                     'value': 'testa_1'})
        r = list(resolver.resolve(lex_1))
        self.assertEqual(set(r), set([testing.testa_1]))
        
        eg_1 = component.createObject('sparc.filter.expression_group',
                    **{'conjunction': 'OR',
                       'expressions': set([lex_1])})
        r = list(resolver.resolve(eg_1))
        self.assertEqual(set(r), set([testing.testa_1]))
        
        
        lex_2 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '==',
                     'value': 'bad_value'})
        r = list(resolver.resolve(lex_2))
        self.assertEqual(set(r), set([]))
    
    def test_multiple_equal_single(self):
        """
        source: collection
        condition: ==
        value: non-collection
        """
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['group'],
                     'conjunction': 'OR',
                     'condition': '==',
                     'value': 'a'})
        r = list(resolver.resolve(lex_1))
        self.assertEqual(set(r), set([testing.testa_1, testing.testa_2]))
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['group'],
                     'conjunction': 'AND',
                     'condition': '==',
                     'value': 'a'})
        r = list(resolver.resolve(lex_1))
        self.assertEqual(set(r), set([testing.testa_2]))
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['group'],
                     'conjunction': 'OR',
                     'condition': '==',
                     'value': 'b'})
        r = list(resolver.resolve(lex_1))
        self.assertEqual(set(r), set([testing.testa_1]))
        
    
    def test_single_equal_multiple(self):
        """
        source: non-collection
        condition: ==
        value: collection
        """
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '==',
                     'value': 'testa_1'})
        
        lex_2 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '==',
                     'value': 'testa_2'})
        
        eg_1 = component.createObject('sparc.filter.expression_group',
                    **{'conjunction': 'OR',
                       'expressions': set([lex_1, lex_2])})
        r = list(resolver.resolve(eg_1))
        self.assertEqual(set(r), set([testing.testa_1,testing.testa_2]))
        
        eg_1 = component.createObject('sparc.filter.expression_group',
                    **{'conjunction': 'AND',
                       'expressions': set([lex_1, lex_2])})
        r = list(resolver.resolve(eg_1))
        self.assertEqual(set(r), set([]))
    
    def test_single_not_equal_single(self):
        """
        source: non-collection
        condition: !=
        value: non-collection
        """
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '!=',
                     'value': 'testa_1'})
        r = list(resolver.resolve(lex_1))
        self.assertTrue(len(r) > 0)
        self.assertNotIn(testing.testa_1, r)
    
        lex_2 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '!=',
                     'value': 'bad_value'})
        r = list(resolver.resolve(lex_2))
        self.assertTrue(len(r) > 0)
        self.assertIn(testing.testa_1, r)
    
    def test_single_not_equal_multiple(self):
        """
        source: non-collection
        condition: !=
        value: collection
        """
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '!=',
                     'value': 'testa_1'})
        
        lex_2 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': '!=',
                     'value': 'testa_2'})
        
        eg_1 = component.createObject('sparc.filter.expression_group',
                    **{'conjunction': 'OR',
                       'expressions': set([lex_1, lex_2])})
        r = list(resolver.resolve(eg_1))
        self.assertTrue(len(r) > 0)
        self.assertIn(testing.testa_1, r)
        self.assertIn(testing.testa_2, r)
        
        eg_1 = component.createObject('sparc.filter.expression_group',
                    **{'conjunction': 'AND',
                       'expressions': set([lex_1, lex_2])})
        r = list(resolver.resolve(eg_1))
        self.assertNotIn(testing.testa_1, r)
        self.assertNotIn(testing.testa_2, r)
    
    def test_single_greater_than_less_than_equal_single(self):
        """
        source: non-collection
        condition: > >= < <=
        value: non-collection
        """
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['number'],
                     'condition': '>',
                     'value': 1})
        r = list(resolver.resolve(lex_1))
        self.assertNotIn(testing.testa_1, r)
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['number'],
                     'condition': '>=',
                     'value': 1})
        r = list(resolver.resolve(lex_1))
        self.assertIn(testing.testa_1, r)
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['number'],
                     'condition': '<',
                     'value': 1})
        r = list(resolver.resolve(lex_1))
        self.assertEquals(r, [])
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['number'],
                     'condition': '<=',
                     'value': 1})
        r = list(resolver.resolve(lex_1))
        self.assertIn(testing.testa_1, r)
        
        
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['number'],
                     'condition': '>',
                     'value': 0})
        lex_2 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['number'],
                     'condition': '<',
                     'value': 2})
        
        eg_1 = component.createObject('sparc.filter.expression_group',
                    **{'conjunction': 'AND',
                       'expressions': set([lex_1, lex_2])})
        
        r = list(resolver.resolve(eg_1))
        self.assertEquals(r, [testing.testa_1])
    
    def test_single_in_not_in_single(self):
        """
        source: non-collection
        condition: in not in
        value: non-collection
        """
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': 'in',
                     'value': 'testa_1'})
        r = list(resolver.resolve(lex_1))
        self.assertEquals(r, [testing.testa_1])
        
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        lex_1 = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestBase['identity'],
                     'condition': 'not in',
                     'value': 'testa_1'})
        r = list(resolver.resolve(lex_1))
        self.assertTrue(len(r)>0)
        self.assertNotIn(testing.testa_1, r)
    
    def test_embedded(self):
        resolver = component.getUtility(interfaces.IExpressionGroupMemberResolver)
        lex_a = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestA['group'],
                     'condition': '==',
                     'value': 'b'})
        lex_b = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestB['test_a'],
                     'condition': 'in',
                     'value': lex_a})
        lex_c = component.createObject("sparc.filter.linked_expression",
                    **{'iterable': testing.test_objects,
                     'field': testing.ITestC['test_b'],
                     'condition': 'in',
                     'value': lex_b})
        r = list(resolver.resolve(lex_c))
        self.assertEquals(r, [testing.testc_1])
        
        r = list(resolver.resolve(lex_b))
        self.assertEquals(r, [testing.testb_1])

class test_suite(test_suite_mixin):
    package = 'sparc.filter'
    module = 'resolver'
    layer = SPARC_FILTER_INTEGRATION_LAYER
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcFilterResolverTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])