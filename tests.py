import unittest
from pysemver import Version, VersionError


class TestVersion(unittest.TestCase):
    def test_input_simple_1(self):
        ver = Version('1')
        self.assertEqual(ver.major, 1)
        self.assertEqual(ver.minor, 0)
        self.assertEqual(ver.patch, 0)
        self.assertEqual(ver.pre_release, [])
        self.assertEqual(ver.build, [])

    def test_input_simple_2(self):
        ver = Version('0.1')
        self.assertEqual(ver.major, 0)
        self.assertEqual(ver.minor, 1)
        self.assertEqual(ver.patch, 0)
        self.assertEqual(ver.pre_release, [])
        self.assertEqual(ver.build, [])

    def test_input_simple_3(self):
        ver = Version('0.0.1')
        self.assertEqual(ver.major, 0)
        self.assertEqual(ver.minor, 0)
        self.assertEqual(ver.patch, 1)
        self.assertEqual(ver.pre_release, [])
        self.assertEqual(ver.build, [])

    def test_input_simple_4(self):
        ver = Version('3.14.15')
        self.assertEqual(ver.major, 3)
        self.assertEqual(ver.minor, 14)
        self.assertEqual(ver.patch, 15)
        self.assertEqual(ver.pre_release, [])
        self.assertEqual(ver.build, [])

    def test_input_simple_5(self):
        with self.assertRaises(VersionError):
            Version('')

    def test_input_simple_6(self):
        with self.assertRaises(VersionError):
            Version('1.2.3.4')

    def test_input_complex_1(self):
        ver = Version('1.2.3-beta3.14.15')
        self.assertEqual(ver.major, 1)
        self.assertEqual(ver.minor, 2)
        self.assertEqual(ver.patch, 3)
        self.assertEqual(ver.pre_release, ['beta3', 14, 15])
        self.assertEqual(ver.build, [])

    def test_input_complex_2(self):
        ver = Version('1.2.3-beta3.14.15-42')
        self.assertEqual(ver.major, 1)
        self.assertEqual(ver.minor, 2)
        self.assertEqual(ver.patch, 3)
        self.assertEqual(ver.pre_release, ['beta3', 14, '15-42'])
        self.assertEqual(ver.build, [])

    def test_input_complex_3(self):
        ver = Version('1.2.3-dinosaurus+bigger-than-ch.1.ck.3.n')
        self.assertEqual(ver.major, 1)
        self.assertEqual(ver.minor, 2)
        self.assertEqual(ver.patch, 3)
        self.assertEqual(ver.pre_release, ['dinosaurus'])
        self.assertEqual(ver.build, ['bigger-than-ch', 1, 'ck', 3, 'n'])

    def test_input_complex_4(self):
        ver = Version('13.37+ch.1.ck.3.n')
        self.assertEqual(ver.major, 13)
        self.assertEqual(ver.minor, 37)
        self.assertEqual(ver.patch, 0)
        self.assertEqual(ver.pre_release, [])
        self.assertEqual(ver.build, ['ch', 1, 'ck', 3, 'n'])

    def test_output_1(self):
        self.assertEqual(
            str(Version('0.1-dino-saurus+bigger-than-ch.1.ck.3.n')),
            '0.1.0-dino-saurus+bigger-than-ch.1.ck.3.n'
        )

    def test_comparison_simple_1(self):
        self.assertTrue(Version('1') < Version('2'))
        self.assertFalse(Version('1') > Version('2'))
        self.assertFalse(Version('1') == Version('2'))
        self.assertTrue(Version('1') != Version('2'))
        self.assertTrue(Version('1') <= Version('2'))
        self.assertFalse(Version('1') >= Version('2'))

    def test_comparison_simple_2(self):
        self.assertFalse(Version('2.0.1') < Version('1.0.2'))
        self.assertTrue(Version('2.0.1') > Version('1.0.2'))
        self.assertFalse(Version('2.0.1') == Version('1.0.2'))
        self.assertTrue(Version('2.0.1') != Version('1.0.2'))
        self.assertFalse(Version('2.0.1') <= Version('1.0.2'))
        self.assertTrue(Version('2.0.1') >= Version('1.0.2'))

    def test_comparison_simple_3(self):
        self.assertFalse(Version('6.6.6') < Version('6.6.6'))
        self.assertFalse(Version('6.6.6') > Version('6.6.6'))
        self.assertTrue(Version('6.6.6') == Version('6.6.6'))
        self.assertFalse(Version('6.6.6') != Version('6.6.6'))
        self.assertTrue(Version('6.6.6') <= Version('6.6.6'))
        self.assertTrue(Version('6.6.6') >= Version('6.6.6'))

    def test_comparison_complex_1(self):
        v = Version
        self.assertTrue(v('3.14.15-alpha.42') < v('3.14.15-beta.42'))
        self.assertFalse(v('3.14.15-beta.42') < v('3.14.15-alpha.42'))

    def test_comparison_complex_2(self):
        v = Version
        self.assertTrue(v('3.14.15-42') < v('3.14.15-alpha'))
        self.assertFalse(v('3.14.15-alpha') < v('3.14.15-42'))

    def test_comparison_complex_3(self):
        v = Version
        self.assertTrue(v('3.14.15-rc3') < v('3.14.15'))
        self.assertFalse(v('3.14.15') < v('3.14.15-rc3'))

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
