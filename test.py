import unittest

from app import detect_text
from app import app
from io import BytesIO
from app import allowed_types
class TestDetectText(unittest.TestCase):
    def test_detect_text_english(self):
        result = detect_text('Test_Images/test_image_english.png')
        self.assertEqual(result, 'TEST')

    def test_detect_text_mandarin(self):
        result = detect_text('Test_Images/test_image_mandarin.png')
        self.assertEqual(result, '漢汉<br>字字')


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_upload_images_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_images_post(self):
        with self.app as client:
            with open('Test_Images/test_image_english.png', 'rb') as img_file:
                data = {
                    'file': (BytesIO(img_file.read()), 'test_image_english.png')
                }
                response = client.post('/', data=data, follow_redirects=True)
                self.assertEqual(response.status_code, 200)

class TestAllowedTypes(unittest.TestCase):
    def test_allowed_extension(self):
        filename = 'Test_Images/test_image_english.png'
        result = allowed_types(filename)
        self.assertTrue(result)

    def test_disallowed_extension(self):
        filename = 'Test_Images/Placeholder-PDF.pdf'
        result = allowed_types(filename)
        self.assertEqual(result, False)



if __name__ == '__main__':
    unittest.main()
