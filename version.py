import sys
import re
if sys.version_info[0] > 2:
    from itertools import zip_longest
else:
    from itertools import izip_longest as zip_longest


class _Comparable(object):
    """Rich comparison operators based on __lt__ and __eq__"""
    __gt__ = lambda self, other: not self < other and not self == other
    __le__ = lambda self, other: self < other or self == other
    __ne__ = lambda self, other: not self == other
    __ge__ = lambda self, other: self > other or self == other


class _Seq(_Comparable):
    """Container to compare agnostic arrays"""
    def __init__(self, seq):
        self.seq = seq

    def __eq__(self, other):
        assert set([int, str]) >= set(map(type, self.seq))
        if len(self.seq) != len(other.seq):
            return False
        for s, o in zip(self.seq, other.seq):
            if not (type(s) is type(o)):
                return False
            if s != o:
                return False
        return True

    def __lt__(self, other):
        assert set([int, str]) >= set(map(type, self.seq))
        for s, o in zip_longest(self.seq, other.seq):
            assert not (s is None and o is None)
            if s is None or o is None:
                return s is None
            elif type(s) is int and type(o) is int:
                if s != o:
                    return s < o
            elif type(s) is int or type(o) is int:
                return type(s) is int
            elif s < o:
                return True
        return False


_re = re.compile(
    r'^'
    r'([0-9]+)(?:\.([0-9]+)(?:\.([0-9]+))?)?'
    r'(?:-([0-9A-Za-z-\.]+))?'
    r'(?:\+([0-9A-Za-z-\.]+))?'
    r'$'
)


def _try_int(s):
    assert type(s) is str
    try:
        return int(s)
    except ValueError:
        return s


def _make_group(g):
    return ([] if g is None else list(map(
        _try_int,
        [g for g in g.split('.') if g]
    )))


class VersionError(Exception):
    pass


class Version(_Comparable):
    """Represent a version as defined by `SemVer 2.0.0`_
    
    It gives the ability to easily compare versions and parse them.
    
    While the object is flexible for the parsing of its input, it strictly
    respect the SemVer specification.
    
    .. _SemVer 2.0.0: http://semver.org/spec/v2.0.0.html
    """
    def __init__(self, version):
        m = _re.match(version)
        if not m:
            raise VersionError('Version malformed: {}'.format(version))
        self.major, self.minor, self.patch = map(int, m.groups(0)[:3])
        self.pre_release = _make_group(m.group(4))
        self.build = _make_group(m.group(5))

    def _mmp(self):
        return [self.major, self.minor, self.patch]

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        if _Seq(self._mmp()) != _Seq(other._mmp()):
            return False
        if _Seq(self.pre_release) != _Seq(other.pre_release):
            return False
        return True

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        if _Seq(self._mmp()) == _Seq(other._mmp()):
            if self.pre_release and other.pre_release:
                return _Seq(self.pre_release) < _Seq(other.pre_release)
            elif (not self.pre_release) and (not other.pre_release):
                return False
            return not self.pre_release is None
        return _Seq(self._mmp()) < _Seq(other._mmp())

    def __str__(self):
        """Returns a version as string
        
        The return format is the format defined by SemVer.
        
        :returns: the version stored
        :rtype: string
        """
        s = '.'.join(str(p) for p in self._mmp())
        if self.pre_release:
            s += '-{}'.format('.'.join(str(p) for p in self.pre_release))
        if self.build:
            s += '+{}'.format('.'.join(str(p) for p in self.build))
        return s

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.__str__())
