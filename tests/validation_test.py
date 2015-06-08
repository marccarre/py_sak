from unittest2 import TestCase, main
from py_sak.validation import is_float, is_int, is_valid_file, is_valid_dir, is_readable
from tests.test_utilities import TempFile, TempDir, UnreadableTempFile, UnreadableTempDir

class ValidationTest(TestCase):
    def test_is_float(self):
        self.assertTrue(is_float('3.14159'))
        self.assertTrue(is_float('-3.14159'))
        self.assertTrue(is_float('42'))
        self.assertTrue(is_float('-42'))
        self.assertFalse(is_float('3.14.159'))
        self.assertFalse(is_float('hello world!'))
        self.assertFalse(is_float(None))

    def test_is_int(self):
        self.assertTrue(is_int('42'))
        self.assertTrue(is_int('-42'))
        self.assertFalse(is_int('3.14159'))
        self.assertFalse(is_int('-3.14159'))
        self.assertFalse(is_int('3.14.159'))
        self.assertFalse(is_int('hello world!'))
        self.assertFalse(is_int(None))

    def test_is_file(self):
        with TempFile() as path:
            self.assertTrue(is_valid_file(path))
            self.assertTrue(is_readable(path))
        self.assertFalse(is_valid_file(path))

    def test_is_unreadable_file(self):
        with UnreadableTempFile() as path:
            self.assertTrue(is_valid_file(path))
            self.assertFalse(is_readable(path))
        self.assertFalse(is_valid_file(path))

    def test_is_dir(self):
        with TempDir() as path:
            self.assertTrue(is_valid_dir(path))
            self.assertTrue(is_readable(path))
        self.assertFalse(is_valid_dir(path))

    def test_is_unreadable_dir(self):
        with UnreadableTempDir() as path:
            self.assertTrue(is_valid_dir(path))
            self.assertFalse(is_readable(path))
        self.assertFalse(is_valid_dir(path))

if __name__ == '__main__':
    main()
