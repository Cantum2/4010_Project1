import unittest
from driver import analyze_strings, init_file
EXE_PATH_PACKED = './strings_upx.exe'
EXE_PATH = './strings.exe'
EXE_BLANK = './blank.exe'


class TestDriver(unittest.TestCase):
    def test_analyze_string_non_blank(self):
        self.assertEqual(len(analyze_strings(EXE_PATH_PACKED)), 2)

    def test_analyze_string_blank(self):
        self.assertEqual(len(analyze_strings(EXE_BLANK)), 1)

    def test_init_file_doesnt_exist_empty(self):
        self.assertEqual(init_file('')[1], False)

    def test_init_file_doesnt_exist_dne(self):
        self.assertEqual(init_file('asdf.exe')[1], False)

    def test_init_file_does_exist_blank(self):
        self.assertEqual(init_file('./blank.exe')[1], True)

    def test_init_file_does_exist_strings(self):
        self.assertEqual(init_file('./strings.exe')[1], True)
