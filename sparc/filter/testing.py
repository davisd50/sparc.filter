import sparc.filter
from sparc.testing.testlayer import SparcZCMLFileLayer

SPARC_FILTER_INTEGRATION_LAYER = SparcZCMLFileLayer(sparc.filter)

from zope import interface
from zope import schema
from zope.schema.fieldproperty import createFieldProperties

#Interfaces
class ITestBase(interface.Interface):
    """Some marker"""
    identity = schema.TextLine(required=True)
    number = schema.Int(required=True)
    group = schema.List()

class ITestA(ITestBase):
    """Schema A"""

class ITestB(ITestBase):
    """Schema B"""
    test_a = schema.Set(value_type=schema.Object(schema=ITestA))

class ITestC(ITestBase):
    """Schema B"""
    test_b = schema.Set(value_type=schema.Object(schema=ITestB))

#Implementations
@interface.implementer(ITestA)
class TestA(object):
    createFieldProperties(ITestA)
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
@interface.implementer(ITestB)
class TestB(object):
    createFieldProperties(ITestB)
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
@interface.implementer(ITestC)
class TestC(object):
    createFieldProperties(ITestC)
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

#Objects
testa_1 = TestA(identity='testa_1',number=1,group=['a','b'])
testa_2 = TestA(identity='testa_2',number=2,group=['a'])
testb_1 = TestB(identity='testb_1',number=3, test_a=set([testa_1]),group=[])
testb_2 = TestB(identity='testb_2',number=4, test_a=set([testa_2]),group=[])
testc_1 = TestC(identity='testc_1',number=5, test_b=set([testb_1, testb_2]),group=[])

test_objects = [i for i in locals().values() if ITestBase.providedBy(i)]