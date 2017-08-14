Python implementation of SemVer 2.0.0
=====================================

Compatibility and dependencies
------------------------------

Compatible with Python >= 3.6

No dependencies required

Usage
-----

.. code:: python

    >>> from version import Version
    >>> v = Version('3.14.15')
    >>> v
    Version(3.14.15)
    >>> str(v)
    '3.14.15'
    >>> v.major
    3
    >>> v.minor
    14
    >>> v.patch
    15
    >>> v.pre_release
    []
    >>> v.build
    []

.. code:: python

    >>> from version import Version
    >>> v = Version('4.2-1337.pi+3.1415')
    >>> v
    Version(4.2.0-1337.pi+3.1415)
    >>> str(v)
    '4.2.0-1337.pi+3.1415'
    >>> v.major
    4
    >>> v.minor
    2
    >>> v.patch
    0
    >>> v.pre_release
    [1337, 'pi']
    >>> v.build
    [3, 1415]

Notes
-----

No CPython magic (ie. ``['a', 'b', 'c'] == ['a', 'b', 'c']``) is used. Since
the code is not compatible with Python < 3.6, it should at least be compatible
with any Python >= 3.6 implementation.
