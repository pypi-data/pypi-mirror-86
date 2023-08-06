# -*- coding: utf-8 -*-
from array import array
from six.moves import collections_abc
import six

from ..operator import Operator


class ContainOperator(Operator):
    """
    Asserts if a given value or values can be found
    in a another object.

    Example::

        # Should style
        'foo bar' | should.contain('bar')
        ['foo', 'bar'] | should.contain('bar')
        ['foo', 'bar'] | should.contain('foo', 'bar')
        [{'foo': True}, 'bar'] | should.contain({'foo': True})

        # Should style - negation form
        'foo bar' | should.do_not.contain('bar')
        ['foo', 'bar'] | should.do_not.contain('baz')

        # Expect style
        'foo bar' | expect.to.contain('bar')
        ['foo', 'bar'] | expect.to.contain('bar')
        ['foo', 'bar'] | expect.to.contain('foo', 'bar')
        [{'foo': True}, 'bar'] | expect.to.contain({'foo': True})

        # Expect style - negation form
        'foo bar' | expect.to_not.contain('bar')
        ['foo', 'bar'] | expect.to_not.contain('baz')
    """

    # Is the operator a keyword
    kind = Operator.Type.MATCHER

    # Enable diff report
    show_diff = True

    # Operator keywords
    operators = ('contain', 'contains', 'includes')

    # Operator chain aliases
    aliases = ('value', 'item', 'string', 'text', 'expression', 'data')

    # Expected template message
    expected_message = Operator.Dsl.Message(
        'a value that contains "{value}"',
        'a value that does not contains "{value}"',
    )

    # Subject template message
    subject_message = Operator.Dsl.Message(
        'a value of type "{type}" with content "{value}"',
    )

    # Stores types to normalize before the assertion
    NORMALIZE_TYPES = (
        collections_abc.Iterator,
        collections_abc.MappingView,
        collections_abc.Set,
        array
    )

    LIST_TYPES = (tuple, list, set, array)

    def match(self, subject, *values):
        if isinstance(subject, self.NORMALIZE_TYPES):
            subject = list(subject)
        elif isinstance(subject, collections_abc.Mapping):
            subject = list(subject.values())

        if not isinstance(subject, collections_abc.Sequence):
            return False, ['is not a valid sequence type']

        reasons = []

        if len(values) == 1 and isinstance(values[0], self.LIST_TYPES):
            values = list(values[0])

        for value in values:
            matches_any, reason = self._matches_any(value, subject)
            reasons.append(reason)

            if not matches_any:
                return False, [reason]

        return True, reasons

    def _matches_any(self, expected, subject):
        if len(subject) == 0:
            return False, 'empty item'

        if isinstance(subject, six.string_types):
            if expected in subject:
                return True, 'item {0!r} found'.format(expected)
            return False, 'item {0!r} not found'.format(expected)

        for item in subject:
            if item == expected:
                return True, 'item {0!r} found'.format(expected)

        return False, 'item {0!r} not found'.format(expected)
