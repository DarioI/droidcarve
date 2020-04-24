import unittest, os
from parsers import ManifestParser


class TestManifestParser(unittest.TestCase):

    def test_unobfuscated_manifest(self):
        manifest_file = open((os.path.dirname(__file__))+'/data/AndroidManifest_unobfuscated.xml', 'rb')
        xml_bytes = manifest_file.read()
        manifest_file.close()
        self.parser = ManifestParser(xml_bytes)
        self.assertEqual(len(self.parser.get_manifest()['activities']), 27, 'Should contain 27 activities.')
        self.assertEqual(len(self.parser.get_manifest()['services']), 11, 'Should contain 11 services.')
        self.assertEqual(len(self.parser.get_manifest()['providers']), 7, 'Should contain 7 providers.')
        self.assertEqual(len(self.parser.get_manifest()['meta_data']), 13, 'Should contain 13 meta-data entries.')
        self.assertEqual(len(self.parser.get_manifest()['features']), 1, 'Should contain 1 features.')
        self.assertEqual(len(self.parser.get_manifest()['permissions']), 12, 'Should contain 12 permissions.')
        self.assertEqual(len(self.parser.get_manifest()['receivers']), 12, 'Should contain 12 receivers.')

    def test_unobfuscated_manifest_2(self):
        manifest_file = open((os.path.dirname(__file__))+'/data/AndroidManifest_unobfuscated_2.xml', 'rb')
        xml_bytes = manifest_file.read()
        manifest_file.close()
        self.parser = ManifestParser(xml_bytes)
        self.assertEqual(len(self.parser.get_manifest()['activities']), 690, 'Should contain 690 activities.')
        self.assertEqual(len(self.parser.get_manifest()['services']), 141, 'Should contain 141 services.')
        self.assertEqual(len(self.parser.get_manifest()['providers']), 21, 'Should contain 21 providers.')
        self.assertEqual(len(self.parser.get_manifest()['meta_data']), 152, 'Should contain 152 meta-data entries.')
        self.assertEqual(len(self.parser.get_manifest()['features']), 9, 'Should contain 9 features.')
        self.assertEqual(len(self.parser.get_manifest()['permissions']), 60, 'Should contain 54 permissions.')
        self.assertEqual(len(self.parser.get_manifest()['receivers']), 78, 'Should contain 78 receivers.')

    def test_obfuscated_manifest(self):
        manifest_file = open((os.path.dirname(__file__))+'/data/AndroidManifest_obfuscated.xml', 'rb')
        xml_bytes = manifest_file.read()
        manifest_file.close()
        self.parser = ManifestParser(xml_bytes)
        self.assertEqual(len(self.parser.get_manifest()['activities']), 12, 'Should contain 12 activities.')
        self.assertEqual(len(self.parser.get_manifest()['services']), 3, 'Should contain 3 services.')
        self.assertEqual(len(self.parser.get_manifest()['providers']), 1, 'Should contain 1 providers.')
        self.assertEqual(len(self.parser.get_manifest()['meta_data']), 3, 'Should contain 2 meta-data entries.')
        self.assertEqual(len(self.parser.get_manifest()['features']), 7, 'Should contain 7 features.')
        self.assertEqual(len(self.parser.get_manifest()['permissions']), 11, 'Should contain 11 permissions.')
        self.assertEqual(len(self.parser.get_manifest()['receivers']), 2, 'Should contain 2 receivers.')


if __name__ == '__main__':
    unittest.main()
