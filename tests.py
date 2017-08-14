import unittest
from version import Version, VersionError


class TestVersion(unittest.TestCase):
    def test_simple_input_output(self):
        self.assertEqual(str(Version('1')), '1.0.0')
        self.assertEqual(str(Version('0.1')), '0.1.0')
        self.assertEqual(str(Version('0.0.1')), '0.0.1')
        self.assertEqual(str(Version('3.14.15')), '3.14.15')
        with self.assertRaises(VersionError):
            Version('')
        with self.assertRaises(VersionError):
            Version('1.2.3.4')

    def test_complex_input_output(self):
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

    def test_tricky_input_output(self):
        self.assertEqual(
            str(Version('42-test..case')),
            '42.0.0-test.case'
        )
        with self.assertRaises(VersionError):
            Version('42-+test..case')
        with self.assertRaises(VersionError):
            Version('8-+')


if __name__ == '__main__':
    unittest.main()
