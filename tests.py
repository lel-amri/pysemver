import unittest
from version import Version, VersionError


class TestVersion(unittest.TestCase):
    def test_input_output_simple(self):
        self.assertEqual(str(Version('1')), '1.0.0')
        self.assertEqual(str(Version('0.1')), '0.1.0')
        self.assertEqual(str(Version('0.0.1')), '0.0.1')
        self.assertEqual(str(Version('3.14.15')), '3.14.15')
        with self.assertRaises(VersionError):
            Version('')
        with self.assertRaises(VersionError):
            Version('1.2.3.4')

    def test_input_output_complex(self):
        self.assertEqual(
            str(Version('1.2.3-beta3.14.15')),
            '1.2.3-beta3.14.15'
        )
        self.assertEqual(
            str(Version('1.2.3-beta3.14.15-42')),
            '1.2.3-beta3.14.15-42'
        )
        self.assertEqual(
            str(Version('1.2.3-dinosaurus+bigger-than-ch1ck3n')),
            '1.2.3-dinosaurus+bigger-than-ch1ck3n'
        )
        self.assertEqual(
            str(Version('13.37+ch1ck3n')),
            '13.37.0+ch1ck3n'
        )
        with self.assertRaises(VersionError):
            Version('-test+case')

    def test_input_output_tricky(self):
        self.assertEqual(
            str(Version('42-test..case')),
            '42.0.0-test.case'
        )
        with self.assertRaises(VersionError):
            Version('42-+test..case')
        with self.assertRaises(VersionError):
            Version('8-+')

    def test_comparison_simple(self):
        self.assertTrue(Version('1') < Version('2'))
        self.assertFalse(Version('1') > Version('2'))
        self.assertFalse(Version('1') == Version('2'))
        self.assertTrue(Version('1') != Version('2'))
        self.assertTrue(Version('1') <= Version('2'))
        self.assertFalse(Version('1') >= Version('2'))
        self.assertFalse(Version('2.0.1') < Version('1.0.2'))
        self.assertTrue(Version('2.0.1') > Version('1.0.2'))
        self.assertFalse(Version('2.0.1') == Version('1.0.2'))
        self.assertTrue(Version('2.0.1') != Version('1.0.2'))
        self.assertFalse(Version('2.0.1') <= Version('1.0.2'))
        self.assertTrue(Version('2.0.1') >= Version('1.0.2'))
        self.assertFalse(Version('6.6.6') < Version('6.6.6'))
        self.assertFalse(Version('6.6.6') > Version('6.6.6'))
        self.assertTrue(Version('6.6.6') == Version('6.6.6'))
        self.assertFalse(Version('6.6.6') != Version('6.6.6'))
        self.assertTrue(Version('6.6.6') <= Version('6.6.6'))
        self.assertTrue(Version('6.6.6') >= Version('6.6.6'))

    def test_comparison_complex(self):
        v = Version
        self.assertTrue(v('3.14.15-alpha.42') < v('3.14.15-beta.42'))
        self.assertFalse(v('3.14.15-alpha.42') > v('3.14.15-beta.42'))
        self.assertTrue(v('3.14.15-42') < v('3.14.15-alpha'))
        self.assertFalse(v('3.14.15-42') > v('3.14.15-alpha'))
        self.assertTrue(v('3.14.15-rc3') < v('3.14.15'))
        self.assertFalse(v('3.14.15-rc3') > v('3.14.15'))
        self.assertFalse(v('3.14.15') < v('3.14.15-rc3'))
        self.assertTrue(v('3.14.15') > v('3.14.15-rc3'))

    def test_comparison_special(self):
        v = Version
        self.assertTrue(
            v('1.0.0-alpha')
            < v('1.0.0-alpha.1')
            < v('1.0.0-alpha.beta')
            < v('1.0.0-beta')
            < v('1.0.0-beta.2')
            < v('1.0.0-beta.11')
            < v('1.0.0-rc.1')
            < v('1.0.0')
        )


if __name__ == '__main__':
    unittest.main()
