.. image:: http://i.imgur.com/kKZPYut.jpg
   :width: 100%
   :alt: grappa logo
   :align: center


|Build Status| |PyPI| |Coverage Status| |Documentation Status| |Stability| |Quality| |Versions| |SayThanks|

About
-----

``grappa`` is a behavior-oriented, self-declarative, expressive and developer-friendly
lightweight assertion library for Python_ that aims to make testing more productive and frictionless for humans.

``grappa`` comes with two declarative `assertion styles`_: ``expect`` and ``should``.

It also comes with a detailed, human-friendly `error reporting`_ system that aims to reduce friction,
provide better feedback and improve human speed and agility while identifying and fixing errors.

To get started, take a look to the `showcase`_ code, `tutorial`_, available `plugins`_ and `operators documentation`_.

For HTTP protocol assertions, see `grappa-http`_.

Status
------

``grappa`` is considered **stable** software, however it's not mature, widely used software. 
New features may be added from time to time or minor bugs may be experienced.

Community contributions and bug reports are very welcome.

Showcase
--------

A small example demonstrating some `grappa` features.
See `documentation`_ and `tutorial`_ for more examples.

.. code-block:: python

    from grappa import should

    True | should.be.true
    False | should.be.false
    None | should.be.none

    '' | should.be.empty
    [] | should.be.empty
    'foo' | should.exists

    3.14 | should.be.lower.than(4)
    3.14 | should.be.higher.than(3)
    3.14 | should.be.within(2, 4)

    'bar' | should.be.equal.to('bar', msg='value is not "bar"')
    [1, 2, 3] | should.be.equal.to([1, 2, 3])

    'hello, grappa' | should.startswith('hello')
    'hello, grappa' | should.endswith('grappa')
    [1, 2, 3, 4] | should.startswith(1)
    [1, 2, 3, 4] | should.endswith(4)

    'Hello grappa' | should.match('(\W)+ grappa$')
    'Hello grappa' | should.contain('grappa') | should.contain('he')
    ['foo', 'bar'] | should.contain('foo') | should.do_not.contain('baz')

    'foo' | should.be.a('string')
    {'foo': True} | should.be.a('dict')

    iter([1, 2, 3]) | should.have.length.of(3)
    [1, 2, 3] | should.be.a('list') > should.have.length.of(3)

    (lambda x: x) | should.be.callable
    (lambda x: x) | should.not_have.type.of('generator')

    'foo' | should.pass_test(lambda x: x in 'foo bar')
    'foo' | should.pass_function(lambda x: len(x) > 2)

    (lambda: x) | should.raises(NameError)
    (lambda: x) | should.does_not.raises(RuntimeError)

    {'foo': 'bar'} | should.have.key('foo').that.should.be.equal('bar')
    (1, 2, 3, 4) | should.be.a(tuple) > should.have.index.at(3) > should.be.equal.to(4)

    an_object | should.have.properties('foo', 'bar', 'baz')
    an_object | should.implement.methods('foo', 'bar', 'baz')

    {'foo': True, 'bar': False} | should.all(should.have.key('foo'), should.have.key('bar'))
    {'foo': True, 'bar': False} | should.any(should.have.key('foo'), should.have.key('baz'))

    ({'bar': [1, 2, 3]}
        | should.have.key('bar')
        > should.be.a('list')
        > should.have.length.of(3)
        > should.contain.item(3)
        > should.have.index.at(1)
        > should.be.equal.to(2))

    with should('foo'):
        should.be.a(str)
        should.have.length.of(3)
        should.be.equal.to('foo')


Let's see how the error report looks like in ``grappa`` running in ``pytest``.

See `error reporting`_ documentation for more details about how ``grappa`` error report system works.

.. code-block:: python

    ======================================================================
    FAIL: tests.should_test.test_grappa_assert
    ======================================================================
    Traceback (most recent call last):
    File ".pyenv/versions/3.6.0/lib/python3.6/site-packages/nose/case.py", line 198, in runTest
    self.test(*self.arg)
    File "grappa/tests/should_test.py", line 16, in test_grappa_assert
    x | should.be.have.length.of(4)
    File "grappa/grappa/test.py", line 248, in __ror__
    return self.__overload__(value)
    File "grappa/grappa/test.py", line 236, in __overload__
    return self.__call__(subject, overload=True)
    File "grappa/grappa/test.py", line 108, in __call__
    return self._trigger() if overload else Test(subject)
    File "grappa/grappa/test.py", line 153, in _trigger
    raise err
    AssertionError: Oops! Something went wrong!

    The following assertion was not satisfied
      subject "[1, 2, 3]" should be have length of "4"

    Message
      subject list must have at least 4 items

    Reasons
      ▸ unexpected object length: 3

    What we expected
      an object that can be length measured and its length is equal to 4

    What we got instead
      an object of type "list" with length 3

    Information
      ▸ Object length is measured by using "len()" built-in
        Python function or consuming an lazy iterable, such as a
        generator. Most built-in types and objects in Python
        can be tested that way, such as str, list, tuple, dict...
        as well as any object that implements "__len__()" method.
        — Reference: https://docs.python.org/3/library/functions.html#len

    Where
      File "grappa/tests/should_test.py", line 16, in test_grappa_assert

     8|
     9|  def test_native_assert():
    10|      x = [1, 2, 3]
    11|      assert len(x) == 4
    12|
    13|
    14|  def test_grappa_assert():
    15|      x = [1, 2, 3]
    16| >    x | should.be.have.length.of(4)
    17|
    18|
    19|  def test_bool():
    20|      True | should.be.true | should.be.present
    21|      False | should.be.false | should.be.equal.to(False)
    22|      False | should.be.false | should.not_be.equal.to(True)

Demo
----

.. image:: https://asciinema.org/a/d6yd2475m41thdku7d3ntkeir.png
   :width: 900
   :alt: showcase
   :align: center
   :target: https://asciinema.org/a/d6yd2475m41thdku7d3ntkeir?autoplay=1&speed=3&size=small

Why grappa?
-----------

``grappa`` aims to assist humans while doing a very recurrent and not very fun task in software development: testing things.

The core idea behind ``grappa`` comes from the fact that human time is considerably more expensive than machine time,
and therefore any machine assistance to optimize processes and close the gap is beneficial.

With ``grappa`` you can express almost in plain English what the test contract actually is, but in a way that's
fun and easy to write but also more easy and pleasant to read or maintain by other developers.


The Zen of grappa
-----------------

- Testing is about feedback: detailed, easy to understand, human-friendly is always better.
- Frictionless testing: introducing self-declarative behavior testing patterns can make testing more fun for test writers and more enjoyable for test readers.
- Expressivity is paramount: humans should easily understand what the code is doing.
- Human time is expensive: any modern software should assist people to identify and understand errors easily.
- Make error reporting great again: feedback during testing is key, let's make it more handy and less frustrating.
- Testing patterns consolidation: software expectations are limited to the boundaries of language data types and structures.
- Hurt less feelings: seeing errors is not a nice thing, but it can be painless if details are showed you in a more gentle way.


Features
--------

-  Behavior-oriented expressive fluent API.
-  Built-in assertion DSL with English lexicon and semantics.
-  Supports both ``expect`` and ``should`` assertion styles.
-  Full-featured built-in `assertion operators`_.
-  Human-friendly and detailed `error reporting`_.
-  Built-in expectations difference comparison between subject and expected values.
-  Extensible assertions supporting third-party `plugins`_.
-  Assertion chaining and composition.
-  Composable assertion via logical operators such as ``and`` & ``or``.
-  Testing framework agnostic. Works with ``unittest``, ``nosetests``, ``pytest``, ``behave`` ...
-  Easy to hack via programmatic API.
-  Lightweight and (almost) dependency-free.
-  Works with Python 2.7+, 3+, PyPy and potentially with other Python implementations.


Installation
------------

Using ``pip`` package manager:

.. code-block:: bash

    pip install --upgrade grappa

Or install the latest sources from Github:

.. code-block:: bash

    pip install -e git+git://github.com/grappa-py/grappa.git#egg=grappa


.. _Python: http://python.org
.. _`documentation`: http://grappa.readthedocs.io
.. _`operators documentation`: http://grappa.readthedocs.io/en/latest/operators.html
.. _`tutorial`: http://grappa.readthedocs.io/en/latest/tutorial.html
.. _`plugins`: http://grappa.readthedocs.io/en/latest/plugins.html
.. _`error reporting`: http://grappa.readthedocs.io/en/latest/errors.html
.. _`assertion styles`: http://grappa.readthedocs.io/en/latest/style.html
.. _`assertion operators`: http://grappa.readthedocs.io/en/latest/operators.html
.. _`grappa-http`: https://github.com/grappa-py/http

.. |Build Status| image:: https://travis-ci.org/grappa-py/grappa.svg?branch=master
   :target: https://travis-ci.org/grappa-py/grappa
.. |PyPI| image:: https://img.shields.io/pypi/v/grappa.svg?maxAge=2592000?style=flat-square
   :target: https://pypi.python.org/pypi/grappa
.. |Coverage Status| image:: https://coveralls.io/repos/github/grappa-py/grappa/badge.svg?branch=master
   :target: https://coveralls.io/github/grappa-py/grappa?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/grappa/badge/?version=latest
   :target: http://grappa.readthedocs.io/en/latest/?badge=latest
.. |Quality| image:: https://codeclimate.com/github/grappa-py/grappa/badges/gpa.svg
   :target: https://codeclimate.com/github/grappa-py/grappa
   :alt: Code Climate
.. |Stability| image:: https://img.shields.io/pypi/status/grappa.svg
   :target: https://pypi.python.org/pypi/grappa
   :alt: Stability
.. |Versions| image:: https://img.shields.io/pypi/pyversions/grappa.svg
   :target: https://pypi.python.org/pypi/grappa
   :alt: Python Versions
.. |SayThanks| image:: https://img.shields.io/badge/Say%20Thanks!-%F0%9F%A6%89-1EAEDB.svg
   :target: https://saythanks.io/to/h2non
   :alt: Say Thanks
