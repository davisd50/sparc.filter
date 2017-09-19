import os
import unittest
import zope.testrunner
from sparc.testing.fixture import test_suite_mixin
from sparc.filter.testing import SPARC_FILTER_INTEGRATION_LAYER

from zope import interface
from zope.schema.interfaces import RequiredMissing
from .. import expression, testing, interfaces

class SparcFilterExpressionTestCase(unittest.TestCase):
    layer = SPARC_FILTER_INTEGRATION_LAYER
    
    def test_linked_expressioin(self):
        lex_1 = expression.LinkedExpression(**{
                        'iterable': [],
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'condition': '==',
                        'value': 'test_1'
                        })
        self.assertTrue(interfaces.IExpression.providedBy(lex_1))
        
        #Missing expression member
        with self.assertRaises(RequiredMissing):
            expression.LinkedExpression(**{
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'condition': '==',
                        'value': 'test_1',
                        })
    
    def test_expression(self):
        ex_1 = expression.Expression(**{
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'condition': '==',
                        'value': 'test_1'
                        })
        self.assertTrue(interfaces.IExpression.providedBy(ex_1))
        
        #Missing expression member
        with self.assertRaises(RequiredMissing):
            expression.Expression(**{
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'value': 'test_1',
                        })
        #Bad conjunction
        with self.assertRaises(KeyError):
            ex_2 = expression.Expression(**{
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['bad_attribute'],
                        'conjunction': 'bad',
                        'condition': '==',
                        'value': 'test_1'
                        })
            interfaces.IExpression.validateInvariants(ex_2)
        
        
        #Bad interface
        """
        with self.assertRaises(interface.Invalid):
            expression.Expression(**{
                        #'schema': None,
                        'field': testing.ITestA['identity'],
                        'condition': '==',
                        'value': 'test_1'
                        })
        """
        
        #Bad attribute name
        with self.assertRaises(KeyError):
            ex_2 = expression.Expression(**{
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['bad_attribute'],
                        'condition': '==',
                        'value': 'test_1'
                        })
            interfaces.IExpression.validateInvariants(ex_2)
        
        #Bad condition
        with self.assertRaises(interface.Invalid):
            expression.Expression(**{
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'condition': 'bad_condition',
                        'value': 'test_1'
                        })
        
        #Bad value
        with self.assertRaises(interface.Invalid):
            expression.Expression(**{
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'condition': 'bad_condition'
                        })
        
        #embeddable expressions
        ex_2 = expression.Expression(**{
                        #'schema': testing.ITestB,
                        'field': testing.ITestB['test_a'],
                        'condition': 'in',
                        'value': ex_1
                        })
        self.assertTrue(interfaces.IExpression.providedBy(ex_2))
        
    
    def test_expression_group(self):
        lex_1 = expression.LinkedExpression(**{
                        'iterable': [],
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'condition': '==',
                        'value': 'testa_1'
                        })
        lex_2 = expression.LinkedExpression(**{
                        'iterable': [],
                        #'schema': testing.ITestA,
                        'field': testing.ITestA['identity'],
                        'condition': '==',
                        'value': 'testa_2'
                        })
        eg_1 = expression.ExpressionGroup(conjunction='OR', expressions=set([lex_1, lex_2]))
        self.assertTrue(interfaces.IExpressionGroup.providedBy(eg_1))
        
        #Bad conjunction
        with self.assertRaises(interface.Invalid):
            eg_1 = expression.ExpressionGroup(conjunction='bad', expressions=set([lex_1, lex_2]))
        
        #Bad expression
        with self.assertRaises(interface.Invalid):
            eg_1 = expression.ExpressionGroup(conjunction='OR', expressions=set(['bad_object']))
        
        #embeddable expression groups
        eg_1 = expression.ExpressionGroup(conjunction='AND', expressions=set([lex_1]))
        eg_2 = expression.ExpressionGroup(conjunction='AND', expressions=set([lex_2]))
        eg_3 = expression.ExpressionGroup(conjunction='OR', expressions=set([eg_1, eg_2]))

class test_suite(test_suite_mixin):
    package = 'sparc.filter'
    module = 'expression'
    layer = SPARC_FILTER_INTEGRATION_LAYER
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcFilterExpressionTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])