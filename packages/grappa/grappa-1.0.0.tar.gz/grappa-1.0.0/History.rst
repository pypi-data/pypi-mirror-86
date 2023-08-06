
History
=======

1.0.0 / 2020-11-21
------------------

  * feat: major version v1
  * fix: #53, #55, #48, #59 (credits to @sgissinger)
  * feat: added mock call operators (credits to @sgissinger)
  * make github actions fail on every flake8
  * pass flake8
  * enforce implements operator
  * missing kwargs argument
  * add contain tests
  * normalize code between contain and key and add lists expectations to contain
  * improve been_called_with reasons when false
  * use os.path.join instead of remove and Foo class for spy tests
  * os.path.basename not a good candidate to count mock calls because it seems to call itself
  * missing experimental for pypy2
  * re-try to use pypy2 on github actions
  * skip tests which does not work on pypy2
  * add contain tests
  * contain now supports dicts and arrays. Partially fix #59
  * use isinstance
  * improve keys operator tests and add array tests
  * keys operator now supports arrays
  * set env var in step only
  * allow errors on 3.10-dev builds
  * allow insecure commands for github action nightly
  * upgrade action version
  * run 3.10-dev on ubuntu only
  * add python 3.10 nightly to github action pipeline
  * set 50 chars to normalization size
  * flake8 correction and docstrings upgrade
  * add key operator tests
  * key operator simplified and works with tuples, lists and sets. fixes #48 ?
  * do not upgrade pip on github actions
  * try to use pypy only on ubuntu for github actions
  * use only include for pypy
  * add python 3.9, prefer jobs over matrix, add pypy env var in travis ci
  * add mocker stop all
  * add python 3.9 to github actions
  * pypy2 does not seem to work in github actions like it does in TravisCI
  * exclude pypy2 on ubuntu
  * exclude macos pypy2 from ci matrix
  * use pypy2 instead
  * add pypy to github actions
  * Create python-package.yml
  * added mock impl validator docstring and error tips
  * added explicit docstrings to have_been operators
  * use pytest-mock 2.0.0 for python 2.7
  * make flake8 pass
  * set exception __cause__ to get direct causes when internal exceptions occurs
  * move mock implementation to decorators module
  * add tests using pytest-mock spies and stubs which are basic funcs
  * do not rely explicitly on MagicMock but test needed implementation
  * better get attribute handling
  * better called once messages
  * add been_called operator tests
  * add been_called operators
  * missing end line
  * fixes #55 should.not_have.key(...)
  * once negated a sentence stays negated
  * make accessor be called
  * fix(Makefile): lovely tabs
  * fix(Makefile): use twine for publishing

0.1.12 / 2020-02-26
--------------------

  * feat(version): bimp
  * feat(setup): add python 3.7 & 3.8 classifiers
  * Merge pull request #56 from jdlourenco/collections-abc-six
  * update code according flake8 warnings and errors
  * feat(requirements): bump flake8
  * feat(travis): add python 3.7 & 3.8
  * fix(travis): remove python 3.3 & 3.4
  * change bump six to 0.14
  * change use six.moves.collections_abc module for importing classes that moved to the collections.abc module on python3

0.1.10 / 2018-10-02
-------------------

   * feat: add ``only`` operator #45

0.1.9 / 2018-06-02
------------------

   * fix(#42): Add string comparison parity for Python 2.7

v0.1.8 / 2018-01-23
-------------------

  * Merge pull request #39 from dancingcactus/master
  * Removes unused imports
  * Allow partials to be used with raises operators
  * fix(operator): minor type in exception message
  * Merge pull request #38 from dancingcactus/master
  * Updates the docs for Raises to encapsulate feedback from #37
  * Update README.rst
  * refactor(docs): remove codesponsor
  * feat(docs): add sponsor ad
  * feat(docs): update status note
  * feat(docs): update status note
  * Merge branch 'master' of https://github.com/grappa-py/grappa
  * fix(docs): use proper organization name
  * Update AUTHORS
  * refactor(docs): import AUTHORS file
  * feat: add AUTHORS file
  * fix(setup.py): update package URL

v0.1.7 / 2017-05-12
-------------------

  * feat(#33): show available operators on attribute error
  * feat(#36): add allowed assertion attributes on error

v0.1.6 / 2017-04-28
-------------------

* fix(type): expose proper type value if a type value is the expected value
* fix(reporter): use search() instead of match() for line code matching. fix(reporters): escape underscore sequences

v0.1.5 / 2017-04-28
-------------------

* feat(reporters): add code reporter
* feat(operators): add "that_is", "which_is" attribute DSL operators
* refactor(reporter): match additional negation assertions

v0.1.4 / 2017-04-27
-------------------

* feat(reporters): match attribute expressions for proper code line reporting
* feat(equal): enable show_diff report in operator
* fix(index_test): bad file formatting
* refactor(index_test): add error test case
* refactor(index_test): remove commented code
* feat(docs): add context assertion example in tutorial
* feat(docs): add context manager example
* fix(docs): update error exception example
* refactor(docs): update showcase example
* feat(operators): add not_satisfy attribute operator

v0.1.3 / 2017-03-29
-------------------

* feat(docs): add raise exception examples
* refactor(docs): update showcase example
* feat(reporter): normalize value output in subject/expect sections
* feat(docs): update examples and FAQs. feat(operators): add aliases for start/end operator
* feat(docs): add link to grappa-http plugin
* refactor(docs): add operators type section
* refactor(docs): add beta status documentation notice
* feat(docs): update description
* refactor(docs): update status description
* feat(docs): update links

v0.1.2 / 2017-03-26
-------------------

* feat(docs): add matchers supported keyword arguments
* feat(docs): improve descriptions
* feat(operators): improve length operator for access based chaining
* fix(docs): update error custom message example
* feat(docs): improve documentation. adds operators composition section
* fix(setup.py): add author email

v0.1.1 / 2017-03-23
-------------------

* refactor(diff): process expected values as tuple first
* fix(contain): remove print statements
* refactor(core): normalize yielding syntax, add missing documentation
* refactor(core): normalize yielding syntax, add missing documentation
* feat(#26): support disable operator chaining
* feat(#28): better assertion reporting. feat(operators): add index operator
* refactor(reporter): support raw mode with proper indent pretty printing
* refactor(operators): add satisfy/satisfies attribute operators
* feat(diff): consume diff specific subject/expected values
* feat(operators): add is/is_not operator attributes
* refactor(core): isolate reporters per module
* feat(#13, #25): add suboperators support and diff output report
* refactor(docs): update organization name
* refactor(docs): update project image
* refactor(reporter): ignore subject/expected output if empty
* refactor(reporter): show diff if enabled
* feat(docs): add in a nutshell section
* feat(#24, #25): feature enhancements
* feat(docs): add say thanks badge
* refactor(reporter): load value from operator first
* fix(docs): use proper badges
* fix(docs): update type operator examples
* fix(metadata): update
* refactor(test): add chained test for keys
* feat(Makefile): add publish commands

0.1.0 (2017-03-05)
------------------

* First version (beta)
