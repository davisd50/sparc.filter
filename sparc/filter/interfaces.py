from zope import interface
from zope import schema as schema_

class IExpressionGroupMember(interface.Interface):
    """Marker for providers that can belong within a IExpressionGroup providers expressions attribute"""

class IExpression(interface.Interface):
    """Describes parameters intended to produce a set of result objects"""

    field = schema_.Field(
                title="Field",
                description="Schema field expression will apply to",
                required=True
                )
    conjunction = schema_.Choice(
                title="Conjunction",
                description="Append logic for multi-value (iterable) fields",
                values=['AND','OR'],
                default='OR'
            )
    condition = schema_.Choice(
                title="Condition",
                description="Filter conditional matching logic",
                values=['==',
                        '!=',
                        '<',
                        '<=',
                        '>',
                        '>=',
                        'in',
                        'not in'
                        ],
                required=True
            )
    value = schema_.Field(
                title="Value",
                description="value to be used in expression condition, or another IExpression provider whose results will be evaluated against",
                required=True
            )

class ILinkedExpression(IExpressionGroupMember, IExpression):
    """A resolvable expression"""
    iterable = schema_.Iterable(
                title="Iterable",
                description="Iterable containing objects to apply expression to.",
                required=True
                )
    value = schema_.Field(
                title="Value",
                description="value to be used in expression condition, or another ILinkedExpression provider whose resolved results will be evaluated against",
                required=True
            )

class IExpressionGroup(IExpressionGroupMember):
    conjunction = schema_.Choice(
                title="Conjunction",
                description="Append logic for condition statements within the group",
                required=True,
                values=['AND','OR']
            )
    expressions = schema_.Set(
                title="Expressions",
                description="Group of expressions and sub-expression groups",
                required=True,
                value_type=schema_.Object(schema=IExpressionGroupMember)
            )

class IExpressionGroupMemberResolver(interface.Interface):
    def resolve(expression_group_member):
        """Returns iterable of resolved result objects
        
        Args:
            expression_group_member: IExpressionGroupMember provider
        """
