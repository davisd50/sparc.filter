from zope import interface
from zope.schema.interfaces import ICollection
from . import ILinkedExpression, IExpressionGroup, IExpressionGroupMemberResolver

@interface.implementer(IExpressionGroupMemberResolver)
class ExpressionGroupMemberResolver(object):
    def resolve(self, expression_group_member):
        if IExpressionGroup.providedBy(expression_group_member):
            if expression_group_member.conjunction == 'OR':
                for expression in expression_group_member.expressions:
                    for o in self._ex(expression):
                        yield o
            if expression_group_member.conjunction == 'AND':
                for o in set.intersection(
                        *[set(list(self._ex(ex))) 
                                for ex in expression_group_member.expressions]):
                    yield o

        else:
            for r in self._ex(expression_group_member):
                yield r
        
    def _ex(self, ex):
        value = ex.value
        if ILinkedExpression.providedBy(value):
            value = set(list(self.resolve(value)))
        #import pdb;pdb.set_trace()
        for o in ex.iterable:
            if not ex.field.interface.providedBy(o):
                continue
            
            # - if field is not collection, then convert to single-entry list
            # - iterate collection of source values
            #   - compare to ex.value and append to source conjunction
            #
            
            compare = getattr(o, ex.field.getName())
            if not ICollection.providedBy(ex.field):
                compare = [compare]
            
            conj = []
            for v in compare:
            
                if ex.condition == '==':
                    if v == value: conj.append(True)
                    else: conj.append(False)
                if ex.condition == '!=':
                    if v != value: conj.append(True)
                    else: conj.append(False)
                if ex.condition == '>':
                    if v > value: conj.append(True)
                    else: conj.append(False)
                if ex.condition == '>=':
                    if v >= value: conj.append(True)
                    else: conj.append(False)
                if ex.condition == '<':
                    if v < value: conj.append(True)
                    else: conj.append(False)
                if ex.condition == '<=':
                    if v <= value: conj.append(True)
                    else: conj.append(False)
                if ex.condition == 'in':
                    if v in value: conj.append(True)
                    else: conj.append(False)
                if ex.condition == 'not in':
                    if v not in value: conj.append(True)
                    else: conj.append(False)
                
            if compare:
                if ex.conjunction == 'OR':
                    if any(conj): yield o
                else:
                    if all(conj): yield o
