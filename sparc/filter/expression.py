from zope import interface
from zope.component.factory import Factory
from zope.schema import getFields
from zope.schema.fieldproperty import createFieldProperties
from . import interfaces

@interface.implementer(interfaces.IExpression)
class Expression(object):
    createFieldProperties(interfaces.IExpression)
    
    def __init__(self, **kwargs):
        fields = getFields(interfaces.IExpression)
        for name in fields:
            setattr(self, name, kwargs.get(name, fields[name].default))
ExpressionFactory = Factory(Expression)

@interface.implementer(interfaces.ILinkedExpression)
class LinkedExpression(object):
    createFieldProperties(interfaces.ILinkedExpression)
    
    def __init__(self, **kwargs):
        fields = getFields(interfaces.ILinkedExpression)
        for name in fields:
            setattr(self, name, kwargs.get(name, fields[name].default))
LinkedExpressionFactory = Factory(LinkedExpression)

@interface.implementer(interfaces.IExpressionGroup)
class ExpressionGroup(object):
    createFieldProperties(interfaces.IExpressionGroup)
    
    def __init__(self, **kwargs):
        fields = getFields(interfaces.IExpressionGroup)
        for name in fields:
            setattr(self, name, kwargs.get(name, fields[name].default))
ExpressionGroupFactory = Factory(ExpressionGroup)
