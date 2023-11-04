import unittest

from app import detect_text

class TestDetectText(unittest.TestCase):
    def test_detect_text_english(self):
        result = detect_text('Test_Images/test_image_english.png')
        self.assertEqual(result, 'TEST')

    def test_detect_text_mandarin(self):
        result = detect_text('Test_Images/test_image_mandarin.png')
        self.assertEqual(result, '漢汉<br>字字')